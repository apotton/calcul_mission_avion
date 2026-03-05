from moteurs.Moteur import Moteur
from atmosphere.Atmosphere import Atmosphere
import numpy as np
from constantes.Constantes import Constantes

class ElodieRoux(Moteur):

    OPR = 32.6
    BPR = 5.7
    F0  = 120_000.
    T4  = 1500.
    dT4_climb = -50.
    dT4_cruise = -90.

    aFMs = [1.79e-12, 4.29e-13, -5.24e-14, -4.51e-14, -4.57e-12]
    aGMs = [1.17e-8, -8.80e-8, -5.25e-9, -3.19e-9, 5.52e-8]
    aFFm = [-5.37e-13, -1.26e-12, 1.29e-14, 2.39e-14, 2.35e-12]
    aGFm = [-3.18e-9, 2.76e-8, 1.97e-9, 1.17e-9, -2.26e-8]

    bFMs = [1.70e-12, 1.51e-12, 1.48e-9, -7.59e-14, -1.07e-11]
    bGMs = [-3.48e-9, -8.41e-8, 2.56e-5, -2.00e-8, -7.17e-8]
    bFFm = [-3.89e-13, -2.05e-12, -9.28e-10, 1.30e-13, 5.39e-12]
    bGFm = [1.77e-9, 2.62e-8, -8.87e-6, 6.66e-9, 4.43e-8]

    aMs = -2.74e-4; aFm = 2.67e-4
    bMs = 1.91e-2; bFm = -2.35e-2
    cMs = 1.21e-3; cFm = -1.32e-3
    dMs = -8.48e-4; dFm = 3.14e-4
    eMs = 8.96e-1; eFm = 5.22e-1






    def __init__(self, Avion):
        super().__init__(Avion)
        # Pas de Donnees_moteur ici, peut-être d'autres constantes spécifiques

    def calculateFmax(self, Atmosphere: Atmosphere, dT4):
        h = self.Avion.geth()
        M = self.Avion.Aero.getMach()
        rho = Atmosphere.getRho_t()

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


        if (h > 11000):
            Mach_s += F_M_s*(h-11000)**2 + G_M_s*(h-11000)
            F_m += F_F_m*(h-11000)**2 + G_F_m*(h-11000)

        alpha = (1-F_m) / Mach_s**2
        QM = alpha * (M - Mach_s)**2 + F_m

        # Loi d'altitude
        k = 1 + 1.2e-3 * dT4
        n = 0.98 + 8e-4 * dT4

        if h <= 11000:
            QH = k * (rho/Constantes.rho0)**n * (1 - 0.04*np.sin(np.pi*h/11000))
        else:
            QH = k * (Constantes.rho11/Constantes.rho0)**n * rho / Constantes.rho11
        
        # Résidus
        QR = -4.51e-3 * self.BPR + 2.19e-5 * self.T4 - 3.09e-4 * (self.OPR - 30) + 0.945

        # Résultat final
        return self.F0 * QM * QH * QR

    def calculateFClimb(self):
        pass