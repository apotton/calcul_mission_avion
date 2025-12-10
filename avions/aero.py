from constantes.constantes import Constantes 
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class Aero:
    def __init__(self, avion):
        self.avion = avion
        self.Cx_t = self.avion.getCx0Climb()
        self.Cz_t = self.avion.getMaxTakeoffWeight()*Constantes.g/(0.7*Constantes.p0_Pa*self.avion.getSref()*self.avion.getMMO()**2) #ATTENTION CHANGER MTOW PAR LA MASSE ACTUELLE ET MMO PAR MACH_T

    #Calcul du Cz
    def CalculateCz(self):
        self.Cz_t = self.avion.getMaxTakeoffWeight()*Constantes.g/(0.7*Constantes.p0_Pa*self.avion.getSref()*self.avion.getMMO()**2) #ATTENTION CHANGER MTOW PAR LA MASSE ACTUELLE ET MMO PAR MACH_T
    
    def getCz(self):
        return self.Cz_t
    

    #Calcul du simplifié de Cx en fonction de la configuration du vol
    def CalculateCxClimb_Simplified(self):
        self.Cx_t = self.avion.getCx0Climb() + 1/(np.pi*self.avion.getAspectRatio()*self.avion.getOswaldClimb()) *self.Cz_t**2

    def CalculateCxCruise_Simplified(self):
        self.Cx_t = self.avion.getCx0Cruise() + 1/(np.pi*self.avion.getAspectRatio()*self.avion.getOswaldCruise()) *self.Cz_t**2

    def CalculateCxDescent_Simplified(self):
        self.Cx_t = self.avion.getCx0Descent() + 1/(np.pi*self.avion.getAspectRatio()*self.avion.getOswaldDescent()) *self.Cz_t**2

    def getCx(self):
        return self.Cx_t
