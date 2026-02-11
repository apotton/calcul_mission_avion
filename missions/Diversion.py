from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from Montee import Montee
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
        Montee.climb_iso_CAS(Avion, Atmosphere, Inputs.Final_climb_altitude_diversion_ft, Inputs.Mach_climb, Inputs.dt_climb)
        Montee.climb_iso_Mach(Avion, Atmosphere, Inputs.Final_climb_altitude_diversion_ft, Inputs.dt_climb)

    # Croisière diversion


    # Descente de diversion


