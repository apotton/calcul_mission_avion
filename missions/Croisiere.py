from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Descente import Descente
from missions.Montee import Montee
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np
import matplotlib.pyplot as plt

class Croisiere:
    @staticmethod
    def Croisiere(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, dt):
        ''' Réalise toute la croisière de la mission principale.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: pas de temps (s)
        '''
        Avion.cruise = True
        l_end = Inputs.l_mission_NM * Constantes.conv_NM_m
        m_init = Avion.Masse.getCurrentMass()
        t_init = Avion.get_t()
        l_init = Avion.getl()

        
        if Inputs.cruiseType == "Mach_SAR":
            Croisiere.cruiseMachSAR(Avion, Atmosphere, Enregistrement, Inputs, l_end, dt)
        elif Inputs.cruiseType == "Alt_Mach":
            Croisiere.cruiseAltMach(Avion, Atmosphere, Enregistrement, Inputs, l_end, dt)
        elif Inputs.cruiseType == "Alt_SAR":
            Croisiere.cruiseAltSAR(Avion,Atmosphere, Enregistrement, Inputs, l_end, dt)
        elif Inputs.cruiseType == "CI":
            Croisiere.cruiseCI(Avion, Atmosphere, Enregistrement, Inputs, l_end, dt)
        else:
            print("Croisière " + Inputs.cruiseType + " inexistante.")
            exit()

        Avion.set_l_cruise(Avion.getl() - l_init)
        Avion.set_t_cruise(Avion.get_t() - t_init)
        Avion.Masse.setFuelCruise(m_init - Avion.Masse.getCurrentMass())
        Avion.Masse.addFuelMission(m_init - Avion.Masse.getCurrentMass())
        Avion.cruise = False

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, dt):
        '''
        Montée iso-Mach à Mach constant jusqu'à ce que les critères de montée ne soient plus vérifiés.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: pas de temps (s)
        '''
        h_init = Avion.geth()

        while Avion.geth() < h_init + Inputs.stepClimb_ft * Constantes.conv_ft_m:

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
            Avion.Moteur.calculateSFCClimb() #On prend quelles tables du coup ? 

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            Vx = Avion.Aero.getTAS() * np.cos(pente) + Inputs.Vw * Constantes.conv_kt_mps
            Vz = Avion.Aero.getTAS() * np.sin(pente)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            # Paramètres économiques
            Avion.Aero.calculateSGR()
            Avion.Aero.calculateECCF()
            
            Enregistrement.save(Avion, Atmosphere, dt)

    @staticmethod
    def checkUp(Avion : Avion, Atmosphere: Atmosphere, Inputs: Inputs):
            '''
            Vérifie si la montée en croisière est intéressante
            
            :param Avion: Instance de la classe Avion
            :param Atmosphere: Instance de la classe Atmosphere
            '''
            # Stockage des paramètres avant évaluation de montée
            Avion.Aero.calculateECCF() 
            Avion.Aero.calculateSGR()
            ECCF_init = Avion.Aero.getECCF()
            SGR_init = Avion.Aero.getSGR()

            h_init = Avion.geth()
            l_init = Avion.getl()
            CAS_init = Avion.Aero.getCAS()
            TAS_init = Avion.Aero.getTAS()
            Mach_init = Avion.Aero.getMach()
            Cz_init = Avion.Aero.getCz()
            Cx_init = Avion.Aero.getCx()
            F_init = Avion.Moteur.getF()
            SFC_init = Avion.Moteur.getSFC()
            P_init = Atmosphere.getP_t()
            T_init = Atmosphere.getT_t()
            Rho_init = Atmosphere.getRho_t()

            ## Calcul des paramètres 2000ft plus haut pour étudier le coût de monter

            # Paramètres 2000 ft plus haut (pour décider la montée)
            delta_h = Inputs.stepClimb_ft * Constantes.conv_ft_m

            # Altitude virtuelle
            Avion.Add_dh(delta_h)

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # TAS (Mach constant avant montée iso-Mach)
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.getTAS()

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz_up = Avion.Aero.getCz()

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx_up = Avion.Aero.getCx()

            finesse_up = Cz_up / Cx_up

            # Traînée / équivalent résistance
            Rx_up = Avion.Masse.getCurrentWeight() / finesse_up

            # Poussée moteur
            Avion.Moteur.calculateFClimb()
            F_N_up = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCCruise()
            
            #Calcul du coût économique ECCF et SGR
            Avion.Aero.calculateECCF() 
            Avion.Aero.calculateSGR()
            ECCF_up = Avion.Aero.getECCF()
            SGR_up = Avion.Aero.getSGR()

            # RRoC (Rate of Climb virtuel)
            RRoC_up = (F_N_up - Rx_up) / Avion.Masse.getCurrentWeight() * Avion.Aero.getTAS() #UTILISER LA MONTEE ISO MACH DE LA PHASE DE MONTEE MAINTENANT

            # Retour aux paramètres initaux pour la montée ou le reste de la croisière 
            Avion.set_h(h_init)
            Avion.set_l(l_init)
            Avion.Aero.setCAS(CAS_init)
            Avion.Aero.setTAS(TAS_init)
            Avion.Aero.setMach(Mach_init)
            Avion.Aero.setCz(Cz_init)
            Avion.Aero.setCx(Cx_init)
            Avion.Aero.setSGR(SGR_init)
            Avion.Moteur.setF(F_init)
            Avion.Moteur.setSFC(SFC_init)
            Atmosphere.setP(P_init)
            Atmosphere.setT(T_init)
            Atmosphere.setRho(Rho_init)

            if not (RRoC_up > Inputs.RRoC_min_ft*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s 
                    Avion.geth()/Constantes.conv_ft_m + delta_h < Avion.getPressurisationCeilingFt()):  # Pas au plafond converti de m en ft
                return False

            if (Inputs.cruiseType == "Mach_SAR"):
                # Condition de montée iso-Mach
                return (SGR_up > SGR_init)
            elif (Inputs.cruiseType == "CI"):
                # Condition de montée Cost Index
                return (ECCF_up < ECCF_init)
            
            return False


    @staticmethod
    def calculateSpeed_target(Avion: Avion, Atmosphere: Atmosphere, Inputs: Inputs):
        '''
        Calcule la vitesse Mach telle que l'on soit à k*SAR (souvent 99%), ou alors au minimum de l'ECCF.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :return Mach_target: Le Mach objectif
        '''
        # Sauvegarde des variables qui vont changer
        Mach = Avion.Aero.getMach()
        CAS  = Avion.Aero.getCAS()
        TAS  = Avion.Aero.getTAS()
        h    = Avion.geth()
        Cz   = Avion.Aero.getCz()
        Cx   = Avion.Aero.getCx()
        SAR  = Avion.Aero.getSAR()
        ECCF = Avion.Aero.getECCF()
        F = Avion.Moteur.getF()
        FF = Avion.Moteur.getFF()
        SFC = Avion.Moteur.getSFC()

        Mach_grid = np.arange(0.2, 0.82, 0.001)

        # Atmosphere
        Atmosphere.CalculateRhoPT(Avion.geth())

        ## CALCUL VECTORISÉ DU SAR (les attributs de Avion deviennent des arrays)
        
        # TAS pour toute la grille
        Avion.Aero.setMach(Mach_grid)
        Avion.Aero.convertMachToTAS(Atmosphere)
        
        # Aérodynamique
        Avion.Aero.calculateCz(Atmosphere)

        # Cx_grid : Ici, il faut que ta fonction accepte un vecteur Cz_grid
        if Inputs.AeroSimplified:
            # Cx = Cx0 + k * Cz^2 (Formule simplifiée typique)
            Avion.Aero.calculateCxCruise_Simplified()
        else:
            # Appel à ta polaire aérodynamique (doit supporter les arrays)
            Avion.Aero.calculateCx(Atmosphere)

        # Calculs vectorisés moteur
        Avion.Moteur.calculateFCruise() # Equilibre
        Avion.Moteur.calculateSFC_Vectorized() # Verion vectorisée: plus lente pour des floats simples

        if (Inputs.cruiseType == "Alt_SAR"):
            # SAR pour toute la grille
            Avion.Aero.calculateSAR()
            SAR_grid = np.array(Avion.Aero.getSAR())

            #On ne se place pas à l'optimum
            SAR_max = np.max(SAR_grid)
            SAR_target = SAR_max * (1 - Inputs.kSARcruise/100)
            idx_max = np.argmax(SAR_grid)
            Mach_opt = Mach_grid[idx_max]

            # On interpole seulement après le maximum
            SAR_sub = SAR_grid[idx_max:]
            Mach_sub = Mach_grid[idx_max:]
            # On inverse l'interpolation car np.interp exige une croissance, ici on est décroissant après SAR_max
            Mach_opt = np.interp(SAR_target, SAR_sub[::-1], Mach_sub[::-1])
            Avion.Aero.setMach(Mach_opt)
            Avion.Aero.convertMachToCAS(Atmosphere)
            CAS_opt = Avion.Aero.getCAS()
        else:
            # Cas croisière CI
            Avion.Aero.calculateECCF()
            ECCF_grid = Avion.Aero.getECCF()

            # Recherche de l'optimum (Minimum de l'ECCF)
            idx_opt = np.argmin(ECCF_grid)
            Mach_opt = Mach_grid[idx_opt]

            # Calcul du CAS correspondant
            Avion.Aero.setMach(Mach_opt)
            Avion.Aero.convertMachToCAS(Atmosphere)
            CAS_opt = Avion.Aero.getCAS()
            pass

        # Remise à zéro
        Avion.Aero.setMach(Mach)
        Avion.Aero.setCAS(CAS)
        Avion.Aero.setTAS(TAS)
        Avion.set_h(h)
        Avion.Aero.setCz(Cz)
        Avion.Aero.setCz(Cx)
        Avion.Aero.setSAR(SAR)
        Avion.Aero.setECCF(ECCF)
        Avion.Moteur.setF(F)
        Avion.Moteur.setFF(FF)
        Avion.Moteur.setSFC(SFC)

        return Mach_opt, CAS_opt

    @staticmethod
    def cruiseMachSAR(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, l_end, dt):
        """
        Croisière en palier à Mach constant, avec des éventuelles montées d'un pallier d'altitude.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        """

        # Tant que l'on n'a pas parcouru assez de distance
        while (Avion.getl() < l_end - Avion.getl_descent()):
            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesse
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Vitesses
            Vx = Avion.Aero.getTAS() + Inputs.Vw * Constantes.conv_kt_mps

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)

            # Poussée moteur
            Avion.Moteur.calculateFCruise()
            Avion.Moteur.calculateSFCCruise()

            # Condition de montée iso-Mach (on ne monte pas si on est très avancé dans la mission)
            if (Avion.getl() < Inputs.cruiseClimbStop*Inputs.l_mission_NM*Constantes.conv_NM_m/100 \
                and Avion.getl() > Inputs.cruiseClimbInit*Inputs.l_mission_NM*Constantes.conv_NM_m/100 \
                and Croisiere.checkUp(Avion, Atmosphere, Inputs)):
                Croisiere.climbIsoMach(Avion,Atmosphere,Enregistrement, Inputs, dt = Inputs.dtClimb)
            else :
                # Fuel burn
                Avion.Masse.burnFuel(dt)

                # Mise à jour avion (pas de changement d'altitude)
                Avion.Add_dl(Vx * dt)
                Avion.Add_dt(dt)

                # Paramètres économiques
                Avion.Aero.calculateSGR()
                Avion.Aero.calculateSAR()
                Avion.Aero.calculateECCF()

                # Enregistrement au pas de temps
                Enregistrement.save(Avion, Atmosphere, dt)


    @staticmethod
    def cruiseAltMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, l_end, dt):
        """
        Croisière à altitude et Mach constant.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        """
        # Atmosphère
        Atmosphere.CalculateRhoPT(Avion.geth())
        Avion.Aero.setMach(Inputs.MachCruise)

        # Tant que l'on n'a pas parcouru assez de distance
        while (Avion.getl() < l_end - Avion.getl_descent()):


            # Vitesse
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Vitesses
            Vx = Avion.Aero.getTAS() + Inputs.Vw * Constantes.conv_kt_mps

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)

            # Poussée moteur
            Avion.Moteur.calculateFCruise()
            Avion.Moteur.calculateSFCCruise()

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion (pas de changement d'altitude)
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            # Paramètres économiques
            Avion.Aero.calculateSGR()
            Avion.Aero.calculateSAR()
            Avion.Aero.calculateECCF()

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)


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
        
        while Avion.getl() < l_end - Avion.getl_descent():
            Mach_opt, CAS_opt = Croisiere.calculateSpeed_target(Avion, Atmosphere, Inputs)

            # Si on est trop loin du Mach optimal, on rejoint la vitesse cible en palier
            if (abs(Avion.Aero.getMach() - Mach_opt) > 0.01):
                if (Avion.Aero.getMach() < Mach_opt):
                    Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt = Inputs.dtClimb)
                else:
                    Descente.descentePalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt = Inputs.dtDescent)

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
            Vx = Avion.Aero.getTAS() + Inputs.Vw * Constantes.conv_kt_mps
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)

            # Consommation
            Avion.Masse.burnFuel(dt)

            # Paramètres économiques
            Avion.Aero.calculateSGR()
            Avion.Aero.calculateSAR()
            Avion.Aero.calculateECCF()

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)


    @staticmethod
    def cruiseCI(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, l_end, dt):
        """
        Croisière en mode Cost Index avec ajustement dynamique du Mach optimal
        et montées (Step Climbs) éventuelles si cela est économiquement rentable.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param Inputs: Instance de la classe Inputs
        :param l_end: Distance à de croisière (m)
        :param dt: Pas de temps (s)        
        """
        while Avion.getl() < l_end - Avion.getl_descent():
            
            # Calcul du Mach optimal pour l'ECCF actuel
            Mach_opt, CAS_opt = Croisiere.calculateSpeed_target(Avion, Atmosphere, Inputs)

            # Ajustement de la vitesse si on s'éloigne trop de l'optimum
            if abs(Avion.Aero.getMach() - Mach_opt) > 0.01:
                if Avion.Aero.getMach() < Mach_opt:
                    Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt=Inputs.dtClimb)
                else:
                    Descente.descentePalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_opt, dt=Inputs.dtDescent)

            # Application du Mach optimal
            Avion.Aero.setMach(Mach_opt)
            Atmosphere.CalculateRhoPT(Avion.geth())
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)
            
            Vx = Avion.Aero.getTAS() + Inputs.Vw * Constantes.conv_kt_mps

            # Évaluation du Step Climb
            if (Avion.getl() < Inputs.cruiseClimbStop * Inputs.l_mission_NM * Constantes.conv_NM_m / 100 
                and Avion.getl() > Inputs.cruiseClimbInit * Inputs.l_mission_NM * Constantes.conv_NM_m / 100 
                and Croisiere.checkUp(Avion, Atmosphere, Inputs)):
                
                Croisiere.climbIsoMach(Avion, Atmosphere, Enregistrement, Inputs, dt=Inputs.dtClimb)
            
            else:
                # Vol en palier classique si pas de montée
                Avion.Aero.calculateCz(Atmosphere)

                if Inputs.AeroSimplified:
                    Avion.Aero.calculateCxCruise_Simplified()
                else:
                    Avion.Aero.calculateCx(Atmosphere)

                Avion.Moteur.calculateFCruise()
                Avion.Moteur.calculateSFCCruise()

                # Intégration
                Avion.Add_dl(Vx * dt)
                Avion.Add_dt(dt)
                Avion.Masse.burnFuel(dt)

                Avion.Aero.calculateSGR()
                Avion.Aero.calculateSAR()
                Avion.Aero.calculateECCF()

                Enregistrement.save(Avion, Atmosphere, dt)  
