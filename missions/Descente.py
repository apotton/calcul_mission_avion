from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Descente:
    @staticmethod
    def Descendre(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        '''
        Réalise toute la descente depuis la fin de la croisière jusqu'à l'altitude finale.

        :param Avion: instance de la classe Avion
        :param Atmosphere: instance de la classe Atmosphere
        :param dt: pas de temps (s)
        '''
        # Reset de la distance de descente pour une estimation plus précise
        Avion.setl_descent(0.)

        # Première phase
        Descente.descenteIsoMach(Avion, Atmosphere, dt)

        # Seconde phase
        h_target = Inputs.h_decel_ft * Constantes.conv_ft_m
        Descente.descenteIsoMaxCAS(Avion, Atmosphere, h_target, dt)

        # Dernière phase
        CAS_target = Inputs.CAS_below_10000_desc_kt * Constantes.conv_kt_mps
        Descente.descentePalier(Avion, Atmosphere, CAS_target, dt)
        Descente.descenteFinaleIsoCAS(Avion, Atmosphere, dt)


    @staticmethod
    def descendreDiversion(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        '''
        Réalise les opérations de descente à la fin de la diversion.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (dt)
        '''
        # Reset de la distance de descente pour une estimation plus précise
        Avion.setl_descent_diversion(0.)

        # Première phase
        Descente.descenteIsoMach(Avion, Atmosphere, dt)

        # Deuxième phase
        h_target = Inputs.h_decel_ft * Constantes.conv_ft_m
        Descente.descenteIsoMaxCAS(Avion, Atmosphere, h_target, dt)

        # Troisième phase
        CAS_target = Inputs.CAS_below_10000_desc_kt * Constantes.conv_kt_mps
        Descente.descentePalier(Avion, Atmosphere, CAS_target, dt)
        Descente.descenteFinaleIsoCAS(Avion, Atmosphere, dt)

    # Phase 1 : Ajustement vitesse à Max CAS avec possibilité de descente libre---
    @staticmethod
    def descenteIsoMach(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        '''
        Laisse l'avion initier une descente libre pour atteindre la vitesse maximale autorisée en CAS (Vmax_CAS) avant de passer à la phase 2.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        # CAS max en m/s
        CAS_max = Avion.getKVMO() * Constantes.conv_kt_mps
        CAS_t = Avion.Aero.getCAS()

        while CAS_t < CAS_max:
            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Mach et TAS 
            Avion.Aero.convertMachToCAS(Atmosphere)
            Avion.Aero.convertMachToTAS(Atmosphere)

            CAS_t = Avion.Aero.getCAS()   
            TAS_t = Avion.Aero.getTAS() 

            # Cz et Cx Calcul des coefs aéro
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxDescent_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur et SFC
            Avion.Moteur.calculateFDescent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCDecent()

            # Résistance horizontale
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente de descente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())
            Vz = TAS_t * np.sin(pente)
            Vx = TAS_t * np.cos(pente)

            # Mise à jour des positions
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)        

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            if (Avion.diversion):
                Avion.Add_l_descent_diversion(Vx * dt)
            else:
                Avion.Add_l_descent(Vx * dt)
            
            Enregistrement.save(Avion, Atmosphere, dt)
            

    @staticmethod
    def descenteIsoMaxCAS(Avion: Avion, Atmosphere: Atmosphere, h_end, dt = Inputs.dt_descent):
        '''
        Phase 2 : Descente jusqu'à 10000ft à vitesse constante Max CAS
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param h_end: Altitude finale de la phase de la descente (m)
        :param dt: Pas de temps (s)
        '''

        # CAS imposée
        CAS_t = Avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s On descend à CAS fixé par la vitesse max de descente
        Avion.Aero.setCAS_t(CAS_t)

        while Avion.geth() > h_end:

            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Conversion CAS -> Mach
            Avion.Aero.convertCASToMach(Atmosphere)

            # TAS
            Avion.Aero.convertMachToTAS(Atmosphere)

            # Mach_t = Avion.Aero.getMach()
            TAS_t  = Avion.Aero.getTAS()

            # Coefficients aérodynamiques
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxDescent_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur (idle en descente)
            Avion.Moteur.calculateFDescent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCDecent()

            # Résistance
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente de trajectoire
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            Vz = TAS_t * np.sin(pente)   # négatif car en descente
            Vx = TAS_t * np.cos(pente)

            # Mise à jour position
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            if (Avion.diversion):
                Avion.Add_l_descent_diversion(Vx * dt)
            else:
                Avion.Add_l_descent(Vx * dt)
            
            Enregistrement.save(Avion, Atmosphere, dt)
            

    @staticmethod
    def descentePalier(Avion: Avion, Atmosphere: Atmosphere, CAS_target, dt = Inputs.dt_descent):
        '''
        Phase 3 : Décélération en palier: l'altitude est fixée et l'avion décélère.

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param CAS_target: CAS à viser à la fin du palier
        :param dt: Pas de temps (s)
        '''

        # CAS initiale (issue phase 2)
        CAS_t = Avion.Aero.getCAS()

        # Conditions atmosphériques constantes
        Atmosphere.CalculateRhoPT(Avion.geth())

        # Vitesses
        Avion.Aero.convertCASToMach(Atmosphere)
        Avion.Aero.convertMachToTAS(Atmosphere)
        TAS_t = Avion.Aero.getTAS()

        # Diminution de la vitesse jusqu'a la valeur désirée
        while CAS_t > CAS_target:

            # Coefficients aérodynamiques
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxDescent_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Forces
            Rx = Avion.Masse.getCurrentWeight() / finesse  # cohérent avec finesse

            # Poussée moteur (idle / freinage)
            Avion.Moteur.calculateFDescent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCDecent()

            # Dynamique longitudinale simplifiée
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # Mise à jour des vitesses
            Avion.Aero.setTAS_t(max(TAS_t + ax * dt, 0.0))
            TAS_t = Avion.Aero.getTAS() #Calcul de la nouvelle vitesse avec la resistance longitudinale

            # Recalcul CAS depuis Mach/TAS
            Avion.Aero.convertTASToMach(Atmosphere)
            Avion.Aero.convertMachToCAS(Atmosphere)
            CAS_t = Avion.Aero.getCAS()

            # Cinématique
            Avion.Add_dl(TAS_t * dt)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            if (Avion.diversion):
                Avion.Add_l_descent_diversion(TAS_t * dt)
            else:
                Avion.Add_l_descent(TAS_t * dt)

            Enregistrement.save(Avion, Atmosphere, dt)
            

    # Phase 4 : Descente finale jusqu'à h_final
    @staticmethod
    def descenteFinaleIsoCAS(Avion: Avion, Atmosphere: Atmosphere, dt = Inputs.dt_descent):
        '''
        Phase 4 : descente à CAS constante (250 kt) jusqu'à l'altitude finale de 1500ft

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        
        # Descente jusqu'à altitude finale
        while Avion.geth() > Inputs.h_final_ft * Constantes.conv_ft_m:
            # Atmosphère
            Atmosphere.CalculateRhoPT(Avion.geth())

            # Mach depuis CAS
            Avion.Aero.convertCASToMach(Atmosphere)

            # TAS
            Avion.Aero.convertMachToTAS(Atmosphere)

            # Aérodynamique
            Avion.Aero.calculateCz(Atmosphere)
            Cz = Avion.Aero.getCz()

            if Inputs.Aero_simplified:
                Avion.Aero.calculateCxDescent_Simplified()
            else:
                Avion.Aero.calculateCx(Atmosphere)
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # Poussée moteur
            Avion.Moteur.calculateFDescent()
            F_N = Avion.Moteur.getF()
            Avion.Moteur.calculateSFCDecent()

            # Résistance
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # Pente
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # Vitesses
            TAS_t = Avion.Aero.getTAS()
            Vz = TAS_t * np.sin(pente)
            Vx = TAS_t * np.cos(pente)

            # Intégration
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)

            # Fuel burn
            Avion.Masse.burnFuel(dt)

            if (Avion.diversion):
                Avion.Add_l_descent_diversion(Vx * dt)
            else:
                Avion.Add_l_descent(Vx * dt)
        
            Enregistrement.save(Avion, Atmosphere, dt)
            

