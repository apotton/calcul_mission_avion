import os

class Inputs:
    # =====================
    # Fichiers des paramètres avions
    # =====================
    csv_folder = "avions" # Dossier de stockage des fichiers csv
    nom_fichier_csv = "Airbus_A320.csv" # Fichier csv des paramètres avions

    # =====================
    # Fichier des moteurs
    # =====================
    py_folder = "moteurs"
    nom_fichier_py = "cfm56.py"

    # =====================
    # Paramètres généraux
    # =====================
    AeroSimplified = False
    dtClimb = 10.      # s
    dtCruise = 60.0    # s
    dtDescent = 10.    # s
    maxIter = 10  # Nombre d'itérations max
    precision = 1 # %

    # =====================
    # MISSION
    # =====================
    m_payload = 18000   # kg
    l_mission_NM = 1000  # NM

    # =====================
    # MONTEE
    # =====================
    hInit_ft = 1500.0      # ft
    hAccel_ft = 10000.0        # ft
    CAS_below_10000_mont_kt = 250.0  # kt
    Mach_climb = 0.78

    # =====================
    # CROISIERE
    # =====================
    # Type de croisière
    cruiseType = "Mach_SAR" # Ou "Alt_SAR", "Mach_SAR", "CI"

    # Croisière Alt Mach (et toutes les autres)
    hCruise_ft = 31000       # ft
    MachCruise = 0.78
    
    # Croisière Mach SAR
    stepClimb_ft = 2000.0      # ft
    RRoC_min_ft = 300.0     # ft/min
    cruiseClimbInit = 20 # % de la distance mission (Moment à partir duquel on peut chosir de monter)
    cruiseClimbStop = 80 # % de la distance mission (Moment jusqu'auquel on peut monter)

    # Croisière alt SAR (dégradation du SAR)
    kSARcruise = 1 # %

    # =====================
    # DESCENTE
    # =====================
    CAS_below_10000_desc_kt = 250.0  # kt
    hDecel_ft = 10000.0 # ft, altitude finale de maxCAS
    hFinal_ft = 1500.0 # ft, altitude finale mission

    # =====================
    # Critère de diversion
    # =====================
    cruiseDiversionAlt_ft = 25000 # ft, altitude de croisière diversion
    rangeDiversion_NM = 200 # nm, longueur de la diversion
    MachCruiseDiversion = 0.65 # Mach de croisière diversion
    
    # =====================
    # Critère Holding
    # =====================
    Time_holding = 30  # min
    
    # =====================
    # Critère contingency
    # =====================
    Contingency = 5/100

    # =====================
    # Paramètres de l'environnement
    # =====================
    Vw = 0                   # kt
    DISA_Cruise = 0          # K
    DISA_sub_Cruise = 0      # K

    # =====================
    # Coefficients de déformation du réseau moteur
    # =====================
    cCz = 1             # Coefficient sur le coefficient de portance
    cCx = 1             # Coefficient sur le coefficient de traînée
    cFF_climb = 1       # Coefficient sur le fuel flow (montée)
    cFF_cruise = 1      # Coefficient sur le fuel flow (croisière)
    cFF_descent = 1     # Coefficient sur le fuel flow (descente)
    cFN_climb = 1       # Coefficient sur la poussée totale (montée)
    cFN_cruise = 1      # Coefficient sur la poussée totale (croisière: n'affecte pas la poussée mais la leecture de la SFC)
    cFN_descent = 1     # Coefficient sur la poussée totale (descente)
    
    # =====================
    # Input des calculs Point Performance
    # =====================
    SpeedType = "Mach"  # Soit Mach, soit  TAS (kt), soit CAS (kt)
    Speed = 0.78        # Valeur de la vitesse
    altPP_ft = 38_000.   # Altitude (ft)
    massPP = 60_000.     # Masse totale (kg)
    DISA_PP = 0.0         # Delta ISA, différence de température avec l'atmosphère standard (°C)
    
    @staticmethod
    def validate():
        assert Inputs.Mach_climb < 0.9, "Mach climb incohérent"
        assert Inputs.hFinal_ft < Inputs.hDecel_ft, "Altitude finale supérieur à l'altitude de pallier en descente"
        assert Inputs.hInit_ft < Inputs.hAccel_ft, "Altitude initiale supérieur à l'altitude de pallier en montée"
        assert Inputs.CAS_below_10000_mont_kt < 250, "Vitesse de montée sous 10 000ft trop élevée"
        assert Inputs.CAS_below_10000_desc_kt < 250, "Vitesse de descente sous 10 000ft trop élevée"

    @staticmethod
    def getAirplaneFile():
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe. '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        csv_folder = os.path.join(data_folder, "avions") #Ajoute le terme "csv_avions" au Directory précédent pour se rendre dans le Directory des fichiers csv à lire
        full_path = os.path.join(csv_folder, Inputs.nom_fichier_csv) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path
    
    @staticmethod
    def getEngineFile():
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe. '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        py_folder = os.path.join(data_folder, "moteurs") #Ajoute le terme "csv_moteurs" au Directory précédent pour se rendre dans le Directory des fichiers csv de moteurs à lire
        full_path = os.path.join(py_folder, Inputs.nom_fichier_py) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path
    
    @staticmethod
    def loadCSVFile(csv_path):
        pass
        # A coder