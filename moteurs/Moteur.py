from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np


class Moteur:
    def __init__(self, BPR=0, OPR=0, Reseau_moteur=0):
        self.BPR = BPR        # Bypass ratio
        self.OPR = OPR        # Overall Pressure Ratio
        self.Reseau_moteur = Reseau_moteur  # choix du modèle
        self.F_T = 0            # Poussée actuelle (N)
        self.SFC_T = 0          # SFC actuelle (kg/(N.s))


    def CalculateSFC(F_max,F,T,Mach,h_m,self):
        
        # Modèle Elodie Roux

        if h_m<=11000 :
            a_1=Constantes.a1_troposphere_1*h_m+Constantes.a1_troposphere_2
            a_2=Constantes.a2_troposphere_1*h_m+Constantes.a2_troposphere_2
            b_1=Constantes.b1_troposphere_1*h_m+Constantes.b1_troposphere_2
            b_2=Constantes.b2_troposphere_1*h_m+Constantes.b2_troposphere_2
            c=Constantes.c_troposphere
        else :
            a_1=Constantes.a1_stratosphere
            a_2=Constantes.a2_stratosphere
            b_1=Constantes.b1_stratosphere
            b_2=Constantes.b2_stratosphere
            c=Constantes.c_stratosphere

        # Calcul de SFC_CLB
        SFC_CLB = ((a_1 * self.BPR + a_2) * Mach + (b_1 * self.BPR + b_2) * np.sqrt(T / Constantes.T0_K) + (Constantes.coef_SFC1 * (self.OPR - 30) * h_m + c) * (self.OPR - 30)) # *SFC_design/coef_SFC

        # Calcul de SFC_reduced_min
        SFC_reduced_min = Constantes.coef_alt_SFCmin * h_m + Constantes.const_SFCmin + Constantes.coef_fpr_SFCmin * self.FPR + Constantes.coef_mach_SFCmin * Mach + Constantes.coef_alt_mach_SFCmin * Mach * h_m

        # Calcul de F_i
        # Note : L'opérateur de puissance '^' en Matlab devient '**' en Python
        # (h).^1.1 devient h**1.1
        F_i = Constantes.coef_alt_Fi * h_m + Constantes.const_Fi + Constantes.coef_fpr_Fi * self.FPR + Constantes.coef_mach_Fi * Mach + Constantes.coef_alt_mach_Fi1 * Mach * h_m + Constantes.coef_alt_mach_Fi2 * Mach * (h_m**1.1)

        # Calcul de SFC_reduced
        SFC_reduced = (1 - SFC_reduced_min) * ((F / F_max - F_i) / (1 - F_i))**2 + SFC_reduced_min

        # Calcul final SFC
        SFC = SFC_reduced * SFC_CLB

        return

    def CalculateSFCbis(F_max,F,Mach,h_m,avion):
        h_ft=h_m/Constantes.conv_ft_m
        rho,p,T = Atmosphere.getRhoPT(avion, h_m)

        if Reseau_moteur == 1:
    
            # Sélection des données par bande d'altitude
            # Utilisation de parenthèses pour le saut de ligne et de & pour le ET logique vectoriel
            Fn_lbf_CRL = (
                Fn_lbf_CRL_30000 * ((h_ft < 30200) & (h_ft > 29800)) +
                Fn_lbf_CRL_31000 * ((h_ft < 31200) & (h_ft > 30800)) +
                Fn_lbf_CRL_32000 * ((h_ft < 32200) & (h_ft > 31800)) +
                Fn_lbf_CRL_33000 * ((h_ft < 33200) & (h_ft > 32800)) +
                Fn_lbf_CRL_34000 * ((h_ft < 34200) & (h_ft > 33800)) +
                Fn_lbf_CRL_35000 * ((h_ft < 35200) & (h_ft > 34800)) +
                Fn_lbf_CRL_36000 * ((h_ft < 36200) & (h_ft > 35800)) +
                Fn_lbf_CRL_37000 * ((h_ft < 37200) & (h_ft > 36800)) +
                Fn_lbf_CRL_38000 * ((h_ft < 38200) & (h_ft > 37800)) +
                Fn_lbf_CRL_39000 * ((h_ft < 39200) & (h_ft > 38800)) +
                Fn_lbf_CRL_40000 * ((h_ft < 40200) & (h_ft > 39800)) +
                Fn_lbf_CRL_41000 * ((h_ft < 41200) & (h_ft > 40800)) +
                Fn_lbf_CRL_42000 * ((h_ft < 42200) & (h_ft > 41800))
            )

            SFC_CRL = (
                SFC_CRL_30000 * ((h_ft < 30200) & (h_ft > 29800)) +
                SFC_CRL_31000 * ((h_ft < 31200) & (h_ft > 30800)) +
                SFC_CRL_32000 * ((h_ft < 32200) & (h_ft > 31800)) +
                SFC_CRL_33000 * ((h_ft < 33200) & (h_ft > 32800)) +
                SFC_CRL_34000 * ((h_ft < 34200) & (h_ft > 33800)) +
                SFC_CRL_35000 * ((h_ft < 35200) & (h_ft > 34800)) +
                SFC_CRL_36000 * ((h_ft < 36200) & (h_ft > 35800)) +
                SFC_CRL_37000 * ((h_ft < 37200) & (h_ft > 36800)) +
                SFC_CRL_38000 * ((h_ft < 38200) & (h_ft > 37800)) +
                SFC_CRL_39000 * ((h_ft < 39200) & (h_ft > 38800)) +
                SFC_CRL_40000 * ((h_ft < 40200) & (h_ft > 39800)) +
                SFC_CRL_41000 * ((h_ft < 41200) & (h_ft > 40800)) +
                SFC_CRL_42000 * ((h_ft < 42200) & (h_ft > 41800))
            )

            # --- INTERPOLATION ---
            # Note: interp2 en Matlab prend (X, Y, V, Xq, Yq).
            # En Python scipy, il faut construire l'interpolateur d'abord.
            # ATTENTION : Cela suppose que Mach_table_CRL et Fn_lbf_CRL forment une grille régulière.
            # Si Fn_lbf_CRL change à chaque pas de temps, il faudra peut-être utiliser griddata 
            # ou interpoler ligne par ligne. Voici l'implémentation standard pour une grille :
            
            # Création des points de requête (couple Mach, Force/2)
            # pts = np.array([Mach, F/2]).T 
            # interpolator = RegularGridInterpolator((Mach_table_CRL, Fn_lbf_CRL_Axis), SFC_CRL, bounds_error=False, fill_value=None)
            # SFC_lbf = interpolator(pts)
            
            # SANS connaitre la forme exacte de vos tables (si Fn_lbf_CRL est un vecteur ou une matrice d'axe),
            # il est difficile de traduire interp2 parfaitement ici.
            # Je laisse la variable calculée pour l'instant :
            # SFC_lbf = ... (à adapter selon vos données d'entrée)
            
            SFC = SFC_lbf / 3600 / g

        else:
            # Modèle Elodie Roux
            # Coef_SFC_MCL et Coef_SFC_cruise supposés être des fonctions ou scripts importés
            # En Python, on les appellerait probablement ici s'ce sont des fonctions
            
            # Calcul des coefficients selon l'altitude (Troposphère vs Stratosphère)
            # np.where(condition, valeur_si_vrai, valeur_si_faux) remplace le if/else pour les vecteurs
            
            # Condition : est-ce dans la troposphère ?
            is_trop = (h <= 11000)

            a_1 = np.where(is_trop, a1_troposphere_1 * h + a1_troposphere_2, a1_stratosphere)
            a_2 = np.where(is_trop, a2_troposphere_1 * h + a2_troposphere_2, a2_stratosphere)
            b_1 = np.where(is_trop, b1_troposphere_1 * h + b1_troposphere_2, b1_stratosphere)
            b_2 = np.where(is_trop, b2_troposphere_1 * h + b2_troposphere_2, b2_stratosphere)
            c   = np.where(is_trop, c_troposphere, c_stratosphere)

            # Calcul SFC_CLB
            SFC_CLB = ((a_1 * BPR + a_2) * Mach + (b_1 * BPR + b_2) * np.sqrt(T / T_0) + 
                    (coef_SFC1 * (OPR - 30) * h + c) * (OPR - 30)) # * SFC_design / coef_SFC
            
            # Calcul SFC_reduced_min
            SFC_reduced_min = (coef_alt_SFCmin * h + const_SFCmin + coef_fpr_SFCmin * FPR + 
                            coef_mach_SFCmin * Mach + coef_alt_mach_SFCmin * Mach * h)
            
            # Calcul F_i
            F_i = (coef_alt_Fi * h + const_Fi + coef_fpr_Fi * FPR + coef_mach_Fi * Mach + 
                coef_alt_mach_Fi1 * Mach * h + coef_alt_mach_Fi2 * Mach * (h**1.1))
            
            # Calcul SFC_reduced
            SFC_reduced = (1 - SFC_reduced_min) * ((F / F_max - F_i) / (1 - F_i))**2 + SFC_reduced_min
            
            # Calcul Final
            SFC = SFC_reduced * SFC_CLB

    # Getters
    def get_BPR(self):
        return self.BPR

    def get_OPR(self):
        return self.OPR

    def get_Reseau_moteur(self):
        return self.Reseau_moteur

    def get_F(self):
        return self.F

    def get_SFC(self):
        return self.SFC
