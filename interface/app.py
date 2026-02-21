# Import autres éléments de l'interface
from interface.utils import PrintRedirector
# from interface.onglets import OngletMission # importe tes onglets
from interface.actions import calculer_mission, importer_mission, calculer_pp, \
                              calculer_batch, importer_batch   # importe tes actions
from interface.onglets import OngletMission

# Code de calcul mission
from enregistrement.Enregistrement import Enregistrement
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere
from inputs.Inputs import Inputs

# Import modules Python
from tkinter import filedialog, messagebox
from datetime import datetime
import customtkinter as ctk # pip install customtkinter
from pathlib import Path
import numpy as np
import sys
import csv
import os

# Affichage Matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



# ==========================================
# Interface Graphique
# ==========================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculateur de Mission")
        self.geometry("1300x600")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")  

        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Dictionnaires de variables
        self.vars = {}
        # Clés à ne pas exporter globalement
        self.pp_keys = ["SpeedType", "Speed", "altPP_ft", "massPP", "DISA_PP"]
        self.batch_keys = ["batch_ranges", "batch_payloads"]
        
        self.Avion = None
        self.Inputs = Inputs()
        self.Atmosphere = Atmosphere(self.Inputs)
        self.Enregistrement  = Enregistrement()
        
        self.chemins_avions = {} 
        self.chemins_moteurs = {} 

        # Paramètres d'affichage
        self.tailleEntrees = 20 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=self.tailleEntrees) 
        self.grid_columnconfigure(1, weight=100 - self.tailleEntrees) 

        # --- GAUCHE: INPUTS ---
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(2, weight=1) # La zone des onglets (row 2) s'étend
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.build_top_selection()
        self.build_action_buttons()
        self.build_tabs()

        # --- DROITE: OUTPUTS ---
        self.right_tabview = ctk.CTkTabview(self)
        self.right_tabview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.right_tabview.add("Console")
        self.right_tabview.add("Graphiques")

        # Tab Console (Avec wrap="none" pour forcer le scroll horizontal)
        self.textbox_out = ctk.CTkTextbox(self.right_tabview.tab("Console"), font=ctk.CTkFont(family="Consolas", size=13), wrap="none")
        self.textbox_out.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Redirection des print() vers la textbox et/ou les fichiers logs
        self.redirector = PrintRedirector(self.textbox_out)
        sys.stdout = self.redirector

        # Tab Graphiques
        self.build_tab_graphiques()

        # Initialisation dynamique
        self.update_cruise_fields()
        self.on_tab_change() # Définit le bouton principal au lancement

    def on_closing(self):
        """ Restaurer la console classique avant de quitter pour éviter des erreurs Tkinter. """
        sys.stdout = sys.__stdout__
        exit()

    # ==========================
    # MÉTHODES DE CONSTRUCTION
    # ==========================
    def build_top_selection(self):
        top_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        top_frame.grid_columnconfigure((0, 5), weight=1)

        self.charger_listes_fichiers()

        ctk.CTkLabel(top_frame, text="Avion :").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        self.cb_avion = ctk.CTkComboBox(top_frame, values=list(self.chemins_avions.keys()))
        self.cb_avion.set("") 
        self.cb_avion.grid(row=0, column=2, padx=(5, 15), pady=5, sticky="w")

        ctk.CTkLabel(top_frame, text="Moteur :").grid(row=0, column=3, padx=15, pady=5, sticky="e")
        self.cb_moteur = ctk.CTkComboBox(top_frame, values=list(self.chemins_moteurs.keys()))
        self.cb_moteur.set("") 
        self.cb_moteur.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    def build_action_buttons(self):
        # Cadre centralisé sous l'avion et le moteur, mais au-dessus des onglets
        self.btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 0))
        self.btn_frame.grid_columnconfigure((0, 1), weight=1) # 2 colonnes

        # Bouton Calculer Dynamique
        self.btn_calculer = ctk.CTkButton(self.btn_frame, text="Calculer Mission", command=lambda: calculer_mission(self), fg_color="#2980b9", hover_color="#3498db")
        self.btn_calculer.grid(row=0, column=0, padx=5, pady=0, sticky="ew")

        # Bouton Importer Dynamique
        self.btn_importer = ctk.CTkButton(self.btn_frame, text="Importer Mission", command=lambda: importer_mission(self), fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_importer.grid(row=0, column=1, padx=5, pady=0, sticky="ew")

    def build_tabs(self):
        self.tabview = ctk.CTkTabview(self.left_frame, command=self.on_tab_change)
        self.tabview.grid(row=2, column=0, sticky="nsew")

        self.tabview.add("Mission")
        self.tabview.add("Autres")
        self.tabview.add("Options")
        self.tabview.add("Point Performance")
        self.tabview.add("Batch")

        # self.build_tab_mission()
        self.onglet_mission = OngletMission(self.tabview.tab("Mission"), app=self)
        self.build_tab_autres()
        self.build_tab_options()
        self.build_tab_pp()
        self.build_tab_batch()

    def on_tab_change(self):
        """ Change dynamiquement le comportement des boutons selon l'onglet actif. """
        current_tab = self.tabview.get()
        
        # Gérer le texte et la commande du bouton de calcul
        if current_tab == "Point Performance":
            self.btn_calculer.configure(text="Calculer PP", command=lambda: calculer_pp(self))
        elif current_tab == "Batch":
            self.btn_calculer.configure(text="Calculer Batch", command=lambda: calculer_batch(self))
        else:
            self.btn_calculer.configure(text="Calculer Mission", command=lambda: calculer_mission(self))
            
        # Gérer l'affichage du bouton d'importation ET le centrage
        if current_tab == "Point Performance":
            self.btn_importer.grid_remove() # Masque le bouton
            self.btn_calculer.grid_configure(columnspan=2) # Étend le bouton restant sur toute la largeur
            self.btn_calculer.grid_configure(padx=(160,160))
        else:
            self.btn_calculer.grid_configure(columnspan=1) # Restreint le bouton à sa moitié
            self.btn_calculer.grid_configure(padx=(5,5))
            self.btn_importer.grid() # Réaffiche le bouton d'import
            
            if current_tab == "Batch":
                self.btn_importer.configure(text="Importer Batch", command= lambda: importer_batch(self), fg_color="#8e44ad", hover_color="#9b59b6")
            else:
                self.btn_importer.configure(text="Importer Mission", command= lambda: importer_mission(self), fg_color="#27ae60", hover_color="#2ecc71")

    # ------------------ ONGLET MISSION ------------------
    # def build_tab_mission(self):


    # ------------------ ONGLET AUTRES ------------------
    def build_tab_autres(self):
        tab = ctk.CTkScrollableFrame(self.tabview.tab("Autres"), fg_color="transparent")
        tab.pack(fill="both", expand=True)

        f_div = ctk.CTkFrame(tab)
        f_div.pack(fill="x", pady=5)
        f_div.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_div, text="Diversion", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_div, "Altitude Croisière", "cruiseDiversionAlt_ft", "25000", "ft", row=1, col=1)
        self.add_field(f_div, "Distance", "rangeDiversion_NM", "200", "nm", row=2, col=1)
        self.add_field(f_div, "Mach Croisière", "MachCruiseDiversion", "0.65", "", row=3, col=1)

        f_hold = ctk.CTkFrame(tab)
        f_hold.pack(fill="x", pady=5)
        f_hold.grid_columnconfigure((0, 4), weight=1)
        ctk.CTkLabel(f_hold, text="Environnement & Réserves", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=5)
        self.add_field(f_hold, "Temps Holding", "Time_holding", "30", "min", row=1, col=1)
        self.add_field(f_hold, "Contingency", "Contingency", "5", "%", row=2, col=1)
        self.add_field(f_hold, "Vitesse Vent Vw", "Vw", "0", "kt", row=3, col=1)
        self.add_field(f_hold, "DISA Croisière", "DISA_Cruise", "0", "K", row=4, col=1)
        self.add_field(f_hold, "DISA Sous Crois.", "DISA_sub_Cruise", "0", "K", row=5, col=1)

        # Grille face-à-face pour les coefficients
        f_coeff = ctk.CTkFrame(tab)
        f_coeff.pack(fill="x", pady=5)
        f_coeff.grid_columnconfigure((0, 7), weight=1) # Centrage
        ctk.CTkLabel(f_coeff, text="Coefficients Déformation Réseau", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=6, pady=5)
        
        self.add_field(f_coeff, "cCz (Portance)", "cCz", "1", "", row=1, col=1)
        self.add_field(f_coeff, "cCx (Traînée)", "cCx", "1", "", row=1, col=4)
        
        self.add_field(f_coeff, "cFF Climb", "cFF_climb", "1", "", row=2, col=1)
        self.add_field(f_coeff, "cFN Climb", "cFN_climb", "1", "", row=2, col=4)
        
        self.add_field(f_coeff, "cFF Cruise", "cFF_cruise", "1", "", row=3, col=1)
        self.add_field(f_coeff, "cFN Cruise", "cFN_cruise", "1", "", row=3, col=4)
        
        self.add_field(f_coeff, "cFF Descent", "cFF_descent", "1", "", row=4, col=1)
        self.add_field(f_coeff, "cFN Descent", "cFN_descent", "1", "", row=4, col=4)

    # ------------------ ONGLET OPTIONS ------------------
    def build_tab_options(self):
        tab = self.tabview.tab("Options")
        f_opt = ctk.CTkFrame(tab)
        f_opt.pack(fill="x", pady=5, padx=5)
        f_opt.grid_columnconfigure((0, 4), weight=1)
        
        self.add_field(f_opt, "dt Montée", "dtClimb", "10.0", "s", row=0, col=1)
        self.add_field(f_opt, "dt Croisière", "dtCruise", "60.0", "s", row=1, col=1)
        self.add_field(f_opt, "dt Descente", "dtDescent", "10.0", "s", row=2, col=1)
        self.add_field(f_opt, "Itérations Max", "maxIter", "10", "", row=3, col=1)
        self.add_field(f_opt, "Précision", "precision", "1", "%", row=4, col=1)
        
        # Ajout Aérodynamique simplifiée
        self.vars["AeroSimplified"] = ctk.BooleanVar(value=False)
        cb_aero = ctk.CTkCheckBox(f_opt, text="Aérodynamique simplifiée", variable=self.vars["AeroSimplified"])
        cb_aero.grid(row=5, column=1, columnspan=3, pady=10)

    # ------------------ ONGLET PP ------------------
    def build_tab_pp(self):
        tab = self.tabview.tab("Point Performance")
        f_pp = ctk.CTkFrame(tab)
        f_pp.pack(fill="x", pady=5, padx=5)
        f_pp.grid_columnconfigure((0, 4), weight=1)
        
        self.vars["SpeedType"] = ctk.StringVar(value="Mach")
        ctk.CTkLabel(f_pp, text="Type Vitesse").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        ctk.CTkComboBox(f_pp, variable=self.vars["SpeedType"], values=["Mach", "TAS", "CAS"], command=self.update_pp_speed_label, width=120).grid(row=0, column=2, padx=5, pady=5)
        
        self.lbl_unit_speed_pp = ctk.CTkLabel(f_pp, text="Mach", width=30, anchor="w")
        self.add_field(f_pp, "Vitesse", "Speed", "0.78", "", row=1, col=1) # Unité gérée manuellement
        self.lbl_unit_speed_pp.grid(row=1, column=3, padx=(5, 10), pady=5, sticky="w")

        self.add_field(f_pp, "Altitude", "altPP_ft", "38000", "ft", row=2, col=1)
        self.add_field(f_pp, "Masse", "massPP", "60000", "kg", row=3, col=1)
        self.add_field(f_pp, "ΔISA", "DISA_PP", "0", "°C", row=4, col=1)

    # ------------------ ONGLET BATCH ------------------
    def build_tab_batch(self):
        tab = self.tabview.tab("Batch")
        f_batch = ctk.CTkFrame(tab)
        f_batch.pack(fill="x", pady=5, padx=5)
        f_batch.grid_columnconfigure((0, 4), weight=1)

        ctk.CTkLabel(f_batch, text="Configuration du calcul en rafale (Batch)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, columnspan=3, pady=(10, 15))

        self.add_field(f_batch, "Payloads (espace séparés)", "batch_payloads", "0 10000 18000 20000", "kg", row=1, col=1, width=200)
        self.add_field(f_batch, "Ranges (espace séparés)", "batch_ranges", "500 1000 1500", "nm", row=2, col=1, width=200)

    # ==========================
    # LOGIQUE GRAPHIQUE (GRAPHIQUES & CHAMPS)
    # ==========================
    def build_tab_graphiques(self):
        tab = self.right_tabview.tab("Graphiques")
        f_controls = ctk.CTkFrame(tab, fg_color="transparent")
        f_controls.pack(fill="x", pady=5)
        
        keys = list(self.Enregistrement.data.keys())
        
        ctk.CTkLabel(f_controls, text="Axe X :").pack(side="left", padx=10)
        self.cb_x = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_x.set("l") 
        self.cb_x.pack(side="left", padx=5)

        ctk.CTkLabel(f_controls, text="Axe Y :").pack(side="left", padx=10)
        self.cb_y = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_y.set("h") 
        self.cb_y.pack(side="left", padx=5)

        ctk.CTkButton(f_controls, text="Tracer", command=self.tracer_graphique, width=100).pack(side="left", padx=20)

        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0') 
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, tab)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def tracer_graphique(self):
        if self.Enregistrement.counter == 0:
            messagebox.showinfo("Info", "Aucune donnée à tracer. Lancez d'abord un calcul de mission ou importez une mission existante.")
            return

        key_x = self.cb_x.get()
        key_y = self.cb_y.get()

        data_x_brut = self.Enregistrement.data[key_x][:self.Enregistrement.counter]
        data_y_brut = self.Enregistrement.data[key_y][:self.Enregistrement.counter]

        def conv_aero(key, arr):
            if key == "h": return arr / Constantes.conv_ft_m, "ft"
            if key == "l": return arr / Constantes.conv_NM_m, "nm"
            if key in ["CAS", "TAS", "Vx"]: return arr / Constantes.conv_kt_mps, "kt"
            if key == "Vz": return (arr / Constantes.conv_ft_m) * 60, "ft/min"
            if key == "t": return arr / 60, "min"
            if key == "P": return arr / 100, "hPa"
            if key == "T": return arr - 273.15, "°C"
            if key == "F_N": return arr / 1000, "kN"
            unites = {"m": "kg", "FB": "kg", "rho": "kg/m³", "FF": "kg/s", "Mach": "Mach"}
            return arr, unites.get(key, "")

        data_x, unit_x = conv_aero(key_x, data_x_brut)
        data_y, unit_y = conv_aero(key_y, data_y_brut)

        self.ax.clear()
        self.ax.plot(data_x, data_y, color='#2980b9', linewidth=2)
        self.ax.set_xlabel(f"{key_x} [{unit_x}]" if unit_x else key_x, fontweight='bold')
        self.ax.set_ylabel(f"{key_y} [{unit_y}]" if unit_y else key_y, fontweight='bold')
        self.ax.set_title(f"Évolution de {key_y} en fonction de {key_x}")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.fig.tight_layout()
        self.canvas.draw()

    def update_pp_speed_label(self, choice):
        if choice == "Mach": self.lbl_unit_speed_pp.configure(text="Mach")
        else: self.lbl_unit_speed_pp.configure(text="kt")

    def update_cruise_fields(self, choice=None):
        for widget in self.onglet_mission.f_cruise_dyn.winfo_children(): widget.destroy()
        c_type = self.vars["cruiseType"].get()
        
        # CHANGEMENT ICI: col=1 au lieu de col=0
        self.add_field(self.onglet_mission.f_cruise_dyn, "Altitude Croisière", "hCruise_ft", "38000", "ft", row=0, col=1)
        self.add_field(self.onglet_mission.f_cruise_dyn, "Mach Croisière", "MachCruise", "0.78", "", row=1, col=1)

        if c_type == "Mach_SAR":
            self.add_field(self.onglet_mission.f_cruise_dyn, "Step Climb", "stepClimb_ft", "2000.0", "ft", row=2, col=1)
            self.add_field(self.onglet_mission.f_cruise_dyn, "RRoC min", "RRoC_min_ft", "300.0", "ft/min", row=3, col=1)
            self.add_field(self.onglet_mission.f_cruise_dyn, "Init Montée", "cruiseClimbInit", "20", "% dist", row=4, col=1)
            self.add_field(self.onglet_mission.f_cruise_dyn, "Stop Montée", "cruiseClimbStop", "80", "% dist", row=5, col=1)
        elif c_type == "Alt_SAR":
            self.add_field(self.onglet_mission.f_cruise_dyn, "Dégradation SAR", "kSARcruise", "1", "%", row=2, col=1)

    def add_field(self, parent, label, var_name, default_value, unit="", row=0, col=0, width=120):
        # Pousse les éléments au centre
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(parent, text=label).grid(row=row, column=col, padx=(10, 5), pady=5, sticky="e")
        if var_name not in self.vars or not isinstance(self.vars[var_name], (ctk.StringVar, ctk.BooleanVar)):
            self.vars[var_name] = ctk.StringVar(value=default_value)
        ctk.CTkEntry(parent, textvariable=self.vars[var_name], width=width).grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")
        if unit: ctk.CTkLabel(parent, text=unit, width=30, anchor="w").grid(row=row, column=col+2, padx=(5, 10), pady=5, sticky="w")

    def charger_listes_fichiers(self):
        dossier_data = Path(__file__).parent.parent / "data"
        self.chemins_avions = {}
        if (dossier_data / "avions").exists():
            for f in (dossier_data / "avions").glob("*.csv"):
                if f.name == "Avion_vide.csv": continue
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        premiere_ligne = file.readline().strip()
                        if premiere_ligne.startswith("Name;"):
                            self.chemins_avions[premiere_ligne.split(";")[1]] = str(f)
                except Exception: pass

        self.chemins_moteurs = {}
        if (dossier_data / "moteurs").exists():
            for f in (dossier_data / "moteurs").glob("*.py"):
                if f.name == "Moteur_vide.py": continue
                self.chemins_moteurs[f.stem] = str(f)


if __name__ == "__main__":
    app = App()
    app.mainloop()