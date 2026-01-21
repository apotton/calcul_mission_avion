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
        self.Cz_t = 0 #Uniquement pour l'initialisation 

    def CalculateAll(self, atmosphere):
        self.CalculateCzBuffet()
        self.CalculateCz(atmosphere)
        self.CalculateCx(atmosphere)
        self.CalculateTAS(atmosphere)
        self.calculateSGR(atmosphere)
        self.calculateECCF(atmosphere)

    #Calcul du Cz
    def CalculateCz(self, atmosphere):
        self.Cz_t = self.Avion.Masse.getCurrentMass()*Constantes.g/(0.7*atmosphere.getP_t()*self.Avion.getSref()*self.getMach()**2) 
    

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
    
    def CalculateCzBuffet(self):
        """
        Calcule le Cz d'apparition du buffeting pour un Mach donné.
        Basé sur une méthode de scaling depuis un avion de référence (A320).
        """
        
        # Récupération des paramètres géométriques de l'avion CIBLE
        lambdac41_deg = self.Avion.getPhi25deg()  # Angle de flèche au quart de corde
        lambdac41 = np.deg2rad(lambdac41_deg)
        
        tc1 = self.Avion.getTtoCref()    # fraction d'épaisseur maximale
        c1 = self.Avion.getCamber()               # Cambrure du profil
        ptc1 = self.Avion.getMaxThicknessPosition()    # Position de l'épaisseur maximale
        AR1 = self.Avion.getAspectRatio()
        t1 = self.Avion.getTaperRatio()

        # Paramètres géométriques de l'avion de RÉFÉRENCE (Seed - A320)        
        lambdac40_deg = 29.74
        lambdac40 = np.deg2rad(lambdac40_deg)
        
        tc0 = 0.1055
        c0 = 0.0145
        ptc0 = 0.350
        AR0 = 11.664
        t0 = 0.235

        # Courbe d'apparition du buffeting de référence (Seed curve)
        M0 = np.array([0.3, 0.32, 0.34, 0.36, 0.4, 0.45, 0.5, 0.55, 0.6, 
                       0.7, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84])
        CL0 = np.array([1.4, 1.31, 1.25, 1.2, 1.12, 1.05, 1.01, 0.975, 0.96, 
                        0.935, 0.902, 0.886, 0.867, 0.849, 0.83, 0.76])

        # Coefficients de régression ---
        tau = 10.0
        k1 = -0.1024
        k2 = 1.0
        k3 = 2.4872
        k4 = 0.2963
        k5 = -1.0
        k6 = 3.1464
        beta = 25.353
        theta = 2.0364
        gamma = 10.050

        # Conversion de la flèche (Quarter chord -> Max thickness line) ---
        # Formule : lambda = atan( tan(lambda_c4) + 4/AR * ... )
        
        term_seed = (4 / AR0) * ((t0 - 1) / (t0 + 1)) * (ptc0 - 0.25)
        lambda0 = np.arctan(np.tan(lambdac40) + term_seed)
        
        term_target = (4 / AR1) * ((t1 - 1) / (t1 + 1)) * (ptc1 - 0.25)
        lambda1 = np.arctan(np.tan(lambdac41) + term_target)

        # Préalcul des termes cosinus
        cos_l0 = np.cos(lambda0)
        cos_l1 = np.cos(lambda1)
        
        # Estimation vectorisée par scaling
        
        # Transformation du Mach (Sweep theory)
        M1 = M0 * (cos_l0 / cos_l1)

        # Calcul des exposants intermédiaires (dépendants du Mach)
        # Note: M0*cos_l0 est un vecteur, donc alphaM et omegaM le deviennent aussi
        M0_eff = M0 * cos_l0
        
        alphaM = k1 + k2 * np.power(M0_eff, k3)
        omegaM = k4 + k5 * np.power(M0_eff, k6)

        # Partie Cambrure (Camber term)
        term_c0 = (theta * c0) / cos_l0
        frac_c = ((c1 / cos_l1) - (c0 / cos_l0)) / (c0 / cos_l0)
        factor_camber = np.power(1 + (term_c0 / (term_c0 + 1)) * frac_c, gamma)
        
        # Partie Épaisseur (Thickness term) - Dépend de omegaM (donc du Mach)
        term_tc0 = (omegaM * tc0) / cos_l0
        frac_tc = ((tc1 / cos_l1) - (tc0 / cos_l0)) / (tc0 / cos_l0)
        factor_thickness = np.power(1 + (term_tc0 / (term_tc0 + 1)) * frac_tc, beta)
        
        # Partie Flèche (Sweep term) - Dépend de alphaM
        lam0_deg = np.degrees(lambda0)
        lam1_deg = np.degrees(lambda1)
        term_sweep_const = tau * lam0_deg
        frac_sweep = (lam1_deg - lam0_deg) / lam0_deg
        factor_sweep = np.power(1 + (term_sweep_const / (term_sweep_const + 1)) * frac_sweep, alphaM)

        # Calcul final de CL1 (Target CL)
        # Formule : CL1 = CL0 * (cos1/cos0)^2 * Factors...
        CL1 = (CL0 * (cos_l1**2 / cos_l0**2) * factor_camber * factor_thickness * factor_sweep)

        # Interpolation Finale
        # Attention : np.interp prend (x_to_find, x_data, y_data)
        self.CzBuffet_t = np.interp(self.getMach(), M1, CL1)

    def CalculateTAS(self, atmosphere):
        self.TAS_t = self.getMach() * np.sqrt(1.4 * Constantes.r * atmosphere.getT_t())

    def calculateECCF(self, atmosphere):
        # Traduire en Python: ECCF=CI/60./(TAS+Vw)+(SFC*m*g)./((TAS+Vw).*finesse);
        TAS = self.getTAS(atmosphere)
        Vw = atmosphere.getVwind()
        finesse = self.getCz()/self.getCx()
        CI = 1.0  # Constante d'Injection (à définir précisément selon le contexte)
        m = self.Avion.Masse.getCurrentMass()
        SFC = self.Avion.moteur.get_SFC()  # Specific Fuel Consumption (à définir précisément selon le contexte)
        self.ECCF_t = (CI / 60.0 / (TAS + Vw) 
                     + (SFC * m * Constantes.g) 
                     / ((TAS + Vw) * finesse) )
        
    def calculateSGR(self, atmosphere):
        # Adapter en Python: SGR=(TAS+Vw).*finesse./(SFC*m*g);
        Vw = atmosphere.getVwind()
        finesse = self.getCz()/self.getCx()
        m = self.Avion.Masse.getCurrentMass()
        SFC = self.Avion.moteur.get_SFC()  # Specific Fuel Consumption (à définir précisément selon le contexte)
        self.SGR_t = (self.TAS_t + Vw) * finesse / (SFC * m * Constantes.g)

    #Getters 
    def getCx(self):
        return self.Cx_t
    
    def getMach(self):
        return 0.5 # self.Mach_T #ATTENTION ATTRIBUT MACH A AJOUTER APRES CALCULS MOTEURS
    
    def getCz(self):
        return self.Cz_t
    
    def getCzBuffet(self):
        return self.CzBuffet_t
    
    def getTAS(self):
        return self.TAS_t
    
    def getECCF(self):
        return self.ECCF_t
    
    def getSGR(self):
        return self.SGR_t