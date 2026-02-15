from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Montee:
    @staticmethod
    def Monter(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_climb):
        '''
        Réalise toute la montée principale jusqu'à la croisière.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        # Initialisations
        Avion.set_h(Inputs.h_initial_ft*Constantes.conv_ft_m)
        Avion.Aero.setCAS_t(Inputs.CAS_below_10000_mont_kt * Constantes.conv_kt_mps)

        h_target = Inputs.h_accel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, h_target, Inputs.dt_climb)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, CAS_target, dt)

        h_target = Inputs.h_cruise_init * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, h_target, Inputs.Mach_climb, Inputs.dt_climb)
        Montee.climbIsoMach(Avion, Atmosphere, h_target, Inputs.dt_climb)

    @staticmethod
    def monterDiversion(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_climb):
        '''
        Réalise la montée de la phase de diversion.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        h_target = Inputs.h_accel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, h_target, dt)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, CAS_target, dt)

        h_target = Inputs.Final_climb_altitude_diversion_ft * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, h_target, Inputs.Mach_cruise_div, dt)
        Montee.climbIsoMach(Avion, Atmosphere, h_target, dt)
        

    @staticmethod
    def climbLowAltitude(Avion: Avion, Atmosphere: Atmosphere, h_lim, dt):
        '''
        Montée à CAS constant jusqu'à atteindre l'altitude d'accéleration en palier.

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        h_lim       : Altitude de fin (en mètres)
        dt          : pas de temps (s)
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

            if Inputs.Aero_simplified:
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

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbPalier(Avion: Avion, Atmosphere: Atmosphere, CAS_target, dt = Inputs.dt_climb):
        '''
        Phase 2 : accélération en palier à 10 000 ft
        CAS : 250 kt -> CAS_climb_target

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
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

            if Inputs.Aero_simplified:
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

            # Dynamique longitudinale
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # Mise à jour vitesse
            TAS_t = max(TAS_t + ax * dt, 0.0)
            Avion.Aero.setTAS_t(TAS_t)

            # Recalcul Mach et CAS
            Avion.Aero.convertTASToMach(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Cinématique
            Avion.Add_dl(Avion.Aero.getTAS() * dt)
            
            # Pas de changement d'altitude en palier            
            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoCAS(Avion: Avion, Atmosphere: Atmosphere, h_lim, Mach_lim, dt = Inputs.dt_climb):
        '''
        Montée à CAS constant jusqu'à atteindre un Mach cible

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param h_lim: Altitude de fin de montée (m)
        :param Mach_lim: Mach de fin de montée
        :param dt: pas de temps (s)
        '''
        Avion.Aero.setCAS_t(Avion.getKVMO() * Constantes.conv_kt_mps)

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

            if Inputs.Aero_simplified:
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

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, h_lim, dt = Inputs.dt_climb):
        '''
        Montée à Mach constant jusqu'à une altitude cible.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
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

            if Inputs.Aero_simplified:
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
            
            Enregistrement.save(Avion, Atmosphere, dt)
