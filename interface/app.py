# Import autres éléments de l'interface
from interface.utils import PrintRedirector
from interface.actions import calculerMission, importerMission, calculerPP, \
                              calculerBatch, importerBatch   # importe les fonctions actions
from interface.onglets import OngletMission, OngletAutres, OngletOptions, OngletPP, OngletBatch
from interface.actions import importCSV, exportCSV

# Code de calcul mission
from enregistrement.Enregistrement import Enregistrement
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs


import csv
import numpy as np

# Import module tkinter (affiche une erreur en rouge dans la console si il n'est pas installé)
from tkinter import messagebox
try:
    import customtkinter as ctk
except:
    print("\033[31mModule customtkinter non trouvé: veuillez l'installer avec la commande 'pip install customtkinter'\033[0m")
    exit()

from pathlib import Path
import sys

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

        # Apparence et propriétés de la fenêtre
        self.title("Calculateur de Mission")
        self.geometry("1300x600")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")  

        # Intercepter la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", exit)
        
        # Dictionnaires de variables
        self.vars = {}

        # Clés à ne pas exporter globalement
        self.pp_keys    = ["SpeedType", "Speed", "altPP_ft", "massPP", "DISA_PP"]
        self.batch_keys = ["batch_ranges", "batch_payloads"]
        self.batch_root_dir = None
        self.batch_missions_map = {} # Dictionnaire pour traduire le nom joli en nom de dossier
        
        # Objets du code mission
        self.Avion           = None
        self.Atmosphere      = None # On a besoin des inputs de l'utilisateur (vent, DISA)
        self.Inputs          = Inputs()
        self.Enregistrement  = Enregistrement()
        
        # Chemins moteur / avion
        self.chemins_avions = {} 
        self.chemins_moteurs = {} 

        # Paramètres d'affichage
        self.tailleEntrees = 20 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=self.tailleEntrees) 
        self.grid_columnconfigure(1, weight=100 - self.tailleEntrees) 

        # Partie gauche: inputs
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(2, weight=1) # La zone des onglets (row 2) s'étend
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Construction des sélections, boutons et onglets
        self.buildTopSelection()
        self.buildActionButtons()
        self.buildTabs()
        self.build_bottom_buttons()

        # Partie droite: outputs
        self.right_tabview = ctk.CTkTabview(self)
        self.right_tabview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.right_tabview.add("Console")
        self.right_tabview.add("Graphiques")

        # Tab Console (wrap="none" force le scroll horizontal)
        self.textbox_out = ctk.CTkTextbox(self.right_tabview.tab("Console"), font=ctk.CTkFont(family="Consolas", size=13), wrap="none")
        self.textbox_out.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Redirection des print() vers la textbox ou fichiers logs
        self.redirector = PrintRedirector(self.textbox_out)
        sys.stdout = self.redirector

        # Tab Graphiques
        self.buildTabGraphiques()

        # Initialisation dynamique
        self.onTabChange() # Définit le bouton principal au lancement

    # ==========================
    # MÉTHODES DE CONSTRUCTION
    # ==========================
    def buildTopSelection(self):
        '''
        Construit les deux menus déroulants du haut (avion, moteur) à partir des répertoires.
        '''
        top_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        top_frame.grid_columnconfigure((0, 5), weight=1)

        # Place les noms des avions/moteurs dans la classe (cb_avion, cv_moteur)
        self.chargerListeFichiers()

        # Sélection avion
        ctk.CTkLabel(top_frame, text="Avion :").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        self.cb_avion = ctk.CTkComboBox(top_frame, values=list(self.chemins_avions.keys()))
        self.cb_avion.set("")
        self.cb_avion.grid(row=0, column=2, padx=(5, 15), pady=5, sticky="w")

        # Sélection moteur
        ctk.CTkLabel(top_frame, text="Moteur :").grid(row=0, column=3, padx=15, pady=5, sticky="e")
        self.cb_moteur = ctk.CTkComboBox(top_frame, values=list(self.chemins_moteurs.keys()))
        self.cb_moteur.set("") 
        self.cb_moteur.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    def buildActionButtons(self):
        '''
        Construit les boutons sous ceux de sélection avion/moteur, qui servent à importer
        ou exporter les missions/batch, ou faire le calcul Point Performance.
        '''
        # Cadre centralisé sous l'avion et le moteur, mais au-dessus des onglets
        self.btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 0))
        self.btn_frame.grid_columnconfigure((0, 1), weight=1) # 2 colonnes

        # Bouton Calculer Dynamique
        self.btn_calculer = ctk.CTkButton(self.btn_frame, text="Calculer Mission",
                                          command=lambda: calculerMission(self), 
                                          fg_color="#2980b9", hover_color="#3498db")
        self.btn_calculer.grid(row=0, column=0, padx=5, pady=0, sticky="ew")

        # Bouton Importer Dynamique
        self.btn_importer = ctk.CTkButton(self.btn_frame, text="Importer résultats Mission",
                                          command=lambda: importerMission(self), 
                                          fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_importer.grid(row=0, column=1, padx=5, pady=0, sticky="ew")

    def build_bottom_buttons(self):
        '''
        Boutons en bas de l'interface, qui permettent d'importer ou d'exporter un jeu de paramètres.
        '''
        # On place ce frame à la row=3, sous les onglets (row=2)
        btn_frame_bas = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        btn_frame_bas.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        btn_frame_bas.grid_columnconfigure((0, 1), weight=1)

        # Boutons avec appels lambda pour passer 'self' aux fonctions externes
        ctk.CTkButton(
            btn_frame_bas, text="Importer config calcul", 
            command=lambda: importCSV(self), 
            fg_color="#E67E22", hover_color="#D35400"
        ).grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkButton(
            btn_frame_bas, text="Exporter config calcul", 
            command=lambda: exportCSV(self), 
            fg_color="#27AE60", hover_color="#2ECC71"
        ).grid(row=0, column=1, padx=5, sticky="ew")

    def buildTabs(self):
        '''
        Construction des onglets de l'interface.
        '''
        # Appel à une fonction à chaque changement d'onglet
        self.tabview = ctk.CTkTabview(self.left_frame, command=self.onTabChange)
        self.tabview.grid(row=2, column=0, sticky="nsew")

        # Ajout de chaque onglet, dans l'ordre
        self.tabview.add("Mission")
        self.tabview.add("Autres")
        self.tabview.add("Options")
        self.tabview.add("Point Performance")
        self.tabview.add("Batch")

        # Remplissage des onglets (classes définies dans le fichier onglets.py)
        self.onglet_mission = OngletMission(self.tabview.tab("Mission"), app=self)
        self.onglet_autres  = OngletAutres(self.tabview.tab("Autres"), app=self)
        self.onglet_options = OngletOptions(self.tabview.tab("Options"), app=self)
        self.onglet_PP      = OngletPP(self.tabview.tab("Point Performance"), app=self)
        self.onglet_batch   = OngletBatch(self.tabview.tab("Batch"), app=self)

    def onTabChange(self):
        '''
        Change dynamiquement le comportement des boutons selon l'onglet actif.
        '''
        current_tab = self.tabview.get()
        
        # Gérer le texte et la commande du bouton de calcul
        if current_tab == "Point Performance":
            self.btn_calculer.configure(text="Calculer PP", command=lambda: calculerPP(self))
        elif current_tab == "Batch":
            self.btn_calculer.configure(text="Calculer Batch", command=lambda: calculerBatch(self))
        else:
            self.btn_calculer.configure(text="Calculer Mission", command=lambda: calculerMission(self))
            
        # Gérer l'affichage du bouton d'importation et le centrage
        if current_tab == "Point Performance": # Cas particulier: un seul bouton
            self.btn_importer.grid_remove() # Masque le bouton d'importation
            self.btn_calculer.grid_configure(columnspan=2) # Étend le bouton restant sur toute la largeur
            self.btn_calculer.grid_configure(padx=(160,160)) # Ajoute du padding pour qu'il reste proportionné
        else:
            self.btn_calculer.grid_configure(columnspan=1) # Restreint le bouton à sa moitié
            self.btn_calculer.grid_configure(padx=(5,5))
            self.btn_importer.grid() # Réaffiche le bouton d'import
            
            # Changement des noms et fonctions appelées
            if current_tab == "Batch":
                self.btn_importer.configure(text="Importer résultats Batch", command=lambda: importerBatch(self), fg_color="#8e44ad", hover_color="#9b59b6")
            else:
                self.btn_importer.configure(text="Importer résultats Mission", command=lambda: importerMission(self), fg_color="#27ae60", hover_color="#2ecc71")

# ==========================
# LOGIQUE GRAPHIQUE (GRAPHIQUES & CHAMPS)
# ==========================
    def buildTabGraphiques(self):
        '''
        Construction de l'onglet "Graphiques" dans la partie outputs.
        '''
        # Position et apparence
        tab = self.right_tabview.tab("Graphiques")
        f_controls = ctk.CTkFrame(tab, fg_color="transparent")
        f_controls.pack(fill="x", pady=5)
        
        # Liste des données traçables (arrays dans Enregistrement.data)
        keys = list(self.Enregistrement.data.keys()) # + list(self.Enregistrement.data_cruise.keys())

        # Choix de l'axe Y
        ctk.CTkLabel(f_controls, text="Axe Y :").pack(side="left", padx=10)
        self.cb_y = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_y.set("h") 
        self.cb_y.pack(side="left", padx=5)
        
        # Choix de l'axe X
        ctk.CTkLabel(f_controls, text="Axe X :").pack(side="left", padx=10)
        self.cb_x = ctk.CTkComboBox(f_controls, values=keys, width=120)
        self.cb_x.set("l") 
        self.cb_x.pack(side="left", padx=5)

        # Choix de la mission pour les batchs
        self.lbl_batch = ctk.CTkLabel(f_controls, text="Mission :")
        self.lbl_batch.pack(side="left", padx=(15, 5))
        
        self.cb_batch = ctk.CTkComboBox(f_controls, values=["Mission unique"], width=200, command=self.loadBatchMission)
        self.cb_batch.set("Mission unique")
        self.cb_batch.pack(side="left", padx=5)

        # Bouton tracer
        ctk.CTkButton(f_controls, text="Tracer", command=self.tracerGraphique, width=100).pack(side="left", padx=20)

        # Paramètres de la figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0') 
        
        # Gestion des outils matplotlib (loupe, déplacement...)
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, tab)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def tracerGraphique(self):
        '''
        Effectue les tracés des valeurs sélectionnées, avec des unités aéronautiques 
        et des couleurs selon la phase de vol.
        '''
        # Check si l'Enregistrement contient des données
        if self.Enregistrement.counter == 0:
            messagebox.showinfo("Info", "Aucune donnée à tracer. Lancez d'abord un calcul de mission ou importez une mission existante.")
            return

        key_x = self.cb_x.get()
        key_y = self.cb_y.get()

        # Données en unités SI
        data_x_brut = self.Enregistrement.data[key_x][:self.Enregistrement.counter]
        data_y_brut = self.Enregistrement.data[key_y][:self.Enregistrement.counter]

        if data_x_brut.size != data_y_brut.size:
            messagebox.showinfo("Attention", "Vous avez sélectionné deux grandeurs n'ayant pas le même nombre d'éléments (sans doute " +
                                "des données croisière et mission). Veuillez tracer des grandeurs de taille similaire.")
            return

        # Récupération du tableau des phases
        phases = self.Enregistrement.data["phase"][:self.Enregistrement.counter]

        # Helper function pour la conversion des unités
        def conv_aero(key, arr):
            if key == "h": return arr / Constantes.conv_ft_m, "ft"
            if key == "l": return arr / Constantes.conv_NM_m, "nm"
            if key in ["CAS", "TAS", "Vx"]: return arr / Constantes.conv_kt_mps, "kt"
            if key == "Vz": return (arr / Constantes.conv_ft_m) * 60, "ft/min"
            if key == "t": return arr / 60, "min"
            if key == "P": return arr / 100, "hPa"
            if key == "T": return arr - 273.15, "°C"
            if key == "F_N": return arr / 1000, "kN"
            if key in ["SAR", "SGR"]: return arr / Constantes.conv_NM_m , "NM/kg"
            if key == "ECCF": return arr * Constantes.conv_NM_m, "kg/NM"
            # Grandeurs qui restent en unités SI
            unites = {"m": "kg", "FB": "kg", "rho": "kg/m³", "FF": "kg/s", "Mach": "Mach"}
            return arr, unites.get(key, "-")

        # Extraction des unités et valeurs
        data_x, unit_x = conv_aero(key_x, data_x_brut)
        data_y, unit_y = conv_aero(key_y, data_y_brut)

        # Dictionnaire associant la valeur de la phase à un nom et une couleur bien lisible
        phase_mapping = {
            0: {"nom": "Montée", "couleur": "#27ae60"},     # Vert
            1: {"nom": "Croisière", "couleur": "#2980b9"},  # Bleu
            2: {"nom": "Descente", "couleur": "#e67e22"},   # Orange
            3: {"nom": "Diversion", "couleur": "#8e44ad"},  # Violet
            4: {"nom": "Holding", "couleur": "#c0392b"}     # Rouge
        }

        # Nettoyage du graphique
        self.ax.clear()

        # Tracé segmenté par phase
        import numpy as np # Assure-toi que numpy est bien importé en haut de ton fichier
        
        for val_phase, infos in phase_mapping.items():
            # Création d'un masque booléen (True là où la phase correspond)
            masque = (phases == val_phase)
            
            # S'il y a des données pour cette phase, on trace le segment
            if np.any(masque):
                self.ax.plot(data_x[masque], data_y[masque], 
                             color=infos["couleur"], 
                             linewidth=2, 
                             label=infos["nom"])

        # Affichage des labels et des unités
        self.ax.set_xlabel(f"{key_x} [{unit_x}]", fontweight='bold')
        self.ax.set_ylabel(f"{key_y} [{unit_y}]", fontweight='bold')
        self.ax.set_title(f"{key_y} = f({key_x})")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Ajout de la légende à l'endroit le moins encombrant ("best")
        self.ax.legend(loc="best", framealpha=0.9)
        
        self.fig.tight_layout()
        self.canvas.draw()

    def loadBatchMission(self, choice=None):
        ''' Charge silencieusement les résultats d'une mission spécifique du batch pour les tracer '''
        if not self.batch_root_dir or choice == "Mission unique" or not choice:
            return
            
        vrai_nom_dossier = self.batch_missions_map.get(choice)
        if not vrai_nom_dossier:
            return
            
        chemin_csv = self.batch_root_dir / vrai_nom_dossier / "resultats_vol.csv"
        
        if not chemin_csv.exists():
            return
            
        # Chargement silencieux dans Enregistrement
        self.chargerFichierResultats(chemin_csv)

    def chargerFichierResultats(self, chemin_csv):
        '''
        Remplit l'attribut enregistrement de la classe avec les données issues du CSV.

        :param chemin_csv: Chemin complet du fichier resultats_vol.csv
        '''
        self.Enregistrement.reset()
        
        with open(chemin_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            
            # On charge toutes les lignes en mémoire
            lignes = list(reader)
            
            if len(lignes) >= 2:
                # Extraction des en-têtes (clés) et des unités
                noms_variables = lignes[0]
                donnees_lignes = lignes[2:] # Tout le reste correspond aux données
                
                if donnees_lignes:
                    # Transposition : on bascule les lignes en colonnes
                    # zip(*donnees_lignes) prend toutes les lignes et regroupe les éléments par colonne
                    colonnes = list(zip(*donnees_lignes))
                    
                    # Traitement colonne par colonne
                    for i, key in enumerate(noms_variables):
                        if key in self.Enregistrement.data:
                            # On récupère la colonne brute (une liste de chaînes de caractères)
                            colonne_brute = colonnes[i]
                            
                            # Conversion : on remplace "" par np.nan, puis on convertit en float32
                            vals = np.array(
                                [np.nan if val == "" else val for val in colonne_brute], 
                                dtype=np.float32
                            )
                            
                            l = len(vals)
                            self.Enregistrement.data[key][:l] = vals
                            self.Enregistrement.counter = max(self.Enregistrement.counter, l)

        # Retrace automatiquement avec les nouvelles données
        self.tracerGraphique()


    def chargerListeFichiers(self):
        '''
        Importe dans la classe le nom des avions et des moteurs.
        '''
        dossier_data = Path(__file__).parent.parent / "data"

        # Check de l'existence du dossier avion
        if not (dossier_data / "avions").exists():
            messagebox.showerror("Problème", "Dossier ./data/avions introuvable. Veuillez créer le répertoire à partir du dossier racine.")
            exit()

        self.chemins_avions = {}
        for f in (dossier_data / "avions").glob("*.csv"):
            # Skip de l'avion vide
            if f.name == "Avion_vide.csv": continue
            try:
                # Ouverture du fichier pour extraire le nom de l'avion
                with open(f, 'r', encoding='utf-8') as file:
                    premiere_ligne = file.readline().strip()
                    if premiere_ligne.startswith("Name;"):
                        self.chemins_avions[premiere_ligne.split(";")[1]] = str(f)
            except Exception: pass

        # Check de l'existence du dossier moteurs
        if not (dossier_data / "moteurs").exists():
            messagebox.showerror("Problème", "Dossier ./data/moteurs introuvable. Veuillez créer le répertoire à partir du dossier racine.")
            exit()
        
        # Chargement du nom de fichier uniquement (sans extension)
        self.chemins_moteurs = {}
        if (dossier_data / "moteurs").exists():
            for f in (dossier_data / "moteurs").glob("*.py"):
                if f.name == "Moteur_vide.py": continue
                self.chemins_moteurs[f.stem] = str(f)
