import customtkinter as ctk

class OngletMission(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app # Permet d'accéder à app.vars et app.add_field
        
        # --- Recopie ici le contenu de build_tab_mission ---
        f_global = ctk.CTkFrame(self)
        f_global.pack(fill="x", pady=5)
        # etc...

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