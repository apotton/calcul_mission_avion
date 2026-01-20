from moteurs.Moteur import Moteur
from constantes.Constantes import Constantes
import numpy as np


test_moteur = Moteur(BPR=5, OPR=30, choix_reseau=1)


h_cruise_step_ft = 3.7012e+04
Mach_cruise_step = 0.78

test_moteur.Calculate_F_MCL_cruise_step(mach=Mach_cruise_step, h_ft=h_cruise_step_ft)
print("Poussée moteur à Mach {:.2f} et {:.0f} ft : {:.2f} N".format(Mach_cruise_step, h_cruise_step_ft, test_moteur.get_F_MCL_cruise_step()))



# 2. Calcul de la SFC pour une poussée donnée
# Imaginons que pour tenir la croisière, on a besoin de 5000 N par moteur

# 1. Définition de la variable (C'est cette ligne qui manquait à l'appel)
F_cruise_step =3.5619e+04

# 2. Calcul (Assurez-vous que test_moteur est bien instancié avant)
test_moteur.Calculate_SFC_cruise(mach=0.78, h_ft=3.7012e+04, F_engine_N=F_cruise_step/2)

# 3. Affichages
# Attention : j'ai changé le formatage ici (voir explication plus bas)
print(f"SFC à {F_cruise_step:.0f} N : {test_moteur.get_SFC_t():.2e} kg/N/s") 
print(f"SFC \"classique\" (g/kN/s) : {test_moteur.get_SFC_t() * 1e6:.4f} g/kN/s")
