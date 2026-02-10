import numpy as np
from moteurs.DonneesMoteur import DonneesMoteur

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

    # Vecteurs d'entrée pour les interpolations principales
    mach_table = 0
    

    alt_table_ft = 0


    # ==============================================================================
    # TABLES GÉNÉRALES (MCL & FI)
    # ==============================================================================
    # Définition du tableau Fn_MCL_table sous forme de numpy array
    Fn_MCL_table = 0



    Fn_FI_table = 0



    # Définition du tableau SFC_MCL_table sous forme de numpy array
    SFC_MCL_table = 0


    # Définition du tableau FF_FI_table sous forme de numpy array
    FF_FI_table = 0



# ==============================================================================
# DONNÉES DE CROISIÈRE (CRUISE LOOP)
# ==============================================================================

    mach_table_crl = 0

    # Dictionnaire structuré par altitude.
    # Format: { Altitude_ft : { 'fn': array_1D, 'sfc': array_2D } }
    cruise_data = {
        25000: {
            "fn": 0,
            "sfc": 0
        },
        30000: {
            "fn": 0,
            "sfc": 0
        },
        31000: {
            "fn": 0,
            "sfc": 0
        },
        32000: {
            "fn": 0,
            "sfc": 0
        },
        33000: {
            "fn": 0,
            "sfc": 0
        },
        34000: {
            "fn": 0,
            "sfc": 0
        },
        35000: {
            "fn": 0,
            "sfc": 0
        },
        36000: {
            "fn": 0,
            "sfc": 0
        },
        37000: {
            "fn": 0,
            "sfc": 0
        },
        38000: {
            "fn": 0,
            "sfc": 0
        },
        39000: {
            "fn": 0,
            "sfc": 0
        },
        40000: {
            "fn": 0,
            "sfc": 0
        },
        41000: {
            "fn": 0,
            "sfc": 0
        },
        42000: {
            "fn": 0,
            "sfc": 0
        }
    }

    # ==============================================================================
    # DONNÉES DE HOLDING (ATTENTE)
    # ==============================================================================

    mach_table_crl_holding = 0

    fn_lbf_crl_holding = 0

    sfc_crl_holding = 0

    return DonneesMoteur(mach_table,
                 alt_table_ft,
                 Fn_MCL_table,
                 Fn_FI_table,
                 SFC_MCL_table,
                 FF_FI_table,
                 mach_table_crl,
                 cruise_data,
                 mach_table_crl_holding,
                 fn_lbf_crl_holding,
                 sfc_crl_holding)
