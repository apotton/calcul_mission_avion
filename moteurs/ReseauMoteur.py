from importlib.util import spec_from_file_location, module_from_spec
from constantes.Constantes import Constantes
from moteurs.Moteur import Moteur
from inputs.Inputs import Inputs
import moteurs.DonneesMoteur as DonneesMoteur
from pathlib import Path
import numpy as np

from scipy.interpolate import RegularGridInterpolator


class ReseauMoteur(Moteur):
    def __init__(self, Avion, path = Inputs.getEngineFile()):
        super().__init__(Avion)
        # Spécifique à cette classe :
        self.DonneesMoteur = self._charger_donnees(path)

        # liste des différentes altitudes disponibles dans le DonneesMoteur
        self.available_alts = list(self.DonneesMoteur.cruise_data.keys())

        # Création des interpolateurs pour le calcul vectorisé de la SFC
        self.interpolateurs = {}
        for alt in self.available_alts:
            data = self.DonneesMoteur.cruise_data[alt]
            
            # Récupération des axes de la table
            fn_axis = data['fn'] 
            mach_axis = self.DonneesMoteur.mach_table_crl
            sfc_table = data['sfc']

            # Création de l'interpolateur
            self.interpolateurs[alt] = RegularGridInterpolator(
                (fn_axis, mach_axis), 
                sfc_table, 
                bounds_error=False,
                method='linear', 
                fill_value=None # type: ignore
            )


    def _charger_donnees(self, chemin_fichier):
        '''
        Charge un fichier de configuration moteur.
        
        :param chemin_fichier: Le chemin du fichier
        '''
        chemin_fichier = Path(chemin_fichier)

        # Check de l'existence du fichier
        if not chemin_fichier.exists():
            raise FileNotFoundError(f"{chemin_fichier} introuvable")

        spec = spec_from_file_location(
            name=chemin_fichier.stem,
            location=str(chemin_fichier)
        )

        # Check de la spec
        if spec is None:
            raise ValueError(f"Impossible de créer une spécification pour {chemin_fichier}")
        module = module_from_spec(spec)
        
        # Check du loader
        if spec.loader is None:
            raise ValueError(f"Impossible de créer un loader pour {chemin_fichier}")
        spec.loader.exec_module(module)

        return module.load()

    @staticmethod
    def interp2d_linear(x, y, values, xq, yq):
        '''
        Réalise une interpolation 2D linéaire sur une matrice.

        :param x: Axe des abscisse de la matrice (Nx1)
        :param y: Axe des ordonnées de la matrice (Nx1)
        :param values: Matrice de valeurs (NxN)
        :param xq: Abscisse de l'interpolation (1x1)
        :param yq: Ordonnée de l'interpolation (1x1)

        :return val: La valeur interpolée correpondant aux coordonnées (x,y)
        '''
        # Trouve les indices i, j tels que x[i] <= xq < x[i+1] et y[j] <= yq < y[j+1]
        i = np.searchsorted(x, xq) - 1
        j = np.searchsorted(y, yq) - 1

        # Gère les cas où xq ou yq sont en dehors des bornes de x ou y
        if i < 0:
            i = 0
        elif i > x.shape[0] - 2:
            i = x.shape[0] - 2

        if j < 0:
            j = 0
        elif j > y.shape[0] - 2:
            j = y.shape[0] - 2

        # Construit les poids d'interpolation
        tx = (xq - x[i]) / (x[i + 1] - x[i])
        ty = (yq - y[j]) / (y[j + 1] - y[j])

        # Effectue l'interpolation bilinéaire
        return (
            (1.0 - tx) * (1.0 - ty) * values[i, j]
        +           tx * (1.0 - ty) * values[i + 1, j]
        +   (1.0 - tx) *         ty * values[i, j + 1]
        +           tx *         ty * values[i + 1, j + 1]
        )

    
    def calculateFCruise(self):
        # Altitude (conversion)
        # Calcul par équilibre des forces
        Cz = self.Avion.Aero.getCz()
        Cx = self.Avion.Aero.getCx()
        finesse = Cz / Cx
        self.F_t = self.Avion.Masse.getCurrentWeight() / finesse
    
    def calculateSFCCruise(self):
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        # Obtention de l'altitude la plus proche dans la base de données (cruise_data)        
        closest_h = min(self.available_alts, key=lambda x: abs(x - h_ft))

        # Détermination de la deuxième altitude pour l'interpolation 3D (Alt)
        if abs(h_ft - closest_h) < 20:
            # On est suffisamment proche de l'altitude dans les tables
            h_refs = [closest_h]
        else:
            # Sinon on choisit la seconde plus proche altitude
            if h_ft < closest_h:
                second_closest_h = max([h for h in self.available_alts if h < closest_h], default=closest_h)
            else:
                second_closest_h = min([h for h in self.available_alts if h > closest_h], default=closest_h)

            # Si la seconde altitude est la même, c'est qu'on est sur les bords des tables
            if second_closest_h != closest_h:
                h_refs = [closest_h, second_closest_h]
            else:
                h_refs = [closest_h]

        # Calcul du SFC pour chaque altitude de référence
        sfc_results = []
        for h_ref in h_refs:
            # Récupération des tables correspondantes
            data = self.DonneesMoteur.cruise_data[h_ref]
            
            fn_lbf_vector = data['fn']                       # Vecteur Poussée en lbf (vecteur lignes)
            sfc_matrix = data['sfc']                         # Matrice SFC (Lignes=Fn, Colonnes=Mach)
            mach_vector = self.DonneesMoteur.mach_table_crl  # Vecteur Mach (vecteur colonnes)

            sfc_lbf = ReseauMoteur.interp2d_linear(fn_lbf_vector,
                                                   mach_vector,
                                                   sfc_matrix,
                                                   self.F_t / 2 / Constantes.conv_lb_kg / Constantes.g * Inputs.cFN_cruise,
                                                   self.Avion.Aero.getMach())
            
            sfc_results.append(sfc_lbf)

        # Interpolation finale entre les deux altitudes (si nécessaire)
        if len(h_refs) == 1:
            sfc_lbf_final = sfc_results[0]
        else:
            # Interpolation linéaire entre les deux plans d'altitude
            ratio = (h_ft - h_refs[0]) / (h_refs[1] - h_refs[0])
            sfc_lbf_final = (1 - ratio) * sfc_results[0] + ratio * sfc_results[1]

        # Conversion finale (lbf/lbf/h -> kg/N/s)
        self.SFC_t = (sfc_lbf_final / 3600.0 / Constantes.g) * Inputs.cFF_cruise
        self.FF_t = self.SFC_t * self.F_t


    #### MONTÉE ####

    def calculateFClimb(self):
        # Altitude
        h_ft = self.Avion.geth()/ Constantes.conv_ft_m  # Conversion m -> ft

        resultat = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table, # mach climb ops
                                                self.DonneesMoteur.alt_table_ft, # h climb ops
                                                self.DonneesMoteur.Fn_MCL_table,
                                                self.Avion.Aero.getMach(), h_ft)

        self.F_t = (2*float(resultat)* Constantes.g * Constantes.conv_lb_kg) * Inputs.cFN_climb  # Conversion lbf -> N et pour 2 moteurs


    def calculateSFCClimb(self): 
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        SFC_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                               self.DonneesMoteur.alt_table_ft,
                                               self.DonneesMoteur.SFC_MCL_table,
                                               self.Avion.Aero.getMach(), h_ft)
    
        self.SFC_t = (float(SFC_lbf) / 3600.0 / Constantes.g) * Inputs.cFF_climb  # Conversion lb/(lbf*h) -> kg/(N*s)
        self.FF_t = self.SFC_t * self.F_t
    
    #### DESENTE ####

    def calculateFDescent(self):
        h_ft = self.Avion.geth() / Constantes.conv_ft_m # Conversion m -> ft

        F_N_Descent_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                                       self.DonneesMoteur.alt_table_ft,
                                                       self.DonneesMoteur.Fn_FI_table,
                                                       self.Avion.Aero.getMach(), h_ft)
        
        self.F_t = float(F_N_Descent_lbf) / 3600. / Constantes.g * Inputs.cFN_descent

    def calculateSFCDecent(self):
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m # Conversion m -> ft

        FuelFlow_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                                    self.DonneesMoteur.alt_table_ft,
                                                    self.DonneesMoteur.FF_FI_table,
                                                    self.Avion.Aero.getMach(), h_ft)
        
        self.SFC_t = (float(FuelFlow_lbf) / 3600. / Constantes.g / self.F_t) * Inputs.cFF_descent
        self.FF_t = self.SFC_t * self.F_t


    ### HOLDING ###

    def calculateFHolding(self):
        # Calcul par équilibre des forces
        Cz = self.Avion.Aero.getCz()
        Cx = self.Avion.Aero.getCx()
        finesse = Cz / Cx
        self.F_t = self.Avion.Masse.getCurrentWeight() / finesse

    def calculateSFCHolding(self):
        SFC_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.fn_lbf_crl_holding * (Constantes.g * Constantes.conv_lb_kg), # poussée en N
                                               self.DonneesMoteur.mach_table_crl_holding,
                                               self.DonneesMoteur.sfc_crl_holding,
                                               self.F_t / 2 * Inputs.cFN_cruise, self.Avion.Aero.getMach())
    
        self.SFC_t = (float(SFC_lbf) / 3600.0 / Constantes.g) * Inputs.cFF_cruise  # Conversion lb/(lbf*h) -> kg/(N*s)
        self.FF_t = self.SFC_t * self.F_t


    ### Diversion ###

    def calculateFCruiseDiversion(self):
        # Calcul par équilibre des forces
        Cz = self.Avion.Aero.getCz()
        Cx = self.Avion.Aero.getCx()
        finesse = Cz / Cx
        self.F_t = self.Avion.Masse.getCurrentWeight() / finesse

    def calculateSFCCruiseDiversion(self):
        # Même calcul qu'en croisière
        self.calculateSFCCruise()


    # ====================
    # calcul vectorisé de la SFC pour la croisière Alt SAR
    # ====================

    def calculateSFC_Vectorized(self):
        """
        Version vectorisée du calcul de SFC (en croisière).
        """
        h_ft = self.Avion.geth() / Constantes.conv_ft_m
        
        # Altitude de référence
        closest_h = min(self.available_alts, key=lambda x: abs(x - h_ft))
        
        # Détermination de la deuxième altitude pour l'interpolation 3D (Alt)
        if abs(h_ft - closest_h) < 20:
            # On est suffisamment proche de l'altitude dans les tables
            h_refs = [closest_h]
        else:
            # Sinon on choisit la seconde plus proche altitude
            if h_ft < closest_h:
                second_closest_h = max([h for h in self.available_alts if h < closest_h], default=closest_h)
            else:
                second_closest_h = min([h for h in self.available_alts if h > closest_h], default=closest_h)

            # Si la seconde altitude est la même, c'est qu'on est sur les bords des tables
            if second_closest_h != closest_h:
                h_refs = [closest_h, second_closest_h]
            else:
                h_refs = [closest_h]


        # Calcul du SFC pour chaque altitude de référence
        sfc_results = []
        for h_ref in h_refs:
            # Récupération de l'interpolateur
            interp_func = self.interpolateurs[h_ref]
            
            # On interpole pour tous les couples (Mach, Fn) d'un coup
            query_points = np.vstack((self.F_t / 2 / Constantes.conv_lb_kg / Constantes.g * Inputs.cFN_cruise, self.Avion.Aero.getMach())).T

            sfc_lbf = interp_func(query_points)
            sfc_results.append(sfc_lbf)

        # Interpolation finale entre les deux altitudes (si nécessaire)
        if len(h_refs) == 1:
            sfc_lbf_final = sfc_results[0]
        else:
            # Interpolation linéaire entre les deux plans d'altitude
            ratio = (h_ft - h_refs[0]) / (h_refs[1] - h_refs[0])
            sfc_lbf_final = (1 - ratio) * sfc_results[0] + ratio * sfc_results[1]

        # Conversion finale (lbf/lbf/h -> kg/N/s)
        self.SFC_t = (sfc_lbf_final / 3600.0 / Constantes.g) * Inputs.cFF_cruise
        self.FF_t = self.SFC_t * self.F_t