from avions.Avion import Avion
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
from enregistrement.Enregistrement import Enregistrement
from inputs.Inputs import Inputs

class Croisiere:
    @staticmethod
    def Croisiere(Avion: Avion, Atmosphere: Atmosphere, l_end, dt=60.0):
        ''' Réalise toute la croisière
        
        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        l_end : distance à parcourir en croisière avant de commencer la descente (UNITE)
        dt : pas de temps (s)
        '''
        Croisiere.Cruise_Mach_SAR(Avion, Atmosphere, l_end, dt)

    @staticmethod
    def climb_iso_Mach(Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        '''
        Montée iso-Mach à Mach constant jusqu'à ce que les critères de montée ne soient plus vérifiés

        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        dt : pas de temps (s)
        '''
        # À implémenter plus tard, pour l'instant on reste en croisière à Mach constant
        pass
    
    ##
    #Croisière MACH SAR
    ##
    @staticmethod
    def Cruise_Mach_SAR(Avion: Avion, Atmosphere: Atmosphere, l_end, dt=60.0):
        """
        Phase : croisière en palier à Mach constant

        Avion : instance de la classe Avion
        Atmosphere : instance de la classe Atmosphere
        l_end : distance à parcourir en croisière avant de commencer la descente (UNITE)
        """

        h_t = Avion.geth()
        l_t = Avion.getl()


        while (l_t < l_end - Avion.getl_descent()) and Avion.Masse.getFuelRemaining() > Avion.Masse.getFuelReserve():

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(Avion.geth())

            # --- Vitesse ---
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            TAS_t = Avion.Aero.getTAS()
            Avion.Aero.Convert_Mach_to_CAS(Atmosphere)
            CAS_t = Avion.Aero.getCAS()

            # --- Vitesses ---
            Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()
            Vz = 0.0

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz/Cx

            # Traînée
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # --- Poussée moteur ---
            Avion.Moteur.Calculate_F()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC()
            SFC = Avion.Moteur.getSFC()

            #Calcul de l'excédent de puissance
            RRoC = (F_N-Rx)/(Avion.Masse.getCurrentWeight())*Avion.Aero.getTAS() #Excédent de puissance qui permet de déterminer si on peut monter de 2000ft 

            #Calcul du coût économique ECCF et SGR
            Avion.Aero.CalculateECCF(Atmosphere)
            Avion.Aero.CalculateSGR(Atmosphere)
            ECCF = Avion.Aero.getECCF()
            SGR = Avion.Aero.getSGR()


            #Calcul du Mach limite 
            #Avion.Aero.CalculateCzBuffet()
            #Cz_Buffet = Avion.Aero.getCzBuffet

            ##Calcul des paramètres 2000ft plus haut pour étudier le coût de monter

            # --- Paramètres 2000 ft plus haut (pour décider la montée) ---
            delta_h_ft = 2000 #ft
            delta_h = delta_h_ft * Constantes.conv_ft_m  # convertir en m

            # Altitude “virtuelle”
            h_up = h_t + delta_h
            Avion.Add_dh(delta_h)

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(Avion.geth())

            # --- TAS (Mach constant avant montée iso-Mach) ---
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            TAS_up = Avion.Aero.getTAS()

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Atmosphere)
            Cz_up = Avion.Aero.getCz()

            Avion.Aero.CalculateCxCruise_Simplified()
            Cx_up = Avion.Aero.getCx()

            finesse_up = Cz_up / Cx_up

            # --- Traînée / équivalent résistance ---
            Rx_up = Avion.Masse.getCurrentWeight() / finesse_up

            # --- Poussée moteur --- #ATTENTION A VOIR CE QU'UTILISE F ET SFC CAR ICI ON MODIFIE QUELQUES CARACTERISTIQUES AVIONS POUR MONTER EN ALTITUDE
            Avion.Moteur.Calculate_F()
            F_N_up = Avion.Moteur.getF()
            Avion.Moteur.Calculate_SFC()
            SFC_up = Avion.Moteur.getSFC()

            
            #Calcul du coût économique ECCF et SGR
            Avion.Aero.CalculateECCF(Atmosphere) 
            Avion.Aero.CalculateSGR(Atmosphere)
            ECCF_up = Avion.Aero.getECCF()
            SGR_up = Avion.Aero.getSGR()


            # --- RRoC (Rate of Climb virtuel) ---
            RRoC_up = (F_N_up - Rx_up) / Avion.Masse.getCurrentWeight() * TAS_up #UTILISER LA MONTEE ISO MACH DE LA PHASE DE MONTEE MAINTENANT

            # --- Condition de montée iso-Mach ---
            if (
                RRoC_up > QUELQUECHOSE.RRoC_min*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s
                h_up < Avion.getPressurisationCeilingFt()*Constantes.conv_ft_m and  # Pas au plafond converti de ft en m
                SGR_up > SGR):                     # Gain SGR positif

                Croisiere.climb_iso_Mach(Avion, Atmosphere , dt=1.0) #CALCUL D ATM DANS LA FONCTION, PEUT ETRE ARRANGER

            else : 
                # --- Intégration ---
                
                dl = Vx * dt

                
                l += dl
                t += dt

                # --- Fuel burn ---
                Avion.Masse.burn_fuel(dt)

                # --- Mise à jour avion ---
                Avion.Add_dh(-delta_h) #On annule la montée en h
                Avion.Add_dl(dl)
                Avion.Aero.setTAS_t(TAS_t)
                Avion.Aero.setMach_t(Inputs.Mach_cruise)
                Avion.Aero.setCAS_t(CAS_t)
                # Pas de changement d'altitude en croisière

                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement à chaque pas de temps pour la croisière

