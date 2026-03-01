import customtkinter as ctk

def addField(app, parent, label, var_name, default_value, unit="", row=0, col=0, width=120):
    '''
    Fonction générale pour ajouter un champ numérique.
    
    :param app: Interface graphique
    :param parent: Objet graphique dans lequel le champ se situera
    :param label: Nom affiché de la variable
    :param var_name: Nom dans Inputs de la variable
    :param default_value: Valeur initiale
    :param unit: Unité affichée à droite du champ
    :param row: Ligne d'affichage
    :param col: Colonne d'affichage
    :param with: Largeur du champ
    '''
    # Pousse les éléments au centre
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(4, weight=1)

    # Affichage du nom de la variable
    ctk.CTkLabel(parent, text=label).grid(row=row, column=col, padx=(10, 5), pady=5, sticky="e")

    # Ajout dans le dictionnaire des variables
    if var_name not in app.vars or not isinstance(app.vars[var_name], (ctk.StringVar, ctk.BooleanVar)):
        app.vars[var_name] = ctk.StringVar(value=default_value)

    # Ajout du champ de remplissage
    ctk.CTkEntry(parent, textvariable=app.vars[var_name], width=width).grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")

    # Ajout de l'unité
    if unit: ctk.CTkLabel(parent, text=unit, width=30, anchor="w").grid(row=row, column=col+2, padx=(5, 10), pady=5, sticky="w")


class OngletMission(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        '''
        Onglet qui gère les variables générales de la mission (montée, croisière, descente).

        :param master: Onglet où insérer le contenu
        :param app: Interface graphique
        '''
        super().__init__(master, fg_color="transparent")
        self.app = app # Permet d'y accéder depuis updateCruiseFields

        # Création de l'onglets
        tab = ctk.CTkScrollableFrame(self.app.tabview.tab("Mission"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        # Création de l'espace où iront les champs
        f_global = ctk.CTkFrame(tab)
        f_global.pack(fill="x", pady=5)
        f_global.grid_columnconfigure((0, 7), weight=1)
        
        # Deux champs globaux côte à côte: Payload et distance
        addField(app, f_global, "Payload", "mPayload", "18000", "kg", row=0, col=1)
        addField(app, f_global, "Distance", "rangeMission_NM", "1000", "nm", row=0, col=4)

        # Montée
        f_climb = ctk.CTkFrame(tab)
        f_climb.pack(fill="x", pady=5)
        f_climb.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_climb, text="Montée", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        addField(app, f_climb, "Altitude Initiale", "hInit_ft", "1500.0", "ft", row=1, col=1)
        addField(app, f_climb, "Altitude Accel.", "hAccel_ft", "10000.0", "ft", row=2, col=1)
        addField(app, f_climb, "CAS < 10000ft", "CAS_below_10000_mont_kt", "250.0", "kt", row=3, col=1)
        addField(app, f_climb, "Mach Climb", "Mach_climb", "0.78", "", row=4, col=1)

        # Croisière (Dynamique)
        self.f_cruise = ctk.CTkFrame(tab)
        self.f_cruise.pack(fill="x", pady=5)
        self.f_cruise.grid_columnconfigure((0, 2), weight=1)
        ctk.CTkLabel(self.f_cruise, text="Croisière", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, pady=5)
        
        # Setup des différents types de croisière
        self.app.vars["cruiseType"] = ctk.StringVar(value="Alt_Mach")
        cb_cruise = ctk.CTkComboBox(self.f_cruise, variable=self.app.vars["cruiseType"], values=["Alt_Mach", "Alt_SAR", "Mach_SAR", "CI"], command= self.updateCruiseFields, width=150)
        cb_cruise.grid(row=1, column=1, padx=10, pady=5)
        
        self.f_cruise_dyn = ctk.CTkFrame(self.f_cruise, fg_color="transparent")
        self.f_cruise_dyn.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Descente
        f_desc = ctk.CTkFrame(tab)
        f_desc.pack(fill="x", pady=5)
        f_desc.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_desc, text="Descente", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        addField(app, f_desc, "CAS < 10000ft", "CAS_below_10000_desc_kt", "250.0", "kt", row=1, col=1)
        addField(app, f_desc, "Altitude Decel.", "hDecel_ft", "10000.0", "ft", row=2, col=1)
        addField(app, f_desc, "Altitude Finale", "hFinal_ft", "1500.0", "ft", row=3, col=1)
        self.updateCruiseFields()

    def updateCruiseFields(self, _=None):
        '''
        Change les inputs de la croisière selon le type sélectionné
        '''
        # Destruction de tous les champs déjà remplis
        for widget in self.f_cruise_dyn.winfo_children(): widget.destroy()
        c_type = self.app.vars["cruiseType"].get()

        # Champs présents tout le temps: Mach et altitude
        addField(self.app, self.f_cruise_dyn, "Altitude Croisière", "hCruise_ft", "38000", "ft", row=0, col=1)
        addField(self.app, self.f_cruise_dyn, "Mach Croisière", "MachCruise", "0.78", "", row=1, col=1)

        # Spécificités de chaque type de croisière
        if c_type in ["Mach_SAR", "CI"]:
            addField(self.app, self.f_cruise_dyn, "Step Climb", "stepClimb_ft", "2000.0", "ft", row=2, col=1)
            addField(self.app, self.f_cruise_dyn, "RRoC min", "RRoC_min_ft", "300.0", "ft/min", row=3, col=1)
            addField(self.app, self.f_cruise_dyn, "Init Montée", "cruiseClimbInit", "20", "% dist", row=4, col=1)
            addField(self.app, self.f_cruise_dyn, "Stop Montée", "cruiseClimbStop", "80", "% dist", row=5, col=1)
        elif c_type == "Alt_SAR":
            addField(self.app, self.f_cruise_dyn, "Dégradation SAR", "kSARcruise", "1", "%", row=2, col=1)
        if c_type == "CI":
            addField(self.app, self.f_cruise_dyn, "Cost Index", "CI_kg_min", "0", "kg/min", row=6, col=1)



class OngletAutres(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        '''
        Onglet qui gère les variables annexes à la mission (diversion, holding, coefficients).

        :param master: Onglet où insérer le contenu
        :param app: Interface graphique
        '''
        super().__init__(master, fg_color="transparent")
        tab = ctk.CTkScrollableFrame(app.tabview.tab("Autres"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        # Apparence de la section diversion
        f_div = ctk.CTkFrame(tab)
        f_div.pack(fill="x", pady=5)
        f_div.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_div, text="Diversion", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)

        # Champs de la diversion
        addField(app, f_div, "Altitude Croisière", "cruiseDiversionAlt_ft", "25000", "ft", row=1, col=1)
        addField(app, f_div, "Distance", "rangeDiversion_NM", "200", "nm", row=2, col=1)
        addField(app, f_div, "Mach Croisière", "MachCruiseDiversion", "0.65", "", row=3, col=1)

        # Apparence de la partie environnement et réserves
        f_hold = ctk.CTkFrame(tab)
        f_hold.pack(fill="x", pady=5)
        f_hold.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_hold, text="Environnement & Réserves", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        
        # Champs de la partie environnement et réserves
        addField(app, f_hold, "Temps Holding", "Time_holding_min", "30", "min", row=1, col=1)
        addField(app, f_hold, "Contingency", "Contingency", "5", "%", row=2, col=1)
        addField(app, f_hold, "Vitesse Vent Vw", "Vw_kt", "0", "kt", row=3, col=1)
        addField(app, f_hold, "DISA Croisière", "DISA_Cruise", "0", "K", row=4, col=1)
        addField(app, f_hold, "DISA Sous Crois.", "DISA_sub_Cruise", "0", "K", row=5, col=1)

        # Grille face-à-face pour les coefficients
        f_coeff = ctk.CTkFrame(tab)
        f_coeff.pack(fill="x", pady=5)
        f_coeff.grid_columnconfigure((0, 7), weight=1) # Centrage
        ctk.CTkLabel(f_coeff, text="Coefficients Déformation Réseau", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=6, pady=5)

        # Champs des coefficients
        # Aero
        addField(app, f_coeff, "cCz (Portance)", "cCz", "1", "", row=1, col=1)
        addField(app, f_coeff, "cCx (Traînée)", "cCx", "1", "", row=1, col=4)
        # Moteur montée
        addField(app, f_coeff, "cFF Climb", "cFF_climb", "1", "", row=2, col=1)
        addField(app, f_coeff, "cFN Climb", "cFN_climb", "1", "", row=2, col=4)
        # Monteur croisière
        addField(app, f_coeff, "cFF Cruise", "cFF_cruise", "1", "", row=3, col=1)
        addField(app, f_coeff, "cFN Cruise", "cFN_cruise", "1", "", row=3, col=4)
        # Moteur descente
        addField(app, f_coeff, "cFF Descent", "cFF_descent", "1", "", row=4, col=1)
        addField(app, f_coeff, "cFN Descent", "cFN_descent", "1", "", row=4, col=4)

class OngletOptions(ctk.CTkFrame):
    def __init__(self, master, app):
        '''
        Onglet qui gère les options de la simulation (pas de temps, précision...).

        :param master: Onglet où insérer le contenu
        :param app: Interface graphique
        '''
        # Apparence de l'onglet
        super().__init__(master, fg_color="transparent")
        tab = app.tabview.tab("Options")
        f_opt = ctk.CTkFrame(tab)
        f_opt.pack(fill="x", pady=5, padx=5)
        f_opt.grid_columnconfigure((0, 4), weight=1)
        
        # Champss de l'onglet
        addField(app, f_opt, "dt Montée", "dtClimb", "10.0", "s", row=0, col=1)
        addField(app, f_opt, "dt Croisière", "dtCruise", "60.0", "s", row=1, col=1)
        addField(app, f_opt, "dt Descente", "dtDescent", "10.0", "s", row=2, col=1)
        addField(app, f_opt, "Itérations Max", "maxIter", "10", "", row=3, col=1)
        addField(app, f_opt, "Précision", "precision", "1", "%", row=4, col=1)
        
        # Choix aérodynamique simplifiée (boîte à cocher)
        app.vars["AeroSimplified"] = ctk.BooleanVar(value=False)
        cb_aero = ctk.CTkCheckBox(f_opt, text="Aérodynamique simplifiée", variable=app.vars["AeroSimplified"])
        cb_aero.grid(row=5, column=1, columnspan=3, pady=10)

class OngletPP(ctk.CTkFrame):
    def __init__(self, master, app):
        '''
        Onglet qui gère le calcul du Point Performance.

        :param master: Onglet où insérer le contenu
        :param app: Interface graphique
        '''
        self.app = app
        # Apparence de l'onglet
        super().__init__(master, fg_color="transparent")        
        tab = app.tabview.tab("Point Performance")
        f_pp = ctk.CTkFrame(tab)
        f_pp.pack(fill="x", pady=5, padx=5)
        f_pp.grid_columnconfigure((0, 4), weight=1)
        
        # Choix du type de vitesse
        app.vars["SpeedType"] = ctk.StringVar(value="Mach") # Valeur par défaut
        self.lbl_unit_speed_pp = ctk.CTkLabel(f_pp, text="-", width=30, anchor="w")
        # addField(app, f_pp, "Vitesse", "Speed", "0.78", "", row=1, col=1) # Unité gérée manuellement

        # addField(app, parent, label, var_name, default_value, unit="", row=0, col=0, width=120)
        # Pousse les éléments au centre
        # parent.grid_columnconfigure(0, weight=1)
        # parent.grid_columnconfigure(4, weight=1)

        # Affichage du nom de la variable
        # ctk.CTkLabel(f_pp, text="Vitesse").grid(row=1, column=1, padx=(10, 5), pady=5, sticky="e")

        # Ajout dans le dictionnaire des variables
        if "Speed" not in app.vars or not isinstance(app.vars["Speed"], (ctk.StringVar, ctk.BooleanVar)):
            app.vars["Speed"] = ctk.StringVar(value="0.78")

        # Ajout du champ de remplissage
        self.champ_vitesse_pp = ctk.CTkEntry(f_pp, textvariable=app.vars["Speed"], width=120)
        self.champ_vitesse_pp.grid(row=1, column=1+1, padx=5, pady=5, sticky="ew")

        # Ajout de l'unité
        # if "": ctk.CTkLabel(f_pp, text="", width=30, anchor="w").grid(row=1, column=1+2, padx=(5, 10), pady=5, sticky="w")


        # Remplacement de "Vitesse" par le choix du type de vitesse
        ctk.CTkComboBox(f_pp, variable=app.vars["SpeedType"], values=["Mach", "TAS", "CAS"],
                        command=self.update_pp_speed_label, width=120).grid(row=1, column=1, padx=5, pady=5)
        self.lbl_unit_speed_pp.grid(row=1, column=3, padx=(5, 10), pady=5, sticky="w")
        
        # Autres champs
        addField(app, f_pp, "Altitude", "altPP_ft", "38000", "ft", row=2, col=1)
        addField(app, f_pp, "Masse", "massPP", "60000", "kg", row=3, col=1)
        addField(app, f_pp, "ΔISA", "DISA_PP", "0", "°C", row=4, col=1)

    def update_pp_speed_label(self, choice):
        ''' Change l'unité de la vitesse sélectionnée, ainsi que la valeur par défaut. '''
        if choice == "Mach":
            self.lbl_unit_speed_pp.configure(text="-")
            self.app.vars["Speed"] = ctk.StringVar(value="0.78")
        else:
            self.lbl_unit_speed_pp.configure(text="kt")
            self.app.vars["Speed"] = ctk.StringVar(value="250")
        self.champ_vitesse_pp.configure(textvariable=self.app.vars["Speed"])

class OngletBatch(ctk.CTkFrame):
    def __init__(self, master, app):
        '''
        Onglet qui gère les calculs en batch (payload - range).

        :param master: Onglet où insérer le contenu
        :param app: Interface graphique
        '''
        # Apparence de l'onglet
        super().__init__(master, fg_color="transparent")
        tab = app.tabview.tab("Batch")
        f_batch = ctk.CTkFrame(tab)
        f_batch.pack(fill="x", pady=5, padx=5)
        f_batch.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_batch, text="Configuration du calcul en rafale (Batch)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=(10, 15))

        # Champs de l'onglet
        addField(app, f_batch, "Payloads (espace séparés)", "batch_payloads", "0 10000 18000 20000", "kg", row=1, col=1, width=200)
        addField(app, f_batch, "Ranges (espace séparés)", "batch_ranges", "500 1000 1500", "nm", row=2, col=1, width=200)
