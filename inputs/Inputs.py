class Inputs:

    # =====================
    # Fichiers des paramètres avions
    # =====================
    csv_folder = "csv_avions" #Dossier de stockage des fichiers csv
    nom_fichier_csv = "Airbus_A320.csv" #Fichier csv des paramètres avions

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

    
