from avions.Avion import Avion
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class Mission:
    def __init__(self):
        # Ajouter les attributs nécessaires pour la mission
        # Exemples : Vitesse phases montée, hauteur palier...

        #Je mets ce qui suit en attribut pour l'instant en attendant de décier ce qu'on en fait
        self.l_descent = 0 #Distance nécessaire à la descente
        self.RRoC_min = 300 #Excédent de puissance minimale pour monter en croisière en ft/min
        self.Pressurisation_Ceiling = 40000 #Valeur du plafond de précurisation en ft qui dépend de chaque avions peut être à ajouter aux fichiers de csv avion 

        # Historique pour suivi de la descente (pour fournir le résultat à chaque pas de temps)
        self.history = {
            "h": [], #Altitude en UNITE
            "l": [], #Distance franchie en UNITE
            "t": [], #Temps en UNITE
            "V_CAS": [], #Vitesse conventionnelle en UNITE
            "V_true": [], #Vitesse vraie en UNITE
            "Mach": [], #Mach
            "Cz": [], #Coef de portance
            "Cx": [], #Coef de trainée
            "F_N": [], #Poussée
            "SFC": [], #Consommation spécifique
            "FB": [], #Carburant consommée
            "m": [] #Masse appareil
        }

##
#MONTEE
##

# --- Accélération en palier à 10 000 ft ---
    def climb_Palier(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
        """
        Phase 2 : accélération en palier à 10 000 ft
        CAS : 250 kt -> CAS_climb_target

        dt      : pas de temps (s)
        """

        # --- Conditions initiales ---
        h_t = Avion.geth()
        l_t = Avion.getl()

        # --- CAS initiale ---
        CAS_t = Avion.getCAS() * Constantes.conv_kt_mps # à mettre dans constantes plus tard

        # --- CAS cible --- A CHANGER
        CAS_target = Avion.getKVMO() * Constantes.conv_kt_mps  # à mettre dans constantes plus tard

        # --- Atmosphère (constante en palier) ---
        Atmosphere.CalculateRhoPT(h_t)

        # --- Initialisation ---
        Avion.Convert_CAS_to_Mach(Atmosphere)
        Mach_t = Avion.getMach()
        Avion.Convert_Mach_to_TAS(Atmosphere)
        TAS_t  = Avion.getTAS()

        while CAS_t < CAS_target:

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Atmosphere)
            Cz_t = Avion.Aero.getCz()

            Avion.Aero.CalculateCxClimb_Simplified()
            Cx_t = Avion.Aero.getCx()
            finesse = Cz_t / Cx_t

            # --- Traînée ---
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # --- Poussée moteur ---
            F_N = Avion.Moteur.getMaxThrustClimb(h_t, Mach_t)
            SFC = Avion.Moteur.getSFC(h_t, Mach_t)

            # --- Dynamique longitudinale ---
            ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

            # --- Mise à jour vitesse ---
            TAS_t = max(TAS_t + ax * dt, 0.0)

            # --- Recalcul Mach et CAS ---
            Mach_t = Avion.Convert_TAS_to_Mach(Atmosphere)
            CAS_t  = Avion.Convert_Mach_to_CAS(Atmosphere)

            # --- Cinématique ---
            Vz_t = 0.0
            Vx_t = TAS_t
            dl = Vx_t * dt

            # --- Fuel burn ---
            Avion.Masse.burn_fuel(dt)

            # --- Mise à jour avion ---
            Avion.Add_dl(dl)
            Avion.setTAS_t(TAS_t)
            Avion.setMach_t(Mach_t)
            Avion.setCAS_t(CAS_t)
            # Pas de changement d'altitude en palier

            # --- Historique ---
            self.history["h"].append(h_t)
            self.history["l"].append(l_t)
            self.history["t"].append(self.history["t"][-1] + dt)
            self.history["V_CAS"].append(CAS_t)
            self.history["V_true"].append(TAS_t)
            self.history["Mach"].append(Mach_t)
            self.history["Cz"].append(Cz_t)
            self.history["Cx"].append(Cx_t)
            self.history["Vz"].append(Vz_t)
            self.history["Vx"].append(Vx_t)
            self.history["F_N"].append(F_N)
            self.history["SFC"].append(SFC)
            self.history["FB"].append(Avion.Masse.getFuelBurned())
            self.history["m"].append(Avion.Masse.getCurrentMass())

# --- Phase 3 : Montée ISO CAS jusqu'au Mach maximal ---

    def climb_iso_CAS(self, Avion: Avion, Atmosphere: Atmosphere, CAS_const, Mach_target, h_end, dt=1.0):
        """
        Montée à CAS constant jusqu'à atteindre un Mach cible

        h_start     : altitude initiale
        h_end       : altitude max de sécurité (optionnelle)
        l_start     : distance initiale
        t_start     : temps initial
        CAS_const   : CAS imposée (m/s)
        Mach_target : Mach cible de transition
        dt          : pas de temps
        """

        h = Avion.geth()
        l = Avion.getl()

        Mach = 0.0
        TAS  = 0.0

        while Mach < Mach_target and h < h_end:

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(h)
            P_t = Atmosphere.getP_t()
            T_t = Atmosphere.getT_t()

            # --- CAS -> Mach ---
            Mach = Constantes.Convert_CAS_to_Mach(self.CAS_const, P_t)

            # --- TAS ---
            TAS = Mach * np.sqrt(Constantes.gamma * Constantes.r * T_t)

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Mach)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCxClimb_Simplified()
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # --- Traînée ---
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # --- Poussée ---
            F_N = Avion.Moteur.getMaxThrustClimb(h, Mach)
            SFC = Avion.Moteur.getSFC(h, Mach)

            # --- Pente ---
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # --- Vitesses ---
            Vz = TAS * np.sin(pente)
            Vx = TAS * np.cos(pente)

            # --- Intégration ---
            h += Vz * dt
            l += Vx * dt

            # --- Fuel burn ---
            Avion.Masse.burn_fuel(dt)

            # --- Mise à jour avion ---
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.setTAS_t(TAS)
            Avion.setMach_t(Mach)
            Avion.setCAS_t(CAS_const)


            # --- Historique ---
            self.history["h"].append(h)
            self.history["l"].append(l)
            self.history["V_CAS"].append(self.CAS_const)
            self.history["V_true"].append(TAS)
            self.history["Mach"].append(Mach)
            self.history["Cz"].append(Cz)
            self.history["Cx"].append(Cx)
            self.history["Vz"].append(Vz)
            self.history["Vx"].append(Vx)
            self.history["F_N"].append(F_N)
            self.history["SFC"].append(SFC)
            self.history["FB"].append(Avion.Masse.getFuelBurned())
            self.history["m"].append(Avion.Masse.getCurrentMass())


# --- Phase 4 : Montée ISO Mach jusqu'à l'altitude de fin de montée et de début de croisière ---

    def climb_iso_Mach(self, Avion: Avion, Atmosphere: Atmosphere, h_target, Mach_const, dt=1.0):
        """
        Montée à Mach constant jusqu'à une altitude cible

        h_start    : altitude initiale
        h_target   : altitude finale
        l_start    : distance initiale
        t_start    : temps initial
        Mach_const : Mach imposé
        dt         : pas de temps
        """

        h = Avion.geth()
        l = Avion.getl()

        Mach = Mach_const

        while h < h_target:

            # --- Atmosphère ---
            Atmosphere.CalculateRhoPT(h)
            P_t = Atmosphere.getP_t()
            T_t = Atmosphere.getT_t()

            # --- TAS ---
            TAS = Mach * np.sqrt(Constantes.gamma * Constantes.r * T_t)

            # --- CAS ---
            CAS = Constantes.Convert_Mach_to_CAS(Mach, P_t)

            # --- Aérodynamique ---
            Avion.Aero.CalculateCz(Mach)
            Cz = Avion.Aero.getCz()

            Avion.Aero.CalculateCxClimb_Simplified()
            Cx = Avion.Aero.getCx()

            finesse = Cz / Cx

            # --- Traînée ---
            Rx = Avion.Masse.getCurrentWeight() / finesse

            # --- Poussée ---
            F_N = Avion.Moteur.getMaxThrustClimb(h, Mach)
            SFC = Avion.Moteur.getSFC(h, Mach)

            # --- Pente ---
            pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

            # --- Vitesses ---
            Vz = TAS * np.sin(pente)
            Vx = TAS * np.cos(pente)

            # --- Intégration ---
            h += Vz * dt
            l += Vx * dt

            # --- Fuel burn ---
            Avion.Masse.burn_fuel(dt)

            # --- Mise à jour avion ---
            Avion.Add_dh(Vz * dt)
            Avion.Add_dl(Vx * dt)
            Avion.setTAS_t(TAS)
            Avion.setMach_t(Mach)
            Avion.setCAS_t(CAS)

            # --- Historique ---
            self.history["h"].append(h)
            self.history["l"].append(l)
            self.history["V_CAS"].append(CAS)
            self.history["V_true"].append(TAS)
            self.history["Mach"].append(Mach)
            self.history["Cz"].append(Cz)
            self.history["Cx"].append(Cx)
            self.history["Vz"].append(Vz)
            self.history["Vx"].append(Vx)
            self.history["F_N"].append(F_N)
            self.history["SFC"].append(SFC)
            self.history["FB"].append(Avion.Masse.getFuelBurned())
            self.history["m"].append(Avion.Masse.getCurrentMass())


##
#Croisière MACH SAR
##
def Cruise_Mach_SAR(self, Avion: Avion, Atmosphere: Atmosphere, l_end, Mach_cruise, dt=60.0):
    """
    Phase : croisière en palier à Mach constant

    h_start      : altitude de croisière (UNITE)
    l_start      : distance initiale
    t_start      : temps initial
    l_end        : l fin de mission
    l_descent : distance prévue pour la descente
    Mach_cruise  : Mach imposé
    dt           : pas de temps (s)
    """

    h = Avion.geth()
    l = Avion.getl()


    while l < l_end - self.l_descent and Avion.Masse.getFuelRemaining() > Avion.Masse.getFuelReserve():

        # --- Atmosphère ---
        Atmosphere.CalculateRhoPT(h)
        rho_t = Atmosphere.getRho_t()
        P_t = Atmosphere.getP_t()
        T_t = Atmosphere.getT_t()

        # --- Vitesse ---
        TAS = Mach_cruise * np.sqrt(Constantes.gamma * Constantes.r * T_t)

        # --- Vitesses ---
        Vx = TAS
        Vz = 0.0

        # --- Aérodynamique ---
        Avion.Aero.CalculateCz(Mach_cruise)
        Cz = Avion.Aero.getCz()

        Avion.Aero.CalculateCx(Atmosphere)
        Cx = Avion.Aero.getCx()

        finesse = Cz/Cx

        # Traînée
        Rx = Avion.Masse.getCurrentWeight() / finesse

        # --- Poussée moteur ---
        F_N, SFC = Avion.Moteur.getThrustCruise(Mach_cruise, h)

        #Calcul de l'excédent de puissance
        RRoC = (F_N-Rx)/(Avion.Masse.getCurrentWeight())*TAS #Excédent de puissance qui permet de déterminer si on peut monter de 2000ft 

        #Calcul du coût économique ECCF et SGR
        Avion.Aero.CalculateECCF(Atmosphere)
        Avion.Aero.CalculateSGR(Atmosphere)
        ECCF = Avion.Aero.getECCF()
        SGR = Avion.Aero.getSGR()


        #Calcul du Mach limite 
        #Avion.Aero.CalculateCzBuffet()
        #Cz_Buffet = Avion.Aero.getCzBuffet

        ##Calcul des paramètres 2000ft plus haut pour étudier le coût de monter

        # --- Paramètres 2000 ft plus haut (pour décider la montée) ---
        delta_h_ft = 2000 #ft
        delta_h = delta_h_ft * Constantes.conv_ft_m  # convertir en m

        # Altitude “virtuelle”
        h_up = h + delta_h

        # --- Atmosphère ---
        Atmosphere.CalculateRhoPT(h_up)
        rho_up = Atmosphere.getRho_t()
        P_t_up = Atmosphere.getP_t()
        T_t_up = Atmosphere.getT_t()

        # --- TAS (Mach constant avant montée iso-Mach) ---
        TAS_up = Mach_cruise * np.sqrt(Constantes.gamma * Constantes.r * T_t_up)

        # --- Aérodynamique ---
        Avion.Aero.CalculateCz(Mach_cruise)
        Cz_up = Avion.Aero.getCz()

        Avion.Aero.CalculateCxCruise()
        Cx_up = Avion.Aero.getCx()

        finesse_up = Cz_up / Cx_up

        # --- Traînée / équivalent résistance ---
        Rx_up = Avion.Masse.getCurrentWeight() / finesse_up

        # --- Poussée moteur ---
        F_N_up, SFC_up = Avion.Moteur.getThrustCruise(Mach_cruise, h_up)

        
        #Calcul du coût économique ECCF et SGR
        Avion.Aero.CalculateECCF(Atmosphere) 
        Avion.Aero.CalculateSGR(Atmosphere)
        ECCF_up = Avion.Aero.getECCF()
        SGR_up = Avion.Aero.getSGR()


        # --- RRoC (Rate of Climb virtuel) ---
        RRoC_up = (F_N_up - Rx_up) / Avion.Masse.getCurrentWeight() * TAS_up #UTILISER LA MONTEE ISO MACH DE LA PHASE DE MONTEE MAINTENANT

        # --- Condition de montée iso-Mach ---
        if (
            RRoC_up > self.RRoC_min*Constantes.conv_ft_m/60 and               # RRoC suffisant converti de ft/min en m/s
            h_up < self.Pressurisation_Ceiling*Constantes.conv_ft_m and  # Pas au plafond converti de ft en m
            SGR_up > SGR):                     # Gain SGR positif

            self.climb_iso_Mach(Avion.geth(), h_up, l, t, Mach_cruise, dt=1.0) #CALCUL D ATM DANS LA FONCTION, PEUT ETRE ARRANGER

        else : 
            # --- Intégration ---
            
            dl = Vx * dt

            
            l += dl
            t += dt

            # --- Fuel burn ---
            Avion.Masse.burn_fuel(dt)

            # --- Mise à jour avion ---
            Avion.Add_dl(dl)
            Avion.setTAS_t(TAS)
            Avion.setMach_t(Mach_cruise)
            Avion.setCAS_t(Constantes.Convert_Mach_to_CAS(Mach_cruise, P_t))
            # Pas de changement d'altitude en croisière

            # --- Historique ---
            self.history["h"].append(h)
            self.history["l"].append(l)
            self.history["t"].append(t)
            self.history["Mach"].append(Mach_cruise)
            self.history["V_true"].append(TAS)
            self.history["Cz"].append(Cz)
            self.history["Cx"].append(Cx)
            self.history["Vz"].append(Vz)
            self.history["Vx"].append(Vx)
            self.history["F_N"].append(F_N)
            self.history["SFC"].append(SFC)
            self.history["FB"].append(Avion.Masse.getFuelBurned())
            self.history["m"].append(Avion.Masse.getCurrentMass())


##
#DESCENTE
##




# --- Phase 1 : Ajustement vitesse à Max CAS avec possibilité de descente libre---
def Descente_Phase1(self, Avion: Avion, Atmosphere: Atmosphere, dt=1.0):
    """
    Laisse l'avion initier une descente libre pour atteindre la vitesse maximale autorisée en CAS (Vmax_CAS) avant de passer à la phase 2

    Arguments :
    h_start : altitude initiale en mètres, récupérée en fin de croisière
    l_start : position en x initiale à cette phase (unité), récupérée en fin de croisière
    t_start : temps initiale à cette phase (unité), récupéré en fin de croisière
    Mach_start : Mach initial à cette phrase, récupéré en fin de croisière
    dt      : pas de temps pour la simulation en secondes (par défaut 1 s)
    """
    h = Avion.geth()
    l = Avion.getl() #ATTENTION A PRENDRE DU CALCUL DE CROISIERE PRECEDENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    Gamma = Constantes.gamma #Coefficient de Laplace thermodynamique pour les conversions entre CAS, Mach et TAS 

    # CAS max en m/s
    CAS_max = Avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s  Vitesse maximale de descente de l'avion
    CAS = 0.0  # Initialisation avant calcul à partir du Mach connu
    Mach = Avion.getMach() #ATTENTION RECUPERER DE LA PHASE DE CROISIERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    TAS = 0.0 # Initialisation avant calcul à partir du Mach connu


    while CAS < CAS_max: #On cherche à diminuer l'altitude h jusqu'à atteindre la vitesse CAS Max

        # --- Atmosphère --- Calcule des conditions atm à cet altitude afin d'extraire la température et la pression au temps t
        Atmosphere.CalculateRhoPT(h) #ATTENTION TRES MAUVAIS CHOIX DE NOM POUR ATM CE DEVRAIT ETRE CALCULATE RHO PT
        P_t = Atmosphere.getP_t() #Pression au temps t, en UNITE
        T_t = Atmosphere.getT_t() #Température au temps t, en K

        # --- Mach et TAS --- 
        CAS = Constantes.Convert_Mach_to_CAS(Mach,P_t) #Calcul du CAS à partir du Mach

        TAS = Mach*np.sqrt(Gamma*Constantes.r*T_t) #Calcul du TAS à partir du Mach

        # --- Cz et Cx --- Calcul des coefs aéro
        Avion.Aero.CalculateCz(Mach)
        Cz = Avion.Aero.getCz()

        Avion.Aero.CalculateCxClimb_Simplified()  # ici on peut remplacer par CalculateCx si on veut le modèle complet
        Cx = Avion.Aero.getCx()

        finesse = Cz / Cx

        # --- Poussée moteur et SFC ---
        if self.moteur.get_Reseau_moteur() == 1:
            # ATTENTION A MODIFIER UNE FOIS QU'ON AURA FAIT LES INTERPOLLATIONS MOTEUR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            F_N = 0.0
            SFC = 0.0
        else:
            F_N = 0.0
            SFC = 0.0

        # --- Résistance horizontale ---
        Rx = Avion.Masse.getCurrentWeight() / finesse

        # --- Pente de descente ---
        pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())
        Vz = TAS * np.sin(pente)
        Vx = TAS * np.cos(pente)

        # --- Mise à jour des positions ---
        dh = Vz * dt
        dl = Vx * dt
        h += dh
        l += dl
        self.l_descent += dl #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière
        t += dt

        # --- Fuel burn ---
        Avion.Masse.burn_fuel(dt) #Carburant consommé à ce pas de temps dt, on met à jour la masse de carburant 
    

        # --- Stockage historique ---
        self.history["h"].append(h)
        self.history["l"].append(l)
        self.history["t"].append(t)
        self.history["V_CAS"].append(CAS)
        self.history["V_true"].append(TAS)
        self.history["Mach"].append(Mach)
        self.history["Cz"].append(Cz)
        self.history["Cx"].append(Cx)
        self.history["Vz"].append(Vz)
        self.history["Vx"].append(Vx)
        self.history["F_N"].append(F_N)
        self.history["SFC"].append(SFC)
        self.history["FB"].append(Avion.Masse.getFuelBurned())
        self.history["m"].append(Avion.Masse.getCurrentMass())


# --- Phase 2 : Descente à V constante jusqu'à 10000 ft ---
def Descente_Phase2(self, Avion: Avion, Atmosphere: Atmosphere, h_end, dt=1.0):
    """
    Phase 2 : Descente jusqu'à 10000ft à vitesse constante Max CAS

    Arguments :
    h_start : altitude initiale, après phase 1 (UNITE)
    h_end   : altitude finale de la phase 2, 10 000ft 
    l_start : distance initiale, après phase 1 (UNITE)
    t_start : temps initial, après phase 1 (UNITE)
    dt      : pas de temps (s)
    """

    # --- Conditions initiales ---
    h = Avion.geth()
    l = Avion.getl()

    # --- CAS imposée ---
    CAS = Avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s On descend à CAS fixé par la vitesse max de descente

    Mach = 0.0 #Initialisation de Mach et de TAS avant calcul à partir du CAS
    TAS  = 0.0

    while h > h_end:

        # --- Atmosphère ---
        Atmosphere.CalculateRhoPT(h) #NOM A CHANGER
        P_t   = Atmosphere.getP_t()
        T_t = Atmosphere.getT_t()

        # --- Conversion CAS -> Mach ---
        Mach = Constantes.Convert_CAS_to_Mach(CAS, P_t)

        # --- TAS ---
        TAS = Mach * np.sqrt(Constantes.gamma * Constantes.r * T_t)

        # --- Coefficients aérodynamiques ---
        Avion.Aero.CalculateCz(Mach)
        Cz = Avion.Aero.getCz()

        Avion.Aero.CalculateCxClimb_Simplified()
        Cx = Avion.Aero.getCx()

        finesse = Cz / Cx

        # --- Poussée moteur (idle en descente) ---
        F_N = 0.0
        SFC = 0.0

        # --- Résistance ---
        Rx = Avion.Masse.getCurrentWeight() / finesse

        # --- Pente de trajectoire ---
        pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

        Vz = TAS * np.sin(pente)   # négatif car en descente
        Vx = TAS * np.cos(pente)

        # --- Mise à jour position ---
        dh = Vz * dt
        dl = Vx * dt

        h += dh
        l += dl
        self.l_descent += dl # Calcul  de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière

        # --- Fuel burn ---
        Avion.Masse.burn_fuel(dt)

        # --- Mise à jour avion ---
        Avion.Add_dh(dh)
        Avion.Add_dl(dl)
        Avion.setTAS_t(TAS)
        Avion.setMach_t(Mach)
        Avion.setCAS_t(CAS)


        # --- Stockage historique ---
        self.history["h"].append(h)
        self.history["l"].append(l)
        # self.history["t"].append(t)
        self.history["V_CAS"].append(CAS)
        self.history["V_true"].append(TAS)
        self.history["Mach"].append(Mach)
        self.history["Cz"].append(Cz)
        self.history["Cx"].append(Cx)
        self.history["Vz"].append(Vz)
        self.history["Vx"].append(Vx)
        self.history["F_N"].append(F_N)
        self.history["SFC"].append(SFC)
        self.history["FB"].append(Avion.Masse.getFuelBurned())
        self.history["m"].append(Avion.Masse.getCurrentMass())


# --- Phase 3 : Réduction de vitesse en plateau à 250 kt ---
def Descente_Phase3(self, Avion: Avion, Atmosphere: Atmosphere, h_const, dt=1.0):
    """
    Phase 3 : Décélération en palier, on fixe l'altitude à 10000ft et on passe la vitesse à Min CAS

    Arguments :
    h_const : altitude constante, après phase 2 (UNITE)
    l_start : distance initiale, après phase 2 (UNITE)
    t_start : temps initial, après phase 2 (UNITE)
    dt      : pas de temps (s)
    """

    # --- Conditions initiales ---
    h = Avion.geth()
    l = Avion.getl()
    Gamma = Constantes.gamma

    # --- CAS initiale (issue phase 2) ---
    CAS = Avion.getCAS() # * Constantes.conv_kt_mps  # kt -> m/s

    # --- Atmosphère --- #NB : on peut calculer les conditions atm en dehors de la boucle car, l'altitude étant constante, les conditions reste les mêmes à chaque pas de temps
    Atmosphere.CalculateRhoPT(h)
    P_t = Atmosphere.getP_t()
    T_t = Atmosphere.getT_t()

    # --- CAS cible (250 kt) ---
    CAS_target = 250.0 * Constantes.conv_kt_mps #PEUT ETRE LE FIXER DANS LES CONSTANTES

    Mach = Constantes.Convert_CAS_to_Mach(CAS,P_t)
    TAS = Mach * np.sqrt(Gamma * Constantes.r * T_t)

    while CAS > CAS_target: #On diminue la vitesse jusqu'à la valeur désirée
        #A noter que les nouvelles vitesses sont calculées en fin de boucle

        # --- Coefficients aérodynamiques ---
        Avion.Aero.CalculateCz(Mach)
        Cz = Avion.Aero.getCz()

        Avion.Aero.CalculateCxClimb_Simplified()
        Cx = Avion.Aero.getCx()

        finesse = Cz / Cx

        # --- Forces ---
        Rx = Avion.Masse.getCurrentWeight() / finesse  # cohérent avec finesse

        # --- Poussée moteur (idle / freinage) ---
        if self.moteur.get_Reseau_moteur() == 1:
            # À raffiner plus tard
            F_N = 0.0
            SFC = 0.0
        else:
            F_N = 0.0
            SFC = 0.0

        # --- Dynamique longitudinale simplifiée --- #c'est la force qui va faire ralentir l'appareil
        ax = (F_N - Rx) / Avion.Masse.getCurrentMass()

        # --- Mise à jour des vitesses ---
        TAS = max(TAS + ax * dt, 0.0) #Calcul de la nouvelle vitesse avec la resistance longitudinale

        # Recalcul CAS depuis Mach/TAS

        Mach = TAS / np.sqrt(Gamma * Constantes.r * T_t)

        CAS = Constantes.Convert_Mach_to_CAS(Mach,P_t)

        # --- Cinématique ---
        Vz = 0.0 #On vole en palier, donc on ne descend pas
        Vx = TAS

        dh = 0.0
        dl = Vx * dt

        l += dl
        self.l_descent += dl #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière

        # --- Fuel burn ---
        Avion.Masse.burn_fuel(dt)

        # --- Stockage historique ---
        self.history["h"].append(h)
        self.history["l"].append(l)
        # self.history["t"].append(t)
        self.history["V_CAS"].append(CAS)
        self.history["V_true"].append(TAS)
        self.history["Mach"].append(Mach)
        self.history["Cz"].append(Cz)
        self.history["Cx"].append(Cx)
        self.history["Vz"].append(Vz)
        self.history["Vx"].append(Vx)
        self.history["F_N"].append(F_N)
        self.history["SFC"].append(SFC)
        self.history["FB"].append(Avion.Masse.getFuelBurned())
        self.history["m"].append(Avion.Masse.getCurrentMass())


# --- Phase 4 : Descente finale jusqu'à h_final ---
def Descente_Phase4(self, Avion: Avion, Atmosphere: Atmosphere, h_final, dt=1.0):
    """
    Phase 4 : descente à CAS constante (250 kt) jusqu'à l'altitude finale de 1500ft

    h_start : altitude initiale, récupérée à la fin de la phase 3 en UNITE
    h_final : altitude finale, fixée par la mission (1500ft)
    l_start : distance franchie initiale, récupérée à la fin de la phase 3 en UNITE
    t_start : temps initial, récupérée à la fin de la phase 3 en UNITE
    dt      : pas de temps (s)
    """

    h = Avion.geth()
    l = Avion.getl()

    # --- CAS imposée ---
    CAS = 250.0 * Constantes.conv_kt_mps  # kt → m/s Ajouter dans les constantes le 250kt ?

    while h > h_final:

        # --- Atmosphère ---
        Atmosphere.CalculateRhoPT(h)
        P_t = Atmosphere.getP_t()
        T_t = Atmosphere.getT_t()

        # --- Mach depuis CAS ---
        Mach = Constantes.Convert_CAS_to_Mach(CAS,P_t)

        # --- TAS ---
        TAS = Mach * np.sqrt(Constantes.gamma * Constantes.r * T_t)

        # --- Aérodynamique ---
        Avion.Aero.CalculateCz(Mach)
        Cz = Avion.Aero.getCz()

        Avion.Aero.CalculateCxDescent_Simplified()
        Cx = Avion.Aero.getCx()

        finesse = Cz / Cx

        # --- Poussée moteur ---
        F_N = 0.0  # idle en descente (à affiner plus tard)
        SFC = 0.0

        # --- Résistance ---
        Rx = Avion.Masse.getCurrentWeight() / finesse

        # --- Pente ---
        pente = np.arcsin((F_N - Rx) / Avion.Masse.getCurrentWeight())

        # --- Vitesses ---
        Vz = TAS * np.sin(pente)
        Vx = TAS * np.cos(pente)

        # --- Intégration ---
        dh = Vz * dt
        dl = Vx * dt

        h += dh
        l += dl
        self.l_descent += dl #Calcule de la distance nécessaire à la descente afin d'avoir le critère d'arrêt de la croisière

        # --- Fuel burn ---
        Avion.Masse.burn_fuel(dt)

        # --- Historique ---
        self.history["h"].append(h)
        self.history["l"].append(l)
        # self.history["t"].append(t)
        self.history["V_CAS"].append(CAS)
        self.history["V_true"].append(TAS)
        self.history["Mach"].append(Mach)
        self.history["Cz"].append(Cz)
        self.history["Cx"].append(Cx)
        self.history["Vz"].append(Vz)
        self.history["Vx"].append(Vx)
        self.history["F_N"].append(F_N)
        self.history["SFC"].append(SFC)
        self.history["FB"].append(Avion.Masse.getFuelBurned())
        self.history["m"].append(Avion.Masse.getCurrentMass())

