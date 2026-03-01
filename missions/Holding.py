from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Descente import Descente
from missions.Montee import Montee
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Holding:

    @staticmethod
    def Hold(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs):
        '''
        Réalisation de l'opération de holding: l'avion atteint la vitesse target et vole
        en palier pendant un temps déterminé.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        m_init = Avion.Masse.getCurrentMass()
        t_init = Avion.get_t()
        l_init = Avion.getl()
        
        # La vitesse souhaitée est celle qui maximise la finesse
        Atmosphere.CalculateRhoPT(Avion.geth())
        _, CAS_target = Holding.calculateMach_target(Avion, Atmosphere, Inputs)

        if (Avion.Aero.getCAS() < CAS_target):
            # Accélération en palier
            Montee.climbPalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_target, dt = Inputs.dtClimb)
        elif (Avion.Aero.getCAS() > CAS_target):
            # Décélération palier avec moteur en idle 
            Descente.descentePalier(Avion, Atmosphere, Enregistrement, Inputs, CAS_target, dt = Inputs.dtClimb)

        #  Vol en palier
        Holding.holdPalier(Avion, Atmosphere, Enregistrement, Inputs, t_init, dt = Inputs.dtCruise)

        Avion.set_l_holding(Avion.getl() - l_init)
        Avion.set_t_holding(Avion.get_t() - t_init)
        Avion.Masse.setFuelHolding(m_init - Avion.Masse.getCurrentMass())
        
    @staticmethod
    def calculateMach_target(Avion: Avion, Atmosphere: Atmosphere, Inputs: Inputs):
        # Sauvegarde des variables qui vont changer
        Mach = Avion.Aero.getMach()
        CAS  = Avion.Aero.getCAS()
        TAS  = Avion.Aero.getTAS()
        h    = Avion.geth()
        Cz   = Avion.Aero.getCz()
        Cx   = Avion.Aero.getCx()

        # Calcul vectorisé du Mach optimal
        Atmosphere.CalculateRhoPT(Avion.geth())
        Mach_grid = np.arange(0.1, 0.82, 0.01)

        Avion.Aero.setMach(Mach_grid)
        Avion.Aero.convertMachToCAS(Atmosphere)
        Avion.Aero.convertMachToTAS(Atmosphere)

        Avion.Aero.calculateCz(Atmosphere)
        if Inputs.AeroSimplified:
            Avion.Aero.calculateCx(Atmosphere)
        else:
            Avion.Aero.calculateCxCruise_Simplified()
        
        finesse = Avion.Aero.getCz() / Avion.Aero.getCx()

        idx_max = np.argmax(finesse)
        Mach_target = Mach_grid[idx_max]
        Avion.Aero.setMach(Mach_target)
        Avion.Aero.convertMachToCAS(Atmosphere)
        CAS_target = Avion.Aero.getCAS()

        # Remise à zéro
        Avion.Aero.setMach(Mach)
        Avion.Aero.setCAS(CAS)
        Avion.Aero.setTAS(TAS)
        Avion.set_h(h)
        Avion.Aero.setCz(Cz)
        Avion.Aero.setCz(Cx)

        return Mach_target, CAS_target

    @staticmethod
    def holdPalier(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, Inputs: Inputs, t_init, dt):
        '''
        Vol en palier à vitesse constante pendant une durée définie.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (dt)
        '''
        # Nombre de pas de temps de holding
        t_target = t_init + Inputs.Time_holding_min * 60
        t = Avion.get_t()

        while t < t_target:
            if (t + dt > t_target):
                dt = t_target - t
                
            # Atmosphere
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Vitesses (iso-CAS)
            Avion.Aero.convertCASToMach(Atmosphere)
            Avion.Aero.convertMachToTAS(Atmosphere)
            
            # Aéro
            Avion.Aero.calculateCz(Atmosphere)

            if Inputs.AeroSimplified:
                Avion.Aero.calculateCxCruise_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)

            # Poussée moteur
            Avion.Moteur.calculateFHolding()
            Avion.Moteur.calculateSFCHolding()
            
            # Masses
            Avion.Masse.burnFuel(dt)

            # Cinématique
            Vx = Avion.Aero.getTAS() + Inputs.Vw_kt * Constantes.conv_kt_mps
            Avion.Add_dl(Vx * dt)
            Avion.Add_dt(dt)
            t = Avion.get_t()

            # Enregistrement pour le pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)

        