from moteurs.ElodieRoux.DonneesMoteur import DonneesMoteur
import numpy as np

"""
Fichier de données moteur converti depuis MATLAB.
Contient les tables de performances (Fn, SFC, FF) pour les phases:
- MCL (Max Climb)
- FI (Flight Idle)
- CRL (Cruise Loop)
- Holding
"""

def load():
    # Paramètres moteur
    OPR = 26 # Overall pressure ratio
    BPR = 5.7 # Bypass ratio
    F0  = 93150. # Poussée max au décollage
    T4  = 1500. # Température en sortie de combustion (K)
    dT4_climb = -50. # Delta de température en montée (K)
    dT4_cruise = -90. # Delta de température en croisière (K)
    h_opt = 10_668. # Altitude optimale de design moteur (m)

    # Niveaux de poussée: 7%, 30%, 85%, 100%
    # fuel_flow_ref = [FF_idle, FF_app, FF_co, FF_to] # En kg/s

    # Source: https://www.easa.europa.eu/en/domains/environment/icao-aircraft-engine-emissions-databank
    fuel_flow_ref = np.array([0.1011, 0.3096, 0.9182, 1.1266], dtype=np.float32) # kg/s
    EI_HC_ref     = np.array([2.3090, 0.0611, 0.0244, 0.0289], dtype=np.float32) # g/kg
    EI_CO_ref     = np.array([34.017, 3.5900, 0.1944, 0.2778], dtype=np.float32) # g/kg
    EI_NOx_ref    = np.array([4.1622, 8.7222, 17.140, 21.808], dtype=np.float32) # g/kg
    EI_nvPM_Mass  = np.array([0.791,  1.543,  42.275, 61.413], dtype=np.float32)/1000 # g/kg

    return DonneesMoteur(OPR, BPR, F0, T4, dT4_climb, dT4_cruise, h_opt,
                        fuel_flow_ref,
                        EI_HC_ref,
                        EI_CO_ref,
                        EI_NOx_ref,
                        EI_nvPM_Mass)





