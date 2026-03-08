from atmosphere.Atmosphere import Atmosphere
from inputs.Inputs import Inputs
import numpy as np
import timeit

inputs = Inputs()

h = np.array([0, 1000, 2000, 10000])

atmos = Atmosphere(Inputs=inputs)

def f():
    atmos.calculateRhoPT(1000)

duree = timeit.timeit(f, number=int(1e6))

print(f"Durée d'exécution: {duree}s")
