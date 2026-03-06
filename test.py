import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
from moteurs.ElodieRoux.ElodieRoux import ElodieRoux
from inputs.Inputs import Inputs

a = 5e-2; b = 13

print(f"a:{a} b:{b}")

inputs = Inputs()
mon_avion = Avion(inputs)
mon_atmosphere = Atmosphere(inputs)
# print(f"Masse avion: {mon_avion.Masse.getCurrentMass()}")

moteur = ElodieRoux(mon_avion)

mon_avion.set_h(10000)
mon_avion.Aero.setMach(0.7)
mon_atmosphere.CalculateRhoPT(mon_avion.geth())

Fmax = moteur.calculateFmax(mon_atmosphere, -40)

print(f"Poussée maximale obtenue: {Fmax:.1f} N")
print(f"Pour deux moteurs: {2*Fmax:.1f} N")