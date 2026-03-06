'''
Classe mère des différentes manières de faire un moteur
'''
from atmosphere.Atmosphere import Atmosphere

class Moteur:
    def __init__(self, Avion):
        self.Avion = Avion
        self.Inputs = Avion.Inputs
        self.F_t = 0.          # Poussée actuelle (N)
        self.SFC_t = 0.        # SFC actuelle (kg/(N.s))
        self.FF_t = 0.         # Consommation de carburant actuelle (kg/s), calculé dans tous les méthodes de SFC
        self.DonneesMoteur = {}

    # Setters

    def setF(self, F: float):
        '''
        Définit la poussée émise par le moteur.
        
        :param F: Poussée à définir (N)
        '''
        self.F_t = F

    def setFF(self, FF: float):
        '''
        Définit le fuel flow du moteur.

        :param FF: Fuel Flow à définir (kg/s)
        '''
        self.FF_t = FF

    def setSFC(self, SFC: float):
        '''
        Définit la SFC actuelle de l'avion.
        
        :param SFC: SFC à définir
        '''
        self.SFC_t = SFC

    def getF(self):
        '''
        Renvoie la poussée émise par le moteur (N).
        '''
        return self.F_t

    def getSFC(self):
        '''
        Renvoie la SFC du moteur (kg/(N.s))
        '''
        return self.SFC_t
    
    def getFF(self):
        '''
        Renvoie la consommation de carburant du moteur (kg/s)
        '''
        return self.FF_t

    ## Poussée ##
    def calculateFClimb(self, Atmosphere: Atmosphere):
        '''
        Calcule la force de poussée du moteur pendant la montée (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFCruise(self, Atmosphere: Atmosphere):
        '''
        Calcule la force de poussée du moteur pendant la croisière, par équilibre des forces (N).
        '''
        Cz = self.Avion.Aero.getCz()
        Cx = self.Avion.Aero.getCx()
        finesse = Cz / Cx
        self.F_t = self.Avion.Masse.getCurrentWeight() / finesse

    def calculateFDescent(self, Atmosphere: Atmosphere):
        '''
        Calcule la force de poussée du moteur pendant la descente (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFHolding(self, Atmosphere: Atmosphere):
        '''
        Calcule la force de poussée du moteur pendant la phase de holding par équilibre des forces (N).
        '''
        # Calcul par équilibre des forces
        self.calculateFCruise(Atmosphere)

    def calculateFCruiseDiversion(self, Atmosphere: Atmosphere):
        '''
        Calcule la force de poussée du moteur pendant la croisière de la diversion (N).
        '''
        # Calcul par équilibre des forces
        self.calculateFCruise(Atmosphere)

    ## SFC ##

    def calculateSFCCruise(self, Atmosphere: Atmosphere):
        '''
        Calcule la poussée spécifique du moteur pendant la croisière (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCClimb(self, Atmosphere: Atmosphere):
        '''
        Calcule la poussée spécifique du moteur pendant la montée (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCDescent(self, Atmosphere: Atmosphere):
        '''
        Calcule la poussée spécifique du moteur pendant la descente (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCHolding(self, Atmosphere: Atmosphere):
        '''
        Calcule la poussée spécifique du moteur pendant la phase de holding (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCCruiseDiversion(self, Atmosphere: Atmosphere):
        '''
        Calcule la poussée spécifique du moteur pendant la croisière de la diversion (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFC_Vectorized(self, Atmosphere):
        """
        Version vectorisée du calcul de SFC (en croisière).
        """
        self.calculateSFCCruise(Atmosphere)

    def getfuel_flow_ref(self):
        return self.DonneesMoteur.fuel_flow_ref
    
    def getEI_HC_ref(self):
        return self.DonneesMoteur.EI_HC_ref
    
    def getEI_CO_ref(self):
        return self.DonneesMoteur.EI_CO_ref
    
    def getEI_NOx_ref(self):
        return self.DonneesMoteur.EI_NOx_ref
    
    def getEI_nvPM_Mass(self):
        return self.DonneesMoteur.EI_nvPM_Mass