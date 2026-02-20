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
    def Croisiere(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtCruise):
        ''' Réalise toute la croisière de la mission principale.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: pas de temps (s)
        '''
        Avion.cruise = True
        l_end = Inputs.l_mission_NM * Constantes.conv_NM_m
        # Croisiere.cruiseMachSAR(Avion, Atmosphere, Enregistrement, l_end, dt)
        # Croisiere.cruiseAltMach(Avion, Atmosphere, Enregistrement, l_end, dt)
        Croisiere.cruiseAltSAR(Avion,Atmosphere,Enregistrement,l_end, dt)
        Avion.cruise = False

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtCruise):
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
            Vz = Avion.Aero.getTAS() * np.sin(pente)
            Vx = Avion.Aero.getTAS() * np.cos(pente)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            # Mise à jour avion
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.Aero.calculateSGR(Atmosphere)
            Avion.Aero.calculateECCF(Atmosphere)
            
            Enregistrement.save(Avion, Atmosphere, dt)
    
    ##
    #Croisière MACH SAR
    ##

    @staticmethod
    def checkUp(Avion : Avion, Atmosphere: Atmosphere):
            '''
            Vérifie si la montée en croisière est intéressante
            
            :param Avion: Instance de la classe Avion
            :param Atmosphere: Instance de la classe Atmosphere
            '''
            # Stockage des paramètres avant évaluation de montée
            Avion.Aero.calculateECCF(Atmosphere) 
            Avion.Aero.calculateSGR(Atmosphere)
            #ECCF_init = Avion.Aero.getECCF()
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
            Avion.Aero.calculateECCF(Atmosphere) 
            Avion.Aero.calculateSGR(Atmosphere)
            #ECCF_up = Avion.Aero.getECCF()
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

            # Condition de montée iso-Mach
            return (RRoC_up > Inputs.RRoC_min_ft*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s 
                    Avion.geth() + delta_h * Constantes.conv_ft_m < Avion.getPressurisationCeilingFt()*Constantes.conv_ft_m and  # Pas au plafond converti de ft en m
                    SGR_up > SGR_init)

    @staticmethod
    def calculateSpeed_target(Avion: Avion, Atmosphere: Atmosphere):
        '''
        Calcule la vitesse Mach telle que l'on soit à k*SAR (souvent 99%)

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

        finesse_grid = Avion.Aero.getCz() / Avion.Aero.getCx()

        # Calculs vectorisés moteur
        Avion.Moteur.calculateFCruise() # Equilibre
        Avion.Moteur.calculateSFC_Vectorized() # Verion vectorisée: plus lente pour des floats simples

        # SAR pour toute la grille
        SAR_grid = Avion.Aero.getTAS() * finesse_grid / (Avion.Moteur.getSFC() * Avion.Masse.getCurrentWeight())

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

        # Remise à zéro
        Avion.Aero.setMach(Mach)
        Avion.Aero.setCAS(CAS)
        Avion.Aero.setTAS(TAS)
        Avion.set_h(h)
        Avion.Aero.setCz(Cz)
        Avion.Aero.setCz(Cx)

        return Mach_opt, CAS_opt

    @staticmethod
    def cruiseMachSAR(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, l_end, dt = Inputs.dtCruise):
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
            Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

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
                and Croisiere.checkUp(Avion, Atmosphere)):
                Croisiere.climbIsoMach(Avion,Atmosphere,Enregistrement, dt = Inputs.dtClimb)
            else :
                # Fuel burn
                Avion.Masse.burnFuel(dt)

                # Mise à jour avion (pas de changement d'altitude)
                Avion.Add_dl(Vx * dt)

                # Enregistrement au pas de temps
                Enregistrement.save(Avion, Atmosphere, dt)


    @staticmethod
    def cruiseAltMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, l_end, dt = Inputs.dtCruise):
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
            Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

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

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)


    @staticmethod
    def cruiseAltSAR(Avion:Avion, Atmosphere:Atmosphere, Enregistrement:Enregistrement, l_end, dt=Inputs.dtCruise):
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
            Mach_opt, CAS_opt = Croisiere.calculateSpeed_target(Avion, Atmosphere)

            # Si on est trop loin du Mach optimal, on rejoint la vitesse cible en palier
            if (abs(Avion.Aero.getMach() - Mach_opt) > 0.01):
                if (Avion.Aero.getMach() < Mach_opt):
                    Montee.climbPalier(Avion, Atmosphere, Enregistrement, CAS_opt, dt = Inputs.dtClimb)
                else:
                    Descente.descentePalier(Avion, Atmosphere, Enregistrement, CAS_opt, dt = Inputs.dtDescent)

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
            Avion.Add_dl(Avion.Aero.getTAS() * dt)

            # Consommation
            Avion.Masse.burnFuel(dt)

            # Enregistrement au pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)




