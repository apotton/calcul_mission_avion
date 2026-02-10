
from avions.Avion import Avion
from moteurs.Moteur import Moteur
from constantes.Constantes import Constantes
import numpy as np

from moteurs.ReseauMoteur import ReseauMoteur
from moteurs.ElodieRoux import ElodieRoux



A320 = Avion()

Mach_cruise_step = 0.78

A320.Aero.setMach_t(0.78)
print(A320.Aero.getMach())

h_cruise_step_ft = 3.7012e+04
h_t = h_cruise_step_ft * Constantes.conv_ft_m


Avion.Add_dh(A320, h_t)
print(Avion.geth(A320))

test_moteur = ReseauMoteur(A320, BPR=5, OPR=30)


test_moteur.Calculate_F()
print("Poussée moteur à Mach {:.2f} et {:.0f} ft : {:.2f} N".format(Mach_cruise_step, h_cruise_step_ft, test_moteur.getF_MCL_cruise_step()))



# 2. Calcul de la SFC pour une poussée donnée
# Imaginons que pour tenir la croisière, on a besoin de 5000 N par moteur

# 1. Définition de la variable (C'est cette ligne qui manquait à l'appel)
F_cruise_step =3.5619e+04

# 2. Calcul (Assurez-vous que test_moteur est bien instancié avant)
test_moteur.Calculate_SFC(F_engine_N=F_cruise_step/2)

# 3. Affichages
# Attention : j'ai changé le formatage ici (voir explication plus bas)
print(f"SFC à {F_cruise_step:.0f} N : {test_moteur.getSFC():.2e} kg/N/s") 
print(f"SFC \"classique\" (g/kN/s) : {test_moteur.getSFC() * 1e6:.4f} g/kN/s")