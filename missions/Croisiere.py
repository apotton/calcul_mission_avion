from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Croisiere:
    @staticmethod
    def Croisiere(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_cruise):
        ''' Réalise toute la croisière
        
        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        l_end : distance à parcourir en croisière avant de commencer la descente (UNITE)
        dt : pas de temps (s)
        '''
        l_end = Inputs.l_mission_NM * Constantes.conv_NM_m
        Croisiere.Cruise_Mach_SAR(Avion, Atmosphere, l_end, dt)

    @staticmethod
    def Climb_iso_Mach(Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        '''
        Montée iso-Mach à Mach constant jusqu'à ce que les critères de montée ne soient plus vérifiés

        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        dt : pas de temps (s)
        '''
        h_init = Avion.geth()

        while Avion.geth() < h_init + Inputs.step_climb_ft * Constantes.conv_ft_m:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesse
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxClimb_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Poussée
            Avion.Moteur.Calculate_F_cruise()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_climb() #On prend quelles tables du coup ? 

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
    
    ##
    #Croisière MACH SAR
    ##

    @staticmethod
    def Check_up(Avion : Avion, Atmosphere : Atmosphere):
            #Stockage des paramètres avant évaluation de montée

            Avion.Aero.CalculateECCF(Atmosphere) 
            Avion.Aero.CalculateSGR(Atmosphere)
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


            ##Calcul des paramètres 2000ft plus haut pour étudier le coût de monter

            # --- Paramètres 2000 ft plus haut (pour décider la montée) ---
            delta_h_ft = Inputs.step_climb_ft #ft
            delta_h = delta_h_ft * Constantes.conv_ft_m  # convertir en m

            # Altitude “virtuelle”
            Avion.Add_dh(delta_h)

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(Avion.geth())

            # --- TAS (Mach constant avant montée iso-Mach) ---
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            Avion.Aero.getTAS()

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Atmosphere)
            Cz_up = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxCruise_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx_up = Avion.Aero.getCx()

            finesse_up = Cz_up / Cx_up

            # --- Traînée / équivalent résistance ---
            Rx_up = Avion.Masse.getCurrentWeight() / finesse_up

            # --- Poussée moteur --- #ATTENTION A VOIR CE QU'UTILISE F ET SFC CAR ICI ON MODIFIE QUELQUES CARACTERISTIQUES AVIONS POUR MONTER EN ALTITUDE
            Avion.Moteur.Calculate_F_cruise()
            F_N_up = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC_cruise()
            #SFC_up = Avion.Moteur.getSFC()

            
            #Calcul du coût économique ECCF et SGR
            Avion.Aero.CalculateECCF(Atmosphere) 
            Avion.Aero.CalculateSGR(Atmosphere)
            #ECCF_up = Avion.Aero.getECCF()
            SGR_up = Avion.Aero.getSGR()


            # --- RRoC (Rate of Climb virtuel) ---
            RRoC_up = (F_N_up - Rx_up) / Avion.Masse.getCurrentWeight() * Avion.Aero.getTAS() #UTILISER LA MONTEE ISO MACH DE LA PHASE DE MONTEE MAINTENANT

            #Retour aux paramètres initaux pour la montée ou le reste de la croisière 

            Avion.set_h(h_init)
            Avion.set_l(l_init)
            Avion.Aero.setCAS_t(CAS_init)
            Avion.Aero.setTAS_t(TAS_init)
            Avion.Aero.setMach_t(Mach_init)
            Avion.Aero.setCz(Cz_init)
            Avion.Aero.setCx(Cx_init)
            Avion.Moteur.setF(F_init)
            Avion.Moteur.setSFC(SFC_init)
            Atmosphere.setP(P_init)
            Atmosphere.setT(T_init)
            Atmosphere.setRho(Rho_init)

            # --- Condition de montée iso-Mach ---
            if (
                RRoC_up > Inputs.RRoC_min_ft_min*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s 
                Avion.geth() + delta_h * Constantes.conv_ft_m < Avion.getPressurisationCeilingFt()*Constantes.conv_ft_m and  # Pas au plafond converti de ft en m
                SGR_up > SGR_init):
                 return 1
            else :
                 return 0
        

    @staticmethod
    def Cruise_Mach_SAR(Avion: Avion, Atmosphere: Atmosphere, l_end, dt=60.0):
        """
        Phase : croisière en palier à Mach constant

        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        l_end : distance à parcourir en croisière avant de commencer la descente (m)
        """
        l_t = Avion.getl()


        while (l_t < l_end - Avion.getl_descent()) and Avion.Masse.getFuelRemaining() > Avion.Masse.getFuelReserve():

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(Avion.geth())

            # --- Vitesse ---
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)

            # --- Vitesses ---
            Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Atmosphere)

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxCruise_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)

            # --- Poussée moteur ---
            Avion.Moteur.Calculate_F_cruise()
            Avion.Moteur.Calculate_SFC_cruise()

            # --- Condition de montée iso-Mach ---
            if (Croisiere.Check_up(Avion, Atmosphere) == 1 ):
                Croisiere.Climb_iso_Mach(Avion,Atmosphere, dt=1)
            else : 
                # --- Intégration ---
                
                dl = Vx * dt

                
                l_t += dl

                # --- Fuel burn ---
                Avion.Masse.burn_fuel(dt)

                # --- Mise à jour avion ---
                Avion.Add_dl(dl)
                # Pas de changement d'altitude en croisière

                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement à chaque pas de temps pour la croisière

