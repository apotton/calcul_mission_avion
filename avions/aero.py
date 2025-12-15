from constantes.constantes import Constantes 
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class Aero:
    def __init__(self, avion):
        self.avion = avion
        self.Cx_t = self.avion.getCx0Climb()
        self.Cz_t = self.CalculateCz() #ATTENTION CHANGER MTOW PAR LA MASSE ACTUELLE ET MMO PAR MACH_T

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
    def getMach(self):
        return self.Mach
    
    def CalculateCx(self):
        #va falloir convertir plein d'angles donc :
        phi_25_deg = 24.97
        phi_rad = np.radians(phi_25_deg) 
        #ules random constante du matlab :
        l_ref = 6
        t_to_c_ref = 0.1093
        #Calcul du nombre de Reynolds
        Re = (47899*Atmosphere.getP_t()*Aero.getMach()*((1+0.126*Aero.getMach()**2)*Atmosphere.getT_t()+110.4)/(Atmosphere.getT_t()**2))/(1+0.126*Aero.getMach()**2)**(5/2)
        #Calcul du Cf
        Cf = 0.455/(1+0.126*Aero.getMach()**2)/(np.log10(Re*l_ref))**2.58
        #Calcul du K_e & K_c
        K_e = 4.688*t_to_c_ref**2+3.146*t_to_c_ref
        le_cosinus = np.cos(phi_rad)**2
        K_c = 2.859*(Aero.getCz()/le_cosinus)**3-1.849*(Aero.getCz()/le_cosinus)**2 + 0.382*(Aero.getCz()/le_cosinus)+0.06
        K_phi = 1-0.000178*(phi_rad)**2-0.00065*phi_rad
        K_i=0.04
        Delta_Cx_0=0.0115
        Cx_0_wing=2*Cf*((K_e+K_c)*K_phi+K_i+1)
        Cx_0=Cx_0_wing+Delta_Cx_0
