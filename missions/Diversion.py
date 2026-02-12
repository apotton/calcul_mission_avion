from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from missions.Montee import Montee
from missions.Descente import Descente
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
        Montee.Monter_Diversion(Avion, Atmosphere, dt = Inputs.dt_climb)
        
        # Croisière diversion
        Diversion.Diversion_Cruise(Avion, Atmosphere)

        # Descente de diversion
        Descente.Descendre_Diversion(Avion, Atmosphere, dt = Inputs.dt_descent)




    @staticmethod
    def Diversion_Cruise(Avion: Avion, Atmosphere: Atmosphere, l_end = Inputs.Range_diversion_NM, dt=Inputs.dt_cruise): #ON PEUT METTRE UN dt ENORME, IL SE PASSE RIEN 
            """
            Phase : croisière en palier à Mach constant

            Avion : instance de la classe Avion
            Atmosphere : instance de la classe Atmosphere
            l_end : distance à parcourir en croisière avant de commencer la descente (UNITE)
            """
            l_init = Avion.getl()
            l_t = l_init


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
                l_t += dl

                # --- Fuel burn ---
                Avion.Masse.burn_fuel(dt)

                # --- Mise à jour avion ---
                Avion.Add_dl(dl)
                # Pas de changement d'altitude en croisière

                Enregistrement.save(Avion, Atmosphere, dt) #Enregistrement à chaque pas de temps pour la croisière



