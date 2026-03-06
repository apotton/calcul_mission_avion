from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class PointPerformance():


    @staticmethod
    def setupAvion(Avion: Avion, Atmosphere: Atmosphere, Inputs: Inputs):
        '''
        Place l'avion aux conditions demandées par l'utilisateur.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Inputs: Instance de la classe Inputs
        '''
        Avion.set_h(Inputs.altPP_ft * Constantes.conv_ft_m)
        Atmosphere.CalculateRhoPT(Inputs.altPP_ft * Constantes.conv_ft_m, Inputs.DISA_PP)
        Avion.Masse.setMass(Inputs.massPP)

        # Set des vitesses
        match Inputs.SpeedType:
            case "Mach":
                Avion.Aero.setMach(Inputs.Speed)
                Avion.Aero.convertMachToCAS(Atmosphere)
                Avion.Aero.convertMachToTAS(Atmosphere)
            case "TAS":
                Avion.Aero.setTAS(Inputs.Speed * Constantes.conv_kt_mps)
                Avion.Aero.convertTASToMach(Atmosphere)
                Avion.Aero.convertMachToCAS(Atmosphere)
            case "CAS":
                Avion.Aero.setCAS(Inputs.Speed * Constantes.conv_kt_mps)
                Avion.Aero.convertCASToMach(Atmosphere)
                Avion.Aero.convertMachToTAS(Atmosphere)
            case _:
                print("Erreur de vitesse (ni Mach, ni CAS, ni TAS)")

    @staticmethod
    def Performance(Avion: Avion, Atmosphere:Atmosphere, Inputs: Inputs):
        '''
        Réalise une simulation dite de "Point Performance", c'est-à-dire qu'on obtient
        les grandeurs importantes de l'avion à un point de vol donné en entrée.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Inputs: Instance de la classe Inputs
        :return string: Chaîne de caractère formatée contenant tous les résultats
        '''
        # Setup avec les inputs
        PointPerformance.setupAvion(Avion, Atmosphere, Inputs)
        
        # Conditions atmosphérique
        Atmosphere.CalculateRhoPT(Avion.get_h(), Inputs.DISA_PP)
        rho = Atmosphere.getRho()
        P = Atmosphere.getP()
        T = Atmosphere.getT()
        DISA = Inputs.DISA_PP

        # Vitesses (en kt)
        Mach = Avion.Aero.getMach()
        TAS  = Avion.Aero.getTAS() / Constantes.conv_kt_mps
        CAS  = Avion.Aero.getCAS() / Constantes.conv_kt_mps
        q = 1/2 * rho * (TAS * Constantes.conv_kt_mps) ** 2 # Pression dynamique

        # Cz, Cx, finesse
        Avion.Aero.calculateCz(Atmosphere)

        # Montee
        Avion.Aero.calculateCxClimb_Simplified()
        CxSimplifieMontee = Avion.Aero.getCx()

        # Croisiere
        Avion.Aero.calculateCxCruise_Simplified()
        CxSimplifieCroisiere = Avion.Aero.getCx()

        # Descente
        Avion.Aero.calculateCxDescent_Simplified()
        CxSimplifieDescente = Avion.Aero.getCx()

        # Cx non simplifie
        Avion.Aero.calculateCx(Atmosphere)
        Cx = Avion.Aero.getCx()
        Cz = Avion.Aero.getCz()
        finesse = Cz/Cx
        R_X = Avion.Masse.getCurrentWeight() / finesse # N

        # Poussée / SFC / FF max (N, kg/N/h, kg/h)
        Avion.Moteur.calculateFClimb(Atmosphere)
        Avion.Moteur.calculateSFCClimb(Atmosphere)
        F_N_max = Avion.Moteur.getF()
        F_F_max = Avion.Moteur.getFF()  * 3600
        SFC_max = Avion.Moteur.getSFC() * 3600
        pente = np.asin((F_N_max - R_X) / Avion.Masse.getCurrentWeight())
        ROC = pente * (TAS * Constantes.conv_kt_mps)

        # Poussée / SFC / FF équilibre
        Avion.Moteur.calculateFCruise(Atmosphere)
        Avion.Moteur.calculateSFCCruise(Atmosphere)
        F_N_eq = Avion.Moteur.getF()
        F_F_eq = Avion.Moteur.getFF()  * 3600
        SFC_eq = Avion.Moteur.getSFC() * 3600
        Avion.Aero.calculateSAR()
        Avion.Aero.calculateSGR()
        SAR = Avion.Aero.getSAR() / Constantes.conv_NM_m
        SGR = Avion.Aero.getSGR() / Constantes.conv_NM_m

        # Poussée / FF / pente idle
        Avion.Moteur.calculateFDescent(Atmosphere)
        Avion.Moteur.calculateSFCDescent(Atmosphere)
        F_N_IF = Avion.Moteur.getF()
        F_F_IF = Avion.Moteur.getFF()  * 3600
        SFC_IF = Avion.Moteur.getSFC() * 3600
        pente_IF = np.asin((F_N_IF - R_X) / Avion.Masse.getCurrentWeight())
        ROC_IF = pente_IF * (TAS * Constantes.conv_kt_mps)

        # Structuration des résultats pour l'affichage
        donnees_perf = {
            "Avion: " + Avion.getName():[
                ("Masse totale", Avion.Masse.getCurrentMass(), "kg")
            ],
            "Conditions Atmosphériques": [
                ("Altitude", Avion.get_h() / Constantes.conv_ft_m , "ft"),
                ("Température", T - 273.15 , "°C"),
                ("ΔISA", DISA, "°C"),
                ("Pression", P, "Pa"),
                ("Densité (rho)", rho, "kg/m³"),
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
                ("Cx simplifié montée", CxSimplifieMontee, "-"),
                ("Cx simplifié croisière", CxSimplifieCroisiere, "-"),
                ("Cx simplifié descente", CxSimplifieDescente, "-"),
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
                ("Specific Air Range (SAR)", SAR, "NM/kg"),
                ("Specific Ground Range (SAR)", SGR, "NM/kg")
            ],
            "Performances Idle (moteur ralenti)": [
                ("Poussée idle", F_N_IF, "N"),
                ("Fuel Flow", F_F_IF, "kg/h"),
                ("SFC", SFC_IF, "kg/N/h"),
                ("Pente de descente", pente_IF * 180/np.pi, "°"),
                ("Rate of Climb (ROC)", ROC_IF / Constantes.conv_kt_mps * 60, "ft/m")
            ]
        }

        string = PointPerformance.formater_point_performance(donnees_perf)
        return(string)

    @staticmethod
    def formater_point_performance(donnees):
        """
        Prend en entrée un dictionnaire de catégories contenant des listes de tuples 
        (nom, valeur, unité) et retourne une unique chaîne de caractères formatée.

        :param donnees: Dictionnaire à formater.
        """
        largeur = 65
        separateur = "=" * largeur
        
        # Création d'une liste qui va contenir toutes les lignes de texte
        lignes_texte = []
        
        # En-tête
        lignes_texte.append(f"\n{separateur}")
        lignes_texte.append(f"{'RÉSUMÉ DU POINT PERFORMANCE':^{largeur}}")
        lignes_texte.append(separateur)

        # Parcours des données
        for categorie, variables in donnees.items():
            lignes_texte.append(f"\n--- {categorie.upper()}")
            
            for nom, valeur, unite in variables:
                # On formate la ligne exactement comme avant, mais on l'ajoute à la liste
                ligne = f"    {nom:<30} : {valeur:>12.4f}  {unite:<8}"
                lignes_texte.append(ligne)
                
        # Pied de page
        lignes_texte.append(f"\n{separateur}\n")
        
        # On assemble toutes les lignes de la liste en y insérant un saut de ligne (\n) entre chaque
        return "\n".join(lignes_texte)






        





