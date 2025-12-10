import numpy as np

class Atmosphere:

    # Constantes SI (m, K, Pa)
    T0_K = 288.15        # Température de référence au niveau de la mer (K)
    p0_Pa = 101325.0      # Pression de référence au niveau de la mer (Pa)
    Th_Kparm = -0.0065       # Gradient thermique troposphérique standard (K/m)
    g = 9.80665         # Accélération de la gravité (m/s^2)
    r_JparKgK = 287.05287    # Constante spécifique des gaz pour l'air (J/(kg*K))
    
    # Constantes de Conversion
    conv_fttom = 0.3048   # Facteur de conversion : 1 pied = 0.3048 mètre
    DISA=0
    #DISA=np.interp(distance_NM_ligne*conv_NM_m,DISA_ligne,d)

    def getRhoPT(h_m) :
        if h_m <= 11000:
            # --- Troposphère (Altitude à gradient constant : h <= 11000 m) ---
            
            # Température (T = T0 + T_h*h + DISA)
            T = T0_K + Th_Kparm * h_m + DISA
            
            # Pression (Formule de pression pour gradient constant)
            exponent_p = -g / (r_JparKgK * Th_Kparm)
            p = p0_Pa * (1 + Th_Kparm / T0_K * h_m) ** exponent_p 
            
            # Densité (Loi des gaz parfaits : rho = p/(R*T))
            rho = p / (r_JparKgK * T)
            
        else:
            # --- Stratosphère Isotherme (Altitude au-dessus de 11000 m) ---
            # 1. Calcul des conditions de transition à 11 km (sans DISA)
            T_11_ISA_0 = T0_K + Th_Kparm * 11000 
            p_11 = p0_Pa * (1 + Th_Kparm / T0_K * 11000) ** (-g / (r_JparKgK * Th_Kparm))
            
            # 2. Calcul des conditions actuelles (T est constante au-dessus de 11 km, corrigée par DISA)
            T = T_11_ISA_0 + DISA
            
            # Pression (Formule de pression pour couche isotherme)
            exponent_p_strato = -g / (r_JparKgK * T_11_ISA_0) * (h_m - 11000)
            p = p_11 * np.exp(exponent_p_strato)
            
            # Densité (Loi des gaz parfaits)
            rho = p / (r_JparKgK * T)

