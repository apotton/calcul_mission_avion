import os

class Inputs:
    # =====================
    # Fichiers des paramètres avions
    # =====================
    csv_folder = "avions" #Dossier de stockage des fichiers csv
    nom_fichier_csv = "Airbus_A320.csv" #Fichier csv des paramètres avions

    # =====================
    # Fichier des moteurs
    # =====================
    py_folder = "moteurs"
    nom_fichier_py = "cfm56.py"

    # =====================
    # Paramètres généraux
    # =====================
    Aero_simplified = True

    # =====================
    # MISSION
    # =====================
    m_payload = 18000
    l_mission = 1000000 # m

    # =====================
    # PAS DE TEMPS
    # =====================
    dt_climb = 1.0      # s
    dt_cruise = 60.0    # s
    dt_descent = 1.0    # s

    # =====================
    # MONTEE
    # =====================
    h_initial_ft = 1500.0      # ft
    h_accel_ft = 10000.0        # ft
    CAS_below_10000_mont_kt = 250.0  # kt 
    CAS_climb_kt = None         # kt (None -> KVMO)
    Mach_climb = 0.78

    # =====================
    # CROISIERE
    # =====================
    h_cruise_init = 35000       # ft
    Mach_cruise = 0.78
    step_climb_ft = 2000.0      # ft
    RRoC_min_ft_min = 300.0     # ft/min
    pressurisation_ceiling_ft = 40000.0

    # =====================
    # DESCENTE
    # =====================
    CAS_max_descent_kt = None   # kt (None -> KVMO)
    CAS_below_10000_desc_kt = 250.0  # kt
    h_decel_ft = 10000.0
    h_final_ft = 1500.0

    # =====================
    # Critère de diversion
    # =====================
    Final_climb_altitude_diversion_ft = 25000
    Range_diversion_NM = 200
    Mach_cruise_div = 0.65
    
    # =====================
    # Critère Holding
    # =====================
    KCAS_holding = 300 # kt
    Time_holding = 30  # min
    
    # =====================
    # Critère contingency
    # =====================
    Contingency = 5 # en %

    # =====================
    # Paramètres de l'environnement
    # =====================
    Vw = 0                   # kt
    DISA_Cruise = 0          #K
    DISA_sub_Cruise = 0      #K

    # =====================
    # VALIDATION
    # =====================
    
    @staticmethod
    def validate():
        assert Inputs.Mach_climb < 0.9, "Mach climb incohérent"
        assert Inputs.h_final_ft < Inputs.h_decel_ft, "Altitude finale supérieur à l'altitude de pallier en descente"
        assert Inputs.h_initial_ft < Inputs.h_accel_ft, "Altitude initiale supérieur à l'altitude de pallier en montée"
        assert Inputs.CAS_below_10000_mont_kt < 250, "Vitesse de montée sous 10 000ft trop élevée"
        assert Inputs.CAS_below_10000_desc_kt < 250, "Vitesse de descente sous 10 000ft trop élevée"

    @staticmethod
    def getAirplaneFile():
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        csv_folder = os.path.join(data_folder, "avions") #Ajoute le terme "csv_avions" au Directory précédent pour se rendre dans le Directory des fichiers csv à lire
        full_path = os.path.join(csv_folder, Inputs.nom_fichier_csv) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path
    
    @staticmethod
    def getEngineFile():
        ''' Retourne le chemin complet du fichier csv de l'avion à partir du nom du fichier et du dossier défini dans les variables de classe '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Remonte de deux crans à partir du fichier actuel pour arriver à la racine du projet
        data_folder = os.path.join(base_dir, "data") #Ajoute le terme "data" au Directory précédent pour se rendre dans le Directory data
        py_folder = os.path.join(data_folder, "moteurs") #Ajoute le terme "csv_moteurs" au Directory précédent pour se rendre dans le Directory des fichiers csv de moteurs à lire
        full_path = os.path.join(py_folder, Inputs.nom_fichier_py) #Ajoute le nom du fichier csv au Directory afin de le compléter
        
        return full_path