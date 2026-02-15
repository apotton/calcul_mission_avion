from enregistrement.Enregistrement import Enregistrement
from missions.Croisiere import Croisiere
from missions.Diversion import Diversion
from missions.Descente import Descente
from missions.Holding import Holding
from missions.Montee import Montee
from atmosphere.Atmosphere import Atmosphere
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Mission:
    @staticmethod
    def Principal(Avion : Avion, Atmosphere: Atmosphere):
        # Mission principale
        ecart_mission = 100 # %
        Enregistrement.save_simu(Avion, ecart_mission)

        while ecart_mission > Inputs.precision:
            Enregistrement.reset()
            masse_init = Avion.Masse.getCurrentMass()
            Montee.Monter(Avion, Atmosphere, dt = Inputs.dt_climb)
            Croisiere.Croisiere(Avion, Atmosphere, dt = Inputs.dt_cruise)
            Descente.Descendre(Avion, Atmosphere, Inputs.dt_descent)
            FB_mission = masse_init - Avion.Masse.getCurrentMass()

            # Diversion
            masse_init = Avion.Masse.getCurrentMass()
            Diversion.Diversion(Avion, Atmosphere)
            FB_diversion = masse_init - Avion.Masse.getCurrentMass()

            # Holding
            masse_init = Avion.Masse.getCurrentMass()
            Holding.Hold(Avion, Atmosphere, Inputs.dt_cruise)
            FB_holding = masse_init - Avion.Masse.getCurrentMass()

            # Calcul de précision
            ecart_mission = abs(FB_mission - Avion.Masse.getFuelMission()) / Avion.Masse.getFuelMission() * 100
            # print(f"Ecart mission {ecart_mission:.2f}%")

            # Remise à zéro pour la boucle suivante
            Avion.reset(FB_mission, FB_diversion, FB_holding)
            Enregistrement.save_simu(Avion, ecart_mission)

        # Fin de l'enregistrement
        Enregistrement.cut()