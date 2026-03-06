from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from moteurs.loadData import loadData
from moteurs.Moteur import Moteur
import numpy as np

class ElodieRoux(Moteur):
    '''
    Simulation d'un moteur par des formules déterministes:
    http://elodieroux.com/ReportFiles/ModelesMoteurVersionPublique.pdf
    '''
    # Coefficients loi de Mach Fmax
    aFMs = [ 1.79e-12,  4.29e-13, -5.24e-14, -4.51e-14, -4.57e-12]
    aGMs = [ 1.17e-8,  -8.80e-8,  -5.25e-9,  -3.19e-9,   5.52e-8]
    aFFm = [-5.37e-13, -1.26e-12,  1.29e-14,  2.39e-14,  2.35e-12]
    aGFm = [-3.18e-9,   2.76e-8,   1.97e-9,   1.17e-9,  -2.26e-8]

    bFMs = [ 1.70e-12,  1.51e-12,  1.48e-9,  -7.59e-14, -1.07e-11]
    bGMs = [-3.48e-9,  -8.41e-8,   2.56e-5,  -2.00e-8,  -7.17e-8]
    bFFm = [-3.89e-13, -2.05e-12, -9.28e-10,  1.30e-13,  5.39e-12]
    bGFm = [ 1.77e-9,   2.62e-8,  -8.87e-6,   6.66e-9,   4.43e-8]

    aMs = -2.74e-4; aFm =  2.67e-4
    bMs =  1.91e-2; bFm = -2.35e-2
    cMs =  1.21e-3; cFm = -1.32e-3
    dMs = -8.48e-4; dFm =  3.14e-4
    eMs =  8.96e-1; eFm =  5.22e-1

    def __init__(self, Avion, path):
        super().__init__(Avion)
        self.DonneesMoteur = loadData(path)

        # Plus simple à importer ici
        self.OPR = self.DonneesMoteur.OPR
        self.BPR = self.DonneesMoteur.BPR
        self.F0  = self.DonneesMoteur.F0
        self.T4  = self.DonneesMoteur.T4
        self.h_opt = self.DonneesMoteur.h_opt
        self.dT4_climb =  self.DonneesMoteur.dT4_climb
        self.dT4_cruise =  self.DonneesMoteur.dT4_cruise

    def calculateFmax(self, Atmosphere: Atmosphere, dT4):
        '''
        Détermine la poussée maximale atteingable par le moteur aux conditions actuelles de l'avion,
        et par rapport à sa configuration propre.

        :param Atmosphere: Instance de la classe Atmosphere
        :param dT4: Delta par rapport à la T4 définie par l'utilisateur (<0, K)
        '''
        h = self.Avion.get_h()
        M = self.Avion.Aero.getMach()
        rho = Atmosphere.getRho()

        # Loi de Mach
        F_M_s = ( self.aFMs[0] * (self.OPR - 30)**2 + self.aFMs[1] * (self.OPR - 30) + self.aFMs[2]
                 + self.aFMs[3] * self.T4 + self.aFMs[4] * dT4 ) * self.BPR + ( self.bFMs[0] * (self.OPR - 30)**2
                 + self.bFMs[1] * (self.OPR - 30) + self.bFMs[2] + self.bFMs[3] * self.T4 + self.bFMs[4] * dT4 )
        
        F_F_m = ( self.aFFm[0] * (self.OPR - 30)**2 + self.aFFm[1] * (self.OPR - 30) + self.aFFm[2]
            + self.aFFm[3] * self.T4 + self.aFFm[4] * dT4 ) * self.BPR + ( self.bFFm[0] * (self.OPR - 30)**2
            + self.bFFm[1] * (self.OPR - 30) + self.bFFm[2] + self.bFFm[3] * self.T4 + self.bFFm[4] * dT4 )
        
        G_M_s = ( self.aGMs[0] * (self.OPR - 30)**2 + self.aGMs[1] * (self.OPR - 30) + self.aGMs[2]
                 + self.aGMs[3] * self.T4 + self.aGMs[4] * dT4 ) * self.BPR + ( self.bGMs[0] * (self.OPR - 30)**2
                 + self.bFMs[1] * (self.OPR - 30) + self.bGMs[2] + self.bGMs[3] * self.T4 + self.bGMs[4] * dT4 )
        
        G_F_m = ( self.aGFm[0] * (self.OPR - 30)**2 + self.aGFm[1] * (self.OPR - 30) + self.aGFm[2]
            + self.aGFm[3] * self.T4 + self.aGFm[4] * dT4 ) * self.BPR + ( self.bGFm[0] * (self.OPR - 30)**2
            + self.bGFm[1] * (self.OPR - 30) + self.bGFm[2] + self.bGFm[3] * self.T4 + self.bGFm[4] * dT4 )

        Mach_s = self.aMs * self.T4 + self.bMs * self.BPR + self.cMs * (self.OPR - 30) + self.dMs * dT4 + self.eMs
        F_m = self.aFm * self.T4 + self.bFm * self.BPR + self.cFm * (self.OPR - 30) + self.dFm * dT4 + self.eFm

        # Vectorisation
        Mach_s += (F_M_s*(h-11000)**2 + G_M_s*(h-11000)) * (h > 11000)
        F_m += (F_F_m*(h-11000)**2 + G_F_m*(h-11000)) * (h > 11000)

        alpha = (1-F_m) / Mach_s**2
        QM = alpha * (M - Mach_s)**2 + F_m

        # Loi d'altitude
        k = 1 + 1.2e-3 * dT4
        n = 0.98 + 8e-4 * dT4

        # Encore une vectorisation
        QH = (k * (rho/Constantes.rho0)**n * (1 - 0.04*np.sin(np.pi*h/11000))) * (h <= 11000) \
            + ( k * (Constantes.rho11/Constantes.rho0)**n * rho / Constantes.rho11) * (h > 11000)
        
        # Résidus
        QR = (-4.51e-3) * self.BPR + (2.19e-5) * self.T4 - (3.09e-4) * (self.OPR - 30) + (0.945)

        # Résultat final
        return self.F0 * QM * QH * QR
    
    def calculateSFCmax(self, Atmosphere: Atmosphere):
        '''
        Calcule la SFC du moteur à sa poussée maximale.

        :param Atmosphere: Instance de la classe Atmosphere
        '''
        h = self.Avion.get_h()
        h_sub_11 = (h <= 11000)
        h_sup_11 = (h >  11000)


        a1 = ((-7.44e-13)*h + 6.54e-7) * h_sub_11 + ( 6.45e-7) * h_sup_11
        a2 = ((-3.32e-10)*h + 8.54e-6) * h_sub_11 + ( 4.89e-6) * h_sup_11
        b1 = ((-3.47e-11)*h - 6.58e-7) * h_sub_11 + (-1.04e-6) * h_sup_11
        b2 = (( 4.23e-10)*h + 1.32e-5) * h_sub_11 + ( 1.79e-5) * h_sup_11
        c  = -1.05e-7

        M = self.Avion.Aero.getMach()
        T = Atmosphere.getT()

        return (a1 * self.BPR + a2) * M + (b1 * self.BPR + b2) * np.sqrt(T/Constantes.T0_K) \
             + ((7.4e-13)*(self.OPR - 30) * h + c) * (self.OPR - 30)

    def calculateSFC(self, Atmosphere: Atmosphere, dT4):
        '''
        Calcul complet de la SFC, pour une situation de poussée non maximale.

        :param Atmosphere: Instance de la classe Atmosphere
        :param dT4: Delta de température avec la T4 définie par l'utilisateur (<0, K)
        '''
        h = self.Avion.get_h()

        # Poussée et consommation spécifique maximales
        Fmax = self.calculateFmax(Atmosphere, dT4)
        SFC_Fmax = self.calculateSFCmax(Atmosphere)

        # Variables nécessaires
        dh = h - self.h_opt
        Fi_red = (-9.6e-5)*dh + 0.85
        SFCmin_red = 0.998 * (dh < -89) + (0.995 - (3.385e-5)*dh) * (dh >= 89)
        a = (1 - SFCmin_red) / ((1 - Fi_red)**2)

        # Modèle Elodie Roux
        self.SFC_t = (a * (self.F_t / 2 / Fmax - Fi_red)**2 + SFCmin_red) * SFC_Fmax
        self.FF_t = self.F_t * self.SFC_t

        # Modèle ESDU
        # n = (3.51e-2)*self.BPR - (1.27e-5)*h + 0.31
        # k = 2.24e-5
        # self.SFC_t = k * np.sqrt(T/Constantes.T0_K) * M**n
        # self.FF_t = self.F_t * self.SFC_t


    def calculateFClimb(self, Atmosphere: Atmosphere):
        # Utilisation de la poussée maximale avec le dT4 de montée
        self.F_t = self.calculateFmax(Atmosphere, self.dT4_climb) * 2 * self.Inputs.cF_climb


    def calculateSFCClimb(self, Atmosphere: Atmosphere):
        # Utilisation de la SFC pour poussée maximale
        self.SFC_t = self.calculateSFCmax(Atmosphere)
        self.FF_t = self.F_t * self.SFC_t * self.Inputs.cFF_climb

    def calculateSFCCruise(self, Atmosphere: Atmosphere):
        # Calcul de SFC avec une poussée partielle
        self.calculateSFC(Atmosphere, dT4=self.dT4_cruise)
        self.SFC_t *= self.Inputs.cFF_cruise
        self.FF_t *= self.Inputs.cFF_cruise

    def calculateSFCCruiseDiversion(self, Atmosphere: Atmosphere):
        self.calculateSFCCruise(Atmosphere)

    def calculateSFCHolding(self, Atmosphere: Atmosphere):
        self.calculateSFCCruise(Atmosphere)

    def calculateFDescent(self, Atmosphere: Atmosphere):
        self.F_t = 0 * self.Inputs.cF_descent

    def calculateSFCDescent(self, Atmosphere: Atmosphere):
        # Les modèles Elodie Roux ne sont pas valables pour un moteur au ralenti
        self.SFC_t = 0
        self.FF_t = 0.16 * self.Inputs.cFF_descent # Moyenne empirique
