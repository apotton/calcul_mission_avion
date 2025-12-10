import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Cette ligne ajoute le dossier parent au chemin de recherche de Python

import numpy as np
from constantes.constantes import Constantes

class Atmosphere:

    # Constantes SI (m, K, Pa)
    T0_K = 288.15        # Température de référence au niveau de la mer (K)
    p0_Pa = 101325.0      # Pression de référence au niveau de la mer (Pa)
    Th_Kparm = -0.0065       # Gradient thermique troposphérique standard (K/m)
    r = 287.05287    # Constante spécifique des gaz pour l'air (J/(kg*K))
    
    # Constantes de Conversion
    conv_fttom = 0.3048   # Facteur de conversion : 1 pied = 0.3048 mètre
    DISA=0
    #DISA=np.interp(d,distance_NM_ligne*Constantes.conv_NM_m,DISA_ligne)

    def getRhoPT(self, h_m) :
        if h_m <= 11000:
            # --- Troposphère (Altitude à gradient constant : h <= 11000 m) ---
            
            # Température (T = T0 + T_h*h + DISA)
            T = self.T0_K + self.Th_Kparm * h_m + self.DISA
            
            # Pression (Formule de pression pour gradient constant)
            exponent_p = -Constantes.g / (self.r * self.Th_Kparm)
            p = self.p0_Pa * (1 + self.Th_Kparm / self.T0_K * h_m) ** exponent_p 
            
            
        else:
            # --- Stratosphère Isotherme (Altitude au-dessus de 11000 m) ---
            # 1. Calcul des conditions de transition à 11 km (sans DISA)
            T_11_ISA_0 = self.T0_K + self.Th_Kparm * 11000 
            p_11 = self.p0_Pa * (1 + self.Th_Kparm / self.T0_K * 11000) ** (-Constantes.g / (self.r * self.Th_Kparm))
            
            # 2. Calcul des conditions actuelles (T est constante au-dessus de 11 km, corrigée par DISA)
            T = T_11_ISA_0 + self.DISA
            
            # Pression (Formule de pression pour couche isotherme)
            exponent_p_strato = -Constantes.g / (self.r * T_11_ISA_0) * (h_m - 11000)
            p = p_11 * np.exp(exponent_p_strato)
            
        # Densité (Loi des gaz parfaits)
        rho = p / (self.r * T)

        return rho,p,T

