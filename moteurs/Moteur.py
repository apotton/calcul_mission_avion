'''
Classe mère des différentes manières de faire un moteur
'''

class Moteur:
    def __init__(self, Avion):
        self.Avion = Avion
        self.F_t = 0          # Poussée actuelle (N)
        self.SFC_t = 0        # SFC actuelle (kg/(N.s))
        self.FF_t = 0         # Consommation de carburant actuelle (kg/s), calculé dans tous les méthodes de SFC

    # Setters

    def setF(self, F: float):
        '''
        Définit la poussée émise par le moteur.
        
        :param F: Poussée à définir (N)
        '''
        self.F_t = F

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

    ## Poussée ##
    def calculateFClimb(self):
        '''
        Calcule la force de poussée du moteur pendant la montée (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFCruise(self):
        '''
        Calcule la force de poussée du moteur pendant la croisière (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFDescent(self):
        '''
        Calcule la force de poussée du moteur pendant la descente (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFHolding(self):
        '''
        Calcule la force de poussée du moteur pendant la phase de holding (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateFCruiseDiversion(self):
        '''
        Calcule la force de poussée du moteur pendant la croisière de la diversion (N).
        '''
        pass  # Méthode à implémenter dans les classes filles

    ## SFC ##

    def calculateSFCCruise(self):
        '''
        Calcule la poussée spécifique du moteur pendant la croisière (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCClimb(self):
        '''
        Calcule la poussée spécifique du moteur pendant la montée (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCDecent(self):
        '''
        Calcule la poussée spécifique du moteur pendant la descente (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCHolding(self):
        '''
        Calcule la poussée spécifique du moteur pendant la phase de holding (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

    def calculateSFCCruiseDiversion(self):
        '''
        Calcule la poussée spécifique du moteur pendant la croisière de la diversion (kg/(N.s)) ainsi que la consommation de carburant (kg/s).
        '''
        pass  # Méthode à implémenter dans les classes filles

         