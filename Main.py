from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Mission import Mission
import matplotlib.pyplot as plt
from avions.Avion import Avion
import timeit

A320 = Avion()
Atmos  = Atmosphere()
Saving = Enregistrement()

tstart = timeit.default_timer()

# Boucle sur une mission
Mission.Principal(A320, Atmos, Saving)

tend = timeit.default_timer()

temps_total = (tend - tstart)

print(f"Temps pour une boucle complète: {temps_total:.4f} secondes")
print("Essence mission: " + str(A320.Masse.getFuelMission()) + " kg")
print("Essence réserve: " + str(A320.Masse.getFuelReserve()) + " kg")


Saving.cut()

# plt.figure()
# plt.plot(Saving.data["t"]/60, Saving.data["CAS"])
# plt.show()

# Altitude en fonction de la distance
plt.figure()
plt.plot(Saving.data["l"]/Constantes.conv_NM_m,
         Saving.data["h"]/Constantes.conv_ft_m)
plt.xlabel("Distance parcourue (NM)")
plt.ylabel("Altitude (ft)")
plt.show()

# plt.figure()
# plt.plot(np.log10(Saving.data_simu["ecart_mission"]))
# plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["l_descent"])
# plt.plot(Saving.data_simu["l_descent_diversion"])
# plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["FB_mission"])
# plt.show()
