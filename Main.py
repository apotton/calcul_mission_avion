from constantes.constantes import Constantes
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere


A320 = Avion("Airbus_A320.csv")

print(A320.getWingspan())
print(A320.getName())
print(A320.getLength())
print(A320.getHeight())

print(Constantes.g)
print(Atmosphere.T0_K)

test  = Atmosphere()
rho, p, T = test.getRhoPT(15000)
print("At 15000 m: rho = {:.4f} kg/m³, p = {:.2f} Pa, T = {:.2f} K".format(rho, p, T))

print("Test complete.")