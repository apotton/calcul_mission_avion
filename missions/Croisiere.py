from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from avions.Aero import Aero
from avions.Masse import Masse
from moteurs.Moteur import Moteur
import numpy as np

class Croisiere:
    @staticmethod
    def Croisiere(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dt_cruise):
        ''' Réalise toute la croisière de la mission principale.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: pas de temps (s)
        '''
        l_end = Inputs.l_mission_NM * Constantes.conv_NM_m
        # Croisiere.cruiseMachSAR(Avion, Atmosphere, Enregistrement, l_end, dt)
        # Croisiere.cruiseAltMach(Avion, Atmosphere, Enregistrement, l_end, dt)
        Croisiere.cruiseAltSAR(Avion,Atmosphere,Enregistrement,l_end, dt)

    @staticmethod
    def climbIsoMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dt_cruise):
        '''
        Montée iso-Mach à Mach constant jusqu'à ce que les critères de montée ne soient plus vérifiés.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: pas de temps (s)
        '''
        h_init = Avion.geth()

        while Avion.geth() < h_init + Inputs.step_climb_ft * Constantes.conv_ft_m:

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
            Avion.Moteur.calculateFCruise()
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
            delta_h = Inputs.step_climb_ft * Constantes.conv_ft_m

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

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx_up = Avion.Aero.getCx()

            finesse_up = Cz_up / Cx_up

            # Traînée / équivalent résistance
            Rx_up = Avion.Masse.getCurrentWeight() / finesse_up

            # Poussée moteur
            Avion.Moteur.calculateFCruise()
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
            Avion.Aero.setCAS_t(CAS_init)
            Avion.Aero.setTAS_t(TAS_init)
            Avion.Aero.setMach_t(Mach_init)
            Avion.Aero.setCz(Cz_init)
            Avion.Aero.setCx(Cx_init)
            Avion.Aero.setSGR(SGR_init)
            Avion.Moteur.setF(F_init)
            Avion.Moteur.setSFC(SFC_init)
            Atmosphere.setP(P_init)
            Atmosphere.setT(T_init)
            Atmosphere.setRho(Rho_init)

            # Condition de montée iso-Mach
            return (RRoC_up > Inputs.RRoC_min_ft_min*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s 
                    Avion.geth() + delta_h * Constantes.conv_ft_m < Avion.getPressurisationCeilingFt()*Constantes.conv_ft_m and  # Pas au plafond converti de ft en m
                    SGR_up > SGR_init)
        

    @staticmethod
    def cruiseMachSAR(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, l_end, dt = Inputs.dt_cruise):
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

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)

            # Poussée moteur
            Avion.Moteur.calculateFCruise()
            Avion.Moteur.calculateSFCCruise()

            # Condition de montée iso-Mach (on ne monte pas si on est très avancé dans la mission)
            if (Avion.getl() < 7/10*Inputs.l_mission_NM and Croisiere.checkUp(Avion, Atmosphere)):
                # print("Je monte")
                Croisiere.climbIsoMach(Avion,Atmosphere,Enregistrement, dt=1)
            else :
                # Fuel burn
                Avion.Masse.burnFuel(dt)

                # Mise à jour avion (pas de changement d'altitude)
                Avion.Add_dl(Vx * dt)

                # Enregistrement au pas de temps
                Enregistrement.save(Avion, Atmosphere, dt)


    @staticmethod
    def cruiseAltMach(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, l_end, dt = Inputs.dt_cruise):
        """
        Croisière à altitude et Mach constant.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        """
        # Atmosphère
        Atmosphere.CalculateRhoPT(Avion.geth())
        Avion.Aero.setMach_t(Inputs.Mach_cruise)

        # Tant que l'on n'a pas parcouru assez de distance
        while (Avion.getl() < l_end - Avion.getl_descent()):


            # Vitesse
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Vitesses
            Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.Aero_simplified:
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
    def cruiseAltSAR(Avion:Avion, Atmosphere:Atmosphere, Enregistrement:Enregistrement, l_end, dt=Inputs.dt_cruise):
        """
        Croisière à altitude constante avec optimisation du SAR.
        Le Mach est recalculé à chaque pas pour atteindre k * SAR_max.

        :param Avion: instance Avion
        :param Atmosphere: instance Atmosphere
        :param Enregistrement: instance Enregistrement
        :param l_end: distance à parcourir en croisière avant de commencer la descente (m)
        :param dt: pas de temps
        """
        # Grille de Mach
        Mach_grid = np.arange(0.6, 0.82, 0.001)
        
        while Avion.getl() < l_end - Avion.getl_descent():
            # Atmosphere
            Atmosphere.CalculateRhoPT(Avion.geth())

            ## CALCUL VECTORISÉ DU SAR (les attributs de Avion deviennent des arrays)
            
            # TAS pour toute la grille
            Avion.Aero.setMach_t(Mach_grid)
            Avion.Aero.convertMachToTAS(Atmosphere)
            
            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            # Cx_grid : Ici, il faut que ta fonction accepte un vecteur Cz_grid
            if Inputs.Aero_simplified:
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
            SAR_target = SAR_max * (1 - Inputs.k_SAR_cruise/100)
            idx_max = np.argmax(SAR_grid)

            # On interpole seulement après le maximum
            SAR_sub = SAR_grid[idx_max:]
            Mach_sub = Mach_grid[idx_max:]
            # On inverse l'interpolation car np.interp exige une croissance, ici on est décroissant après SAR_max
            Mach_opt = np.interp(SAR_target, SAR_sub[::-1], Mach_sub[::-1])

            ## Mise à jour avion en fonction du Mach optimal, tout repasse en scalaire
            Avion.Aero.setMach_t(Mach_opt)
            Avion.Aero.convertMachToTAS(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.Aero_simplified:
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




