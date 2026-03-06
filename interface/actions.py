import customtkinter as ctk # pip install customtkinter
from missions.PointPerformance import PointPerformance
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Mission import Mission
from avions.Avion import Avion

from tkinter import filedialog, messagebox

from missions.Mission import Mission
from avions.Avion import Avion
from datetime import datetime
from pathlib import Path
import numpy as np
import csv
import os

import traceback

# ==========================
# MÉTIER : INSTANCIATION ET FICHIERS
# ==========================
def checkAvion(app):
    '''
    Vérifie que l'avion existe bien
    '''
    nom_avion = app.cb_avion.get()
    nom_moteur = app.cb_moteur.get()
    # print("Nom moteur: " + nom_moteur)
    # print("Chemin moteur: " + app.chemins_moteurs)
    # Au moment de la sauvegarde ou du chargement de l'avion :
    
    # Vérification du choix utilisateur et de la présence des fichiers
    if nom_avion and nom_moteur:
        if nom_avion not in app.chemins_avions or nom_moteur not in app.chemins_moteurs:
            messagebox.showwarning("Attention", "Erreur dans les noms des avions ou moteur.")
            return False
        return True
    else:
        messagebox.showwarning("Attention", "Veuillez sélectionner un avion et un moteur valides d'abord.")
        return False

def loadAvion(app):
    '''
    Charge l'avion en attribut de la classe (une fois avoir vérifié son existence et instancié la classe Inputs).
    '''
    chemin_absolu_moteur = Path(app.chemins_moteurs[app.cb_moteur.get()])

    # Tu peux extraire automatiquement les deux informations nécessaires :
    nom_fichier_py = chemin_absolu_moteur.name       # Renvoie "cfm56.py"
    engine_folder = chemin_absolu_moteur.parent.name # Renvoie "elodie_roux" ou "reseau_moteur"

    app.Inputs.engine_folder = engine_folder
    app.nom_fichier_py = nom_fichier_py

    app.Avion = Avion(app.Inputs)
    print(f">> Avion initialisé en mémoire.\n   - Modèle: {app.cb_avion.get()}\n   - Moteur: {app.cb_moteur.get()}\n")

def saveSettings(app, chemin_csv):
    '''
    Enregistre les paramètres choisis pour le calcul mission (onglet Mission, Autres, Options).
    '''
    with open(chemin_csv, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Attribut", "Valeur"])

        # Nom de fichier avion et moteur (non inclus car présent dans l'output console
        # et que les fichiers ne seront pas forcément là si l'utilisateur veut rejouer la mission)
        # nom_fichier_avion = Path(app.chemins_avions[app.cb_avion.get()]).name
        # nom_fichier_moteur = Path(app.chemins_moteurs[app.cb_moteur.get()]).name
        # writer.writerow(["nom_fichier_csv", nom_fichier_avion])
        # writer.writerow(["nom_fichier_py", nom_fichier_moteur])

        # Itération sur toutes les cases (uniquement mission, pas Point Performance ou Batch)
        for var_name, tk_var in app.vars.items():
            if var_name not in app.pp_keys and var_name not in app.batch_keys:
                writer.writerow([var_name, str(tk_var.get())])

def exportCSV(app):
    '''
    Exporte un CSV de la configuration actuelle.
    '''

    # Ouverture de l'interface système d'enregistrement
    chemin = filedialog.asksaveasfilename(
        defaultextension=".csv", 
        filetypes=[("Fichiers CSV", "*.csv")]
    )
    if not chemin: 
        return

    try:
        # Enregistrement des paramètres dans le fichier créé
        saveSettings(app, chemin)
                    
        # On utilise le redirector pour écrire dans la console
        app.redirector.write(f">> Configuration exportée vers {os.path.basename(chemin)}\n")
        messagebox.showinfo("Succès", "Fichier exporté avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def importCSV(app, chemin = None):
    '''
    Charge une configuration CSV dans l'interface.
    '''

    # Ouverture de l'interface système du choix de fichier
    if not (chemin):
        chemin = filedialog.askopenfilename(
            filetypes=[("Fichiers CSV", "*.csv")]
        )
    if not chemin: 
        return

    try:
        # Lecture ligne par ligne des paramètres du fichier
        with open(chemin, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    var_name, value = row
                    if var_name in app.vars:
                        # Gestion des cases à cocher (booléens) vs texte classique
                        if isinstance(app.vars[var_name], ctk.BooleanVar):
                            app.vars[var_name].set(value == "True")
                        else:
                            app.vars[var_name].set(value)
        
        # Actualise les champs dynamiques de la croisière en fonction du nouveau choix
        if hasattr(app, "update_cruise_fields"):
            app.update_cruise_fields()
            
        app.redirector.write(f">> Configuration importée depuis {os.path.basename(chemin)}\n")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de lecture: {str(e)}")

# ==========================
# MÉTIER : CALCULS
# ==========================
def calculerMission(app):
    '''
    Effectue une boucle mission complète.
    '''
    # Réinitialisation du menu Batch
    app.batch_root_dir = None
    app.batch_missions_map = {}
    app.cb_batch.configure(values=["Mission unique"])
    app.cb_batch.set("Mission unique")

    if not checkAvion(app): return

    # Remise à zéro de l'interface de sortie
    # app.textbox_out.delete("1.0", "end")
    
    # Préparation des dossiers
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    chemin_dossier = Path("./results") / timestamp
    chemin_dossier.mkdir(parents=True, exist_ok=True)
    
    # Redirection vers output.txt
    app.redirector.start_logging(chemin_dossier / "output.txt")
    
    # Sauvegarde & Chargement des paramètres dans Inputs
    chemin_csv = chemin_dossier / "param.csv"
    try:
        saveSettings(app, chemin_csv)
        app.Inputs.loadCSVFile(str(chemin_csv))
    except Exception as e:
        print(f"Erreur de sauvegarde/chargement des paramètres : {e}")
        app.redirector.stop_logging()
        return

    # Une fois qu'on a importé les inputs, on crée l'interface
    app.Atmosphere = Atmosphere(app.Inputs)

    try:
        print("\nLancement calcul de mission...\n")
        # Chargement de l'avion
        loadAvion(app)

        # Dernier check (redondant normalement)
        if not(app.Avion):
            return
        
        # Lancement du calcul de boucle mission
        app.Enregistrement.reset()
        Mission.Principal(app.Avion, app.Atmosphere, app.Enregistrement, app.Inputs)
        
        chemin_resultats = chemin_dossier / "resultats_vol.csv"
        app.Enregistrement.exportCSV(str(chemin_resultats))
        print(f"\n>> Résultats sauvegardés dans {chemin_resultats}")
        
        # Affichage graphes
        # app.right_tabview.set("Graphiques")
        app.tracerGraphique()
    except Exception as e:
        print(f"Erreur lors du calcul de la mission : {e}")
        print(traceback.format_exc()) # Erreur complète
    
    # Fin de l'enregistrement de l'output
    app.redirector.stop_logging()

def calculerPP(app):
    '''
    Effectue un calcul de Point Performance.
    '''
    if not checkAvion(app): return

    # Set des valeurs renseignées dans la classe Inputs 
    try:
        app.Inputs.cCz          = float(app.vars["cCz"].get())
        app.Inputs.cCx          = float(app.vars["cCx"].get())
        app.Inputs.cFF_climb    = float(app.vars["cFF_climb"].get())
        app.Inputs.cF_climb     = float(app.vars["cF_climb"].get())
        app.Inputs.cFF_cruise   = float(app.vars["cFF_cruise"].get())
        app.Inputs.cF_cruise    = float(app.vars["cF_cruise"].get())
        app.Inputs.cFF_descent  = float(app.vars["cFF_descent"].get())
        app.Inputs.cF_descent   = float(app.vars["cF_descent"].get())
        app.Inputs.SpeedType    = app.vars["SpeedType"].get()
        app.Inputs.Speed        = float(app.vars["Speed"].get())
        app.Inputs.altPP_ft     = float(app.vars["altPP_ft"].get())
        app.Inputs.massPP       = float(app.vars["massPP"].get())
        app.Inputs.DISA_PP      = float(app.vars["DISA_PP"].get())
        app.Inputs.Vw_kt        = float(app.vars["Vw_kt"].get())
    except ValueError:
        messagebox.showerror("Erreur", "Valeurs numériques invalides pour le Point Performance.")
        return
    
    # Une fois qu'on a importé les inputs, on crée l'interface
    app.Atmosphere = Atmosphere(app.Inputs)

    # Remise à zéro de la console
    # app.textbox_out.delete("1.0", "end")
    loadAvion(app)
    if not(app.Avion):
        return
    
    # Lancement des calculs
    print("\nLancement calcul Point Performance...")
    try:
        resultat = PointPerformance.Performance(app.Avion, app.Atmosphere, app.Inputs)
        print(resultat)
    except Exception as e:
        print(f"Erreur lors du calcul Point Performance : {e}")

def calculerBatch(app):
    '''
    Effectue un calcul de plusieurs missions à la fois.
    '''
    if not checkAvion(app): return
    
    # Parsing des inputs
    try:
        payloads = [float(p) for p in app.vars["batch_payloads"].get().split()]
        ranges   = [float(r) for r in app.vars["batch_ranges"].get().split()]
    except ValueError:
        messagebox.showerror("Erreur", "Format invalide pour Payloads/Ranges. Utilisez des espaces.")
        return

    # Remise à zéro de la console
    # app.textbox_out.delete("1.0", "end")
    
    # Préparation dossier racine (date et heure)
    timestamp = datetime.now().strftime("BATCH_%Y-%m-%d_%H-%M-%S")
    root_dir = Path("./results") / timestamp
    root_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Lancement du Batch : {len(payloads)} Payloads x {len(ranges)} Ranges.")
    print(f"Dossier racine : {root_dir}\n")

    # En-tête sur plusieurs lignes (inspiré de Piano-X). Ex:
    # Payload
    #    Load
    #    (kg)
    colonnes = [
        ("Fuel",     "Load",  "(kg)"),  ("Payload", "Mass", "(kg)"), # Paramètres globaux
        ("Mission",  "Range", "(NM)"),
        ("Mission",  "Dist",  "(NM)"),  ("Mission", "Time", "(min)"), ("Mission",  "Fuel", "(kg)"), 
        ("Climb",    "Dist",  "(NM)"),  ("Climb",   "Time", "(min)"), ("Climb",    "Fuel", "(kg)"), 
        ("Cruise",   "Dist",  "(NM)"),  ("Cruise",  "Time", "(min)"), ("Cruise",   "Fuel", "(kg)"), 
        ("Descent",  "Dist",  "(NM)"),  ("Descent", "Time", "(min)"), ("Descent",  "Fuel", "(kg)"),
                                        ("Reserve", "Time", "(min)"), ("Reserve",  "Fuel", "(kg)"), 
        ("Div",      "Dist",  "(NM)"),  ("Div",     "Time", "(min)"), ("Div",      "Fuel", "(kg)"),
        ("Hold",     "Dist",  "(NM)"),  ("Hold",    "Time", "(min)"), ("Hold",     "Fuel", "(kg)"),
                                                                      ("Conting.", "Fuel", "(kg)")
    ]
    
    # Espace de dix caractères pour chaque colonne
    ligne1 = "".join(f"{c[0]:>10}" for c in colonnes)
    ligne2 = "".join(f"{c[1]:>10}" for c in colonnes)
    ligne3 = "".join(f"{c[2]:>10}" for c in colonnes)
    
    summary_lines = [ligne1, ligne2, ligne3]
    summary_lines.append("")
    
    # Sauvegarde de l'état original
    orig_payload = app.vars["mPayload"].get()
    orig_range = app.vars["rangeMission_NM"].get()

    # Boucles Batch (groupement par payloads)
    for p in payloads:
        app.vars["mPayload"].set(str(p))
        for r in ranges:
            app.vars["rangeMission_NM"].set(str(r))
            
            # Choix du nom sous-dossier (payload et range)
            nom_dossier = f"m_payload_{int(p)}-range_{int(r)}"
            sub_dir = root_dir / nom_dossier
            sub_dir.mkdir(parents=True, exist_ok=True)
            
            # Passage en mode silencieux (rien dans la console mais uniquement
            # dans un fichier d'output)
            app.redirector.start_logging(sub_dir / "output.txt", silent=True)
            
            try:
                # Sauvegarde et chargement des paramètres
                chemin_csv = sub_dir / "param.csv"
                saveSettings(app, chemin_csv)
                app.Inputs.loadCSVFile(str(chemin_csv))

                # Une fois qu'on a importé les inputs, on crée l'interface
                app.Atmosphere = Atmosphere(app.Inputs)
                
                loadAvion(app)
                if not(app.Avion):
                    continue
                
                # Run d'une mission individuelle
                app.Enregistrement.reset()
                Mission.Principal(app.Avion, app.Atmosphere, app.Enregistrement, app.Inputs)
                app.Enregistrement.exportCSV(str(sub_dir / "resultats_vol.csv"))
                
                # Extraction des données ponctuelles finales
                md = app.Enregistrement.mission_data
                
                # Formatage des sorties
                fuel_load = md["FB_mission"] + md["FB_reserve"]
                mission_time = (md["t_climb"] + md["t_cruise"] + md["t_descent"]) / 60.0
                l_mission = (md["l_climb"] + md["l_cruise"] + md["l_descent"])
                t_reserve = (md['t_diversion'] + md['t_holding']) / 60.0
                
                conv = Constantes.conv_NM_m

                # Valeur de chaque colonne
                valeurs = [
                    fuel_load, p,
                    r, l_mission/conv,        mission_time,             md['FB_mission'],
                    md['l_climb']     / conv, md['t_climb']   / 60.0,   md['FB_climb'],
                    md['l_cruise']    / conv, md['t_cruise']  / 60.0,   md["FB_cruise"],
                    md['l_descent']   / conv, md['t_descent'] / 60.0,   md['FB_descent'],
                                              t_reserve,                md['FB_reserve'],
                    md['l_diversion'] / conv, md['t_diversion'] / 60.0, md['FB_diversion'],
                    md['l_holding']   / conv, md['t_holding']   / 60.0, md['FB_holding'],
                                                                        md['mF_contingency']
                ]
                
                ligne_valeurs = "".join(f"{v:10.1f}" for v in valeurs)
                summary_lines.append(ligne_valeurs)
                
            except Exception as e:
                print(f"Erreur fatale sur cette itération: {e}")
                print(traceback.format_exc()) # Erreur complète
                summary_lines.append(f"Erreur pour Payload={p}, Range={r}: {e}")
            
            # Fin de l'interception des outputs
            app.redirector.stop_logging()
            
        summary_lines.append("") # Saut de ligne par payload
        print(f">> Payload {p}kg terminée.")
        
    # Restauration GUI et sauvegarde Batch
    app.vars["mPayload"].set(orig_payload)
    app.vars["rangeMission_NM"].set(orig_range)
    
    # Écriture Summary.txt
    summary_text = "\n".join(summary_lines)
    with open(root_dir / "summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)
        
    # Écriture Summary.csv (extraction des blocs de 10 caractères pour faire des colonnes propres)
    with open(root_dir / "summary.csv", "w", encoding="utf-8") as f:
        f.write(";".join([f"{c[0]} {c[1]} {c[2]}" for c in colonnes]) + "\n")
        for ligne in summary_lines[3:]:
            if ligne.strip() == "":
                # f.write("\n") # Ecrire une ligne vide dans le CSV ?
                pass
            elif "Erreur" in ligne:
                f.write(ligne + "\n")
            else:
                valeurs_csv = [ligne[i:i+10].strip() for i in range(0, len(ligne), 10)]
                f.write(";".join(valeurs_csv) + "\n")

    # Menu déroulant batch
    app.batch_root_dir = root_dir
    app.batch_missions_map = {}
    noms_affiches = []

    for d in root_dir.iterdir():
        if d.is_dir() and "range" in d.name:
            # Extraction des valeurs depuis "m_payload_XXXX-range_YYYY"
            try:
                parts = d.name.split('-')
                payload_val = parts[0].split('_')[-1]
                range_val = parts[1].split('_')[-1]
                nom_joli = f"Payload: {payload_val} kg | Range: {range_val} NM"
            except:
                nom_joli = d.name # Sécurité au cas où le nom du dossier est inattendu

            app.batch_missions_map[nom_joli] = d.name
            noms_affiches.append(nom_joli)

    app.cb_batch.configure(values=noms_affiches)
    if noms_affiches:
        app.cb_batch.set(noms_affiches[-1])

    # Affichage final
    print("\n=== RÉSULTATS BATCH ===")
    print(summary_text)
    print(f"\n>> Résultats sauvegardés dans {root_dir}")

# ==========================
# MÉTIER : IMPORTATIONS
# ==========================
def importerMission(app):
    '''
    Importe les résultats d'une boucle mission faire précédemment.
    '''
    # Interface système de sélection d'un dossier
    init = Path.cwd() / "results"
    dossier = filedialog.askdirectory(title="Sélectionner le dossier de résultat de la mission",
                                      initialdir = init)
    
    if not dossier: return
    dossier = Path(dossier) # Permet d'utiliser la syntaxe /
    
    # Lire Output et afficher dans la console
    if (dossier / "output.txt").exists():
        # app.textbox_out.delete("1.0", "end")
        with open(dossier / "output.txt", "r", encoding="utf-8") as f:
            app.textbox_out.insert("end", f.read())
            
    # Lire Paramètres (à l'aide d'import CSV)
    if (dossier / "param.csv").exists():
        importCSV(app, dossier / "param.csv")
    
    # Lecture du csv des résultats
    chemin_csv = dossier / "resultats_vol.csv"
    if (chemin_csv).exists():
        app.Enregistrement.loadCSV(chemin_csv)
        
        # Réinitialisation du menu Batch
        app.batch_root_dir = None
        app.batch_missions_map = {}
        app.cb_batch.configure(values=["Mission unique"])
        app.cb_batch.set("Mission unique")
        messagebox.showinfo("Succès", "Mission importée et graphiques disponibles.")

        app.tracerGraphique()

def importerBatch(app):
    '''
    Importe les résultats d'un calcul en batch effectué précédemment.
    '''
    # Interface système pour le choix d'un dossier
    init = Path.cwd() / "results"
    dossier = filedialog.askdirectory(title="Sélectionner le dossier de résultat du batch",
                                      initialdir=init)
    if not dossier: return
    dossier = Path(dossier)
    
    # Affichage uniquement de la sortie texte
    if (dossier / "summary.txt").exists():
        # app.textbox_out.delete("1.0", "end")
        with open(dossier / "summary.txt", "r", encoding="utf-8") as f:
            app.textbox_out.insert("end", f.read())
        app.right_tabview.set("Console")

        # Menu déroulant batch
        app.batch_root_dir = dossier
        app.batch_missions_map = {}
        noms_affiches = []

        for d in dossier.iterdir():
            if d.is_dir() and "range" in d.name:
                try:
                    # Séparation du nom de dossier pour l'affichage
                    parts = d.name.split('-')
                    payload_val = parts[0].split('_')[-1]
                    range_val = parts[1].split('_')[-1]
                    nom_joli = f"Payload: {payload_val} kg | Range: {range_val} NM"
                except:
                    nom_joli = d.name

                # Mise à jour du dictionnaire
                app.batch_missions_map[nom_joli] = d.name
                noms_affiches.append(nom_joli)

        # Chargement de la mission sélectionnée
        app.cb_batch.configure(values=noms_affiches)
        if noms_affiches:
            app.cb_batch.set(noms_affiches[0])
            app.loadBatchMission(noms_affiches[0])
    else:
        messagebox.showerror("Erreur", "Fichier summary.txt introuvable dans ce dossier.")
