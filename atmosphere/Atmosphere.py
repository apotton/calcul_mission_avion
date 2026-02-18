from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
import numpy as np

class Atmosphere:

    # Constantes SI (m, K, Pa)
    T0_K = 288.15           # Température de référence au niveau de la mer (K)
    p0_Pa = 101325.0        # Pression de référence au niveau de la mer (Pa)
    Th_Kparm = -0.0065      # Gradient thermique troposphérique standard (K/m)
    r = 287.05287           # Constante spécifique des gaz pour l'air (J/(kg*K))
    
    # Constantes de Conversion
    conv_fttom = 0.3048     # Facteur de conversion : 1 pied = 0.3048 mètre

    def __init__(self):
        '''
        Initialise une instance de l'atmosphère standard au niveau de la mer
        
        :param self: Instance de la classe Atmosphère
        '''
        self.rho_t = 1.225  # Densité standard au niveau de la mer (kg/m^3)
        self.P_t = 101325.0 # Pression standard au niveau de la mer (Pa)
        self.T_t = 288.15   # Température standard au niveau de la mer (K)
        self.Vwind_t = Inputs.Vw*Constantes.conv_kt_mps  # Vitesse du vent à l'altitude t (m/s)

    def CalculateRhoPT(self, h_m, DISA_dC = 0) :
        '''
        Calcule les conditions atmosphériques (rho, P, T) en unités SI d'un avion, en prenant en compte l'écart avec l'atmosphère standard.
        
        :param self: Instance de la classe Atmosphere
        :param h_m: Altitude de l'avion (m)
        :param DISA_dC: Différence de température avec l'atmosphère standard, utilisée pour le point performance
        '''
        if h_m < Inputs.h_cruise_init:
            DISA = Inputs.DISA_sub_Cruise + DISA_dC
        else:
            DISA = Inputs.DISA_Cruise + DISA_dC

            
        if h_m <= 11000:
            # Troposphère (Altitude à gradient constant : h <= 11000 m)
            
            # Température (T = T0 + T_h*h + DISA)
            T = self.T0_K + self.Th_Kparm * h_m + DISA
            
            # Pression (Formule de pression pour gradient constant)
            exponent_p = -Constantes.g / (self.r * self.Th_Kparm)
            p = self.p0_Pa * (1 + self.Th_Kparm / self.T0_K * h_m) ** exponent_p 
            
            
        else:
            # Stratosphère Isotherme (Altitude au-dessus de 11000 m)
            # Calcul des conditions de transition à 11 km (sans DISA)
            T_11_ISA_0 = self.T0_K + self.Th_Kparm * 11000 
            p_11 = self.p0_Pa * (1 + self.Th_Kparm / self.T0_K * 11000) ** (-Constantes.g / (self.r * self.Th_Kparm))
            
            # Calcul des conditions actuelles (T est constante au-dessus de 11 km, corrigée par DISA)
            T = T_11_ISA_0 + DISA
            
            # Pression (Formule de pression pour couche isotherme)
            exponent_p_strato = -Constantes.g / (self.r * T_11_ISA_0) * (h_m - 11000)
            p = p_11 * np.exp(exponent_p_strato)
            
        # Densité (Loi des gaz parfaits)
        rho = p / (self.r * T)

        self.rho_t = rho
        self.P_t = p
        self.T_t = T

    def setRho(self, Rho: float):
        '''
        Définit la masse volumique de l'air.
        
        :param self: Instance de la classe Atmosphère
        :param Rho: masse volumique (kg/m^3)
        '''
        self.rho_t = Rho  

    def setP(self, P: float):
        '''
        Définit la pression de l'air.
        
        :param self: Instance de la classe Atmosphère
        :param P: Pression statique (Pa)
        '''
        self.P_t = P   

    def setT(self, T: float):
        '''
        Définit la température de l'air.
        
        :param self: Instance de la classe Atmosphère
        :param T: Température de l'air (K)
        '''
        self.T_t = T 

    def getRho_t(self):
        '''
        Renvoie la masse volumique de l'air précédemment calculée (kg/m^3)
        
        :param self: Instance de la classe Atmosphère
        '''
        return self.rho_t
    
    def getP_t(self):
        '''
        Renvoie la pression statique de l'air précédemment calculée (Pa)
        
        :param self: Instance de la classe Atmosphère
        '''
        return self.P_t
    
    def getT_t(self):
        '''
        Renvoie la température de l'air précédemment calculée (K)
        
        :param self: Instance de la classe Atmosphère
        '''
        return self.T_t

    def getVwind(self):
        '''
        Renvoie la vitesse du vent (m/s)
        
        :param self: Instance de la classe Atmosphère
        '''
        return self.Vwind_t