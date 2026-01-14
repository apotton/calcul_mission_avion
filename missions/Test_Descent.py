from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
import numpy as np

class Mission:
    def __init__(self, avion, moteur, masse, aero):
        self.avion = avion
        self.moteur = moteur
        self.masse = masse
        self.aero = aero

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

    # --- Phase 1 : Ajustement vitesse à Max CAS avec possibilité de descente libre---
    def phase1(self, h_start, l_start, t_start, Mach_start, dt=1.0):
        """
        Laisse l'avion initier une descente libre pour atteindre la vitesse maximale autorisée en CAS (Vmax_CAS) avant de passer à la phase 2

        Arguments :
        h_start : altitude initiale en mètres, récupérée en fin de croisière
        l_start : position en x initiale à cette phase (unité), récupérée en fin de croisière
        t_start : temps initiale à cette phase (unité), récupéré en fin de croisière
        Mach_start : Mach initial à cette phrase, récupéré en fin de croisière
        dt      : pas de temps pour la simulation en secondes (par défaut 1 s)
        """
        h = h_start
        l = l_start #ATTENTION A PRENDRE DU CALCUL DE CROISIERE PRECEDENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        t = t_start
        Gamma = Constantes.gamma #Coefficient de Laplace thermodynamique pour les conversions entre CAS, Mach et TAS 

        # CAS max en m/s
        CAS_max = self.avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s  Vitesse maximale de descente de l'avion
        CAS = 0.0  # Initialisation avant calcul à partir du Mach connu
        Mach = Mach_start #ATTENTION RECUPERER DE LA PHASE DE CROISIERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TAS = 0.0 # Initialisation avant calcul à partir du Mach connu


        while CAS < CAS_max: #On cherche à diminuer l'altitude h jusqu'à atteindre la vitesse CAS Max

            # --- Atmosphère --- Calcule des conditions atm à cet altitude afin d'extraire la température et la pression au temps t
            self.atmosphere.getRhoPT(h) #ATTENTION TRES MAUVAIS CHOIX DE NOM POUR ATM CE DEVRAIT ETRE CALCULATE RHO PT
            P_t = self.atmosphere.getP_t() #Pression au temps t, en UNITE
            T_t = self.atmosphere.getT_t() #Température au temps t, en K

            # --- Mach et TAS --- 
            CAS = Constantes.Convert_Mach_to_CAS(Mach,P_t) #Calcul du CAS à partir du Mach

            TAS = Mach*np.sqrt(Gamma*Constantes.r*T_t) #Calcul du TAS à partir du Mach

            # --- Cz et Cx --- Calcul des coefs aéro
            self.aero.CalculateCz(Mach)
            Cz = self.aero.getCz()

            self.aero.CalculateCxClimb_Simplified()  # ici on peut remplacer par CalculateCx si on veut le modèle complet
            Cx = self.aero.getCx()

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
            Rx = self.masse.getCurrentWeight() / finesse

            # --- Pente de descente ---
            pente = np.arcsin((F_N - Rx) / self.masse.getCurrentWeight())
            Vz = TAS * np.sin(pente)
            Vx = TAS * np.cos(pente)

            # --- Mise à jour des positions ---
            dh = Vz * dt
            dl = Vx * dt
            h += dh
            l += dl
            t += dt

            # --- Fuel burn ---
            self.masse.burn_fuel(dt) #Carburant consommé à ce pas de temps dt, on met à jour la masse de carburant 
        

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
            self.history["FB"].append(self.masse.getFuelBurned())
            self.history["m"].append(self.masse.getCurrentMass())


    # --- Phase 2 : Descente à V constante jusqu'à 10000 ft ---
    def phase2(self, h_start, h_end, l_start, t_start, dt=1.0):
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
        h = h_start
        l = l_start
        t = t_start
        Gamma = Constantes.gamma

        # --- CAS imposée ---
        CAS = self.avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s On descend à CAS fixé par la vitesse max de descente

        Mach = 0.0 #Initialisation de Mach et de TAS avant calcul à partir du CAS
        TAS  = 0.0

        while h > h_end:

            # --- Atmosphère ---
            self.atmosphere.getRhoPT(h) #NOM A CHANGER
            P_t   = self.atmosphere.getP_t()
            T_t = self.atmosphere.getT_t()

            # --- Conversion CAS -> Mach ---
            Mach = Constantes.Convert_CAS_to_Mach(CAS, P_t)

            # --- TAS ---
            TAS = Mach * np.sqrt(Gamma * Constantes.r * T_t)

            # --- Coefficients aérodynamiques ---
            self.aero.CalculateCz(Mach)
            Cz = self.aero.getCz()

            self.aero.CalculateCxClimb_Simplified()
            Cx = self.aero.getCx()

            finesse = Cz / Cx

            # --- Poussée moteur (idle en descente) ---
            if self.moteur.get_Reseau_moteur() == 1:
                # A MODIFIER PLUS TARD AVEC MODELE MOTEUR
                F_N = 0.0
                SFC = 0.0
            else:
                F_N = 0.0
                SFC = 0.0

            # --- Résistance ---
            Rx = self.masse.getCurrentWeight() / finesse

            # --- Pente de trajectoire ---
            pente = np.arcsin((F_N - Rx) / self.masse.getCurrentWeight())

            Vz = TAS * np.sin(pente)   # négatif car en descente
            Vx = TAS * np.cos(pente)

            # --- Mise à jour position ---
            dh = Vz * dt
            dl = Vx * dt

            h += dh
            l += dl
            t += dt

            # --- Fuel burn ---
            self.masse.burn_fuel(dt)

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
            self.history["FB"].append(self.masse.getFuelBurned())
            self.history["m"].append(self.masse.getCurrentMass())


    # --- Phase 3 : Réduction de vitesse en plateau à 250 kt ---
    def phase3(self, h_const, l_start, t_start, dt=1.0):
        """
        Phase 3 : Décélération en palier, on fixe l'altitude à 10000ft et on passe la vitesse à Min CAS

        Arguments :
        h_const : altitude constante, après phase 2 (UNITE)
        l_start : distance initiale, après phase 2 (UNITE)
        t_start : temps initial, après phase 2 (UNITE)
        dt      : pas de temps (s)
        """

        # --- Conditions initiales ---
        h = h_const
        l = l_start
        t = t_start
        Gamma = Constantes.gamma

        # --- CAS initiale (issue phase 2) ---
        CAS = self.history["V_CAS"][-1]

        # --- CAS cible (250 kt) ---
        CAS_target = 250.0 * Constantes.conv_kt_mps #PEUT ETRE LE FIXER DANS LES CONSTANTES

        Mach = Constantes.Convert_CAS_to_Mach
        TAS = Mach * np.sqrt(Gamma * Constantes.r * T_t)

        # --- Atmosphère --- #NB : on peut calculer les conditions atm en dehors de la boucle car, l'altitude étant constante, les conditions reste les mêmes à chaque pas de temps
        self.atmosphere.getRhoPT(h)
        P_t = self.atmosphere.getP_t()
        T_t = self.atmosphere.getT_t()

        while CAS > CAS_target: #On diminue la vitesse jusqu'à la valeur désirée
            #A noter que les nouvelles vitesses sont calculées en fin de boucle

            # --- Coefficients aérodynamiques ---
            self.aero.CalculateCz(Mach)
            Cz = self.aero.getCz()

            self.aero.CalculateCxClimb_Simplified()
            Cx = self.aero.getCx()

            finesse = Cz / Cx

            # --- Forces ---
            Rx = self.masse.getCurrentWeight() / finesse  # cohérent avec finesse

            # --- Poussée moteur (idle / freinage) ---
            if self.moteur.get_Reseau_moteur() == 1:
                # À raffiner plus tard
                F_N = 0.0
                SFC = 0.0
            else:
                F_N = 0.0
                SFC = 0.0

            # --- Dynamique longitudinale simplifiée --- #c'est la force qui va faire ralentir l'appareil
            ax = (F_N - Rx) / self.masse.getCurrentMass()

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
            t += dt

            # --- Fuel burn ---
            self.masse.burn_fuel(dt)

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
            self.history["FB"].append(self.masse.getFuelBurned())
            self.history["m"].append(self.masse.getCurrentMass())


    # --- Phase 4 : Descente finale jusqu'à h_final ---
    def phase4(self, h_start, l_start, t_start, h_final, dt=1.0):
        """
        Phase 4 : descente à CAS constante (250 kt) jusqu'à l'altitude finale de 1500ft

        h_start : altitude initiale, récupérée à la fin de la phase 3 en UNITE
        h_final : altitude finale, fixée par la mission (1500ft)
        l_start : distance franchie initiale, récupérée à la fin de la phase 3 en UNITE
        t_start : temps initial, récupérée à la fin de la phase 3 en UNITE
        dt      : pas de temps (s)
        """

        h = h_start
        l = l_start
        t = t_start
        Gamma = Constantes.gamma

        # --- CAS imposée ---
        CAS = 250.0 * Constantes.conv_kt_mps  # kt → m/s Ajouter dans les constantes le 250kt ?

        
        while h > h_final:

            # --- Atmosphère ---
            self.atmosphere.getRhoPT(h)
            P_t = self.atmosphere.getP_t()
            T_t = self.atmosphere.getT_t()

            # --- Mach depuis CAS ---
            Mach = Constantes.Convert_CAS_to_Mach(CAS,P_t)

            # --- TAS ---
            TAS = Mach * np.sqrt(Gamma * Constantes.r * T_t)

            # --- Aérodynamique ---
            self.aero.CalculateCz(Mach)
            Cz = self.aero.getCz()

            self.aero.CalculateCxDescent_Simplified()
            Cx = self.aero.getCx()

            finesse = Cz / Cx

            # --- Poussée moteur ---
            if self.moteur.get_Reseau_moteur() == 1:
                F_N = 0.0  # idle en descente (à affiner plus tard)
                SFC = 0.0
            else:
                F_N = 0.0
                SFC = 0.0

            # --- Résistance ---
            Rx = self.masse.getCurrentWeight() / finesse

            # --- Pente ---
            pente = np.arcsin((F_N - Rx) / self.masse.getCurrentWeight())

            # --- Vitesses ---
            Vz = TAS * np.sin(pente)
            Vx = TAS * np.cos(pente)

            # --- Intégration ---
            dh = Vz * dt
            dl = Vx * dt

            h += dh
            l += dl
            t += dt

            # --- Fuel burn ---
            self.masse.burn_fuel(dt)

            # --- Historique ---
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
            self.history["FB"].append(self.masse.getFuelBurned())
            self.history["m"].append(self.masse.getCurrentMass())

