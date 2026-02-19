from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere

class PointPerformance():


    @staticmethod
    def setupAvion(Avion: Avion, Atmosphere: Atmosphere):
        SpeedType = "Mach"  # Inputs.SpeedType
        Speed = 0.78
        alt_ft = 33_000 # Inputs.Altitude
        mass_kg = 32_000 # Inputs.Mass
        DISA_dC = 0

        Atmosphere.CalculateRhoPT(alt_ft * Constantes.conv_ft_m, DISA_dC)
        Avion.Masse.setMass(mass_kg)

        # Set des vitesses
        match SpeedType:
            case "Mach":
                Avion.Aero.setMach_t(Speed)
                Avion.Aero.convertMachToCAS(Atmosphere)
                Avion.Aero.convertMachToTAS(Atmosphere)
            case "TAS":
                Avion.Aero.setTAS_t(Speed * Constantes.conv_kt_mps)
                Avion.Aero.convertTASToMach(Atmosphere)
                Avion.Aero.convertMachToCAS(Atmosphere)
            case "CAS":
                Avion.Aero.setCAS_t(Speed * Constantes.conv_kt_mps)
                Avion.Aero.convertCASToMach(Atmosphere)
                Avion.Aero.convertMachToTAS(Atmosphere)
            case _:
                print("Erreur de vitesse (ni Mach, ni CAS, ni TAS)")

    @staticmethod
    def Performance(Avion: Avion, Atmosphere:Atmosphere):
        # Setup avec les inputs
        PointPerformance.setupAvion(Avion, Atmosphere)
        
        # Conditions atmosphérique
        Atmosphere.CalculateRhoPT(Avion.geth())
        rho = Atmosphere.getRho_t()
        P = Atmosphere.getP_t()
        T = Atmosphere.getT_t()

        # Cz, Cx, finesse, vitesses
        Avion.Aero.calculateCz(Atmosphere)
        Avion.Aero.calculateCx(Atmosphere)
        Cx = Avion.Aero.getCx()
        Cz = Avion.Aero.getCz()
        finesse = Cz/Cx


        # Poussée / SFC / FF max
        Avion.Moteur.calculateFClimb()
        Avion.Moteur.calculateSFCClimb()
        F_N_max = Avion.Moteur.getF()
        F_F_max = Avion.Moteur.getFF()
        SFC_max = Avion.Moteur.getSFC()


        # Poussée / SFC / FF équilibre
        Avion.Moteur.calculateFCruise()
        Avion.Moteur.calculateSFCCruise()
        F_N_max = Avion.Moteur.getF()
        F_F_max = Avion.Moteur.getFF()
        SFC_max = Avion.Moteur.getSFC()



        





