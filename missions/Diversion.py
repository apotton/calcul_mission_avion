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
    def Diversion(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs):
        '''
        Réalise toutes les opérations liées à la phase de diversion.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param Inputs: Instance de la classe Inputs
        '''
        # Entrée en diversion
        m_init = Avion.Masse.getCurrentMass()
        t_init = Avion.get_t()
        l_init = Avion.getl()

        # Enregistrement de la distance actuelle pour mesurer la longueur de la diversion
        l_end = Avion.getl() + Inputs.rangeDiversion_NM * Constantes.conv_NM_m

        # Montée de diversion
        Montee.monterDiversion(Avion, Atmosphere, Enregistrement, Inputs, dt = Inputs.dtClimb)
        
        # Croisière diversion
        Diversion.cruiseAltSAR(Avion, Atmosphere, Enregistrement, Inputs, l_end, dt = Inputs.dtCruise)

        # Descente de diversion
        Descente.descendreDiversion(Avion, Atmosphere, Enregistrement, Inputs, dt = Inputs.dtDescent)

        # Fin de la diversion
        Avion.set_l_diversion(Avion.getl() - l_init)
        Avion.set_t_diversion(Avion.get_t() - t_init)
        Avion.Masse.setFuelDiversion(m_init - Avion.Masse.getCurrentMass())


    @staticmethod
    def cruiseAltSAR(Avion:Avion, Atmosphere:Atmosphere, Enregistrement:Enregistrement, Inputs: Inputs, l_end, dt):
        """
        Croisière à altitude constante avec optimisation du SAR.
        Le Mach est recalculé à chaque pas pour atteindre k * SAR_max.

        :param Avion: instance Avion
        :param Atmosphere: instance Atmosphere
        :param Enregistrement: instance Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        :param dt: pas de temps
        """
        l_t = Avion.getl()
        l_target = l_end - Avion.getl_descent_diversion()
        
        while (l_t < l_target):
            Mach_opt, CAS_opt = Croisiere.calculateSpeed_target(Avion, Atmosphere, Inputs)

            # Ajustement de la vitesse si on s'éloigne trop de l'optimum
            if abs(Avion.Aero.getMach() - Mach_opt) > 0.01:
                if Avion.Aero.getMach() < Mach_opt:
                    Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt=Inputs.dtClimb)
                else:
                    Descente.descentePalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt=Inputs.dtDescent)

            ## Mise à jour avion en fonction du Mach optimal
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
            Vx = Avion.Aero.getTAS() + Inputs.Vw_kt * Constantes.conv_kt_mps
            Avion.Add_dl(Vx * dt)

            if Avion.getl() > l_target:
                # Intersection du pas de temps
                dt = (l_target - l_t) / (Avion.getl() - l_t) * dt
                # On se place à la distance visée
                Avion.set_l(l_target)
            
            l_t = Avion.getl()

            # Consommation
            Avion.Masse.burnFuel(dt)

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)

