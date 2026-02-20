from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from missions.Montee import Montee
from missions.Descente import Descente
from missions.Croisiere import Croisiere
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
        m_init = Avion.Masse.getCurrentMass()

        # Enregistrement de la distance actuelle pour mesurer la longueur de la diversion
        l_end = Avion.getl() + Inputs.rangeDiversion_NM * Constantes.conv_NM_m

        # Montée de diversion
        Montee.monterDiversion(Avion, Atmosphere, Enregistrement, dt = Inputs.dtClimb)
        
        # Croisière diversion
        Diversion.cruiseAltSAR(Avion, Atmosphere, Enregistrement, l_end, dt = Inputs.dtCruise)

        # Descente de diversion
        Descente.descendreDiversion(Avion, Atmosphere, Enregistrement, dt = Inputs.dtDescent)

        # Fin de la diversion
        Avion.diversion = False
        Avion.Masse.m_fuel_diversion = m_init - Avion.Masse.getCurrentMass()


    @staticmethod
    def cruiseAltSAR(Avion:Avion, Atmosphere:Atmosphere, Enregistrement:Enregistrement, l_end, dt=Inputs.dtCruise):
        """
        Croisière à altitude constante avec optimisation du SAR.
        Le Mach est recalculé à chaque pas pour atteindre k * SAR_max.

        :param Avion: instance Avion
        :param Atmosphere: instance Atmosphere
        :param Enregistrement: instance Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        :param dt: pas de temps
        """
        
        while Avion.getl() < l_end - Avion.getl_descent_diversion():
            Mach_opt, _ = Croisiere.calculateSpeed_target(Avion, Atmosphere)

            ## Mise à jour avion en fonction du Mach optimal, tout passe en scalaire
            Avion.Aero.setMach(Mach_opt)
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)

            # Moteur
            Avion.Moteur.calculateFCruise()
            Avion.Moteur.calculateSFCCruise()

            # Intégration
            Avion.Add_dl(Avion.Aero.getTAS() * dt)

            # Consommation
            Avion.Masse.burnFuel(dt)

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)

