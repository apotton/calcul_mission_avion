from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
import numpy as np

class Atmosphere:

    # Constantes SI (m, K, Pa)
    T0_K = 288.15           # Température de référence au niveau de la mer (K)
    p0_Pa = 101325.0        # Pression de référence au niveau de la mer (Pa)
    Th_Kparm = -0.0065      # Gradient thermique troposphérique standard (K/m)
    r = 287.05287           # Constante spécifique des gaz pour l'air (J/(kg*K))

    # Constantes dans le calcul ISA
    T_11_ISA = T0_K + Th_Kparm * 11000 
    exponent_p = -Constantes.g / (r * Th_Kparm)
    p_11 = p0_Pa * (1 + Th_Kparm / T0_K * 11000) ** (-Constantes.g / (r * Th_Kparm))


    def __init__(self, Inputs: Inputs):
        '''
        Initialise une instance de l'atmosphère standard au niveau de la mer
        
        :param self: Instance de la classe Atmosphère
        '''
        self.rho_t = 1.225  # Densité standard au niveau de la mer (kg/m^3)
        self.P_t = 101325.0 # Pression standard au niveau de la mer (Pa)
        self.T_t = 288.15   # Température standard au niveau de la mer (K)

        self.DISA_sub_Cruise = Inputs.DISA_sub_Cruise
        self.DISA_Cruise = Inputs.DISA_Cruise
        self.hCruise = Inputs.hCruise_ft * Constantes.conv_ft_m

        self.w = [] # Humidité spécifique (kg eau / kg air sec)
        self.e_Pa = [] # Pression partielle de vapeur d'eau

    def calculateRhoPT(self, h, DISA_dC = 0.) :
        '''
        Calcule les conditions atmosphériques (rho, P, T) en unités SI d'un avion, en prenant en compte l'écart avec l'atmosphère standard.
        
        :param self: Instance de la classe Atmosphere
        :param h_m: Altitude de l'avion (m)
        :param DISA_dC: Différence de température avec l'atmosphère standard, utilisée pour le point performance (°C)
        '''
        # Calcul du dISA
        if h < self.hCruise:
            DISA = self.DISA_sub_Cruise + DISA_dC
        else:
            DISA = self.DISA_Cruise + DISA_dC

        # Calculs de température et pression
        if h <= 11000:
            # Troposphère (Altitude à gradient constant : h <= 11000 m)
            # Température (T = T0 + T_h*h + DISA)
            T_ISA = self.T0_K + self.Th_Kparm * h
            self.T_t = T_ISA + DISA
            
            # Pression (Formule de pression pour gradient constant)
            self.P_t = self.p0_Pa * (1 + self.Th_Kparm / self.T0_K * h) ** self.exponent_p             
        else:
            # Stratosphère Isotherme (Altitude au-dessus de 11000 m)
            # Calcul des conditions actuelles (T est constante au-dessus de 11 km, corrigée par DISA)
            self.T_t = self.T_11_ISA + DISA
            
            # Pression (Formule de pression pour couche isotherme)
            exponent_p_strato = -Constantes.g / (self.r * self.T_11_ISA) * (h - 11000)
            self.P_t = self.p_11 * np.exp(exponent_p_strato)
        
        # Densité (Loi des gaz parfaits)
        self.rho_t = self.P_t / (self.r * self.T_t)

    @staticmethod
    def RelativeHumidity(h):
        return 0.6 * np.exp(-h / 2000) # Modèle simplifié d'humidité relative

    def calculateHumidity(self, Enregistrement):
        '''
        Détermine les pressions partielles, saturantes et l'humidité spécifique de l'air.

        :param Enregistrement: Instance de la classe enregistrement 
        '''
        # Calcul de la pression saturante (formule de Murphy & Koop)
        es_Pa = self.calculateLiquidMurphyKoop(Enregistrement.data["T"])
        RH_h = self.RelativeHumidity(Enregistrement.data["h"])
        self.e_Pa = RH_h * es_Pa # Pression partielle vapeur
        self.w = 0.622 * self.e_Pa / (Enregistrement.data["P"] - self.e_Pa) # kg eau / kg air sec

    @staticmethod
    def calculateLiquidMurphyKoop(T_K):
        """
        Calcule la pression de vapeur saturante de l'eau liquide (Pa) 
        selon Murphy & Koop (2005).

        :param T_K: Array de températures (en Kelvins)
        :return es: La pression de vapeur saturante de l'eau liquide (en Pa)
        """
        # Calcul des différents termes
        term_main = 54.842763 - 6763.22 / T_K - 4.210 * np.log(T_K) + 0.000367 * T_K
        term_tanh = np.tanh(0.0415 * (T_K - 218.8))
        term_sub = 53.878 - 1331.22 / T_K - 9.44523 * np.log(T_K) + 0.014025 * T_K
        
        ln_es = term_main + term_tanh * term_sub
        return np.exp(ln_es)
    
    @staticmethod
    def calculate_T_LC_murphy_koop(G_array):
        """
        Trouve T_LC en utilisant Newton-Raphson avec dérivée numérique.
        """
        G = np.asarray(G_array)
        
        # Initialisation de la température (guess) à -40°C (233.15 K)
        T = np.full_like(G, 233.15, dtype=float)
        
        # Epsilon pour le calcul de la dérivée numérique (ex: 0.0001 K)
        eps = 1e-4 
        
        # 8 itérations suffisent largement avec cette méthode
        for _ in range(8):
            # Calcul de e_s aux points T, T+eps et T-eps
            es_center = Atmosphere.calculateLiquidMurphyKoop(T)
            es_plus   = Atmosphere.calculateLiquidMurphyKoop(T + eps)
            es_minus  = Atmosphere.calculateLiquidMurphyKoop(T - eps)
            
            # Dérivée première numérique : f'(T) = d(es)/dT
            d_es_dT = (es_plus - es_minus) / (2 * eps)
            
            # Dérivée seconde numérique : f''(T) = d2(es)/dT2
            d2_es_dT2 = (es_plus - 2 * es_center + es_minus) / (eps**2)
            
            # Fonction dont on cherche le zéro : F(T) = d_es_dT - G
            # On applique l'étape de Newton : T_new = T - F(T) / F'(T)
            F_T = d_es_dT - G
            T = T - F_T / d2_es_dT2
            
        return T
    
    def check_contrail_persistence(self, T_amb, e_amb):
        """
        T_amb : Température ambiante en Kelvin
        e_amb : Pression partielle de vapeur d'eau ambiante en Pascals (votre modèle météo)
        """
        # Formule de Murphy & Koop pour la GLACE
        self.es_ice_Pa = np.exp(9.550426 - 5723.265/T_amb + 3.53068 * np.log(T_amb) - 0.00728332*T_amb)
        
        # Persistance vraie si l'humidité relative par rapport à la glace est >= 100%
        persistence = e_amb >= self.es_ice_Pa
        
        return persistence

    def determineContrails(self, Enregistrement):
        # Efficacité du moteur
        eta = (Enregistrement.data["F"] * Enregistrement.data["TAS"] 
                / Enregistrement.data["FF"] / Constantes.Q )
        
        # Pente de mélange (dilution eau/chaleur dans l'atmosphère)
        G = (Constantes.EI_H2O * Constantes.Cp * Enregistrement.data["P"]
             / Constantes.epsilon / Constantes.Q / (1-eta) )

        T_LC = self.calculate_T_LC_murphy_koop(G)
        T_max = T_LC - (self.calculateLiquidMurphyKoop(T_LC) - self.e_Pa) / G

        # Formation de contrails
        print("")
        contrailsFormation = (Enregistrement.data["T"] < T_max)
        persistance = self.check_contrail_persistence(Enregistrement.data["T"], self.e_Pa) & contrailsFormation
        persistentContrailsTime = np.sum(np.diff(Enregistrement.data["t"]) * persistance[:-1])
        print(f"Contrails persistants formés pendant {persistentContrailsTime/60:.1f} minutes.")


    def setRho(self, Rho: float):
        '''
        Définit la masse volumique de l'air.
        
        :param Rho: masse volumique (kg/m^3)
        '''
        self.rho_t = Rho  

    def setP(self, P: float):
        '''
        Définit la pression de l'air.
        
        :param P: Pression statique (Pa)
        '''
        self.P_t = P   

    def setT(self, T: float):
        '''
        Définit la température de l'air.
        
        :param T: Température de l'air (K)
        '''
        self.T_t = T 

    def getRho(self):
        '''
        Renvoie la masse volumique de l'air précédemment calculée (kg/m^3)
        '''
        return self.rho_t
    
    def getP(self):
        '''
        Renvoie la pression statique de l'air précédemment calculée (Pa)
        '''
        return self.P_t
    
    def getT(self):
        '''
        Renvoie la température de l'air précédemment calculée (K)
        '''
        return self.T_t