from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
from missions.Montee import Montee
from missions.Descente import Descente
import numpy as np

class Holding:

    @staticmethod
    def Hold(Avion:Avion, Atmosphere:Atmosphere,  dt = Inputs.dt_cruise):

        if (Avion.Aero.getCAS() < Inputs.KCAS_holding):
            # Accélération en palier
            CAS_target = Inputs.KCAS_holding * Constantes.conv_kt_mps
            Montee.climb_Palier(Avion, Atmosphere, CAS_target, dt = Inputs.dt_climb)
        elif (Avion.Aero.getCAS() > Inputs.KCAS_holding):
            # Décélération palier avec moteur en idle 
            CAS_target = Inputs.KCAS_holding * Constantes.conv_kt_mps
            Descente.descent_Palier(Avion, Atmosphere, CAS_target, Inputs.dt_climb)


        Holding.hold_palier(Avion, Atmosphere, dt)
        

    @staticmethod
    def hold_palier(Avion:Avion, Atmosphere:Atmosphere, dt = Inputs.dt_cruise):

        n_pas_de_temps = int(Inputs.Time_holding * 60 / dt)

        for i in range(n_pas_de_temps):
            # Atmosphere
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses (iso-CAS)
            Avion.Aero.Convert_CAS_to_Mach(Atmosphere)
            Avion.Aero.Convert_Mach_to_TAS(Atmosphere)
            
            # Aéro
            Avion.Aero.CalculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.CalculateCxCruise_Simplified()
            else:
                Avion.Aero.CalculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()


            Avion.Moteur.Calculate_F_holding()
            Avion.Moteur.Calculate_SFC_holding()

            Avion.Add_dl(Avion.Aero.getTAS() * dt)
            Avion.Masse.burn_fuel(dt)

            Enregistrement.save(Avion, Atmosphere, dt)

        