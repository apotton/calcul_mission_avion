from avions.Avion import Avion
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
from enregistrement.Enregistrement import Enregistrement
from inputs.Inputs import Inputs
import numpy as np

class Montee:
    def __init__(self):
        self.rien = 0

    def climb_sub_h_1500_ft(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        """
        Montée à CAS constant jusqu'à atteindre l'altitude d'accéleration en palier

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """
        # Initialisations
        Avion.set_h(Inputs.h_initial_ft*Constantes.conv_ft_m)
        Avion.Aero.setCAS_t(Inputs.CAS_below_10000_mont_kt * Constantes.conv_kt_mps) #On initialise la CAS de l'avion

        while Avion.geth() < Inputs.h_accel_ft * Constantes.conv_ft_m:
            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses
            Avion.Aero.Convert_CAS_to_Mach(Atmosphere)
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.Calculate_F()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_climb()

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)

            Enregistrement.save(Avion, Atmosphere, dt)


    def climb_Palier(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        """
        Phase 2 : accélération en palier à 10 000 ft
        CAS : 250 kt -> CAS_climb_target

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """

        # CAS initiale
        CAS_t = Avion.Aero.getCAS() * Constantes.conv_kt_mps

        # CAS cible A CHANGER
        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps

        # Atmosphère (constante en palier)
        Atmosphere.CalculateRhoPT(Avion.geth())

        # Vitesses
        Avion.Aero.Convert_CAS_to_Mach(Atmosphere)
        Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
        TAS_t  = Avion.Aero.getTAS()

        while CAS_t < CAS_target:

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz_t = Avion.Aero.getCz()

            Avion.Aero.CalculateCx(Atmosphere)
            Cx_t = Avion.Aero.getCx()
            finesse = Cz_t / Cx_t

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée moteur
            Avion.Moteur.Calculate_F()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_climb()

            # Dynamique longitudinale
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # Mise à jour vitesse
            TAS_t = max(TAS_t + ax * dt, 0.0)
            Avion.Aero.setTAS_t(TAS_t)

            # Recalcul Mach et CAS
            Avion.Aero.Convert_TAS_to_Mach(Atmosphere)
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)
            CAS_t = Avion.Aero.getCAS()

            # Cinématique (pas de Vz)
            Vx_t = TAS_t
            dl = Vx_t * dt

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            # Mise à jour avion
            Avion.Add_dl(dl)
            
            # Pas de changement d'altitude en palier            
            Enregistrement.save(Avion, Atmosphere, dt)


    def climb_iso_CAS(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        """
        Montée à CAS constant jusqu'à atteindre un Mach cible

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """

        Avion.Aero.setCAS_t(Avion.getKVMO() * Constantes.conv_kt_mps) #On initialise la CAS de l'avion)

        while Avion.Aero.getMach() < Inputs.Mach_climb and Avion.geth() < Inputs.h_cruise_init:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses
            Avion.Aero.Convert_CAS_to_Mach(Atmosphere)
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.Calculate_F()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_climb()

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt) #Un peu redondant, à voir comment modifier
            Avion.Add_dl(Vx * dt)

            Enregistrement.save(Avion, Atmosphere, dt)


    def climb_iso_Mach(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        """
        Montée à Mach constant jusqu'à une altitude cible

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """

        # Mach constant
        Avion.Aero.setMach_t(Inputs.Mach_cruise)

        while Avion.geth() < Inputs.h_cruise_init * Constantes.conv_ft_m:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesse
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.Calculate_F()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_climb()

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            
            Enregistrement.save(Avion, Atmosphere, dt)
