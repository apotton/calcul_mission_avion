import customtkinter as ctk

class OngletMission(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app # Permet d'accéder à app.vars et app.add_field

        tab = ctk.CTkScrollableFrame(self.app.tabview.tab("Mission"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        # Globaux 
        f_global = ctk.CTkFrame(tab)
        f_global.pack(fill="x", pady=5)
        f_global.grid_columnconfigure((0, 7), weight=1)
        
        self.app.add_field(f_global, "Payload", "m_payload", "18000", "kg", row=0, col=1)
        self.app.add_field(f_global, "Distance", "l_mission_NM", "1000", "nm", row=0, col=4)

        # Montée
        f_climb = ctk.CTkFrame(tab)
        f_climb.pack(fill="x", pady=5)
        f_climb.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_climb, text="Montée", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.app.add_field(f_climb, "Altitude Initiale", "hInit_ft", "1500.0", "ft", row=1, col=1)
        self.app.add_field(f_climb, "Altitude Accel.", "hAccel_ft", "10000.0", "ft", row=2, col=1)
        self.app.add_field(f_climb, "CAS < 10000ft", "CAS_below_10000_mont_kt", "250.0", "kt", row=3, col=1)
        self.app.add_field(f_climb, "Mach Climb", "Mach_climb", "0.78", "", row=4, col=1)

        # Croisière (Dynamique)
        self.f_cruise = ctk.CTkFrame(tab)
        self.f_cruise.pack(fill="x", pady=5)
        self.f_cruise.grid_columnconfigure((0, 2), weight=1)
        ctk.CTkLabel(self.f_cruise, text="Croisière", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, pady=5)
        
        self.app.vars["cruiseType"] = ctk.StringVar(value="Alt_Mach")
        cb_cruise = ctk.CTkComboBox(self.f_cruise, variable=self.app.vars["cruiseType"], values=["Alt_Mach", "Alt_SAR", "Mach_SAR", "CI"], command=self.app.update_cruise_fields, width=150)
        cb_cruise.grid(row=1, column=1, padx=10, pady=5)
        
        self.f_cruise_dyn = ctk.CTkFrame(self.f_cruise, fg_color="transparent")
        self.f_cruise_dyn.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Descente
        f_desc = ctk.CTkFrame(tab)
        f_desc.pack(fill="x", pady=5)
        f_desc.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_desc, text="Descente", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.app.add_field(f_desc, "CAS < 10000ft", "CAS_below_10000_desc_kt", "250.0", "kt", row=1, col=1)
        self.app.add_field(f_desc, "Altitude Decel.", "hDecel_ft", "10000.0", "ft", row=2, col=1)
        self.app.add_field(f_desc, "Altitude Finale", "hFinal_ft", "1500.0", "ft", row=3, col=1)

class OngletAutres(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app # Permet d'accéder à app.vars et app.add_field

        tab = ctk.CTkScrollableFrame(self.app.tabview.tab("Autres"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        f_div = ctk.CTkFrame(tab)
        f_div.pack(fill="x", pady=5)
        f_div.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_div, text="Diversion", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        app.add_field(f_div, "Altitude Croisière", "cruiseDiversionAlt_ft", "25000", "ft", row=1, col=1)
        app.add_field(f_div, "Distance", "rangeDiversion_NM", "200", "nm", row=2, col=1)
        app.add_field(f_div, "Mach Croisière", "MachCruiseDiversion", "0.65", "", row=3, col=1)

        f_hold = ctk.CTkFrame(tab)
        f_hold.pack(fill="x", pady=5)
        f_hold.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_hold, text="Environnement & Réserves", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        app.add_field(f_hold, "Temps Holding", "Time_holding", "30", "min", row=1, col=1)
        app.add_field(f_hold, "Contingency", "Contingency", "5", "%", row=2, col=1)
        app.add_field(f_hold, "Vitesse Vent Vw", "Vw", "0", "kt", row=3, col=1)
        app.add_field(f_hold, "DISA Croisière", "DISA_Cruise", "0", "K", row=4, col=1)
        app.add_field(f_hold, "DISA Sous Crois.", "DISA_sub_Cruise", "0", "K", row=5, col=1)

        # Grille face-à-face pour les coefficients
        f_coeff = ctk.CTkFrame(tab)
        f_coeff.pack(fill="x", pady=5)
        f_coeff.grid_columnconfigure((0, 7), weight=1) # Centrage
        ctk.CTkLabel(f_coeff, text="Coefficients Déformation Réseau", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=6, pady=5)
        
        app.add_field(f_coeff, "cCz (Portance)", "cCz", "1", "", row=1, col=1)
        app.add_field(f_coeff, "cCx (Traînée)", "cCx", "1", "", row=1, col=4)
        
        app.add_field(f_coeff, "cFF Climb", "cFF_climb", "1", "", row=2, col=1)
        app.add_field(f_coeff, "cFN Climb", "cFN_climb", "1", "", row=2, col=4)
        
        app.add_field(f_coeff, "cFF Cruise", "cFF_cruise", "1", "", row=3, col=1)
        app.add_field(f_coeff, "cFN Cruise", "cFN_cruise", "1", "", row=3, col=4)
        
        app.add_field(f_coeff, "cFF Descent", "cFF_descent", "1", "", row=4, col=1)
        app.add_field(f_coeff, "cFN Descent", "cFN_descent", "1", "", row=4, col=4)

class OngletOptions(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app # Permet d'accéder à app.vars et app.add_field

        tab = self.app.tabview.tab("Options")
        f_opt = ctk.CTkFrame(tab)
        f_opt.pack(fill="x", pady=5, padx=5)
        f_opt.grid_columnconfigure((0, 4), weight=1)
        
        self.app.add_field(f_opt, "dt Montée", "dtClimb", "10.0", "s", row=0, col=1)
        self.app.add_field(f_opt, "dt Croisière", "dtCruise", "60.0", "s", row=1, col=1)
        self.app.add_field(f_opt, "dt Descente", "dtDescent", "10.0", "s", row=2, col=1)
        self.app.add_field(f_opt, "Itérations Max", "maxIter", "10", "", row=3, col=1)
        self.app.add_field(f_opt, "Précision", "precision", "1", "%", row=4, col=1)
        
        # Ajout Aérodynamique simplifiée
        self.app.vars["AeroSimplified"] = ctk.BooleanVar(value=False)
        cb_aero = ctk.CTkCheckBox(f_opt, text="Aérodynamique simplifiée", variable=self.app.vars["AeroSimplified"])
        cb_aero.grid(row=5, column=1, columnspan=3, pady=10)

class OngletPP(ctk.CTkFrame):
    def __init__(self, master, app):
            super().__init__(master, fg_color="transparent")
            self.app = app # Permet d'accéder à app.vars et app.add_field
            
            tab = self.app.tabview.tab("Point Performance")
            f_pp = ctk.CTkFrame(tab)
            f_pp.pack(fill="x", pady=5, padx=5)
            f_pp.grid_columnconfigure((0, 4), weight=1)
            
            self.app.vars["SpeedType"] = ctk.StringVar(value="Mach")
            ctk.CTkLabel(f_pp, text="Type Vitesse").grid(row=0, column=1, padx=10, pady=5, sticky="e")
            ctk.CTkComboBox(f_pp, variable=self.app.vars["SpeedType"], values=["Mach", "TAS", "CAS"], command=self.app.update_pp_speed_label, width=120).grid(row=0, column=2, padx=5, pady=5)
            
            self.lbl_unit_speed_pp = ctk.CTkLabel(f_pp, text="Mach", width=30, anchor="w")
            self.app.add_field(f_pp, "Vitesse", "Speed", "0.78", "", row=1, col=1) # Unité gérée manuellement
            self.lbl_unit_speed_pp.grid(row=1, column=3, padx=(5, 10), pady=5, sticky="w")

            self.app.add_field(f_pp, "Altitude", "altPP_ft", "38000", "ft", row=2, col=1)
            self.app.add_field(f_pp, "Masse", "massPP", "60000", "kg", row=3, col=1)
            self.app.add_field(f_pp, "ΔISA", "DISA_PP", "0", "°C", row=4, col=1)

class OngletBatch(ctk.CTkFrame):
    def __init__(self, master, app):
            super().__init__(master, fg_color="transparent")
            self.app = app # Permet d'accéder à app.vars et app.add_field

            tab = self.app.tabview.tab("Batch")
            f_batch = ctk.CTkFrame(tab)
            f_batch.pack(fill="x", pady=5, padx=5)
            f_batch.grid_columnconfigure((0, 4), weight=1)

            ctk.CTkLabel(f_batch, text="Configuration du calcul en rafale (Batch)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=(10, 15))

            self.app.add_field(f_batch, "Payloads (espace séparés)", "batch_payloads", "0 10000 18000 20000", "kg", row=1, col=1, width=200)
            self.app.add_field(f_batch, "Ranges (espace séparés)", "batch_ranges", "500 1000 1500", "nm", row=2, col=1, width=200)
