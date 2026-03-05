from constantes.Constantes import Constantes
from moteurs.Moteur import Moteur
import numpy as np

class ElodieRoux(Moteur):
    def __init__(self, Avion):
        super().__init__(Avion)
        
        # ==========================================
        # PARAMÈTRES MOTEUR (Inputs globaux)
        # ==========================================
        self.BPR = getattr(self.Inputs, 'BPR', 5.0)
        self.OPR = getattr(self.Inputs, 'OPR', 30.0)
        self.FPR = getattr(self.Inputs, 'FPR', 1.5)
        
        # Nouveaux paramètres requis pour la poussée
        # Poussée statique au niveau de la mer (N)
        self.F_0 = getattr(self.Inputs, 'F0', 100000.0) 
        # Température d'entrée de turbine (K)
        self.T_41 = getattr(self.Inputs, 'T_41', 1400.0) 
        # Écart de température d'entrée de turbine par rapport au design (K)
        self.Delta_T41 = getattr(self.Inputs, 'Delta_T41', 0.0) 

        self.T_0 = 288.15 
        self.rho_0 = 1.225   # Densité standard au niveau de la mer (kg/m^3)
        self.rho_11 = 0.364  # Densité à 11000m (kg/m^3)

        # ==========================================
        # COEFFICIENTS SFC (Déjà implémentés précédemment)
        # ==========================================
        self.a1_tropo_1 = -7.44e-13
        self.a1_tropo_2 = 6.54e-7
        self.a2_tropo_1 = -3.32e-10
        self.a2_tropo_2 = 8.54e-6
        self.b1_tropo_1 = -3.47e-11
        self.b1_tropo_2 = -6.58e-7
        self.b2_tropo_1 = 4.23e-10
        self.b2_tropo_2 = 1.32e-5
        self.c_tropo = -1.05e-7
        
        self.a1_strato = self.a1_tropo_1 * 11000 + self.a1_tropo_2
        self.a2_strato = self.a2_tropo_1 * 11000 + self.a2_tropo_2
        self.b1_strato = self.b1_tropo_1 * 11000 + self.b1_tropo_2
        self.b2_strato = self.b2_tropo_1 * 11000 + self.b2_tropo_2
        self.c_strato  = self.c_tropo
        self.coef_SFC1 = 7.4e-13

        self.const_SFCmin = 0.998
        self.coef_alt_SFCmin = 0.0
        self.coef_mach_SFCmin = 0.0
        self.coef_alt_mach_SFCmin = 0.0
        self.coef_fpr_SFCmin = 0.0
        self.const_Fi = 0.85
        self.coef_alt_Fi = 0.0
        self.coef_mach_Fi = 0.0
        self.coef_alt_mach_Fi1 = 0.0
        self.coef_alt_mach_Fi2 = 0.0
        self.coef_fpr_Fi = 0.0

        # ==========================================
        # COEFFICIENTS F_MAX (Nouvellement ajoutés)
        # ==========================================
        self.a_Ms = -2.74e-4
        self.b_Ms = 1.91e-2
        self.c_Ms = 1.21e-3
        self.d_Ms = -8.48e-4
        self.e_Ms = 8.96e-1
        
        self.a_Fm = 2.67e-4
        self.b_Fm = -2.35e-2
        self.c_Fm = -1.32e-3
        self.d_Fm = 3.14e-4
        self.e_Fm = 5.22e-1

        self.alpha_1_fMs = 1.79e-12
        self.alpha_2_fMs = 4.29e-13
        self.alpha_3_fMs = -5.24e-14
        self.alpha_4_fMs = -4.51e-14
        self.alpha_5_fMs = -4.57e-12
        
        self.alpha_1_gMs = 1.17e-8
        self.alpha_2_gMs = -8.8e-8
        self.alpha_3_gMs = -5.25e-9
        self.alpha_4_gMs = -3.19e-9
        self.alpha_5_gMs = 5.52e-8

        self.alpha_1_fFm = -5.37e-13
        self.alpha_2_fFm = -1.26e-12
        self.alpha_3_fFm = -1.29e-14
        self.alpha_4_fFm = 2.39e-14
        self.alpha_5_fFm = 2.53e-12

        self.alpha_1_gFm = -3.18e-9
        self.alpha_2_gFm = 2.76e-8
        self.alpha_3_gFm = 1.97e-9
        self.alpha_4_gFm = 1.17e-9
        self.alpha_5_gFm = -2.26e-8

        self.beta_1_fMs = 1.7e-12
        self.beta_2_fMs = 1.51e-12
        self.beta_3_fMs = 1.48e-9
        self.beta_4_fMs = -7.59e-14
        self.beta_5_fMs = -1.07e-11

        self.beta_1_gMs = -3.48e-9
        self.beta_2_gMs = -8.41e-8
        self.beta_3_gMs = 2.56e-5
        self.beta_4_gMs = -2e-8
        self.beta_5_gMs = -7.17e-8

        self.beta_1_fFm = -3.89e-13
        self.beta_2_fFm = -2.05e-12
        self.beta_3_fFm = -9.28e-10
        self.beta_4_fFm = 1.3e-13
        self.beta_5_fFm = 5.39e-12

        self.beta_1_gFm = 1.77e-9
        self.beta_2_gFm = 2.62e-8
        self.beta_3_gFm = -8.87e-6
        self.beta_4_gFm = 6.66e-9
        self.beta_5_gFm = 4.43e-8

        self.coef1_R = -4.51e-3
        self.coef2_R = 2.19e-5
        self.coef3_R = -3.09e-4
        self.coef4_R = 0.945
        self.k_dtamb = 0.0


    def _get_F_max(self, mach, h_m):
        '''
        Traduction de la fonction MATLAB CalculateFmax(F_0, Mach, h).
        Calcule la poussée maximale disponible à une altitude et un Mach donnés.
        '''
        # Récupération de la densité atmosphérique
        if hasattr(self.Avion.Atmosphere, 'getRho'):
            rho = self.Avion.Atmosphere.getRho()
        else:
            # Modèle ISA simplifié en cas d'absence
            T = 288.15 - 0.0065 * h_m if h_m <= 11000 else 216.65
            p = 101325 * (T / 288.15)**5.25588 if h_m <= 11000 else 22632 * np.exp(-9.81 * (h_m - 11000) / (287.05 * 216.65))
            rho = p / (287.05 * T)

        # --- Détermination de la forme d'évolution (f et g) ---
        opr_term = self.OPR - 30
        
        # Polynomes f_M_s et g_M_s
        f_M_s = (self.alpha_1_fMs * opr_term**2 + self.alpha_2_fMs * opr_term + self.alpha_3_fMs + self.alpha_4_fMs * self.T_41 + self.alpha_5_fMs * self.Delta_T41) * self.BPR + \
                (self.beta_1_fMs * opr_term**2 + self.beta_2_fMs * opr_term + self.beta_3_fMs + self.beta_4_fMs * self.T_41 + self.beta_5_fMs * self.Delta_T41)
        
        g_M_s = (self.alpha_1_gMs * opr_term**2 + self.alpha_2_gMs * opr_term + self.alpha_3_gMs + self.alpha_4_gMs * self.T_41 + self.alpha_5_gMs * self.Delta_T41) * self.BPR + \
                (self.beta_1_gMs * opr_term**2 + self.beta_2_gMs * opr_term + self.beta_3_gMs + self.beta_4_gMs * self.T_41 + self.beta_5_gMs * self.Delta_T41)
        
        # Polynomes f_F_m et g_F_m
        f_F_m = (self.alpha_1_fFm * opr_term**2 + self.alpha_2_fFm * opr_term + self.alpha_3_fFm + self.alpha_4_fFm * self.T_41 + self.alpha_5_fFm * self.Delta_T41) * self.BPR + \
                (self.beta_1_fFm * opr_term**2 + self.beta_2_fFm * opr_term + self.beta_3_fFm + self.beta_4_fFm * self.T_41 + self.beta_5_fFm * self.Delta_T41)
        
        g_F_m = (self.alpha_1_gFm * opr_term**2 + self.alpha_2_gFm * opr_term + self.alpha_3_gFm + self.alpha_4_gFm * self.T_41 + self.alpha_5_gFm * self.Delta_T41) * self.BPR + \
                (self.beta_1_gFm * opr_term**2 + self.beta_2_gFm * opr_term + self.beta_3_gFm + self.beta_4_gFm * self.T_41 + self.beta_5_gFm * self.Delta_T41)

        # Points de référence à 11000m
        Mach_s_11 = self.a_Ms * self.T_41 + self.b_Ms * self.BPR + self.c_Ms * opr_term + self.d_Ms * self.Delta_T41 + self.e_Ms
        F_m_11 = self.a_Fm * self.T_41 + self.b_Fm * self.BPR + self.c_Fm * opr_term + self.d_Fm * self.Delta_T41 + self.e_Fm

        # --- Extrapolation parabolique selon l'altitude ---
        if h_m <= 11000:
            dh = h_m - 11000
            Mach_s = Mach_s_11 + f_M_s * (dh**2) + g_M_s * dh
            F_m = F_m_11 + f_F_m * (dh**2) + g_F_m * dh
        else:
            Mach_s = Mach_s_11
            F_m = F_m_11

        # --- Facteur d'effet du Mach (Q_M) ---
        alpha = (1 - F_m) / (Mach_s**2 if Mach_s != 0 else 1e-6)
        Q_M = alpha * (mach - Mach_s)**2 + F_m

        # --- Facteur d'effet de l'altitude / Densité (Q_h) ---
        k = 1 + 1.2e-3 * self.Delta_T41
        n = 0.98 + 8e-4 * self.Delta_T41
        
        if h_m <= 11000:
            # Correction par un terme sinusoïdal dans la troposphère
            correction = 1 - 0.04 * np.sin(np.pi * h_m / 11000)
            Q_h = k * (rho / self.rho_0)**n / correction
        else:
            # Loi exponentielle de la stratosphère
            Q_h = k * (self.rho_11 / self.rho_0)**n * (rho / self.rho_11)

        # --- Facteur résiduel (Q_R) ---
        Q_R = self.coef1_R * self.BPR + self.coef2_R * self.T_41 + self.coef3_R * opr_term + self.coef4_R + self.k_dtamb * self.Delta_T41

        # --- Assemblage F_max final ---
        F_max = self.F_0 * Q_M * Q_h * Q_R
        
        # Sécurité pour éviter des poussées irréalistes (ou négatives)
        return max(F_max, 100.0)


    def _calculer_SFC_analytique(self):
        ''' Cœur du calcul de SFC vu précédemment. '''
        h_m = self.Avion.geth()
        mach = self.Avion.Aero.getMach()
        F_actuelle = self.F_t
        
        if hasattr(self.Avion.Atmosphere, 'getT'):
            T = self.Avion.Atmosphere.getT()
        else:
            T = 288.15 - 0.0065 * h_m if h_m <= 11000 else 216.65

        F_max = self._get_F_max(mach, h_m)

        if h_m <= 11000:
            a_1 = self.a1_tropo_1 * h_m + self.a1_tropo_2
            a_2 = self.a2_tropo_1 * h_m + self.a2_tropo_2
            b_1 = self.b1_tropo_1 * h_m + self.b1_tropo_2
            b_2 = self.b2_tropo_1 * h_m + self.b2_tropo_2
            c   = self.c_tropo
        else:
            a_1, a_2, b_1, b_2, c = self.a1_strato, self.a2_strato, self.b1_strato, self.b2_strato, self.c_strato

        SFC_CLB = ((a_1 * self.BPR + a_2) * mach + 
                   (b_1 * self.BPR + b_2) * np.sqrt(T / self.T_0) + 
                   (self.coef_SFC1 * (self.OPR - 30) * h_m + c) * (self.OPR - 30))

        F_i = (self.coef_alt_Fi * h_m + self.const_Fi + self.coef_fpr_Fi * self.FPR + 
               self.coef_mach_Fi * mach + self.coef_alt_mach_Fi1 * mach * h_m + 
               self.coef_alt_mach_Fi2 * mach * (h_m ** 1.1))

        SFC_reduced_min = (self.coef_alt_SFCmin * h_m + self.const_SFCmin + 
                           self.coef_fpr_SFCmin * self.FPR + self.coef_mach_SFCmin * mach + 
                           self.coef_alt_mach_SFCmin * mach * h_m)

        ratio_poussee = F_actuelle / F_max
        denominateur = (1 - F_i) if (1 - F_i) != 0 else 1e-6
        SFC_reduced = (1 - SFC_reduced_min) * ((ratio_poussee - F_i) / denominateur)**2 + SFC_reduced_min

        return SFC_reduced * SFC_CLB

    # ==========================================
    # MÉTHODES D'INTERFACE POUR LA POUSSÉE (F)
    # ==========================================

    def calculateFClimb(self):
        '''
        Poussée maximale en montée.
        Utilise F_max du modèle analytique pondéré par le coefficient de l'avion.
        '''
        mach = self.Avion.Aero.getMach()
        h_m = self.Avion.geth()
        
        # Le modèle d'Elodie Roux donne la poussée max possible
        F_max = self._get_F_max(mach, h_m)
        
        # On applique le pourcentage alloué pour le Climb (ex: 100% ou 90% selon self.Inputs.cF_climb)
        # Et on gère le bimoteur (si F_0 était pour un moteur, on multiplie par le nbr de moteurs)
        self.F_t = F_max * getattr(self.Inputs, 'cF_climb', 1.0) * getattr(self.Inputs, 'nb_moteurs', 2)

    def calculateFCruise(self):
        '''
        En croisière, la poussée équilibre simplement la traînée.
        '''
        Cz = self.Avion.Aero.getCz()
        Cx = self.Avion.Aero.getCx()
        finesse = Cz / Cx if Cx != 0 else 1.0
        # Poussée TOTALE requise par l'avion
        self.F_t = self.Avion.Masse.getCurrentWeight() / finesse

    def calculateFDescent(self):
        '''
        Poussée de descente. Souvent idle (ralenti).
        '''
        mach = self.Avion.Aero.getMach()
        h_m = self.Avion.geth()
        F_max = self._get_F_max(mach, h_m)
        
        # En descente, on utilise un coefficient très bas (ex: 5% ou 10% de F_max)
        self.F_t = F_max * getattr(self.Inputs, 'cF_descent', 0.1) * getattr(self.Inputs, 'nb_moteurs', 2)

    def calculateFHolding(self):
        ''' Identique à la croisière. '''
        self.calculateFCruise()

    def calculateFCruiseDiversion(self):
        ''' Identique à la croisière. '''
        self.calculateFCruise()

    # ==========================================
    # MÉTHODES D'INTERFACE POUR LA SFC ET LE FF
    # ==========================================

    def calculateSFCCruise(self):
        self.SFC_t = self._calculer_SFC_analytique() * getattr(self.Inputs, 'cFF_cruise', 1.0)
        self.FF_t = self.SFC_t * self.F_t

    def calculateSFCClimb(self):
        self.SFC_t = self._calculer_SFC_analytique() * getattr(self.Inputs, 'cFF_climb', 1.0)
        self.FF_t = self.SFC_t * self.F_t

    def calculateSFCDescent(self):
        self.SFC_t = self._calculer_SFC_analytique() * getattr(self.Inputs, 'cFF_descent', 1.0)
        self.FF_t = self.SFC_t * self.F_t
        if abs(self.SFC_t) > 1e-4:  
            self.SFC_t = 0
            self.FF_t = 0

    def calculateSFCHolding(self):
        self.SFC_t = self._calculer_SFC_analytique() * getattr(self.Inputs, 'cFF_cruise', 1.0)
        self.FF_t = self.SFC_t * self.F_t

    def calculateSFCCruiseDiversion(self):
        self.calculateSFCCruise()