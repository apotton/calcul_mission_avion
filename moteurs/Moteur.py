from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np
from moteurs.Reseau_moteur import Reseau_moteur 

from scipy.interpolate import RegularGridInterpolator

class Moteur:
    def __init__(self, BPR=0, OPR=0, choix_reseau=1):
        self.BPR = BPR        # Bypass ratio
        self.OPR = OPR        # Overall Pressure Ratio
        
        if choix_reseau == 1:
            self.Reseau_moteur = Reseau_moteur() 
        else:
            # Gestion d'un cas par défaut ou d'une erreur si nécessaire
            self.Reseau_moteur = None

        self.F_t = 0            # Poussée actuelle (N)
        self.SFC_t = 0          # SFC actuelle (kg/(N.s))

    # Getters
    def get_BPR(self):
        return self.BPR

    def get_OPR(self):
        return self.OPR

    def get_Reseau_moteur(self):
        return self.Reseau_moteur

    def get_F(self):
        return self.F_t

    def get_SFC(self):
        return self.SFC_t
    
    def get_F_MCL_cruise_step(self):
        return self.F_t


    # méthodes de calcul de la poussée et du SFC en croisière


    # Cette fonction permet de calculer *F_MCL_cruise_step* et aussi *F_MCL_cruise_step_up* (il suffit de mettre h_ft=h_ft + 2000)
    # et aussi *F_N_AEO_lbf*
    def Calculate_F_MCL_cruise_step(self, mach, h_ft):
        "Calcule la poussée Max Climb"
        # Création de l'interpolateur
        interp = RegularGridInterpolator(
            (self.Reseau_moteur.mach_table, self.Reseau_moteur.alt_table_ft), 
            self.Reseau_moteur.Fn_MCL_table,
            bounds_error=False, # Évite le crash si légèrement hors bornes
            fill_value=None     # Extrapole si nécessaire (optionnel)
        )
        
        # L'interpolateur renvoie un tableau numpy (ex: array([15000.5])), 
        # on prend la valeur [0] ou .item() pour avoir un float propre.
        resultat = interp((mach, h_ft)) # résultat pour un moteur en lbf
        self.F_t = 2*float(resultat)* Constantes.g * Constantes.conv_lb_kg  # Conversion lbf -> N et pour 2 moteurs
        
        
    

    def Calculate_SFC_cruise(self, mach, h_ft, F_engine_N=None):
        "Calcule le SFC en croisière"
        

        # 1. Gestion de la poussée d'entrée
        # Si aucune poussée n'est fournie, on utilise la poussée actuelle de l'objet (self.F)
        if F_engine_N is None:
            thrust_to_use = self.F_t
        else:
            thrust_to_use = F_engine_N

    
        # Conversion lbf -> Newtons : 1 lbf = 0.4535 kg * 9.81 m/s²
        conv_lbf_N = Constantes.g * Constantes.conv_lb_kg

        # 2. Trouver l'altitude la plus proche dans la base de données (cruise_data)
        # liste des différentes altitudes disponibles dans le Reseau_moteur
        available_alts = list(self.Reseau_moteur.cruise_data.keys())
        
        closest_h = min(available_alts, key=lambda x: abs(x - h_ft)) # Trouve l'altitude la plus proche de h_ft présente dans le Reseau_moteur

        # (Optionnel) : On pourrait mettre une alerte si l'altitude est trop éloignée d'un niveau standard
        # if abs(h_ft - closest_h) > 500: print("Attention: Interpolation SFC loin du FL standard")

        # 3. Récupération des tables correspondantes
        data = self.Reseau_moteur.cruise_data[closest_h]
        
        fn_lbf_vector = data['fn']                       # Vecteur Poussée en lbf (vecteur lignes)
        sfc_matrix = data['sfc']                         # Matrice SFC (Lignes=Fn, Colonnes=Mach)
        mach_vector = self.Reseau_moteur.mach_table_crl  # Vecteur Mach (vecteur colonnes)

        # 4. Conversion de l'axe Poussée de la table (lbf -> Newtons)
        # Nécessaire car l'entrée 'thrust_to_use' est en Newtons
        fn_newton_vector = fn_lbf_vector * Constantes.g * Constantes.conv_lb_kg

        # 5. Interpolation 2D
        # RegularGridInterpolator attend (x_grid, y_grid). 
        # Ici la matrice SFC a pour forme (len(Fn), len(Mach)).
        interp_func = RegularGridInterpolator(
            (fn_newton_vector, mach_vector), 
            sfc_matrix,
            bounds_error=False, # no crash si hors bornes
            fill_value=None #extrapolation
        )

        # On interpole au point (Poussée_Moteur_N, Mach)
        # Note: MATLAB faisait F/2 car F était la poussée avion totale. 
        # Ici, thrust_to_use est déjà censé être pour UN moteur.
        sfc_lbf_raw = float(interp_func((thrust_to_use, mach)))

        # 6. Conversion finale des unités
        # MATLAB: SFC = SFC_lbf / 3600 / g
        # Cela convertit des [lb/(lbf*h)] ou [kg/(kgf*h)] vers [kg/(N*s)] (SI)
        self.SFC_t = sfc_lbf_raw / 3600.0 / Constantes.g

         