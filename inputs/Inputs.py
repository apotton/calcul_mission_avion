import csv
import os

class Inputs:
    def __init__(self):
        # =====================
        # Fichiers des paramètres avions
        # =====================
        self.csv_folder      = "avions"              # Dossier de stockage des fichiers csv
        self.nom_fichier_csv = "Airbus_A320.csv"     # Fichier csv des paramètres avions

        # =====================
        # Fichier des moteurs
        # =====================
        self.py_folder      = "moteurs"
        self.nom_fichier_py = "cfm56.py"

        # =====================
        # Paramètres généraux
        # =====================
        self.AeroSimplified = False
        self.dtClimb        = 10.    # s
        self.dtCruise       = 60.    # s
        self.dtDescent      = 10.    # s
        self.maxIter        = 20     # Nombre d'itérations max
        self.precision      = 1      # %

        # =====================
        # MISSION
        # =====================
        self.m_payload = 20000   # kg
        self.l_mission_NM = 1500  # NM

        # =====================
        # MONTEE
        # =====================
        self.hInit_ft   = 1500.0         # ft
        self.hAccel_ft  = 10000.0        # ft
        self.CAS_below_10000_mont_kt = 250.0  # kt
        self.Mach_climb = 0.78

        # =====================
        # CROISIERE
        # =====================
        # Type de croisière
        self.cruiseType = "Alt_Mach" # "Alt_Mach", "Alt_SAR", "Mach_SAR" ou "CI"


        # Croisière Alt Mach (et toutes les autres)
        self.hCruise_ft = 38000       # ft
        self.MachCruise = 0.78
        
        # Croisière Mach SAR
        self.stepClimb_ft = 2000.0      # ft
        self.RRoC_min_ft = 300.0        # ft/min
        self.cruiseClimbInit = 20       # % de la distance mission (Moment à partir duquel on peut chosir de monter)
        self.cruiseClimbStop = 80       # % de la distance mission (Moment jusqu'auquel on peut monter)

        # Croisière alt SAR (dégradation du SAR)
        self.kSARcruise = 1 # %

        # Croisière CI (Cost Index)
        self.CI_kg_min = 0 # kg/min

        # =====================
        # DESCENTE
        # =====================
        self.CAS_below_10000_desc_kt = 250.0  # kt
        self.hDecel_ft = 10000.0 # ft, altitude finale de maxCAS
        self.hFinal_ft = 1500.0 # ft, altitude finale mission

        # =====================
        # Critère de diversion
        # =====================
        self.cruiseDiversionAlt_ft = 25000  # ft, altitude de croisière diversion
        self.rangeDiversion_NM = 200        # NM, longueur de la diversion
        self.MachCruiseDiversion = 0.65     # Mach de croisière diversion
        
        # =====================
        # Critère Holding
        # =====================
        self.Time_holding = 30  # min
        
        # =====================
        # Critère contingency
        # =====================
        self.Contingency = 5

        # =====================
        # Paramètres de l'environnement
        # =====================
        self.Vw = 0                   # kt
        self.DISA_Cruise = 0          # K
        self.DISA_sub_Cruise = 0      # K

        # =====================
        # Coefficients de déformation du réseau moteur
        # =====================
        self.cCz            = 1     # Coefficient sur le coefficient de portance
        self.cCx            = 1     # Coefficient sur le coefficient de traînée
        self.cFF_climb      = 1     # Coefficient sur le fuel flow (montée)
        self.cFF_cruise     = 1     # Coefficient sur le fuel flow (croisière)
        self.cFF_descent    = 1     # Coefficient sur le fuel flow (descente)
        self.cFN_climb      = 1     # Coefficient sur la poussée totale (montée)
        self.cFN_cruise     = 1     # Coefficient sur la poussée totale (croisière: n'affecte pas la poussée mais la leecture de la SFC)
        self.cFN_descent    = 1     # Coefficient sur la poussée totale (descente)
        
        # =====================
        # Input des calculs Point Performance
        # =====================
        self.SpeedType  = "Mach"    # Soit Mach, soit TAS (kt), soit CAS (kt)
        self.Speed      = 0.78      # Valeur de la vitesse
        self.altPP_ft   = 38_000.   # Altitude (ft)
        self.massPP     = 60_000.   # Masse totale (kg)
        self.DISA_PP    = 0.0       # Delta ISA, différence de température avec l'atmosphère standard (°C)
    

    def validate(self):
        if self.Mach_climb > 0.9:
            print("Mach climb incohérent")

        if self.hFinal_ft > self.hDecel_ft:
            print("Altitude finale supérieur à l'altitude de pallier en descente")

        if self.hInit_ft > self.hAccel_ft:
            print("Altitude initiale supérieur à l'altitude de pallier en montée")

        if self.CAS_below_10000_mont_kt > 250:
            print("Vitesse de montée sous 10 000ft trop élevée (>250kt)")

        if self.CAS_below_10000_desc_kt > 250:
            print("Vitesse de descente sous 10 000ft trop élevée (>250kt)")

        if (abs(self.Mach_climb - self.MachCruise) > 0.01):
            print("Mach de fin de montée et Mach de début de croisière sont éloignées")

    def getAirplaneFile(self):
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe. '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        csv_folder = os.path.join(data_folder, "avions") #Ajoute le terme "csv_avions" au Directory précédent pour se rendre dans le Directory des fichiers csv à lire
        full_path = os.path.join(csv_folder, self.nom_fichier_csv) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path
    
    def getEngineFile(self):
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe. '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        py_folder = os.path.join(data_folder, "moteurs") #Ajoute le terme "csv_moteurs" au Directory précédent pour se rendre dans le Directory des fichiers csv de moteurs à lire
        full_path = os.path.join(py_folder, self.nom_fichier_py) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path
    
    def loadCSVFile(self, csv_path):

         # Si fichier non trouvé
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"Le fichier {csv_path} n'a pas été trouvé. Veuillez vérifier le chemin et le nom du fichier CSV de l'avion.")

        # Lecture CSV
        with open(csv_path, mode='r', encoding='utf-8') as f:
            # Ouverture du fichier
            lecteur = csv.reader(f, delimiter=';')

            # Lecture ligne par ligne
            for ligne in lecteur:

                if len(ligne) == 2:
                    # Récupération des noms de paramètre (clé) et de leur valeur
                    cle, valeur = ligne

                    # Conversion en float si possible
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        valeur = str(valeur)
                        # Gestion de AeroSimplified
                        if valeur == "True":
                            valeur = True
                        elif valeur == "False":
                            valeur = False
                        pass

                    # Attribution dynamique des attributs
                    setattr(self, cle, valeur)