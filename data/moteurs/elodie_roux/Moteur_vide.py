from moteurs.ElodieRoux.DonneesMoteur import DonneesMoteur
import numpy as np

"""
Fichier de données moteur converti depuis MATLAB.
Contient les tables de performances (Fn, SFC, FF) pour les phases:
- MCL (Max Climb)
- FI (Flight Idle)
- CRL (Cruise Loop)
- Holding
Préférer les np.ascontiguousarray(..., dtype=np.float64)
"""

def load():

    # Paramètres moteur
    OPR = 0. # Overall pressure ratio
    BPR = 0. # Bypass ratio
    F0  = 0. # Poussée max au décollage
    T4  = 0. # Température en sortie de combustion (K)
    dT4_climb = 0. # Delta de température en montée (K)
    dT4_cruise = 0. # Delta de température en croisière (K)
    h_opt = 0. # Altitude optimale de design moteur (m)

    # ==============================================================================
    # DONNÉES D'ÉMISSIONS DE POLLUANTS
    # ==============================================================================

    # Source: https://www.easa.europa.eu/en/domains/environment/icao-aircraft-engine-emissions-databank
    # Les tableaux doivent être de la même forme: [X_idle, X_app, X_co, X_to] (ordre croissant de puissance moteur)

    # Niveaux de poussée approximatifs: 7%, 30%, 85%, 100%
    # fuel_flow_ref = [FF_idle, FF_app, FF_co, FF_to] # En kg/s
    fuel_flow_ref = 0 # kg/s
    # Emissions d'hydrocarbures non brulés
    EI_HC_ref     = 0 # g/kg
    # Emissions de monoxyde de carbone
    EI_CO_ref     = 0 # g/kg
    # Emissions d'oxydes d'azote
    EI_NOx_ref    = 0 # g/kg
    # Emissions de non-volatile particulate matter (attention à ne pas mettre en mg/kg)
    EI_nvPM_Mass  = 0 # g/kg

    return DonneesMoteur(OPR, BPR, F0, T4, 
                         dT4_climb, dT4_cruise, h_opt,
                         fuel_flow_ref,
                         EI_HC_ref,
                         EI_CO_ref,
                         EI_NOx_ref,
                         EI_nvPM_Mass)
