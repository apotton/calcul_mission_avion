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
        #Calcul du Cx0
        ################################################################
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
        #################################################################

        #Calcul du Cx_i
        Taper_ratio=0.246
        D_fuselage = 3.95
        Envergure = 34.1
        Aspect_ratio = 9.603
        delta_e=0.233*Taper_ratio**2-0.068*Taper_ratio+0.012
        delta_to_delta_0=(0.7/Aero.getCz())**2
        Cx_i=(1.03+delta_e*delta_to_delta_0+(D_fuselage/Envergure)**2)/(np.pi*Aspect_ratio)*Aero.getCz()**2

        #Calcul du Cx_trim
        Cx_trim = (5.89*10**(-4))*Aero.getCz()

        #Calcul du Cx_compressibility
        MDD= 0.95/np.cos(phi_rad) - t_to_c_ref/le_cosinus - Aero.getCz()/(10*(np.cos(phi_rad))**3)
        M_cr = MDD - (0.1/80)**(1/3)

        #Maintenant c'est la boucle :
        if Aero.getMach()>M_cr :
            Cx_compressibility = 20 * (Aero.getMach()-M_cr)**4
        else :
            Cx_compressibility = 0
        
        #Calcul final
        Cx = Cx_0 + Cx_i + Cx_trim + Cx_compressibility
        return Cx