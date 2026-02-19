from atmosphere.Atmosphere import Atmosphere
from avions.Avion import Avion
import numpy as np


class Enregistrement:
    def __init__(self):
        self.default_size = 10000  # Taille par défaut des tableaux numpy

        # Compteur (pour la taille à chaque changement)
        self.counter = 0

        self.data = {
            # Cinématique
            "t" : np.zeros(self.default_size, dtype=np.float32),
            "h" : np.zeros(self.default_size, dtype=np.float32),
            "l" : np.zeros(self.default_size, dtype=np.float32),

            # Vitesses
            "CAS" : np.zeros(self.default_size, dtype=np.float32),
            "TAS" : np.zeros(self.default_size, dtype=np.float32),
            "Mach" : np.zeros(self.default_size, dtype=np.float32),

            # Aérodynamique
            "Cz" : np.zeros(self.default_size, dtype=np.float32),
            "Cx" : np.zeros(self.default_size, dtype=np.float32),
            "f"  : np.zeros(self.default_size, dtype=np.float32),

            # Vitesses composantes
            "Vx" : np.zeros(self.default_size, dtype=np.float32),
            "Vz" : np.zeros(self.default_size, dtype=np.float32),

            # Propulsion
            "F_N" : np.zeros(self.default_size, dtype=np.float32),
            "SFC" : np.zeros(self.default_size, dtype=np.float32),
            "FF" : np.zeros(self.default_size, dtype=np.float32),

            # Masse / carburant
            "FB" : np.zeros(self.default_size, dtype=np.float32),
            "m" : np.zeros(self.default_size, dtype=np.float32),

            # Atmosphere
            "P" : np.zeros(self.default_size, dtype=np.float32),
            "T" : np.zeros(self.default_size, dtype=np.float32),
            "rho" : np.zeros(self.default_size, dtype=np.float32)
        }

        # Données de convergence simu
        self.data_simu = {
            # Précision
            "ecart_mission" : [],

            # Longueur descentes
            "l_descent" : [],
            "l_descent_diversion" : [],

            # Masse fuel mission
            "FB_mission" : []
        }

    
    def save(self, Avion: Avion, Atmosphere: Atmosphere, dt):
        '''
        Enregistre toutes les variables dynamiques contenues dans les deux classes.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        self.data["t"][self.counter] = self.data["t"][self.counter - 1] + dt if self.counter > 1 else 0

        self.data["h"][self.counter] = Avion.geth()
        self.data["l"][self.counter] = Avion.getl()

        self.data["CAS"][self.counter] = Avion.Aero.getCAS()
        self.data["TAS"][self.counter] = Avion.Aero.getTAS()
        self.data["Mach"][self.counter] = Avion.Aero.getMach()

        self.data["Cz"][self.counter] = Avion.Aero.getCz()
        self.data["Cx"][self.counter] = Avion.Aero.getCx()
        self.data["f"][self.counter]  = Avion.Aero.getCz() / Avion.Aero.getCx()

        self.data["F_N"][self.counter] = Avion.Moteur.getF()
        self.data["SFC"][self.counter] = Avion.Moteur.getSFC()
        self.data["FF"][self.counter] = Avion.Moteur.getFF()

        self.data["FB"][self.counter] = Avion.Masse.getFuelBurned()
        self.data["m"][self.counter] = Avion.Masse.getCurrentMass()

        self.data["P"][self.counter] = Atmosphere.getP_t()
        self.data["T"][self.counter] = Atmosphere.getT_t()
        self.data["rho"][self.counter] = Atmosphere.getRho_t()

        self.counter += 1
        
        if self.counter >= len(self.data["t"]):
            self.extend()


    def save_simu(self, Avion: Avion, ecart_mission):
        '''
        Enregistre les données de performance de la boucle (l'écart de précision,
        les longueurs de descente et la masse de fuel brulée pour la mission).
        
        :param Avion: Instance de la classe Avion
        :param ecart_mission: Ecart relatif sur le fuel burn mission (%)
        '''
        self.data_simu["ecart_mission"].append(ecart_mission)
        self.data_simu["l_descent"].append(Avion.getl_descent())
        self.data_simu["l_descent_diversion"].append(Avion.getl_descent_diversion())
        self.data_simu["FB_mission"].append(Avion.Masse.getFuelMission())


    def extend(self):
        '''
        Rajoute des 0 à la fin des tableaux pré-alloués si ceux-ci sont remplis.
        '''
        for key in self.data:
            self.data[key] = np.concatenate([
                self.data[key],
                np.zeros(self.default_size, dtype=np.float32)
            ])

    def cut(self):
        '''
        Enlève toutes les valeurs non atteintes après le counter.
        '''
        for key in self.data:
            self.data[key] = self.data[key][:self.counter]


    def reset(self):
        '''
        Remet tous les tableaux à zéro.
        '''
        self.counter = 0
        for key in self.data:
            self.data[key] = np.zeros(self.default_size, dtype=np.float32)