from inputs.Inputs import Inputs
from constantes.Constantes import Constantes

class Masse:
    def __init__(self, avion):
        self.Avion = avion
        # self.moteur = moteur

        # --- Masses mission ---
        self.m_payload = 18000.0 #Payload de la mission
        self.m_fuel_mission = 19000.0 #Fuel nécessaire à la mission
        self.m_fuel_reserve = 0.0 #Fuel de reserve : diversion + holding + contingency
        self.m_fuel_contingency = 0.0 #Fuel de contingence, ce qu'il doit obligatoirement resté au minimum à la fin de la mission (typiquement 5%)
        self.m_fuel_diversion = 0.0 #Fuel en cas de diversion vers un aéroport de dégagement
        self.m_fuel_holding = 0.0 #Fuel en cas de holding réglementaire

        # --- Masses dynamiques ---
        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve #Fuel dans l'avion à l'instant t
        self.m_burned_total_t = 0.0 #Quantité de Fuel consommé à l'instant t

    def initialize_mission(self, fuel_mission): #Initialisation des masses réalisée au début de la mission
        self.m_payload = Inputs.m_payload
        self.m_fuel_mission = fuel_mission

        self.compute_reserves()

        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve
        self.m_burned_total_t = 0.0

    def compute_reserves(self, contingency_percent=5):
        self.m_fuel_contingency = contingency_percent * self.m_fuel_mission / 100 #On prend 5% de contingence 
        self.m_fuel_reserve = (
            self.m_fuel_diversion +
            self.m_fuel_holding +
            self.m_fuel_contingency
        )

    def burn_fuel(self, dt):
        dm = self.Avion.Moteur.getF() * self.Avion.Moteur.getSFC() * dt #Débit de carburant consommé pendant dt
        self.m_fuel_remaining_t -= dm #On soustrait le fuel consommé au fuel restant
        self.m_burned_total_t += dm #On ajoute le fuel consommé au fuel brulé

#Getters

    def getCurrentMass(self):
        return (
            self.Avion.getEmptyWeight() +
            self.m_payload +
            self.m_fuel_remaining_t
        )


    def getCurrentWeight(self):
        '''
        Renvoie le poids (en N) de l'avion
        '''
        return self.getCurrentMass() * Constantes.g

    def getFuelBurned(self):
        return self.m_burned_total_t
    
    def getFuelRemaining(self):
        return self.m_fuel_remaining_t
    
    def getFuelReserve(self):
        return self.m_fuel_reserve


