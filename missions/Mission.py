from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from missions.Croisiere import Croisiere
from missions.Diversion import Diversion
from missions.Descente import Descente
from missions.Holding import Holding
from missions.Montee import Montee
from inputs.Inputs import Inputs
from avions.Avion import Avion
import timeit

class Mission:
    @staticmethod
    def Principal(Avion : Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement):
        '''
        Réalisation de la boucle principale: l'avion effectue plusieurs missions complètes
        jusqu'à convergence du fuel mission utilisé.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphère
        :param Enregistrement: Instance de la classe Enregistrement
        '''
        ecart_mission = 100 # %
        Enregistrement.reset()
        Enregistrement.save_simu(Avion, ecart_mission)
        n_iter = 0

        tstart = timeit.default_timer()
        while ecart_mission > Inputs.precision and n_iter < Inputs.maxIter:
            # Initialisations
            Enregistrement.reset()
            masse_init = Avion.Masse.getCurrentMass()

            # Mission principale (montée, croisière, descente)
            Montee.Monter(Avion, Atmosphere, Enregistrement)
            Croisiere.Croisiere(Avion, Atmosphere, Enregistrement)
            Descente.Descendre(Avion, Atmosphere, Enregistrement)
            FB_mission = masse_init - Avion.Masse.getCurrentMass()

            # Diversion
            masse_init = Avion.Masse.getCurrentMass()
            Diversion.Diversion(Avion, Atmosphere, Enregistrement)
            FB_diversion = masse_init - Avion.Masse.getCurrentMass()

            # Holding
            masse_init = Avion.Masse.getCurrentMass()
            Holding.Hold(Avion, Atmosphere, Enregistrement)
            FB_holding = masse_init - Avion.Masse.getCurrentMass()

            # Calcul de précision (écart relatif)
            ecart_mission = abs(FB_mission - Avion.Masse.getFuelMission()) / Avion.Masse.getFuelMission() * 100
            print(f"Ecart mission {ecart_mission:.3f}%")

            # Remise à zéro pour la boucle suivante
            Avion.reset(FB_mission, FB_diversion, FB_holding)
            Enregistrement.save_simu(Avion, ecart_mission)
            n_iter += 1
        tend = timeit.default_timer()
        temps_total = (tend - tstart)

        print(f"Temps pour une boucle complète: {temps_total:.4f} secondes")
        print("Carburant mission: " + str(Avion.Masse.getFuelMission()) + " kg")
        print("Carburant réserve: " + str(Avion.Masse.getFuelReserve()) + " kg")

        # Fin de l'enregistrement
        Enregistrement.cut()