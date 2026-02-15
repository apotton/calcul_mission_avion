from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Descente import Descente
from missions.Montee import Montee
from inputs.Inputs import Inputs
from avions.Avion import Avion

class Holding:

    @staticmethod
    def Hold(Avion: Avion, Atmosphere: Atmosphere,  dt = Inputs.dt_cruise):
        '''
        Réalisation de l'opération de holding: l'avion atteint la vitesse target et vole
        en palier pendant un temps déterminé.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        
        # Accélération / Décélération à la vitesse souhaitée
        CAS_target = Inputs.KCAS_holding * Constantes.conv_kt_mps

        if (Avion.Aero.getCAS() < Inputs.KCAS_holding):
            # Accélération en palier
            Montee.climbPalier(Avion, Atmosphere, CAS_target, dt = Inputs.dt_climb)
        elif (Avion.Aero.getCAS() > Inputs.KCAS_holding):
            # Décélération palier avec moteur en idle 
            Descente.descentePalier(Avion, Atmosphere, CAS_target, dt = Inputs.dt_climb)

        #  Vol en palier
        Holding.holdPalier(Avion, Atmosphere, dt)
        

    @staticmethod
    def holdPalier(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_cruise):
        '''
        Vol en palier à vitesse constante pendant une durée définie.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
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

            if Inputs.Aero_simplified:
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

        