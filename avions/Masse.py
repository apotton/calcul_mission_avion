from constantes.Constantes import Constantes
from inputs.Inputs import Inputs

class Masse:
    def __init__(self, Avion, m_payload):
        '''
        Initialisation de la sous-classe Masse d'un avion: les masses de fuel nécessaires à la mission, la contingence,
        la diversion et le holding sont définies (pour l'instant seule la masse mission est définie à la MFW, les 
        autres à 0). Les masses dynamiques sont également initialisées.

        :param Avion: Instance de la classe Avion
        :param m_payload: Masse de la payload (m)
        '''
        self.Avion = Avion

        # Masses mission
        self.m_payload          = m_payload                 # Payload de la mission
        self.m_fuel_mission     = Avion.getMaxFuelWeight()  # Fuel nécessaire à la mission (set au max au début)
        self.m_fuel_contingency = 0.0                       # Fuel de contingence, ce qu'il doit obligatoirement resté au minimum à la fin de la mission (typiquement 5%)
        self.m_fuel_diversion   = 0.0                       # Fuel en cas de diversion vers un aéroport de dégagement
        self.m_fuel_holding     = 0.0                       # Fuel en cas de holding réglementaire
        self.m_fuel_reserve     = (self.m_fuel_contingency
                                +  self.m_fuel_diversion
                                +  self.m_fuel_holding)     # Fuel de reserve : diversion + holding + contingency

        # Si on a mis trop d'essence au début
        assert self.m_fuel_mission + self.m_fuel_reserve <= Avion.getMaxFuelWeight(), "Trop d'essence dans l'avion"

        # Masses dynamiques
        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve # Fuel dans l'avion à l'instant t
        self.m_burned_total_t   = 0.0 # Quantité de fuel consommée à l'instant t

    def initializeMission(self, FB_mission, FB_diversion, FB_holding):
        '''
        Méthode qui set les différentes masses selon les fuels burn données en entrée,
        et remet à zéro les masses dynamiques.
        
        :param FB_mission: Masse de carburant brulée lors de la mission (kg).
        :param FB_diversion: Masse de carburant brulée lors de la diversion (kg).
        :param FB_holding: Masse de carburant brulée lors de la phase de holding (kg)
        '''
        # Set des différentes masses en argument
        self.m_fuel_mission     = FB_mission
        self.m_fuel_contingency = FB_mission * Inputs.Contingency
        self.m_fuel_diversion   = FB_diversion
        self.m_fuel_holding     = FB_holding

        self.m_fuel_reserve     = self.m_fuel_contingency + self.m_fuel_diversion + self.m_fuel_holding

        assert self.m_fuel_mission + self.m_fuel_remaining_t <= self.Avion.getMaxFuelWeight(), "La mission demande trop d'essence"

        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve
        self.m_burned_total_t   = 0.0

    def burnFuel(self, dt):
        '''
        Ajoute la quantité de fuel consommée pendant le pas de temps dt.
        
        :param dt: Pas de temps (s)
        '''
        dm = self.Avion.Moteur.getF() * self.Avion.Moteur.getSFC() * dt # Débit de carburant consommé pendant dt
        self.m_fuel_remaining_t -= dm   # Soustraction du fuel consommé au fuel restant
        self.m_burned_total_t   += dm   # Ajout du fuel consommé au fuel brulé


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
        Renvoie la masse d'essence pour la réserve (kg).
        '''
        return self.m_fuel_reserve


