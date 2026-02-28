from constantes.Constantes import Constantes
from inputs.Inputs import Inputs

class Masse:
    def __init__(self, Avion):
        '''
        Initialisation de la sous-classe Masse d'un avion: les masses de fuel nécessaires à la mission, la contingence,
        la diversion et le holding sont définies (pour l'instant seule la masse mission est définie à la MFW, les 
        autres à 0). Les masses dynamiques sont également initialisées.

        :param Avion: Instance de la classe Avion
        :param m_payload: Masse de la payload (m)
        '''
        self.Avion = Avion
        self.Inputs = Avion.Inputs

        # Masses mission
        self.m_payload          = self.Inputs.m_payload     # Payload de la mission
        self.m_fuel_mission     = Avion.getMaxFuelWeight()/2  # Fuel nécessaire à la mission (set au max au début)
        self.m_fuel_contingency = 0.0                       # Fuel de contingence, ce qu'il doit obligatoirement resté au minimum à la fin de la mission (typiquement 5%)
        self.m_fuel_diversion   = 0.0                       # Fuel en cas de diversion vers un aéroport de dégagement
        self.m_fuel_holding     = 0.0                       # Fuel en cas de holding réglementaire
        self.m_fuel_reserve     = (self.m_fuel_contingency
                                +  self.m_fuel_diversion
                                +  self.m_fuel_holding)     # Fuel de reserve : diversion + holding + contingency

        # Masses détaillées
        self.m_fuel_climb       = 0.0
        self.m_fuel_cruise      = 0.0
        self.m_fuel_descent     = 0.0

        # Masses dynamiques
        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve # Fuel dans l'avion à l'instant t
        self.m_burned_total_t   = 0.0 # Quantité de fuel consommée à l'instant t

    def initializeMission(self):
        '''
        Méthode qui remet à zéro les masses dynamiques.
        '''
        self.m_fuel_contingency = self.Inputs.Contingency * self.m_fuel_mission / 100
        self.m_fuel_reserve     = self.m_fuel_contingency + self.m_fuel_diversion + self.m_fuel_holding

        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve
        self.m_burned_total_t   = 0.0

    def burnFuel(self, dt):
        '''
        Ajoute la quantité de fuel consommée pendant le pas de temps dt.
        
        :param dt: Pas de temps (s)
        '''
        dm = self.Avion.Moteur.getFF() * dt # Débit de carburant consommé pendant dt
        self.m_fuel_remaining_t -= dm   # Soustraction du fuel consommé au fuel restant
        self.m_burned_total_t   += dm   # Ajout du fuel consommé au fuel brulé

    def setMass(self, masse_kg):
        '''
        Définit la masse de l'avion en le remplissant d'essence, puis en ajoutant de la payload.
        
        :param masse_kg: Masse à set.
        '''
        # Remise à zéro
        self.m_payload = 0
        self.m_fuel_mission = 0
        self.m_fuel_diversion = 0
        self.m_fuel_contingency = 0
        self.m_fuel_holding = 0
        self.m_fuel_reserve = 0
        self.m_fuel_remaining_t = 0
        self.m_burned_total_t = 0

        # Si la masse est trop petite
        if masse_kg < self.Avion.getEmptyWeight():
            print("Masse plus faible que la masse à vide: calcul effectué à masse vide.")
            return
        
        masse = masse_kg - self.Avion.getEmptyWeight()

        # Si la masse restante est plus petite que le max fuel
        if masse < self.Avion.getMaxFuelWeight():
            self.m_fuel_mission = masse
            self.m_fuel_remaining_t = masse
            return
        
        self.m_fuel_mission = self.Avion.getMaxFuelWeight()
        self.m_fuel_remaining_t = self.Avion.getMaxFuelWeight()

        masse = masse - self.Avion.getMaxFuelWeight()

        # Si la masse restante est plus petite que la max payload
        if masse <= self.Avion.getMaxPLWeight():
            self.m_payload = masse
            return
        
        # Sinon la masse voulue est trop lourde
        self.m_payload = self.Avion.getMaxPLWeight()
        print("Masse voulue trop lourde, calcul effectué à max payload + max fuel.")



    def getCurrentMass(self):
        '''
        Renvoie la masse totale: masse à vide + masse payload + masse carburant restant (kg).
        '''
        return (
            self.Avion.getEmptyWeight() +
            self.m_payload +
            self.m_fuel_remaining_t
        )

    def getCurrentWeight(self):
        '''
        Renvoie le poids (en N) de l'avion.
        '''
        return self.getCurrentMass() * Constantes.g

    def getFuelBurned(self):
        '''
        Renvoie la masse de fuel consommée (kg).
        '''
        return self.m_burned_total_t
    
    def getFuelRemaining(self):
        '''
        Renvoie la masse restante de fuel (kg).
        '''
        return self.m_fuel_remaining_t
    
    def getFuelMission(self):
        '''
        Renvoie la masse de fuel emportée pour la mission (kg).
        '''
        return self.m_fuel_mission

    def getFuelReserve(self):
        '''
        Renvoie la masse de carburant pour la réserve (kg).
        '''
        return self.m_fuel_reserve

    def setFuelMission(self, m_fuel_mission):
        self.m_fuel_mission = m_fuel_mission

    def addFuelMission(self, dm_fuel):
        self.m_fuel_mission += dm_fuel

    # Montée
    def setFuelClimb(self, m_fuel_climb):
        self.m_fuel_climb = m_fuel_climb

    def getFuelClimb(self):
        return self.m_fuel_climb

    # Croisière
    def setFuelCruise(self, m_fuel_cruise):
        self.m_fuel_cruise = m_fuel_cruise

    def getFuelCruise(self):
        return self.m_fuel_cruise

    # Descente
    def setFuelDescent(self, m_fuel_descent):
        self.m_fuel_descent = m_fuel_descent

    def getFuelDescent(self):
        return self.m_fuel_descent

    # Diversion
    def setFuelDiversion(self, m_fuel_diversion):
        self.m_fuel_diversion = m_fuel_diversion

    def getFuelDiversion(self):
        return self.m_fuel_diversion

    # Holding
    def setFuelHolding(self, m_fuel_holding):
        self.m_fuel_holding = m_fuel_holding

    def getFuelHolding(self):
        return self.m_fuel_holding
    
    # Contingency
    def getFuelContingency(self):
        return self.m_fuel_contingency

