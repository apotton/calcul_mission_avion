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
    def Hold(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtCruise):
        '''
        Réalisation de l'opération de holding: l'avion atteint la vitesse target et vole
        en palier pendant un temps déterminé.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (s)
        '''
        
        # La vitesse souhaitée est celle qui maximise la finesse
        Atmosphere.CalculateRhoPT(Avion.geth())
        Mach_target = Holding.calculateMach_target(Avion, Atmosphere)

        # Delta pression compressible
        gamma = Constantes.gamma
        Delta_p = Atmosphere.getP_t() * (
            ((gamma - 1) / 2 * Mach_target**2 + 1) ** (gamma / (gamma - 1)) - 1
        )

        # CAS target
        CAS_target = np.sqrt(
            2 * gamma * Constantes.r * Constantes.T0_K / (gamma - 1)
            * ((1 + Delta_p / Constantes.p0_Pa) ** (0.4 / gamma) - 1)
        )

        if (Avion.Aero.getCAS() < CAS_target):
            # Accélération en palier
            Montee.climbPalier(Avion, Atmosphere, Enregistrement, CAS_target, dt = Inputs.dtClimb)
        elif (Avion.Aero.getCAS() > CAS_target):
            # Décélération palier avec moteur en idle 
            Descente.descentePalier(Avion, Atmosphere, Enregistrement, CAS_target, dt = Inputs.dtClimb)

        #  Vol en palier
        Holding.holdPalier(Avion, Atmosphere, Enregistrement, dt)
        
    @staticmethod
    def calculateMach_target(Avion: Avion, Atmosphere: Atmosphere):
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

        # Remise à zéro
        Avion.Aero.setMach(Mach)
        Avion.Aero.setCAS(CAS)
        Avion.Aero.setTAS(TAS)
        Avion.set_h(h)
        Avion.Aero.setCz(Cz)
        Avion.Aero.setCz(Cx)

        return Mach_target

    @staticmethod
    def holdPalier(Avion: Avion, Atmosphere: Atmosphere, Enregistrement: Enregistrement, dt = Inputs.dtCruise):
        '''
        Vol en palier à vitesse constante pendant une durée définie.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param Enregistrement: Instance de la classe Enregistrement
        :param dt: Pas de temps (dt)
        '''
        # Nombre de pas de temps de holding
        n_pas_de_temps = int(Inputs.Time_holding * 60 / dt)

        for _ in range(n_pas_de_temps):
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
            Avion.Add_dl(Avion.Aero.getTAS() * dt)

            # Enregistrement pour le pas de temps
            Enregistrement.save(Avion, Atmosphere, dt)

        