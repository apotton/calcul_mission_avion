from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np
# from .Avion import Avion
# from .Masse import Masse

class Aero:
    def __init__(self, avion):
        self.Avion = avion
        self.Cx_t = self.Avion.getCx0Climb()
        # print("Test" + str(Constantes().a1_stratosphere))
        self.Cz_t = self.CalculateCz() #ATTENTION CHANGER MMO PAR MACH_T

    #Calcul du Cz
    def CalculateCz(self):
        self.Cz_t = self.Avion.Masse.getCurrentMass()*Constantes.g/(0.7*Constantes.p0_Pa*self.Avion.getSref()*self.Avion.getMMO()**2) #CHANGER MMO PAR MACH_T
    

    #Calcul du simplifié de Cx en fonction de la configuration du vol
    def CalculateCxClimb_Simplified(self):
        self.Cx_t = self.Avion.getCx0Climb() + 1/(np.pi*self.Avion.getAspectRatio()*self.Avion.getOswaldClimb()) *self.Cz_t**2

    def CalculateCxCruise_Simplified(self):
        self.Cx_t = self.Avion.getCx0Cruise() + 1/(np.pi*self.Avion.getAspectRatio()*self.Avion.getOswaldCruise()) *self.Cz_t**2

    def CalculateCxDescent_Simplified(self):
        self.Cx_t = self.Avion.getCx0Descent() + 1/(np.pi*self.Avion.getAspectRatio()*self.Avion.getOswaldDescent()) *self.Cz_t**2

    

    #Calcul avancé du Cx
    def CalculateCx(self, atmosphere):
        #Calcul du Cx0
        ################################################################
        #va falloir convertir plein d'angles donc :
        phi_rad = np.radians(self.Avion.getPhi25deg())
        cos_phi = np.cos(phi_rad)
        cos_phi_c = np.cos(phi_rad)**2

        #Calcul du nombre de Reynolds
        Re = (47899*atmosphere.getP_t()*self.getMach()*
              ((1+0.126*self.getMach()**2)*atmosphere.getT_t()+110.4)
              /(atmosphere.getT_t()**2))/(1+0.126*self.getMach()**2)**(5/2)
        
        #Calcul du Cf
        Cf = 0.455/(1+0.126*self.getMach()**2)/(np.log10(Re*self.Avion.getLref()))**2.58

        #Calcul du K_e & K_c
        K_e = 4.688*self.Avion.getTtoCref()**2 + 3.146*self.Avion.getTtoCref()
        K_c = 2.859*(self.getCz()/cos_phi_c)**3 - 1.849*(self.getCz()/cos_phi_c)**2 + 0.382*(self.getCz()/cos_phi_c)+0.06
        K_phi = 1 - 0.000178*(phi_rad)**2 - 0.00065*phi_rad

        # ??? Trouver origine constantes
        K_i = 0.04
        Delta_Cx_0 = 0.0115
        Cx_0_wing = 2*Cf*((K_e+K_c)*K_phi+K_i+1)
        Cx_0 = Cx_0_wing + Delta_Cx_0
        #################################################################

        #Calcul du Cx_i

        delta_e = 0.233*self.Avion.getTaperRatio()**2-0.068*self.Avion.getTaperRatio()+0.012
        delta_to_delta_0 = (0.7/self.getCz())**2
        Cx_i = (1.03+delta_e*delta_to_delta_0+(self.Avion.getDFuselage()
               /self.Avion.getEnvergure())**2)/(np.pi*self.Avion.getAspectRatio())*self.getCz()**2

        #Calcul du Cx_trim
        Cx_trim = (5.89*10**(-4))*self.getCz()

        #Calcul du Cx_compressibility
        MDD = 0.95/cos_phi - self.Avion.getTtoCref()/cos_phi_c - self.getCz()/(10*cos_phi**3)
        M_cr = MDD - (0.1/80)**(1/3)

        #Maintenant c'est la boucle :
        if self.getMach()>M_cr :
            Cx_compressibility = 20 * (self.getMach()-M_cr)**4
        else :
            Cx_compressibility = 0
        
        #Calcul final
        self.Cx_t = Cx_0 + Cx_i + Cx_trim + Cx_compressibility
    
    #Getters 
    def getCx(self):
        return self.Cx_t
    
    def getMach(self):
        return 0.5 # self.Mach_T #ATTENTION ATTRIBUT MACH A AJOUTER APRES CALCULS MOTEURS
    
    def getCz(self):
        return self.Cz_t