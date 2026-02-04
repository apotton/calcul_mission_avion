from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np
from moteurs.Donnees_moteur import Donnees_moteur 



class Moteur:
    def __init__(self, Avion, BPR=0., OPR=0., choix_reseau=1):
        self.Avion = Avion
        self.BPR = BPR        # Bypass ratio
        self.OPR = OPR        # Overall Pressure Ratio
        self.F_t = 0          # Poussée actuelle (N)
        self.SFC_t = 0        # SFC actuelle (kg/(N.s))

    # Getters
    def getBPR(self):
        return self.BPR

    def getOPR(self):
        return self.OPR

    def getDonnees_moteur(self):
        return self.Donnees_moteur

    def getF(self):
        return self.F_t

    def getSFC(self):
        return self.SFC_t
    
    def getF_MCL_cruise_step(self):
        return self.F_t


    def calculate_F(self, Avion):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC(self, Avion, F_engine_N=None):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC_climb(self, Avion):
        pass  # Méthode à implémenter dans les classes filles


 
         