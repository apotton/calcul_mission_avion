from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class PointPerformance():


    @staticmethod
    def setupAvion(Avion: Avion, Atmosphere: Atmosphere):
        SpeedType = "Mach"  # Inputs.SpeedType
        Speed = 0.78
        alt_ft = 38_000 # Inputs.Altitude
        mass_kg = 60_000 # Inputs.Mass
        DISA_dC = 0

        Avion.set_h(alt_ft * Constantes.conv_ft_m)
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

        # Vitesses (en kt)
        Mach = Avion.Aero.getMach()
        TAS  = Avion.Aero.getTAS() / Constantes.conv_kt_mps
        CAS  = Avion.Aero.getCAS() / Constantes.conv_kt_mps
        q = 1/2 * rho * (TAS * Constantes.conv_kt_mps) ** 2 # Pression dynamique

        # Cz, Cx, finesse
        Avion.Aero.calculateCz(Atmosphere)
        Avion.Aero.calculateCx(Atmosphere)
        Cx = Avion.Aero.getCx()
        Cz = Avion.Aero.getCz()
        finesse = Cz/Cx
        R_X = Avion.Masse.getCurrentWeight() / finesse # N

        # Poussée / SFC / FF max (N, kg/N/h, kg/h)
        Avion.Moteur.calculateFClimb()
        Avion.Moteur.calculateSFCClimb()
        F_N_max = Avion.Moteur.getF()
        F_F_max = Avion.Moteur.getFF()  * 3600
        SFC_max = Avion.Moteur.getSFC() * 3600
        pente = np.asin((F_N_max - R_X) / Avion.Masse.getCurrentWeight())
        ROC = pente * (TAS * Constantes.conv_kt_mps)

        # Poussée / SFC / FF équilibre
        Avion.Moteur.calculateFCruise()
        Avion.Moteur.calculateSFCCruise()
        F_N_eq = Avion.Moteur.getF()
        F_F_eq = Avion.Moteur.getFF()  * 3600
        SFC_eq = Avion.Moteur.getSFC() * 3600
        SAR = TAS / F_F_eq 

        # Structuration des résultats pour l'affichage
        donnees_perf = {
            "Conditions Atmosphériques": [
                ("Altitude", Avion.geth() / Constantes.conv_ft_m , "ft"),
                ("Température", T - 273.15 , "°C"),
                ("Pression", P, "Pa"),
                ("Densité (rho)", rho, "kg/m³")
            ],
            "Vitesses & Pressions": [
                ("Mach", Mach, "-"),
                ("TAS", TAS, "kt"),
                ("CAS", CAS, "kt"),
                ("Pression dynamique (q)", q, "Pa")
            ],
            "Aérodynamique": [
                ("Cz", Cz, "-"),
                ("Cx", Cx, "-"),
                ("Finesse (L/D)", finesse, "-"),
                ("Traînée (Rx)", R_X, "N")
            ],
            "Performances Montée (Max)": [
                ("Poussée max", F_N_max, "N"),
                ("Fuel Flow max", F_F_max, "kg/h"),
                ("SFC max", SFC_max, "kg/N/h"),
                ("Pente de montée", pente * 180 / np.pi, "°"),
                ("Rate of Climb (ROC)", ROC / Constantes.conv_kt_mps * 60 , "ft/m") 
            ],
            "Performances Croisière (Équilibre)": [
                ("Poussée équilibre", F_N_eq, "N"),
                ("Fuel Flow", F_F_eq, "kg/h"),
                ("SFC", SFC_eq, "kg/N/h"),
                ("Specific Air Range (SAR)", SAR, "nm/kg")
            ]
        }

        PointPerformance.afficher_point_performance(donnees_perf)

    @staticmethod
    def afficher_point_performance(donnees):
        """
        Prend en entrée un dictionnaire de catégories contenant des listes de tuples 
        (nom, valeur, unité) et les affiche proprement dans la console.
        """
        ligne = "=" * 65
        print(f"\n{ligne}")
        print(f"{'RÉSUMÉ DU POINT PERFORMANCE':^65}")
        print(f"{ligne}")

        for categorie, variables in donnees.items():
            print(f"\n--- {categorie.upper()}")
            
            for nom, valeur, unite in variables:
                # <30  : Nom aligné à gauche sur 30 caractères
                # >12.4f : Valeur alignée à droite sur 12 caractères avec 4 décimales
                # <8   : Unité alignée à gauche sur 8 caractères
                print(f"    {nom:<30} : {valeur:>12.4f}  {unite:<8}")
                
        print(f"\n{ligne}\n")






        





