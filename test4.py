from missions.Mission import Mission
from avions.Avion import Avion
from missions.PointPerformance import PointPerformance
from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from inputs.Inputs import Inputs
from constantes.Constantes import Constantes

import os
import sys
import csv
from datetime import datetime
import customtkinter as ctk # pip install customtkinter
from tkinter import filedialog, messagebox
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

# ==========================================
# Redirection de la console (print -> interface)
# ==========================================
class PrintRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, texte):
        self.textbox.insert("end", texte)
        self.textbox.see("end")
        self.textbox.update_idletasks() # Garde l'interface fluide pendant les boucles de calcul

    def flush(self):
        pass

# ==========================================
# Interface Graphique
# ==========================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculateur de Mission - Type Piano-X")
        self.geometry("1400x900")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")  

        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Dictionnaires de variables
        self.vars = {}
        self.pp_keys = ["SpeedType", "Speed", "altPP_ft", "massPP", "DISA_PP"]
        
        self.Avion = None 
        self.Atmosphere = Atmosphere()
        self.Enregistrement  = Enregistrement()
        self.chemins_avions = {} 
        self.chemins_moteurs = {} 

        # Paramètres d'affichage
        self.tailleEntrees = 15 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=self.tailleEntrees) 
        self.grid_columnconfigure(1, weight=100 - self.tailleEntrees) 

        # A gauche: les inputs
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.build_top_selection()
        self.build_tabs()
        self.build_bottom_buttons()

        # A droite: les outputs
        self.right_tabview = ctk.CTkTabview(self)
        self.right_tabview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.right_tabview.add("Console")
        self.right_tabview.add("Graphiques")

        # Tab Console
        self.textbox_out = ctk.CTkTextbox(self.right_tabview.tab("Console"), font=ctk.CTkFont(family="Consolas", size=13))
        self.textbox_out.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Redirection des print() vers la textbox
        sys.stdout = PrintRedirector(self.textbox_out)

        # Tab Graphiques
        self.build_tab_graphiques()

        # Initialisation dynamique
        self.update_cruise_fields()

    # Actions à la fermeture de la fenêtre
    def on_closing(self):
        # Restaure la console standard de Python
        sys.stdout = sys.__stdout__
        
        # Détruit proprement l'interface
        self.quit()
        self.destroy()
        exit()

    # ==========================
    # MÉTHODES DE CONSTRUCTION
    # ==========================
    def build_top_selection(self):
        top_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_frame.grid_columnconfigure((0, 5), weight=1)

        self.charger_listes_fichiers()

        ctk.CTkLabel(top_frame, text="Avion :").grid(row=0, column=1, padx=5, pady=10, sticky="e")
        self.cb_avion = ctk.CTkComboBox(top_frame, values=list(self.chemins_avions.keys()), command=self.check_avion_instantiation)
        self.cb_avion.set("") 
        self.cb_avion.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="w")

        ctk.CTkLabel(top_frame, text="Moteur :").grid(row=0, column=3, padx=15, pady=10, sticky="e")
        self.cb_moteur = ctk.CTkComboBox(top_frame, values=list(self.chemins_moteurs.keys()), command=self.check_avion_instantiation)
        self.cb_moteur.set("") 
        self.cb_moteur.grid(row=0, column=4, padx=5, pady=10, sticky="w")

    def build_tabs(self):
        self.tabview = ctk.CTkTabview(self.left_frame)
        self.tabview.grid(row=1, column=0, sticky="nsew")

        self.tabview.add("Mission")
        self.tabview.add("Autres")
        self.tabview.add("Options")
        self.tabview.add("Point Performance")

        self.build_tab_mission()
        self.build_tab_autres()
        self.build_tab_options()
        self.build_tab_pp()

    def build_tab_graphiques(self):
        tab = self.right_tabview.tab("Graphiques")
        
        # Contrôles du graphique
        f_controls = ctk.CTkFrame(tab, fg_color="transparent")
        f_controls.pack(fill="x", pady=5)
        
        keys = list(self.Enregistrement.data.keys())
        
        ctk.CTkLabel(f_controls, text="Axe X :").pack(side="left", padx=10)
        self.cb_x = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_x.set("l") # Distance par défaut
        self.cb_x.pack(side="left", padx=5)

        ctk.CTkLabel(f_controls, text="Axe Y :").pack(side="left", padx=10)
        self.cb_y = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_y.set("h") # Altitude par défaut
        self.cb_y.pack(side="left", padx=5)

        ctk.CTkButton(f_controls, text="Tracer", command=self.tracer_graphique, width=100).pack(side="left", padx=20)

        # Figure Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0') # Couleur de fond
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))
        
        # Barre d'outils Matplotlib (Zoom, save, etc.)
        self.toolbar = NavigationToolbar2Tk(self.canvas, tab)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_bottom_buttons(self):
        btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Importer CSV", command=self.importer_csv, fg_color="#E67E22", hover_color="#D35400").grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Exporter CSV", command=self.exporter_csv, fg_color="#27AE60", hover_color="#2ECC71").grid(row=0, column=1, padx=5, sticky="ew")

    def build_tab_mission(self):
        tab = ctk.CTkScrollableFrame(self.tabview.tab("Mission"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        # Globaux (Côte à côte et centrés)
        f_global = ctk.CTkFrame(tab)
        f_global.pack(fill="x", pady=5)
        self.vars["m_payload"] = ctk.StringVar(value="18000")
        self.vars["l_mission_NM"] = ctk.StringVar(value="1000")
        
        f_global.grid_columnconfigure((0, 7), weight=1) # Bords flexibles pour centrer
        
        ctk.CTkLabel(f_global, text="Payload").grid(row=0, column=1, padx=(10, 5), pady=10, sticky="e")
        ctk.CTkEntry(f_global, textvariable=self.vars["m_payload"], width=80).grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkLabel(f_global, text="kg", width=20, anchor="w").grid(row=0, column=3, padx=(0, 15), pady=10, sticky="w")
        
        ctk.CTkLabel(f_global, text="Distance").grid(row=0, column=4, padx=(15, 5), pady=10, sticky="e")
        ctk.CTkEntry(f_global, textvariable=self.vars["l_mission_NM"], width=80).grid(row=0, column=5, padx=5, pady=10)
        ctk.CTkLabel(f_global, text="nm", width=20, anchor="w").grid(row=0, column=6, padx=(0, 10), pady=10, sticky="w")

        # Montée
        f_climb = ctk.CTkFrame(tab)
        f_climb.pack(fill="x", pady=5)
        f_climb.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_climb, text="Montée", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_climb, "Altitude Initiale", "hInit_ft", "1500.0", "ft", row=1)
        self.add_field(f_climb, "Altitude Accélération", "hAccel_ft", "10000.0", "ft", row=2)
        self.add_field(f_climb, "CAS < 10000ft", "CAS_below_10000_mont_kt", "250.0", "kt", row=3)
        self.add_field(f_climb, "Mach Climb", "Mach_climb", "0.78", "", row=4)

        # Croisière (Dynamique)
        self.f_cruise = ctk.CTkFrame(tab)
        self.f_cruise.pack(fill="x", pady=5)
        self.f_cruise.grid_columnconfigure((0, 2), weight=1)
        ctk.CTkLabel(self.f_cruise, text="Croisière", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, pady=5)
        
        self.vars["cruiseType"] = ctk.StringVar(value="Alt_Mach")
        cb_cruise = ctk.CTkComboBox(self.f_cruise, variable=self.vars["cruiseType"], values=["Alt_Mach", "Alt_SAR", "Mach_SAR", "CI"], command=self.update_cruise_fields, width=150)
        cb_cruise.grid(row=1, column=1, padx=10, pady=5)
        
        self.f_cruise_dyn = ctk.CTkFrame(self.f_cruise, fg_color="transparent")
        self.f_cruise_dyn.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Descente
        f_desc = ctk.CTkFrame(tab)
        f_desc.pack(fill="x", pady=5)
        f_desc.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_desc, text="Descente", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_desc, "CAS < 10000ft", "CAS_below_10000_desc_kt", "250.0", "kt", row=1)
        self.add_field(f_desc, "Altitude Décélération", "hDecel_ft", "10000.0", "ft", row=2)
        self.add_field(f_desc, "Altitude Finale", "hFinal_ft", "1500.0", "ft", row=3)

        ctk.CTkButton(tab, text="Calculer Mission", command=self.calculer_mission).pack(pady=15)

    def build_tab_autres(self):
        tab = ctk.CTkScrollableFrame(self.tabview.tab("Autres"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        f_div = ctk.CTkFrame(tab)
        f_div.pack(fill="x", pady=5)
        f_div.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_div, text="Diversion", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_div, "Altitude Croisière", "cruiseDiversionAlt_ft", "25000", "ft", row=1)
        self.add_field(f_div, "Distance", "rangeDiversion_NM", "200", "nm", row=2)
        self.add_field(f_div, "Mach Croisière", "MachCruiseDiversion", "0.65", "", row=3)

        f_hold = ctk.CTkFrame(tab)
        f_hold.pack(fill="x", pady=5)
        f_hold.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_hold, text="Environnement & Réserves", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_hold, "Temps Holding", "Time_holding", "30", "min", row=1)
        self.add_field(f_hold, "Contingency", "Contingency", "5", "%", row=2)
        self.add_field(f_hold, "Vitesse Vent Vw", "Vw", "0", "kt", row=3)
        self.add_field(f_hold, "DISA Croisière", "DISA_Cruise", "0", "K", row=4)
        self.add_field(f_hold, "DISA Sous Croisière", "DISA_sub_Cruise", "0", "K", row=5)

        f_coeff = ctk.CTkFrame(tab)
        f_coeff.pack(fill="x", pady=5)
        f_coeff.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_coeff, text="Coefficients Déformation Réseau", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_coeff, "cCz (Portance)", "cCz", "1", "", row=1)
        self.add_field(f_coeff, "cCx (Traînée)", "cCx", "1", "", row=2)
        self.add_field(f_coeff, "cFF Climb", "cFF_climb", "1", "", row=3)
        self.add_field(f_coeff, "cFF Cruise", "cFF_cruise", "1", "", row=4)
        self.add_field(f_coeff, "cFF Descent", "cFF_descent", "1", "", row=5)
        self.add_field(f_coeff, "cFN Climb", "cFN_climb", "1", "", row=6)
        self.add_field(f_coeff, "cFN Cruise", "cFN_cruise", "1", "", row=7)
        self.add_field(f_coeff, "cFN Descent", "cFN_descent", "1", "", row=8)

    def build_tab_options(self):
        tab = self.tabview.tab("Options")
        f_opt = ctk.CTkFrame(tab)
        f_opt.pack(fill="x", pady=5, padx=5)
        f_opt.grid_columnconfigure((0, 4), weight=1)
        
        self.add_field(f_opt, "Pas de temps Montée", "dtClimb", "10.0", "s", row=0)
        self.add_field(f_opt, "Pas de temps Croisière", "dtCruise", "60.0", "s", row=1)
        self.add_field(f_opt, "Pas de temps Descente", "dtDescent", "10.0", "s", row=2)
        self.add_field(f_opt, "Itérations Max", "maxIter", "10", "", row=3)
        self.add_field(f_opt, "Précision", "precision", "1", "%", row=4)

    def build_tab_pp(self):
        tab = self.tabview.tab("Point Performance")
        f_pp = ctk.CTkFrame(tab)
        f_pp.pack(fill="x", pady=5, padx=5)
        
        f_pp.grid_columnconfigure((0, 4), weight=1)
        
        self.vars["SpeedType"] = ctk.StringVar(value="Mach")
        ctk.CTkLabel(f_pp, text="Type de Vitesse").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        cb_speed_type = ctk.CTkComboBox(f_pp, variable=self.vars["SpeedType"], values=["Mach", "TAS", "CAS"], command=self.update_pp_speed_label, width=120)
        cb_speed_type.grid(row=0, column=2, padx=5, pady=5)
        
        self.lbl_speed_pp = ctk.CTkLabel(f_pp, text="Vitesse")
        self.lbl_speed_pp.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        if "Speed" not in self.vars:
            self.vars["Speed"] = ctk.StringVar(value="0.78")
        ctk.CTkEntry(f_pp, textvariable=self.vars["Speed"], width=120).grid(row=1, column=2, padx=5, pady=5)
        
        self.lbl_unit_speed_pp = ctk.CTkLabel(f_pp, text="Mach", width=30, anchor="w")
        self.lbl_unit_speed_pp.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.add_field(f_pp, "Altitude", "altPP_ft", "38000", "ft", row=2)
        self.add_field(f_pp, "Masse", "massPP", "60000", "kg", row=3)
        self.add_field(f_pp, "ΔISA", "DISA_PP", "0", "°C", row=4)

        ctk.CTkButton(tab, text="Calculer PP", command=self.calculer_pp).pack(pady=15)

    def update_pp_speed_label(self, choice):
        if choice == "Mach":
            self.lbl_unit_speed_pp.configure(text="Mach")
        else:
            self.lbl_unit_speed_pp.configure(text="kt")

    # ==========================
    # LOGIQUE GRAPHIQUE
    # ==========================
    def convertir_donnees(self, key, array_brut):
        """ Applique les conversions SI -> Aero et renvoie (array_converti, unité) """
        if key == "h": 
            return array_brut / Constantes.conv_ft_m, "ft"
        elif key == "l": 
            return array_brut / Constantes.conv_NM_m, "nm"
        elif key in ["CAS", "TAS", "Vx"]: 
            return array_brut / Constantes.conv_kt_mps, "kt"
        elif key == "Vz": 
            return (array_brut / Constantes.conv_ft_m) * 60, "ft/min"
        elif key == "t": 
            return array_brut / 60, "min"
        elif key == "P": 
            return array_brut / 100, "hPa"
        elif key == "T": 
            return array_brut - 273.15, "°C"
        elif key == "F_N": 
            return array_brut / 1000, "kN"
        
        # Données ne nécessitant pas de multiplicateur
        unites = {"m": "kg", "FB": "kg", "rho": "kg/m³", "FF": "kg/s", "Mach": "Mach"}
        return array_brut, unites.get(key, "")

    def tracer_graphique(self):
        # On s'assure qu'une simulation a bien tourné
        if self.Enregistrement.counter == 0:
            messagebox.showinfo("Info", "Aucune donnée à tracer. Lancez d'abord un calcul de mission.")
            return

        key_x = self.cb_x.get()
        key_y = self.cb_y.get()

        # On récupère les tableaux tronqués à la valeur du compteur réel (évite les zéros de fin)
        data_x_brut = self.Enregistrement.data[key_x][:self.Enregistrement.counter]
        data_y_brut = self.Enregistrement.data[key_y][:self.Enregistrement.counter]

        data_x, unit_x = self.convertir_donnees(key_x, data_x_brut)
        data_y, unit_y = self.convertir_donnees(key_y, data_y_brut)

        # Mise à jour du graphique
        self.ax.clear()
        self.ax.plot(data_x, data_y, color='#2980b9', linewidth=2)
        
        self.ax.set_xlabel(f"{key_x} [{unit_x}]" if unit_x else key_x, fontweight='bold')
        self.ax.set_ylabel(f"{key_y} [{unit_y}]" if unit_y else key_y, fontweight='bold')
        self.ax.set_title(f"Évolution de {key_y} en fonction de {key_x}")
        
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.fig.tight_layout()
        self.canvas.draw()

    # ==========================
    # LOGIQUE MÉTIER
    # ==========================
    def check_avion_instantiation(self, event=None):
        nom_avion = self.cb_avion.get()
        nom_moteur = self.cb_moteur.get()
        
        if nom_avion and nom_moteur and nom_avion != "" and nom_moteur != "":
            path_avion = self.chemins_avions.get(nom_avion, "")
            path_moteur = self.chemins_moteurs.get(nom_moteur, "")
            
            if path_avion and path_moteur:
                self.textbox_out.delete("1.0", "end")
                self.Avion = Avion(path_avion, path_moteur)
                print(f">> Avion initialisé en mémoire.\n   - Modèle: {nom_avion}\n   - Moteur: {nom_moteur}\n")
                # On utilise print() ici au lieu de print, puisque print() est intercepté !

    def calculer_mission(self):
        if not self.Avion:
            messagebox.showwarning("Attention", "Veuillez sélectionner un avion et un moteur valides d'abord.")
            return

        # Vider la console à chaque nouveau run
        self.textbox_out.delete("1.0", "end")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        chemin_dossier = Path("./results") / timestamp
        chemin_dossier.mkdir(parents=True, exist_ok=True)
        chemin_csv = chemin_dossier / "param.csv"

        try:
            with open(chemin_csv, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["Attribut", "Valeur"])
                for var_name, tk_var in self.vars.items():
                    if var_name not in self.pp_keys:
                        writer.writerow([var_name, tk_var.get()])
            print(f">> Paramètres sauvegardés dans {chemin_csv}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return

        try:
            Inputs.loadCSVFile(str(chemin_csv))
        except Exception as e:
            print(f"Erreur lors du chargement via Inputs.loadCSVFile : {e}")
            return

        print("Lancement calcul de mission...")
        print("Lancement calcul de mission...")
        try:
            # L'enregistrement sera mis à jour en interne
            self.Enregistrement.reset()
            Mission.Principal(self.Avion, self.Atmosphere, self.Enregistrement)
            
            # ---- NOUVEAU : Sauvegarde des résultats ----
            chemin_resultats = chemin_dossier / "resultats_vol.csv"
            self.Enregistrement.export_csv(str(chemin_resultats))
            print(f">> Résultats sauvegardés dans {chemin_resultats}")
            # --------------------------------------------
            
            # On bascule automatiquement sur l'onglet graphiques à la fin
            self.right_tabview.set("Graphiques")
            self.tracer_graphique() 
        except Exception as e:
            print(f"Erreur lors du calcul de la mission : {e}")

    def calculer_pp(self):
        if not self.Avion:
            messagebox.showwarning("Attention", "Veuillez sélectionner un avion et un moteur valides d'abord.")
            return
            
        try:
            Inputs.SpeedType = self.vars["SpeedType"].get()
            Inputs.Speed = float(self.vars["Speed"].get())
            Inputs.altPP_ft = float(self.vars["altPP_ft"].get())
            Inputs.massPP = float(self.vars["massPP"].get())
            Inputs.DISA_PP = float(self.vars["DISA_PP"].get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour le Point Performance.")
            return
            
        print("Lancement calcul Point Performance...")
        try:
            resultat = PointPerformance.Performance(self.Avion, self.Atmosphere)
            print(resultat)
        except Exception as e:
            print(f"Erreur lors du calcul Point Performance : {e}")

    def update_cruise_fields(self, choice=None):
        for widget in self.f_cruise_dyn.winfo_children():
            widget.destroy()
            
        c_type = self.vars["cruiseType"].get()
        
        self.add_field(self.f_cruise_dyn, "Altitude Croisière", "hCruise_ft", "38000", "ft", row=0)
        self.add_field(self.f_cruise_dyn, "Mach Croisière", "MachCruise", "0.78", "", row=1)

        if c_type == "Mach_SAR":
            self.add_field(self.f_cruise_dyn, "Step Climb", "stepClimb_ft", "2000.0", "ft", row=2)
            self.add_field(self.f_cruise_dyn, "RRoC min", "RRoC_min_ft", "300.0", "ft/min", row=3)
            self.add_field(self.f_cruise_dyn, "Init Montée", "cruiseClimbInit", "20", "% dist", row=4)
            self.add_field(self.f_cruise_dyn, "Stop Montée", "cruiseClimbStop", "80", "% dist", row=5)
        elif c_type == "Alt_SAR":
            self.add_field(self.f_cruise_dyn, "Dégradation SAR", "kSARcruise", "1", "%", row=2)

    def add_field(self, parent, label, var_name, default_value, unit="", row=None):
        if row is None:
            row = parent.grid_size()[1]
            
        # Pousse les éléments au centre
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(4, weight=1)
        
        # Label aligné à droite contre l'entry
        ctk.CTkLabel(parent, text=label).grid(row=row, column=1, padx=(10, 5), pady=5, sticky="e")
        
        if var_name not in self.vars or not isinstance(self.vars[var_name], ctk.StringVar):
            self.vars[var_name] = ctk.StringVar(value=default_value)
            
        # Entry centrée
        entry = ctk.CTkEntry(parent, textvariable=self.vars[var_name], width=120)
        entry.grid(row=row, column=2, padx=5, pady=5, sticky="")
        
        # Unité alignée à gauche de la case
        ctk.CTkLabel(parent, text=unit, width=30, anchor="w").grid(row=row, column=3, padx=(5, 10), pady=5, sticky="w")

    def charger_listes_fichiers(self):
        dossier_data = Path(__file__).parent / "data"
        dossier_avions = dossier_data / "avions"
        dossier_moteurs = dossier_data / "moteurs"
        
        self.chemins_avions = {}
        if dossier_avions.exists():
            for f in dossier_avions.glob("*.csv"):
                if f.name == "Avion_vide.csv": continue
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        premiere_ligne = file.readline().strip()
                        if premiere_ligne.startswith("Name;"):
                            nom_affiche = premiere_ligne.split(";")[1]
                            self.chemins_avions[nom_affiche] = str(f)
                except Exception as e:
                    print(f"Erreur lecture {f.name}: {e}")

        self.chemins_moteurs = {}
        if dossier_moteurs.exists():
            for f in dossier_moteurs.glob("*.py"):
                if f.name == "Moteur_vide.py": continue
                self.chemins_moteurs[f.stem] = str(f)

    def exporter_csv(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not chemin: return

        try:
            with open(chemin, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["Attribut", "Valeur"])
                for var_name, tk_var in self.vars.items():
                    if var_name not in self.pp_keys:
                        writer.writerow([var_name, tk_var.get()])
            print(f">> Configuration exportée vers {os.path.basename(chemin)}")
            messagebox.showinfo("Succès", "Fichier exporté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def importer_csv(self):
        chemin = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not chemin: return

        try:
            with open(chemin, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    if len(row) == 2:
                        var_name, value = row
                        if var_name in self.vars:
                            self.vars[var_name].set(value)
            
            self.update_cruise_fields() 
            print(f">> Configuration importée depuis {os.path.basename(chemin)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de lecture: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()