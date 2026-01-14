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

        self.F = 0            # Poussée actuelle (N)
        self.SFC = 0          # SFC actuelle (kg/(N.s))

    # Getters
    def get_BPR(self):
        return self.BPR

    def get_OPR(self):
        return self.OPR

    def get_Reseau_moteur(self):
        return self.Reseau_moteur

    def get_F(self):
        return self.F

    def get_SFC(self):
        return self.SFC
    
    def get_F_MCL_cruise_step(self):
        return self.F

    def Calculate_F_MCL_cruise_step(self, mach, h_ft):
        # Création de l'interpolateur
        interp = RegularGridInterpolator(
            (self.Reseau_moteur.mach_table, self.Reseau_moteur.alt_table_ft), 
            self.Reseau_moteur.Fn_MCL_table,
            bounds_error=False, # Évite le crash si légèrement hors bornes
            fill_value=None     # Extrapole si nécessaire (optionnel)
        )
        
        # L'interpolateur renvoie un tableau numpy (ex: array([15000.5])), 
        # on prend la valeur [0] ou .item() pour avoir un float propre.
        resultat = interp((mach, h_ft))
        self.F = float(resultat) 
        
        return self.F