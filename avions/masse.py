from constantes.constantes import Constantes

class Masse:
    def __init__(self, avion):
        self.Avion = avion

        # --- Masses mission ---
        self.m_payload = 0.0 #Payload de la mission
        self.m_fuel_mission = 0.0 #Fuel nécessaire à la mission
        self.m_fuel_reserve = 0.0 #Fuel de reserve : diversion + holding + contingency
        self.m_fuel_contingency = 0.0 #Fuel de contingence, ce qu'il doit obligatoirement resté au minimum à la fin de la mission (typiquement 5%)
        self.m_fuel_diversion = 0.0 #Fuel en cas de diversion vers un aéroport de dégagement
        self.m_fuel_holding = 0.0 #Fuel en cas de holding réglementaire

        # --- Masses dynamiques ---
        self.m_fuel_remaining_T = 0.0 #Fuel dans l'avion à l'instant T
        self.m_burned_total_T = 0.0 #Quantité de Fuel consommé à l'instant T

    def initialize_mission(self, payload, fuel_mission): #Initialisation des masses réalisée au début de la mission
        self.m_payload = payload
        self.m_fuel_mission = fuel_mission

        self.compute_reserves()

        self.m_fuel_remaining_T = self.m_fuel_mission + self.m_fuel_reserve
        self.m_burned_total_T = 0.0

    def compute_reserves(self, contingency_percent=5):
        self.m_fuel_contingency = contingency_percent * self.m_fuel_mission / 100 #On prend 5% de contingence 
        self.m_fuel_reserve = (
            self.m_fuel_diversion +
            self.m_fuel_holding +
            self.m_fuel_contingency
        )

    def burn_fuel(self, dt):
        fuel_flow = SFC * F #ATTENTION UTILISER LES GETTERS DE LA CLASSE MOTEUR UNE FOIS CREES
        dm = fuel_flow * dt #Débit de carburant consommé pendant dt
        self.m_fuel_remaining -= dm #On soustrait le fuel consommé au fuel restant
        self.m_burned_total += dm #On ajoute le fuel consommé au fuel brulé

#Getters

    def getCurrentMass(self):
        return (
            self.Avion.getEmptyWeight() +
            self.m_payload +
            self.m_fuel_remaining_T
        )


    def getCurrentWeight(self):
        return self.getCurrentMass() * Constantes.g

    def getFuelBurned(self):
        return self.m_burned_total


