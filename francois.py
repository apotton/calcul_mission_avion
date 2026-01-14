from moteurs.Moteur import Moteur
from constantes.Constantes import Constantes
import numpy as np


test_moteur = Moteur(BPR=5, OPR=30, choix_reseau=1)

test_moteur.Calculate_F_MCL_cruise_step(mach=0.78, h_ft=35000)
print("Poussée moteur à Mach 0.78 et 35000 ft : {:.2f} N".format(test_moteur.get_F_MCL_cruise_step()))

# 2. Calcul de la SFC pour une poussée donnée
# Imaginons que pour tenir la croisière, on a besoin de 5000 N par moteur
poussee_requise = 5000 # Newtons
sfc = test_moteur.Calculate_SFC_cruise(mach=0.78, h_ft=35000, F_engine_N=poussee_requise)

print(f"SFC à {poussee_requise} N : {sfc:.8f} kg/N/s")
print(f"SFC \"classique\" (g/kN/s) : {sfc * 1000 * 1000:.4f} g/kN/s")