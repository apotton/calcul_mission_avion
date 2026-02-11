from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from Montee import Montee
from Descente import Descente
import numpy as np

class Diversion:
    @staticmethod
    def Diversion(Avion: Avion, Atmosphere: Atmosphere):
        """
        Réalise toute la montée jusqu'à la croisière

        Avion       : instance de la classe Avion
        Atmosphere  : instance de la classe Atmosphere
        dt          : pas de temps (s)
        """

    # Montée de diversion
        Montee.climb_sub_h_10000_ft(Avion, Atmosphere, Inputs.h_accel_ft, Inputs.dt_climb)
        Montee.climb_Palier(Avion, Atmosphere, Inputs.dt_climb)
        Montee.climb_iso_CAS(Avion, Atmosphere, Inputs.Final_climb_altitude_diversion_ft, Inputs.Mach_cruise_div, Inputs.dt_climb)
        Montee.climb_iso_Mach(Avion, Atmosphere, Inputs.Final_climb_altitude_diversion_ft, Inputs.dt_climb)

    # Croisière diversion
        Diversion.Diversion_Cruise(Avion, Atmosphere)

    # Descente de diversion
    ## ATTENTION IL VA FALLOIR CHANGER LES FONCTIONS POUR EVITER LE CONFLIT ENTRE l_descent ET l_descent_diversion ET AJOUTER l_descent_diversion
        Descente.descent_iso_Mach(Avion, Atmosphere, Inputs.dt_descent)
        Descente.descent_iso_max_CAS(Avion, Atmosphere, Inputs.dt_descent)
        Descente.descent_Palier(Avion, Atmosphere, Inputs.dt_descent)
        Descente.descent_final_iso_CAS(Avion, Atmosphere, Inputs.dt_descent)




    @staticmethod
    def Diversion_Cruise(Avion: Avion, Atmosphere: Atmosphere, l_end = Inputs.Range_diversion_NM, dt=60.0): #ON PEUT METTRE UN dt ENORME, IL SE PASSE RIEN 
            """
            Phase : croisière en palier à Mach constant

            Avion : instance de la classe Avion
            Atmosphere : instance de la classe Atmosphere
            l_end : distance à parcourir en croisière avant de commencer la descente (UNITE)
            """

            h_t = Avion.geth()
            l_t = Avion.getl()


            while (l_t < l_end - Avion.getl_descent()) and Avion.Masse.getFuelRemaining() > Avion.Masse.getFuelReserve(): #METTRE UN L DESCENT DIVERSION ??? ET QUESTION SUR LA LIMITE DE FUEL

                # --- Atmosphère ---
                Atmosphere.CalculateRhoPT(Avion.geth())

                # --- Vitesse ---
                Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
                Avion.Aero.Convert_Mach_to_CAS(Atmosphere)

                # --- Vitesses ---
                Vx = Avion.Aero.getTAS() + Atmosphere.getVwind()

                # --- Aérodynamique ---
                Avion.Aero.CalculateCz(Atmosphere)
                Avion.Aero.CalculateCx(Atmosphere)

                # --- Poussée moteur ---
                Avion.Moteur.Calculate_F_cruise_diversion()
                Avion.Moteur.Calculate_SFC_cruise_diversion()

                # --- Intégration ---
                    
                dl = Vx * dt

                    
                l += dl

                # --- Fuel burn ---
                Avion.Masse.burn_fuel(dt)

                # --- Mise à jour avion ---
                Avion.Add_dl(dl)
                # Pas de changement d'altitude en croisière

                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement à chaque pas de temps pour la croisière



