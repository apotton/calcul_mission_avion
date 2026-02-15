from atmosphere.Atmosphere import Atmosphere
from avions.Avion import Avion
import numpy as np


class Enregistrement:
    default_size = 10000  # Taille par défaut des tableaux numpy

    # Compteur (pour la taille à chaque changement)
    counter = 0

    data = {
        # Cinématique
        "t" : np.zeros(default_size, dtype=np.float32),
        "h" : np.zeros(default_size, dtype=np.float32),
        "l" : np.zeros(default_size, dtype=np.float32),

        # Vitesses
        "CAS" : np.zeros(default_size, dtype=np.float32),
        "TAS" : np.zeros(default_size, dtype=np.float32),
        "Mach" : np.zeros(default_size, dtype=np.float32),

        # Aérodynamique
        "Cz" : np.zeros(default_size, dtype=np.float32),
        "Cx" : np.zeros(default_size, dtype=np.float32),

        # Vitesses composantes
        "Vx" : np.zeros(default_size, dtype=np.float32),
        "Vz" : np.zeros(default_size, dtype=np.float32),

        # Propulsion
        "F_N" : np.zeros(default_size, dtype=np.float32),
        "SFC" : np.zeros(default_size, dtype=np.float32),

        # Masse / carburant
        "FB" : np.zeros(default_size, dtype=np.float32),
        "m" : np.zeros(default_size, dtype=np.float32),

        # Atmosphere
        "P" : np.zeros(default_size, dtype=np.float32),
        "T" : np.zeros(default_size, dtype=np.float32),
        "rho" : np.zeros(default_size, dtype=np.float32)
    }

    # Données de convergence simu
    data_simu = {
        # Précision
        "ecart_mission" : [],

        # Longueur descentes
        "l_descent" : [],
        "l_descent_diversion" : [],

        # Masse fuel mission
        "FB_mission" : []
    }

    @staticmethod
    def save(Avion: Avion, Atmosphere: Atmosphere, dt):
        Enregistrement.data["t"][Enregistrement.counter] = Enregistrement.data["t"][Enregistrement.counter - 1] + dt if Enregistrement.counter > 1 else 0

        Enregistrement.data["h"][Enregistrement.counter] = Avion.geth()
        Enregistrement.data["l"][Enregistrement.counter] = Avion.getl()

        Enregistrement.data["CAS"][Enregistrement.counter] = Avion.Aero.getCAS()
        Enregistrement.data["TAS"][Enregistrement.counter] = Avion.Aero.getTAS()
        Enregistrement.data["Mach"][Enregistrement.counter] = Avion.Aero.getMach()

        Enregistrement.data["Cz"][Enregistrement.counter] = Avion.Aero.getCz()
        Enregistrement.data["Cx"][Enregistrement.counter] = Avion.Aero.getCx()
        
        # Enregistrement.Vx.append(Avion.getVx())
        # Enregistrement.Vz.append(Avion.getVz())

        Enregistrement.data["F_N"][Enregistrement.counter] = Avion.Moteur.getF()
        Enregistrement.data["SFC"][Enregistrement.counter] = Avion.Moteur.getSFC()

        Enregistrement.data["FB"][Enregistrement.counter] = Avion.Masse.getFuelBurned()
        Enregistrement.data["m"][Enregistrement.counter] = Avion.Masse.getCurrentMass()

        Enregistrement.data["P"][Enregistrement.counter] = Atmosphere.getP_t()
        Enregistrement.data["T"][Enregistrement.counter] = Atmosphere.getT_t()
        Enregistrement.data["rho"][Enregistrement.counter] = Atmosphere.getRho_t()

        Enregistrement.counter += 1
        
        if Enregistrement.counter >= len(Enregistrement.data["t"]):
            Enregistrement.extend()

    @staticmethod
    def save_simu(Avion: Avion, ecart_mission):
        Enregistrement.data_simu["ecart_mission"].append(ecart_mission)
        Enregistrement.data_simu["l_descent"].append(Avion.getl_descent())
        Enregistrement.data_simu["l_descent_diversion"].append(Avion.getl_descent_diversion())
        Enregistrement.data_simu["FB_mission"].append(Avion.Masse.getFuelMission())

    @staticmethod
    def extend():
        for key in Enregistrement.data:
            Enregistrement.data[key] = np.concatenate([
                Enregistrement.data[key],
                np.zeros(Enregistrement.default_size, dtype=np.float32)
            ])

    @staticmethod
    def cut():
        # Enlève tout à partir du dernier ajout (counter)

        for key in Enregistrement.data:
            Enregistrement.data[key] = Enregistrement.data[key][:Enregistrement.counter]

    @staticmethod
    def reset():
        Enregistrement.counter = 0
        for key in Enregistrement.data:
            Enregistrement.data[key] = np.zeros(Enregistrement.default_size, dtype=np.float32)