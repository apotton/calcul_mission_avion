from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from missions.Montee import Montee
from missions.Descente import Descente
import numpy as np

class Diversion:
    @staticmethod
    def Diversion(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement):
        '''
        Réalise toutes les opérations liées à la phase de diversion.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        '''
        # Entrée en diversion
        Avion.diversion = True

        # Enregistrement de la distance actuelle pour mesurer la longueur de la diversion
        l_fin_mission = Avion.getl()

        # Montée de diversion
        Montee.monterDiversion(Avion, Atmosphere, Enregistrement, dt = Inputs.dt_climb)
        
        # Croisière diversion
        Diversion.croisiereDiversion(Avion, Atmosphere, Enregistrement, l_fin_mission, dt = Inputs.dt_cruise)

        # Descente de diversion
        Descente.descendreDiversion(Avion, Atmosphere, Enregistrement, dt = Inputs.dt_descent)

        # Fin de la diversion
        Avion.diversion = False


    @staticmethod
    def croisiereDiversion(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, l_debut, dt = Inputs.dt_cruise):
            '''
            Croisière en palier à Mach constant

            :param Avion: instance de la classe Avion
            :param Atmosphere: instance de la classe Atmosphere
            :param Enregistrement: Instance de la classe Enregistrement
            :param l_debut: début de la diversion, avant la montée (m)
            :param dt: Pas de temps (s)
            '''

            l_end_diversion = Inputs.Range_diversion_NM * Constantes.conv_NM_m
            l_descent_diversion = Avion.getl_descent_diversion()

            # Tant que l'on n'a pas parcouru la distance de diversion
            while (Avion.getl() < (l_debut + l_end_diversion - l_descent_diversion)):

                # Atmosphère
                Atmosphere.CalculateRhoPT(Avion.geth())

                # Vitesse
                Avion.Aero.convertMachToTAS(Atmosphere)
                Avion.Aero.convertMachToCAS(Atmosphere)

                # Vitesses
                Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

                # Aérodynamique
                Avion.Aero.calculateCz(Atmosphere)
                Avion.Aero.calculateCx(Atmosphere)

                # Poussée moteur
                Avion.Moteur.calculateFCruiseDiversion()
                Avion.Moteur.calculateSFCCruiseDiversion()

                # Fuel burn
                Avion.Masse.burnFuel(dt)

                # Mise à jour avion
                Avion.Add_dl(Vx * dt)

                Enregistrement.save(Avion, Atmosphere, dt)



