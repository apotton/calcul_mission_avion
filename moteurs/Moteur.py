'''
Classe mère des différentes manières de faire un moteur
'''

class Moteur:
    def __init__(self, Avion, BPR=0., OPR=0., choix_reseau=1):
        self.Avion = Avion
        self.BPR = BPR        # Bypass ratio
        self.OPR = OPR        # Overall Pressure Ratio
        self.F_t = 0          # Poussée actuelle (N)
        self.SFC_t = 0        # SFC actuelle (kg/(N.s))

    # Setters

    def setF(self, F: float):
        '''
        Définit la vitesse CAS actuelle de l'avion.
        
        :param self: Instance de la classe Avion
        :param CAS: Vitesse CAS à définir (m/s)
        '''
        self.F_t = F

    def setSFC(self, SFC: float):
        '''
        Définit la vitesse CAS actuelle de l'avion.
        
        :param self: Instance de la classe Avion
        :param CAS: Vitesse CAS à définir (m/s)
        '''
        self.SFC_t = SFC

    # Getters
    def getBPR(self):
        return self.BPR

    def getOPR(self):
        return self.OPR

    # def getDonnees_moteur(self):
    #     return self.Donnees_moteur

    def getF(self):
        return self.F_t

    def getSFC(self):
        return self.SFC_t
    
    def getF_MCL_cruise_step(self):
        return self.F_t

    ## Poussée ##

    def Calculate_F_climb(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_F_cruise(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_F_descent(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_F_holding(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_F_cruise_diversion(self):
        pass  # Méthode à implémenter dans les classes filles

    ## SFC ##

    def Calculate_SFC_cruise(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC_climb(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC_descent(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC_holding(self):
        pass  # Méthode à implémenter dans les classes filles

    def Calculate_SFC_cruise_diversion(self):
        pass  # Méthode à implémenter dans les classes filles

         