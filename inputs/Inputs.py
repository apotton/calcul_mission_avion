class Inputs:
    def __init__(self):

        # =====================
        # Fichiers des paramètres avions
        # =====================
        self.csv_folder = "csv_avions" #Dossier de stockage des fichiers csv
        self.nom_fichier_csv = "Airbus_A320.csv" #Fichier csv des paramètres avions

        # =====================
        # PAS DE TEMPS
        # =====================
        self.dt_climb = 1.0      # s
        self.dt_cruise = 60.0    # s
        self.dt_descent = 1.0    # s

        # =====================
        # MONTEE
        # =====================
        self.h_initial_ft = 1500.0      # ft
        self.h_accel_ft = 10000.0        # ft
        self.CAS_below_10000_mont_kt = 250.0  # kt 
        self.CAS_climb_kt = None         # kt (None -> KVMO)
        self.Mach_climb = 0.78

        # =====================
        # CROISIERE
        # =====================
        self.Mach_cruise = 0.78
        self.step_climb_ft = 2000.0      # ft
        self.RRoC_min_ft_min = 300.0     # ft/min
        self.pressurisation_ceiling_ft = 40000.0

        # =====================
        # DESCENTE
        # =====================
        self.CAS_max_descent_kt = None   # kt (None -> KVMO)
        self.CAS_below_10000_desc_kt = 250.0  # kt
        self.h_decel_ft = 10000.0
        self.h_final_ft = 1500.0

    # =====================
    # GETTERS
    # =====================

    # Fichiers
    def get_csv_folder(self):
        return self.csv_folder

    def get_nom_fichier_csv(self):
        return self.nom_fichier_csv

    # Pas de temps
    def get_dt_climb(self):
        return self.dt_climb

    def get_dt_cruise(self):
        return self.dt_cruise

    def get_dt_descent(self):
        return self.dt_descent

    # Montée
    def get_h_initial_ft(self):
        return self.h_initial_ft

    def get_h_accel_ft(self):
        return self.h_accel_ft

    def get_CAS_below_10000_mont_kt(self):
        return self.CAS_below_10000_mont_kt

    def get_CAS_climb_kt(self):
        return self.CAS_climb_kt

    def get_Mach_climb(self):
        return self.Mach_climb

    # Croisière
    def get_Mach_cruise(self):
        return self.Mach_cruise

    def get_step_climb_ft(self):
        return self.step_climb_ft

    def get_RRoC_min_ft_min(self):
        return self.RRoC_min_ft_min

    def get_pressurisation_ceiling_ft(self):
        return self.pressurisation_ceiling_ft

    # Descente
    def get_CAS_max_descent_kt(self):
        return self.CAS_max_descent_kt

    def get_CAS_below_10000_desc_kt(self):
        return self.CAS_below_10000_desc_kt

    def get_h_decel_ft(self):
        return self.h_decel_ft

    def get_h_final_ft(self):
        return self.h_final_ft
    

    # =====================
    # VALIDATION
    # =====================

    def validate(self):
        assert self.Mach_climb < 0.9, "Mach climb incohérent"
        assert self.h_final_ft < self.h_decel_ft, "Altitude finale supérieur à l'altitude de pallier en descente"
        assert self.h_initial_ft < self.h_accel_ft, "Altitude initiale supérieur à l'altitude de pallier en montée"
        assert self.CAS_below_10000_mont_kt < 250, "Vitesse de montée sous 10 000ft trop élevée"
        assert self.CAS_below_10000_desc_kt < 250, "Vitesse de descente sous 10 000ft trop élevée"

    
