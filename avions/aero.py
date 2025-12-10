from constantes.constantes import Constantes 
from atmosphere.Atmosphere import Atmosphere
from Avion import Avion

class Aero:
    def __init__(self, avion):
        self.avion = avion
        self.Current_Cx = 0
        self.Current_Cz = 0

    def CalculateCz(self,Mach,Pressure):
        return self.avion.getMaxTakeoffWeight()*Constantes.g/(0.7*Pressure*self.avion.getSref()*Mach**2)

