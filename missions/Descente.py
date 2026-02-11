from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Descente:
    @staticmethod
    def Descendre(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        """
        Réalise toute la descente depuis la fin de la croisière jusqu'à l'atterrissage

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """
        Descente.descent_iso_Mach(Avion, Atmosphere, dt)
        Descente.descent_iso_max_CAS(Avion, Atmosphere, dt)
        Descente.descent_Palier(Avion, Atmosphere, dt)
        Descente.descent_final_iso_CAS(Avion, Atmosphere, dt)

    # Phase 1 : Ajustement vitesse à Max CAS avec possibilité de descente libre---
    @staticmethod
    def descent_iso_Mach(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        """
        Laisse l'avion initier une descente libre pour atteindre la vitesse maximale autorisée en CAS (Vmax_CAS) avant de passer à la phase 2

        Arguments :
        h_start : altitude initiale en mètres, récupérée en fin de croisière
        l_start : position en x initiale à cette phase (unité), récupérée en fin de croisière
        t_start : temps initiale à cette phase (unité), récupéré en fin de croisière
        Mach_start : Mach initial à cette phrase, récupéré en fin de croisière
        dt      : pas de temps pour la simulation en secondes (par défaut 1 s)
        """
        
        # CAS max en m/s
        CAS_max = Avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s  Vitesse maximale de descente de l'avion
        CAS_t = Avion.Aero.getCAS()   
        # Mach_t = Avion.Aero.getMach() 
        # TAS_t = Avion.Aero.getTAS() 


        while CAS_t < CAS_max: #On cherche à diminuer l'altitude h jusqu'à atteindre la vitesse CAS Max

            # Atmosphère Calcule des conditions atm à cet altitude afin d'extraire la température et la pression au temps t
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Mach et TAS 
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere) #Calcul du CAS à partir du Mach
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere) #Calcul du TAS à partir du Mach

            CAS_t = Avion.Aero.getCAS()   
            TAS_t = Avion.Aero.getTAS() 

            # Cz et Cx Calcul des coefs aéro
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxDescent_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur et SFC
            Avion.Moteur.Calculate_F_descent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_descent()

            # Résistance horizontale
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente de descente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())
            Vz = TAS_t * np.sin(pente)
            Vx = TAS_t * np.cos(pente)

            # Mise à jour des positions
            Avion.Add_dh(Vz * dt) #On met à jour l'altitude de l'avion en fonction de la vitesse verticale et du pas de temps
            Avion.Add_dl(Vx * dt) #On met à jour la distance parcourue en fonction de la vitesse horizontale et du pas de temps
        

            # Fuel burn
            Avion.Masse.burn_fuel(dt) #Carburant consommé à ce pas de temps dt, on met à jour la masse de carburant 

            if Enregistrement.enregistrement_descente:
                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement des données à ce pas de temps
            else:
                Avion.Add_l_descent(Vx * dt) #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière


    # Phase 2 : Descente à V constante jusqu'à 10000 ft
    @staticmethod
    def descent_iso_max_CAS(Avion: Avion, Atmosphere: Atmosphere, h_end, dt = Inputs.dt_descent):
        """
        Phase 2 : Descente jusqu'à 10000ft à vitesse constante Max CAS

        Arguments :
        h_start : altitude initiale, après phase 1 (UNITE)
        h_end   : altitude finale de la phase 2, 10 000ft 
        l_start : distance initiale, après phase 1 (UNITE)
        t_start : temps initial, après phase 1 (UNITE)
        dt      : pas de temps (s)
        """

        # CAS imposée
        CAS_t = Avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s On descend à CAS fixé par la vitesse max de descente
        Avion.Aero.setCAS_t(CAS_t)

        while Avion.geth() > Inputs.h_decel_ft * Constantes.conv_ft_m:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Conversion CAS -> Mach
            Avion.Aero.Convert_CAS_to_Mach(Atmosphere)

            # TAS
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)

            # Mach_t = Avion.Aero.getMach()
            TAS_t  = Avion.Aero.getTAS()

            # Coefficients aérodynamiques
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxDescent_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur (idle en descente)
            Avion.Moteur.Calculate_F_descent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_descent()

            # Résistance
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente de trajectoire
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            Vz = TAS_t * np.sin(pente)   # négatif car en descente
            Vx = TAS_t * np.cos(pente)

            # Mise à jour position
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            if Enregistrement.enregistrement_descente:
                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement des données à ce pas de temps
            else:
                Avion.Add_l_descent(Vx * dt) #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière


    # Phase 3 : Réduction de vitesse en plateau à 250 kt
    @staticmethod
    def descent_Palier(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        """
        Phase 3 : Décélération en palier, on fixe l'altitude à 10000ft et on passe la vitesse à Min CAS

        Arguments :
        h_const : altitude constante, après phase 2 (UNITE)
        l_start : distance initiale, après phase 2 (UNITE)
        t_start : temps initial, après phase 2 (UNITE)
        dt      : pas de temps (s)
        """

        # CAS initiale (issue phase 2)
        CAS_t = Avion.Aero.getCAS() # * Constantes.conv_kt_mps  # kt -> m/s

        # Atmosphère #NB : on peut calculer les conditions atm en dehors de la boucle car, l'altitude étant constante, les conditions restent les mêmes à chaque pas de temps
        Atmosphere.CalculateRhoPT(Avion.geth())

        # CAS cible (250 kt)
        CAS_target = Inputs.CAS_below_10000_desc_kt * Constantes.conv_kt_mps #PEUT ETRE LE FIXER DANS LES CONSTANTES

        Avion.Aero.Convert_CAS_to_Mach(Atmosphere)
        Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
        # Mach_t = Avion.Aero.getMach()
        TAS_t = Avion.Aero.getTAS()

        while CAS_t > CAS_target: #On diminue la vitesse jusqu'à la valeur désirée
            # A noter que les nouvelles vitesses sont calculées en fin de boucle
            # Atmosphere.CalculateRhoPT(Avion.geth())

            # Coefficients aérodynamiques
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxDescent_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Forces
            Rx = Avion.Masse.getCurrentWeight() / finesse  # cohérent avec finesse

            # Poussée moteur (idle / freinage)
            Avion.Moteur.Calculate_F_descent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_descent()

            # Dynamique longitudinale simplifiée #c'est la force qui va faire ralentir l'appareil
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # Mise à jour des vitesses
            Avion.Aero.setTAS_t(max(TAS_t + ax * dt, 0.0))
            TAS_t = Avion.Aero.getTAS() #Calcul de la nouvelle vitesse avec la resistance longitudinale

            # Recalcul CAS depuis Mach/TAS

            Avion.Aero.Convert_TAS_to_Mach(Atmosphere)
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)
            CAS_t = Avion.Aero.getCAS()
            # Mach_t = Avion.Aero.getCAS()

            # Cinématique
            Avion.Add_dh(0.0) #On vole en palier, donc on ne descend pas
            Avion.Add_dl(TAS_t * dt) #On met à jour la distance parcourue en fonction de la vitesse horizontale et du pas de temps

            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            if Enregistrement.enregistrement_descente:
                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement des données à ce pas de temps
            else:
                Avion.Add_l_descent(TAS_t * dt) #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière


    # Phase 4 : Descente finale jusqu'à h_final
    @staticmethod
    def descent_final_iso_CAS(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        """
        Phase 4 : descente à CAS constante (250 kt) jusqu'à l'altitude finale de 1500ft

        h_start : altitude initiale, récupérée à la fin de la phase 3 en UNITE
        h_final : altitude finale, fixée par la mission (1500ft)
        l_start : distance franchie initiale, récupérée à la fin de la phase 3 en UNITE
        t_start : temps initial, récupérée à la fin de la phase 3 en UNITE
        dt      : pas de temps (s)
        """

        # CAS imposée
        CAS = Inputs.CAS_below_10000_desc_kt * Constantes.conv_kt_mps  # kt → m/s Ajouter dans les constantes le 250kt ?

        while Avion.geth() > Inputs.h_final_ft * Constantes.conv_ft_m: #On continue à descendre jusqu'à l'altitude finale

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Mach depuis CAS
            Avion.Aero.Convert_CAS_to_Mach(Atmosphere)

            # TAS
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxDescent_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur
            Avion.Moteur.Calculate_F_descent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_descent()

            # Résistance
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            TAS_t = Avion.Aero.getTAS()
            Vz = TAS_t * np.sin(pente)
            Vx = TAS_t * np.cos(pente)

            # Intégration
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)


            # Fuel burn
            Avion.Masse.burn_fuel(dt)

            if Enregistrement.enregistrement_descente:
                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement des données à ce pas de temps
            else:
                Avion.Add_l_descent(Vx * dt) #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière


