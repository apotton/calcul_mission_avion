from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Montee:
    @staticmethod
    def Monter(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, dt):
        '''
        Réalise toute la montée principale jusqu'à la croisière.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        Avion.Masse.setFuelMission(0.)
        m_init = Avion.Masse.getCurrentMass()
        t_init = Avion.get_t()
        l_init = Avion.getl()

        # Initialisations
        Avion.set_h(Inputs.hInit_ft*Constantes.conv_ft_m)
        Avion.Aero.setCAS(Inputs.CAS_below_10000_mont_kt * Constantes.conv_kt_mps)

        h_target = Inputs.hAccel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, Enregistrement, Inputs, h_target, Inputs.dtClimb)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_target, dt)

        h_target = Inputs.hCruise_ft * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, Enregistrement, Inputs, h_target, Inputs.Mach_climb, Inputs.dtClimb)
        Montee.climbIsoMach(Avion, Atmosphere, Enregistrement, Inputs, h_target, Inputs.dtClimb)

        Avion.set_l_climb(Avion.getl() - l_init)
        Avion.set_t_climb(Avion.get_t() - t_init)
        Avion.Masse.setFuelClimb(m_init - Avion.Masse.getCurrentMass())
        Avion.Masse.addFuelMission(m_init - Avion.Masse.getCurrentMass())

    @staticmethod
    def monterDiversion(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, dt):
        '''
        Réalise la montée de la phase de diversion.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        h_target = Inputs.hAccel_ft * Constantes.conv_ft_m
        Montee.climbLowAltitude(Avion, Atmosphere, Enregistrement, Inputs, h_target, dt)

        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps
        Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_target, dt)

        h_target = Inputs.cruiseDiversionAlt_ft * Constantes.conv_ft_m
        Montee.climbIsoCAS(Avion, Atmosphere, Enregistrement, Inputs, h_target, Inputs.MachCruiseDiversion, dt)
        
        Montee.climbIsoMach(Avion, Atmosphere, Enregistrement, Inputs, h_target, dt)
        

    @staticmethod
    def climbLowAltitude(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, h_lim, dt):
        '''
        Montée à CAS constant jusqu'à atteindre l'altitude d'accéleration en palier.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin (en mètres)
        :param dt: pas de temps (s)
        '''
        h_t = Avion.geth()

        while h_t < h_lim:
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
            Vx = Avion.Aero.getTAS() * np.cos(pente) + Inputs.Vw_kt * Constantes.conv_kt_mps

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)

            if Avion.geth() > h_lim:
                # Intersection du pas de temps
                dt = (h_lim - h_t) / (Avion.geth() - h_t) * dt
                # On se place à l'altitude visée
                Avion.set_h(h_lim)
            
            h_t = Avion.geth()

            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbPalier(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, CAS_target, dt):
        '''
        Phase 2 : accélération en palier à 10 000 ft
        CAS : 250 kt -> CAS_climb_target

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param Inputs: Instance de la classe Inputs
        :param CAS_target: Vitesse CAS à atteindre
        :param dt: Pas de temps (s)
        '''

        # Atmosphère (constante en palier)
        Atmosphere.CalculateRhoPT(Avion.geth())

        # Vitesses
        Avion.Aero.convertCASToMach(Atmosphere)
        Avion.Aero.convertMachToTAS(Atmosphere)

        CAS_t = Avion.Aero.getCAS()

        while CAS_t < CAS_target:

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
            Avion.Aero.setTAS(Avion.Aero.getTAS() + ax*dt)

            # Recalcul Mach et CAS
            Avion.Aero.convertTASToMach(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            if Avion.Aero.getCAS() > CAS_target:
                # Intersection du pas de temps
                dt = (CAS_target - CAS_t) / (Avion.Aero.getCAS() - CAS_t) * dt

                # Set du CAS visé
                Avion.Aero.setCAS(CAS_target)
                Avion.Aero.convertCASToMach(Atmosphere)
                Avion.Aero.convertMachToTAS(Atmosphere)

            CAS_t = Avion.Aero.getCAS()

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Cinématique
            Vx = Avion.Aero.getTAS() + Inputs.Vw_kt * Constantes.conv_kt_mps
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)
            
            # Pas de changement d'altitude en palier            
            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoCAS(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, h_lim, Mach_lim, dt):
        '''
        Montée à CAS constant jusqu'à atteindre un Mach cible

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin de montée (m)
        :param Mach_lim: Mach de fin de montée
        :param dt: pas de temps (s)
        '''
        Mach_t = Avion.Aero.getMach()
        h_t = Avion.geth()

        # Tant que l'on a pas atteint le Mach limite ou l'altitude limite
        while Avion.Aero.getMach() < Mach_lim and h_t < h_lim:
            # Atmosphère
            Atmosphere.CalculateRhoPT(h_t)

            # Vitesses
            Avion.Aero.convertCASToMach(Atmosphere)

            # On checke si on a atteint le Mach visé
            if Avion.Aero.getMach() > Mach_lim:
                # On adapte le pas de temps à l'intersection des Machs
                dt = (Mach_lim - Mach_t) / (Avion.Aero.getMach() - Mach_t) * dt

                # On se place au Mach visé
                Avion.Aero.setMach(Mach_lim)
                Avion.Aero.convertMachToCAS(Atmosphere)
            
            Avion.Aero.convertMachToTAS(Atmosphere)
            Mach_t = Avion.Aero.getMach()

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
            Vx = Avion.Aero.getTAS() * np.cos(pente) + Inputs.Vw_kt * Constantes.conv_kt_mps

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)

            if Avion.geth() > h_lim:
                # Intersection du pas de temps
                dt = (h_lim - h_t) / (Avion.geth() - h_t) * dt
                # On se place à l'altitude visée
                Avion.set_h(h_lim)
            
            h_t = Avion.geth()

            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, h_lim, dt):
        '''
        Montée à Mach constant jusqu'à une altitude cible.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param h_lim: Altitude de fin de montée (m)
        :param dt: pas de temps (s)
        '''
        h_t = Avion.geth()

        # Tant que l'on n'a pas atteint l'altitude cible
        while h_t < h_lim:

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
            Vx = Avion.Aero.getTAS() * np.cos(pente) + Inputs.Vw_kt * Constantes.conv_kt_mps

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)

            if Avion.geth() > h_lim:
                # Intersection du pas de temps
                dt = (h_lim - h_t) / (Avion.geth() - h_t) * dt
                # On se place à l'altitude visée
                Avion.set_h(h_lim)
            
            h_t = Avion.geth()

            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)
            
            # Fuel burn
            Avion.Masse.burnFuel(dt)
            
            Enregistrement.save(Avion, Atmosphere, dt)
