from constantes.Constantes import Constantes
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere


A320 = Avion("Airbus_A320.csv")

print(A320.getWingspan())
print(A320.getName())
print(A320.getLength())
print(A320.getHeight())

print(Constantes.g)
print(Atmosphere.T0_K)

test_atmos  = Atmosphere()
test_atmos.CalculateRhoPT(15000)
print("At 15000 m: rho = {:.4f} kg/m³, p = {:.2f} Pa, T = {:.2f} K".format(test_atmos.rho_t, test_atmos.P_t, test_atmos.T_t))

print("Cx_t = " + str(A320.Aero.Cx_t))

print("Masse actuelle = " + str(A320.Masse.getCurrentMass()) + " kg")

#Test Aero

A320.Aero.CalculateCz(test_atmos)
Cz = A320.Aero.getCz()

A320.Aero.CalculateCxClimb_Simplified()
Cx_Climb = A320.Aero.getCx()

A320.Aero.CalculateCxCruise_Simplified()
Cx_Cruise = A320.Aero.getCx()

A320.Aero.CalculateCxDescent_Simplified()
Cx_Descent = A320.Aero.getCx()

print(Cz)
print(Cx_Climb)
print(Cx_Cruise)
print(Cx_Descent)

# Test de l'obtention de l'envergure dans la classe avion
env = A320.Envergure
print("Envergure de l'avion : " + str(env) + " m")

# Test de l'obtention de l'envergure via la méthode getEnvergure()
env_method = A320.getEnvergure()
print("Envergure de l'avion via méthode : " + str(env_method) + " m")

# Test du calcul complet de Cx
A320.Aero.CalculateCx(test_atmos)
Cx_complete = A320.Aero.getCx()
print("Cx complet calculé : " + str(Cx_complete))

# Test du calcul de Cz buffet
cz_buffet = A320.Aero.CalculateCzBuffet()
print("Cz buffet calculé : " + str(A320.Aero.getCzBuffet()))

# Test du calcul de Cz
A320.Aero.CalculateCz(test_atmos)
print("Cz calculé : " + str(A320.Aero.getCz()))

print("Test complete.")