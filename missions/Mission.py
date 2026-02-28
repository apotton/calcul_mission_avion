from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
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
    def Principal(Avion : Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs):
        '''
        Réalisation de la boucle principale: l'avion effectue plusieurs missions complètes
        jusqu'à convergence du fuel mission utilisé.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphère
        :param Enregistrement: Instance de la classe Enregistrement
        '''
        n_iter = 0
        Inputs.validate()
        ecart_mission = 100 # %
        Enregistrement.reset()
        Enregistrement.save_simu(Avion, ecart_mission)

        tstart = timeit.default_timer()
        while ecart_mission > Inputs.precision and n_iter < Inputs.maxIter:
            # Initialisations
            Enregistrement.reset()
            FB_mission = Avion.Masse.getFuelMission()

            # Mission principale (montée, croisière, descente)
            Montee.Monter(Avion, Atmosphere, Enregistrement, Inputs, Inputs.dtClimb)
            Croisiere.Croisiere(Avion, Atmosphere, Enregistrement, Inputs, Inputs.dtCruise)
            Descente.Descendre(Avion, Atmosphere, Enregistrement, Inputs, Inputs.dtDescent)

            # Diversion
            Diversion.Diversion(Avion, Atmosphere, Enregistrement, Inputs)

            # Holding
            Holding.Hold(Avion, Atmosphere, Enregistrement, Inputs)

            # Calcul de précision (écart relatif)
            ecart_mission = abs(FB_mission - Avion.Masse.getFuelMission()) / FB_mission * 100
            print(f"Boucle n°{n_iter+1} - Précision {ecart_mission:.3f}%")

            # Remise à zéro pour la boucle suivante
            Avion.reset()
            Enregistrement.save_simu(Avion, ecart_mission)
            n_iter += 1

        tend = timeit.default_timer()
        temps_total = (tend - tstart)

        # Vérification de la solution obtenue
        Mission.checkMission(Avion, Inputs, ecart_mission)
        
        print("")
        print(f"Temps de calcul complet: {temps_total:.4f} secondes")
        print("")

        Enregistrement.save_final(Avion)

        # Fin de l'enregistrement
        Enregistrement.cut()

    @staticmethod
    def checkMission(Avion: Avion, Inputs: Inputs, ecart_mission):
        # Vérification de la validité de la solution (mettre une fonction précise)
        m_fuel_total = Avion.Masse.getFuelMission() + Avion.Masse.getFuelReserve()
        assert m_fuel_total <= Avion.getMaxFuelWeight(), \
              f"\033[31mLa mission demande trop de carburant (m_fuel obtenue: {m_fuel_total:.2f}, m_fuel max: {Avion.getMaxFuelWeight():.2f})\033[0m"

        succes = True

        # Croisière inexistante
        if (Avion.l_climb + Avion.l_descent > Inputs.l_mission_NM * Constantes.conv_NM_m):
            succes = False
            print("\033[33mLa mission est trop courte au vu de la montée et descente souhaitées: la croisière n'a pas eu lieu.\033[0m") 

        # Précision non atteinte
        if (ecart_mission > Inputs.precision):
            succes = False
            print("\033[33mLa précision demandée n'a pas été atteinte. Essayez d'augmenter le nombre d'itérations ou de réduire les pas de temps.\033[0m")

        if succes:
            print("\033[32mMission calculée avec succès.\033[0m")
