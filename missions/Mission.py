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
            FB_mission = Avion.Masse.getFuelMission()

            # Mission principale (montée, croisière, descente)
            Montee.Monter(Avion, Atmosphere, Enregistrement)
            Croisiere.Croisiere(Avion, Atmosphere, Enregistrement)
            Descente.Descendre(Avion, Atmosphere, Enregistrement)

            # Diversion
            Diversion.Diversion(Avion, Atmosphere, Enregistrement)

            # Holding
            Holding.Hold(Avion, Atmosphere, Enregistrement)

            # Calcul de précision (écart relatif)
            ecart_mission = abs(FB_mission - Avion.Masse.getFuelMission()) / FB_mission * 100
            print(f"Ecart mission {ecart_mission:.3f}%")

            # Remise à zéro pour la boucle suivante
            Avion.reset()
            Enregistrement.save_simu(Avion, ecart_mission)
            n_iter += 1
        tend = timeit.default_timer()
        temps_total = (tend - tstart)
        Enregistrement.save_final(Avion)

        print(f"Temps pour une boucle complète: {temps_total:.4f} secondes")

        # Fin de l'enregistrement
        Enregistrement.cut()