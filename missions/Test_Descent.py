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
            "h": [],
            "l": [],
            "t": [],
            "V_CAS": [],
            "V_true": [],
            "Mach": [],
            "Cz": [],
            "Cx": [],
            "F_N": [],
            "SFC": [],
            "FB": [],
            "m": []
        }

    # --- Phase 1 : Ajustement vitesse à Max CAS ---
    def phase1(self, h_start, l_start, t_start, dt=1.0): #Ajuste la vitesse avant d'initier la descente réelle
        """
        Ajuste l'avion pour atteindre la vitesse maximale autorisée en CAS (Vmax_CAS).
        La descente commence à l'altitude h_start.

        Arguments :
        h_start : altitude initiale en mètres
        dt      : pas de temps pour la simulation en secondes (par défaut 1 s)
        """
        h = h_start
        l = l_start #ATTENTION A PRENDRE DU CALCUL DE CROISIERE PRECEDENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        t = t_start

        # CAS max en m/s
        V_CAS_max = self.avion.getKVMO() * Constantes.conv_kt_mps  # kt -> m/s
        CAS = 0.0  # CAS initial
        Mach = 0.0 #ATTENTION RECUPERER DE LA PHASE DE CROISIERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TAS = 0.0


        while CAS < V_CAS_max:
            # --- Atmosphère ---
            self.atmosphere.getRhoPT(h) #ATTENTION TRES MAUVAIS CHOIX DE NOM POUR ATM CE DEVRAIT ETRE CALCULATE RHO PT

            rho_t = self.atmosphere.getRho_t()
            P_t = self.atmosphere.getP_t()
            T_t = self.atmosphere.getT_t()

            # --- Mach et TAS --- ##UTILISER LES FONCTIONS CREES DANS MON CODE PERSO CONVERT MACH TO CAS
            Gamma = Constantes.gamma
            Delta_p = P_t*(((Gamma-1)/2*Mach**2+1)**(Gamma/(Gamma-1))-1)
            CAS = np.sqrt(2*Gamma*Constantes.r*(Constantes.T0_K)/(Gamma-1)*((1+Delta_p/Constantes.p0_Pa)**(0.4/Gamma)-1))

            TAS = Mach*np.sqrt(1.4*Constantes.r*T_t)

            # --- Cz et Cx ---
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


    # --- Phase 2 : Descente à V constante jusqu'à 10000 ft ---
    def phase2(self, h_start, h_end, l_start, t_start, dt=1.0):
        """
        Phase 2 : Descente réelle à CAS constant

        Arguments :
        h_start : altitude initiale (m)
        h_end   : altitude finale de la phase (m)
        l_start : distance initiale (m)
        t_start : temps initial (s)
        dt      : pas de temps (s)
        """

        # --- Conditions initiales ---
        h = h_start
        l = l_start
        t = t_start

        # --- CAS imposée ---
        CAS = self.avion.getCAS_descent() * Constantes.conv_kt_mps  # kt -> m/s N'EXISTE PAS!!!!!!!!!

        Mach = 0.0
        TAS  = 0.0

        while h > h_end:

            # --- Atmosphère ---
            self.atmosphere.getRhoPT(h) #NOM A CHANGER

            rho_t = self.atmosphere.getRho_t()
            P_t   = self.atmosphere.getP_t()
            T_t   = self.atmosphere.getT_t()

            # --- Conversion CAS -> Mach ---
            Gamma = Constantes.gamma

            Delta_p = Constantes.p0_Pa * (
                (1 + (Gamma - 1) / 2 * CAS**2 / (Gamma * Constantes.r * Constantes.T0_K)) #A CHANGER PAR LA FONCTION CODER DANS MON MAIN
                ** (Gamma / (Gamma - 1)) - 1
            )

            Mach = np.sqrt(
                2 / (Gamma - 1)
                * ((Delta_p / P_t + 1) ** ((Gamma - 1) / Gamma) - 1) #A CHANGER PAR LA FONCTION CODER DANS MON MAIN CONVERT CAS TO MACH
            )

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

            Vz = TAS * np.sin(pente)   # négatif
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
        Phase 3 : Décélération en palier (ex : 10000 ft -> 250 kt)

        Arguments :
        h_const : altitude constante (m)
        l_start : distance initiale (m)
        t_start : temps initial (s)
        dt      : pas de temps (s)
        """

        # --- Conditions initiales ---
        h = h_const
        l = l_start
        t = t_start

        # --- CAS initiale (issue phase 2) ---
        CAS = self.history["V_CAS"][-1]

        # --- CAS cible (250 kt) ---
        CAS_target = 250.0 * Constantes.conv_kt_mps

        Mach = 0.0
        TAS  = 0.0

        # --- Atmosphère --- ##ALTITUDE CONSTANTE DONC CONDITIONS ATM CONSTANTES
        self.atmosphere.getRhoPT(h)

        rho_t = self.atmosphere.getRho_t()
        P_t   = self.atmosphere.getP_t()
        T_t   = self.atmosphere.getT_t()

        # --- Conversion CAS -> Mach --- ##SUREMENT MIEUX DE PASSER LES CONSTANTES EN DEHORS DE LA FONCTION POUR PAS LES RECALCULER H24
        Gamma = Constantes.gamma

        while CAS > CAS_target:

            Delta_p = Constantes.p0_Pa * (
                (1 + (Gamma - 1) / 2 * CAS**2 / (Gamma * Constantes.r * Constantes.T0_K)) #REMPLACER PAR LA FONCTION CAS TO MACH
                ** (Gamma / (Gamma - 1)) - 1
            )

            Mach = np.sqrt(
                2 / (Gamma - 1)
                * ((Delta_p / P_t + 1) ** ((Gamma - 1) / Gamma) - 1)
            )

            # --- TAS ---
            TAS = Mach * np.sqrt(Gamma * Constantes.r * T_t)

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

            # --- Dynamique longitudinale simplifiée --- ##ON A PAS DE PENTE ICI CAR EN PALIER
            ax = (F_N - Rx) / self.masse.getCurrentMass()

            # --- Mise à jour des vitesses ---
            TAS = max(TAS + ax * dt, 0.0)

            # Recalcul CAS depuis Mach/TAS

            Mach = TAS / np.sqrt(Gamma * Constantes.r * T_t)

            Delta_p = P_t * (((Gamma - 1) / 2 * Mach**2 + 1) ** (Gamma / (Gamma - 1)) - 1)

            CAS = np.sqrt(
                2 * Gamma * Constantes.r * Constantes.T0_K / (Gamma - 1)
                * ((1 + Delta_p / Constantes.p0_Pa) ** (0.4 / Gamma) - 1)
            ) ## A REMPLACER PAR CONVERT MACH TO CAS

            # --- Cinématique ---
            Vz = 0.0
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
        Phase 4 : descente à CAS constante (250 kt) jusqu'à l'altitude finale.

        h_start : altitude initiale (m)
        h_final : altitude finale (m)
        dt      : pas de temps (s)
        """

        h = h_start
        l = l_start
        t = t_start

        # --- CAS imposée ---
        CAS_target = 250.0 * Constantes.conv_kt_mps  # kt → m/s

        Gamma = Constantes.gamma

        while h > h_final:

            # --- Atmosphère ---
            self.atmosphere.getRhoPT(h)
            P_t = self.atmosphere.getP_t()
            T_t = self.atmosphere.getT_t()

            # --- Mach depuis CAS ---
            Delta_p = Constantes.p0_Pa * (
                (1 + (Gamma - 1) / 2 * CAS**2 / (Gamma * Constantes.r * Constantes.T0_K)) #REMPLACER PAR LA FONCTION CAS TO MACH
                ** (Gamma / (Gamma - 1)) - 1
            )

            Mach = np.sqrt(
                2 / (Gamma - 1)
                * ((Delta_p / P_t + 1) ** ((Gamma - 1) / Gamma) - 1)
            )

            ##Mach = convert_CAS_to_Mach(CAS_target, h)

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
            self.history["V_CAS"].append(CAS_target)
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

