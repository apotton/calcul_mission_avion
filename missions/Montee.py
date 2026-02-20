from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Montee:
    @staticmethod
    def Monter(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtClimb):
        '''
        Réalise toute la montée principale jusqu'à la croisière.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        Avion.Masse.m_fuel_mission = 0
        l_init = Avion.getl()
        m_init = Avion.Masse.getCurrentMass()
        t_init = Avion.t

        # Initialisations
        Avion.set_h(Inputs.hInit_ft*Constantes.conv_ft_m)
        Avion.Aero.setCAS(Inputs.CAS_below_10000_mont_kt * Constantes.conv_kt_mps)

        h_target = Inputs.hAccel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, Enregistrement, h_target, Inputs.dtClimb)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, Enregistrement, CAS_target, dt)

        h_target = Inputs.hCruise_ft * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, Enregistrement, h_target, Inputs.Mach_climb, Inputs.dtClimb)
        Montee.climbIsoMach(Avion, Atmosphere, Enregistrement, h_target, Inputs.dtClimb)

        l_end = Avion.getl()
        m_end = Avion.Masse.getCurrentMass()
        t_end = Avion.t

        Avion.l_climb = l_end - l_init
        Avion.t_climb = t_end - t_init
        Avion.Masse.m_fuel_climb = m_init - m_end
        Avion.Masse.m_fuel_mission += Avion.Masse.m_fuel_climb

    @staticmethod
    def monterDiversion(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtClimb):
        '''
        Réalise la montée de la phase de diversion.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        h_target = Inputs.hAccel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, Enregistrement, h_target, dt)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, Enregistrement, CAS_target, dt)

        h_target = Inputs.cruiseDiversionAlt_ft * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, Enregistrement, h_target, Inputs.MachCruiseDiversion, dt)
        Montee.climbIsoMach(Avion, Atmosphere, Enregistrement, h_target, dt)
        

    @staticmethod
    def climbLowAltitude(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, h_lim, dt):
        '''
        Montée à CAS constant jusqu'à atteindre l'altitude d'accéleration en palier.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin (en mètres)
        :param dt: pas de temps (s)
        '''

        while Avion.geth() < h_lim:
            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses
            Avion.Aero.convertCASToMach(Atmosphere)
            Avion.Aero.convertMachToTAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxClimb_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.calculateFClimb()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCClimb()

            # Check puissance suffisante
            assert F_N >= Rx, "Moteur trop peu puissant en montée"

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbPalier(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, CAS_target, dt = Inputs.dtClimb):
        '''
        Phase 2 : accélération en palier à 10 000 ft
        CAS : 250 kt -> CAS_climb_target

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        dt          : pas de temps (s)
        '''

        # Atmosphère (constante en palier)
        Atmosphere.CalculateRhoPT(Avion.geth())

        # Vitesses
        Avion.Aero.convertCASToMach(Atmosphere)
        Avion.Aero.convertMachToTAS(Atmosphere)
        TAS_t  = Avion.Aero.getTAS()

        while Avion.Aero.getCAS() < CAS_target:

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz_t = Avion.Aero.getCz()

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxClimb_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            
            Cx_t = Avion.Aero.getCx()
            
            finesse = Cz_t / Cx_t
            
            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée moteur
            Avion.Moteur.calculateFClimb()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCClimb()

            # Check puissance suffisante
            assert F_N >= Rx, "Moteur trop peu puissant en montée"

            # Dynamique longitudinale
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # Mise à jour vitesse
            TAS_t = max(TAS_t + ax * dt, 0.0)
            Avion.Aero.setTAS(TAS_t)

            # Recalcul Mach et CAS
            Avion.Aero.convertTASToMach(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Cinématique
            Avion.Add_dl(Avion.Aero.getTAS() * dt)
            Avion.Add_dt(dt)
            
            # Pas de changement d'altitude en palier            
            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoCAS(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, h_lim, Mach_lim, dt = Inputs.dtClimb):
        '''
        Montée à CAS constant jusqu'à atteindre un Mach cible

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin de montée (m)
        :param Mach_lim: Mach de fin de montée
        :param dt: pas de temps (s)
        '''
        Avion.Aero.setCAS(Avion.getKVMO() * Constantes.conv_kt_mps)

        # Tant que l'on a pas atteint le Mach limite ou l'altitude limit
        while Avion.Aero.getMach() < Mach_lim and Avion.geth() < h_lim:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses
            Avion.Aero.convertCASToMach(Atmosphere)
            Avion.Aero.convertMachToTAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxClimb_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.calculateFClimb()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCClimb()

            # Check puissance suffisante
            assert F_N >= Rx, "Moteur trop peu puissant en montée"

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, h_lim, dt = Inputs.dtClimb):
        '''
        Montée à Mach constant jusqu'à une altitude cible.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin de montée (m)
        :param dt: pas de temps (s)
        '''

        # Tant que l'on n'a pas atteint l'altitude cible
        while Avion.geth() < h_lim:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesse
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxClimb_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.calculateFClimb()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCClimb()

            # Check puissance suffisante
            assert F_N >= Rx, "Moteur trop peu puissant en montée"

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)
            
            Enregistrement.save(Avion, Atmosphere, dt)
