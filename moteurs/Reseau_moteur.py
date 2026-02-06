# classe qui hérite de la classe Moteur et qui utilise les Donnees_moteur pour calculer la poussée et le SFC
# from avions.Avion import Avion
# from avions.Avion import Avion
from moteurs.Moteur import Moteur
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np
from moteurs.Donnees_moteur import Donnees_moteur
from scipy.ndimage import map_coordinates
# from numba import njit

from scipy.interpolate import RegularGridInterpolator


class Reseau_moteur(Moteur):
    def __init__(self, Avion, BPR=0., OPR=0.):
        super().__init__(Avion, BPR, OPR) # On force choix_reseau=1 pour utiliser Donnees_moteur
        # Spécifique à cette classe :
        self.Donnees_moteur = Donnees_moteur()

        # liste des différentes altitudes disponibles dans le Donnees_moteur
        self.available_alts = list(self.Donnees_moteur.cruise_data.keys())


        
    @staticmethod
    def interp2d_linear(x, y, values, xq, yq):
        """
        xq, yq : (N,) tableaux de points
        out    : (N,) tableau pré-alloué
        """
        # Trouve les indices i, j tels que x[i] <= xq < x[i+1] et y[j] <= yq < y[j+1]
        i = np.searchsorted(x, xq) - 1
        j = np.searchsorted(y, yq) - 1

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

    
        

   # Cette fonction permet de calculer *F_MCL_cruise_step* et aussi *F_MCL_cruise_step_up* (il suffit de mettre h_ft=h_ft + 2000)
    # et aussi *F_N_AEO_lbf*
    def Calculate_F(self):
        "Calcule la poussée Max Climb"
        h_ft = self.Avion.geth()/ Constantes.conv_ft_m  # Conversion m -> ft

        resultat = Reseau_moteur.interp2d_linear(self.Donnees_moteur.mach_table,
                                                 self.Donnees_moteur.alt_table_ft,
                                                 self.Donnees_moteur.Fn_MCL_table,
                                                 self.Avion.Aero.getMach(), h_ft)

        self.F_t = 2*float(resultat)* Constantes.g * Constantes.conv_lb_kg  # Conversion lbf -> N et pour 2 moteurs
        
        
    
    # calcule la SFC en croisière, utilise la partie data de Donnes_moteur.py
    def Calculate_SFC(self, F_engine_N=None): # F_engine correspond à F_cruise_step pour 2 moteurs (poussée totale actuelle)
        "Calcule le SFC en croisière"
        
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        # 1. Gestion de la poussée d'entrée
        # Si aucune poussée n'est fournie, on utilise la poussée actuelle de l'objet (self.F)
        if F_engine_N is None:
            thrust_to_use = self.F_t
        else:
            thrust_to_use = F_engine_N

    
        # Conversion lbf -> Newtons : 1 lbf = 0.4535 kg * 9.81 m/s²
        # conv_lbf_N = Constantes.g * Constantes.conv_lb_kg

        # 2. Trouver l'altitude la plus proche dans la base de données (cruise_data)        
        closest_h = min(self.available_alts, key=lambda x: abs(x - h_ft)) # Trouve l'altitude la plus proche de h_ft présente dans le Donnees_moteur

        # (Optionnel) : On pourrait mettre une alerte si l'altitude est trop éloignée d'un niveau standard
        # if abs(h_ft - closest_h) > 500: print("Attention: Interpolation SFC loin du FL standard")

        # 3. Récupération des tables correspondantes
        data = self.Donnees_moteur.cruise_data[closest_h]
        
        fn_lbf_vector = data['fn']                       # Vecteur Poussée en lbf (vecteur lignes)
        sfc_matrix = data['sfc']                         # Matrice SFC (Lignes=Fn, Colonnes=Mach)
        mach_vector = self.Donnees_moteur.mach_table_crl  # Vecteur Mach (vecteur colonnes)
        # 4. Conversion de l'axe Poussée de la table (lbf -> Newtons)
        # Nécessaire car l'entrée 'thrust_to_use' est en Newtons
        fn_newton_vector = fn_lbf_vector * Constantes.g * Constantes.conv_lb_kg

        # 5. Interpolation 2D
        # RegularGridInterpolator attend (x_grid, y_grid). 
        # Ici la matrice SFC a pour forme (len(Fn), len(Mach)).
        # interp_func = RegularGridInterpolator(
        #     (fn_newton_vector, mach_vector), 
        #     sfc_matrix,
        #     bounds_error=False, # no crash si hors bornes
        # )

        # On interpole au point (Poussée_Moteur_N, Mach)
        # Note: MATLAB faisait F/2 car F était la poussée avion totale. 
        # Ici, thrust_to_use est déjà censé être pour UN moteur.
        # sfc_lbf_raw = float(interp_func((thrust_to_use, self.Avion.Aero.getMach())))  # Résultat en lb/(lbf*h)
        # Interpolation avec la fonction Reseau_moteur.interp2d_linear
        sfc_lbf_raw = Reseau_moteur.interp2d_linear(fn_newton_vector,
                                                    mach_vector,
                                                    sfc_matrix,
                                                    thrust_to_use,
                                                    self.Avion.Aero.getMach())

        # 6. Conversion finale des unités
        # MATLAB: SFC = SFC_lbf / 3600 / g
        # Cela convertit des [lb/(lbf*h)] ou [kg/(kgf*h)] vers [kg/(N*s)] (SI)
        self.SFC_t = sfc_lbf_raw / 3600.0 / Constantes.g




    # Utilise la SFC_MCL tables pour la montée
    def Calculate_SFC_climb(self): 
        "Calcule la SFC en montée"
        h_ft = self.Avion.geth() / Constantes.conv_ft_m  # Conversion m -> ft

        SFC_lbf = Reseau_moteur.interp2d_linear(self.Donnees_moteur.mach_table,
                                                self.Donnees_moteur.alt_table_ft,
                                                self.Donnees_moteur.SFC_MCL_table,
                                                self.Avion.Aero.getMach(), h_ft)
    
        self.SFC_t = float(SFC_lbf) / 3600.0 / Constantes.g  # Conversion lb/(lbf*h) -> kg/(N*s)
        
            
