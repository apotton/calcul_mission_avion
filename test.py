import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
from moteurs.ElodieRoux.ElodieRoux import ElodieRoux
from inputs.Inputs import Inputs
from constantes.Constantes import Constantes

a = 5e-2; b = 13

print(f"a:{a} b:{b}")
print(f"A est plus petit que b: {3*(a<b) + 2*(b<a)}")

inputs = Inputs()
mon_avion = Avion(inputs)
mon_atmosphere = Atmosphere(inputs)
