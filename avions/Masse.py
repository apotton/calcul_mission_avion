from constantes.Constantes import Constantes
from inputs.Inputs import Inputs

class Masse:
    def __init__(self, avion):
        self.Avion = avion
        # self.moteur = moteur

        # --- Masses mission ---
        self.m_payload = Inputs.m_payload               # Payload de la mission
        self.m_fuel_mission = avion.getMaxFuelWeight()  # Fuel nécessaire à la mission
        self.m_fuel_contingency = 0.0                   # Fuel de contingence, ce qu'il doit obligatoirement resté au minimum à la fin de la mission (typiquement 5%)
        self.m_fuel_diversion = 0.0                     # Fuel en cas de diversion vers un aéroport de dégagement
        self.m_fuel_holding = 0.0                       # Fuel en cas de holding réglementaire
        self.m_fuel_reserve = (self.m_fuel_contingency
                             + self.m_fuel_diversion
                             + self.m_fuel_holding)     # Fuel de reserve : diversion + holding + contingency

        assert self.m_fuel_mission + self.m_fuel_reserve <= avion.getMaxFuelWeight(), "Trop d'essence dans l'avion"

        # --- Masses dynamiques ---
        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve # Fuel dans l'avion à l'instant t
        self.m_burned_total_t = 0.0 #Quantité de Fuel consommé à l'instant t

    def initialize_mission(self, FB_mission, FB_diversion, FB_holding): #Initialisation des masses réalisée au début de la mission
        self.m_fuel_mission = FB_mission
        self.m_fuel_contingency = FB_mission * Inputs.Contingency
        self.m_fuel_diversion = FB_diversion
        self.m_fuel_holding = FB_holding

        self.m_fuel_reserve = self.m_fuel_contingency + self.m_fuel_diversion + self.m_fuel_holding

        self.m_fuel_remaining_t = self.m_fuel_mission + self.m_fuel_reserve
        self.m_burned_total_t = 0.0

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
    
    def getFuelMission(self):
        return self.m_fuel_mission

    def getFuelReserve(self):
        return self.m_fuel_reserve


