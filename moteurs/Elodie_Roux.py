from moteurs.Moteur import Moteur

class Elodie_roux(Moteur):
    def __init__(self, BPR=0, OPR=0):
        super().__init__(BPR, OPR)
        # Pas de Donnees_moteur ici, peut-être d'autres constantes spécifiques

    def Calculate_F_MCL_cruise_step(self, Avion):
        print("Calcul Poussée via méthode analytique (Elodie Roux)")
        # Ici tu mets tes équations mathématiques
        # self.F_t = ... formule mathématique ...

    def Calculate_SFC_cruise(self, Avion, F_engine_N=None):
        print("Calcul SFC via méthode analytique (Elodie Roux)")
        # Ici tu mets tes équations mathématiques
        # self.SFC_t = ... formule mathématique ...