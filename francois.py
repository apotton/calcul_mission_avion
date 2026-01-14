from moteurs.Moteur import Moteur
from constantes.Constantes import Constantes
import numpy as np


test_moteur = Moteur(BPR=5, OPR=30, choix_reseau=1)

test_moteur.Calculate_F_MCL_cruise_step(mach=0.78, h_ft=35000)
print("Poussée moteur à Mach 0.78 et 35000 ft : {:.2f} N".format(test_moteur.get_F_MCL_cruise_step()))