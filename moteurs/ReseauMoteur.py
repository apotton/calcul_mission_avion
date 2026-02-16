from importlib.util import spec_from_file_location, module_from_spec
from constantes.Constantes import Constantes
from moteurs.Moteur import Moteur
from inputs.Inputs import Inputs
import moteurs.DonneesMoteur as DonneesMoteur
from pathlib import Path
import numpy as np


class ReseauMoteur(Moteur):
    def __init__(self, Avion):
        super().__init__(Avion)
        # Spécifique à cette classe :
        self.DonneesMoteur = self._charger_donnees(Inputs.getEngineFile())

        # liste des différentes altitudes disponibles dans le DonneesMoteur
        self.available_alts = list(self.DonneesMoteur.cruise_data.keys())


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
        h_ft = self.Avion.geth()/ Constantes.conv_ft_m

        resultat = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                                self.DonneesMoteur.alt_table_ft,
                                                self.DonneesMoteur.Fn_MCL_table,
                                                self.Avion.Aero.getMach(), h_ft)

        self.F_t = 2*float(resultat)* Constantes.g * Constantes.conv_lb_kg  # Conversion lbf -> N et pour 2 moteurs
    
    def calculateSFCCruise(self):
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        # Obtention de l'altitude la plus proche dans la base de données (cruise_data)        
        closest_h = min(self.available_alts, key=lambda x: abs(x - h_ft))

        # Récupération des tables correspondantes
        data = self.DonneesMoteur.cruise_data[closest_h]
        
        fn_lbf_vector = data['fn']                       # Vecteur Poussée en lbf (vecteur lignes)
        sfc_matrix = data['sfc']                         # Matrice SFC (Lignes=Fn, Colonnes=Mach)
        mach_vector = self.DonneesMoteur.mach_table_crl  # Vecteur Mach (vecteur colonnes)

        # Interpolation de la table de SFC (poussée en lbf)
        sfc_lbf_raw = ReseauMoteur.interp2d_linear(fn_lbf_vector,
                                                   mach_vector,
                                                   sfc_matrix,
                                                   self.F_t / 2 / Constantes.conv_lb_kg / Constantes.g,
                                                   self.Avion.Aero.getMach())

        # Conversion finale des unités
        self.SFC_t = sfc_lbf_raw / 3600.0 / Constantes.g

    #### MONTÉE ####

    def calculateFClimb(self):
        # Altitude
        h_ft = self.Avion.geth()/ Constantes.conv_ft_m  # Conversion m -> ft

        resultat = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table, # mach climb ops
                                                self.DonneesMoteur.alt_table_ft, # h climb ops
                                                self.DonneesMoteur.Fn_MCL_table,
                                                self.Avion.Aero.getMach(), h_ft)

        self.F_t = 2*float(resultat)* Constantes.g * Constantes.conv_lb_kg  # Conversion lbf -> N et pour 2 moteurs


    def calculateSFCClimb(self): 
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        SFC_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                               self.DonneesMoteur.alt_table_ft,
                                               self.DonneesMoteur.SFC_MCL_table,
                                               self.Avion.Aero.getMach(), h_ft)
    
        self.SFC_t = float(SFC_lbf) / 3600.0 / Constantes.g  # Conversion lb/(lbf*h) -> kg/(N*s)
    
    #### DESENTE ####

    def calculateFDescent(self):
        h_ft = self.Avion.geth() / Constantes.conv_ft_m # Conversion m -> ft

        F_N_Descent_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                                       self.DonneesMoteur.alt_table_ft,
                                                       self.DonneesMoteur.Fn_FI_table,
                                                       self.Avion.Aero.getMach(), h_ft)
        
        self.F_t = float(F_N_Descent_lbf) / 3600. / Constantes.g

    def calculateSFCDecent(self):
        # Altitude
        h_ft = self.Avion.geth() / Constantes.conv_ft_m # Conversion m -> ft

        FuelFlow_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.mach_table,
                                                    self.DonneesMoteur.alt_table_ft,
                                                    self.DonneesMoteur.FF_FI_table,
                                                    self.Avion.Aero.getMach(), h_ft)
        
        self.SFC_t = float(FuelFlow_lbf) / 3600. / Constantes.g / self.F_t


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
                                               self.F_t / 2, self.Avion.Aero.getMach())
    
        self.SFC_t = float(SFC_lbf) / 3600.0 / Constantes.g  # Conversion lb/(lbf*h) -> kg/(N*s)


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
        # h_ft = 25000  # ft

        # SFC_lbf = ReseauMoteur.interp2d_linear(self.DonneesMoteur.cruise_data[h_ft]['fn'] * (Constantes.g * Constantes.conv_lb_kg), # poussée en N
        #                                        self.DonneesMoteur.mach_table_crl,
        #                                        self.DonneesMoteur.cruise_data[h_ft]['sfc'],
        #                                        self.F_t/2, self.Avion.Aero.getMach())
    
        # self.SFC_t = float(SFC_lbf) / 3600.0 / Constantes.g  # Conversion lb/(lbf*h) -> kg/(N*s)


