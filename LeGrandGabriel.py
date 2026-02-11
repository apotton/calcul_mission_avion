import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
root = tk.Tk()
root.title("PIE COA26")
root.geometry("1200x900")



COMMUN = {"font": ("Arial", 10)}
#-------------------Normalement tu l'as déjà---------------------------
main_frame_gauche = tk.Frame(root)
main_frame_droite= tk.Frame(root)
tk.Label(main_frame_gauche, text="Adjust:").grid(row=1, column=0, sticky="w")
entree_choisie = tk.StringVar()
menu_deroulant_1 = ttk.Combobox(main_frame_gauche, textvariable = entree_choisie, state="readonly")
menu_deroulant_1['values'] = ('Basic Design Weights', "Thrust Drag Fuel Flow", "Emission indices", "Speed and flight levels", "Reserve and Allowances", "Unit preferences")
menu_deroulant_1.grid(row=1, column =1,columnspan = 3, sticky= "ew")
#-------------------Fin du normalement tu l'as déjà----------------------------

#------------------Début de la partie affichage dans un .txt -----------------------------------------------
DOSSIER_SORTIE = Path(__file__).parent


if not DOSSIER_SORTIE.exists():
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)

def sauvegarder_donnees():
    # CHANGEMENT 1 : Extension .csv par défaut
    chemin = filedialog.asksaveasfilename(
        initialdir=DOSSIER_SORTIE, 
        defaultextension=".csv", 
        filetypes=[("Fichier CSV", "*.csv"), ("Tous les fichiers", "*.*")], 
        title="Sauvegarder les données de mission"
    )
    
    if not chemin:
        return

    try:
        # Dictionnaire de toutes tes variables Entry
        # Format : "Nom_Dans_Le_CSV": variable_python
        data = {
            # Reserves and Allowances
            "Diversion_Distance": distance_de_diversion, "Holding_Time": temps_attente,
            "Contingency_Fuel": carburant_de_reserve, "Taxi_Out": t_taxi_out,
            "Takeoff_Allowance": t_take_off, "Approach_Allowance": t_approach,
            "Taxi_In": t_taxi_in, "Missed_Approach": t_miis_approach,
            
            # Basic Design Weights
            "MTOW": m_MTOW, "OWE": m_OWE, "MZFW": m_MZFW, "MLW": m_MLW,
            "N_Passengers": n_passengers, "Mass_Per_Pax": m_passenger, "Cargo_Mass": m_cargo,
            
            # Thrust Drag Fuel Flow
            "TO_Thrust_Factor": pousee_takeoff_facteur, "Climb_Thrust_Factor": pousee_montée_facteur,
            "Cruise_Thrust_Factor": poussee_croisiere_facteur, "All_Thrust_Factor": pousee_totale_facteur,
            "Zero_Lift_Drag_Factor": trainee_zeroportance_facteur, "Induced_Drag_Factor": trainee_induite_facteur,
            "Divergence_Mach": mach_divergence_trainee, "All_Drag_Factor": trainee_complete_facteur, "SFC": sfc,
            
            # Emission Indices (Fuel Flow)
            "FF_Idle": debit_carburant_idle, "FF_App": debit_carburant_approach,
            "FF_Climb": debit_carburant_climbout, "FF_TO": debit_carburant_takeoff,
            "NOx_Idle": emissions_nox_idle, "NOx_App": emissions_nox_approach,
            "NOx_Climb": emissions_nox_climbout, "NOx_TO": emissions_nox_takeoff,
            "HC_Idle": emissions_hc_idle, "HC_App": emissions_hc_approach,
            "HC_Climb": emissions_hc_climbout, "HC_TO": emissions_hc_takeoff,
            "CO_Idle": emissions_co_idle, "CO_App": emissions_co_approach,
            "CO_Climb": emissions_co_climbout, "CO_TO": emissions_co_takeoff,
            
            # Performance Points
            "Point_Mach": mach_choisi, "Point_KCAS": kcas_choisie,
            "Point_KEAS": keas_choisie, "Point_KTAS": ktas_choisie,
            "Point_Alt": altitude, "Point_Weight": poids,
            
            # Field Lengths
            "TO_Weight": poids_decolage, "LD_Weight": poids_atterrissage,
            "TO_Alt": altitude_decolage, "LD_Alt": altitude_atterrissage,
            "TO_Temp_Dev": t_deviation_decolage, "LD_Temp_Dev": t_deviasion_atterrissage
        }

        # CHANGEMENT 2 : newline='' évite les lignes vides sous Windows
        with open(chemin, "w", encoding="utf-8", newline='') as f:
            # On écrit l'en-tête (Titres des colonnes)
            f.write("Attribut;Valeur\n")
            
            for cle, widget in data.items():
                valeur = widget.get() if widget else ""
                # CHANGEMENT 3 : Utilisation du point-virgule
                f.write(f"{cle};{valeur}\n")
        
        messagebox.showinfo("Succès", f"Fichier CSV créé dans :\n{chemin}")
        
        # Ouvre le fichier avec le logiciel par défaut (Excel ou Bloc-notes)
        try:
            os.startfile(chemin)
        except AttributeError:
            # Fallback pour Mac/Linux si jamais le code bouge un jour
            import subprocess
            subprocess.call(['open', chemin])
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de créer le fichier : {e}")

def charger_donnees():
    # CHANGEMENT 4 : Filtre pour .csv
    chemin = filedialog.askopenfilename(
        initialdir=DOSSIER_SORTIE,
        filetypes=[("Fichier CSV", "*.csv"), ("Fichier texte", "*.txt")]
    )
    
    if not chemin:
        return
        
    try:
        # Mapping (identique à sauvegarder_donnees)
        mapping = {
            "Diversion_Distance": distance_de_diversion, "Holding_Time": temps_attente,
            "Contingency_Fuel": carburant_de_reserve, "Taxi_Out": t_taxi_out,
            "Takeoff_Allowance": t_take_off, "Approach_Allowance": t_approach,
            "Taxi_In": t_taxi_in, "Missed_Approach": t_miis_approach,
            "MTOW": m_MTOW, "OWE": m_OWE, "MZFW": m_MZFW, "MLW": m_MLW,
            "N_Passengers": n_passengers, "Mass_Per_Pax": m_passenger, "Cargo_Mass": m_cargo,
            "TO_Thrust_Factor": pousee_takeoff_facteur, "Climb_Thrust_Factor": pousee_montée_facteur,
            "Cruise_Thrust_Factor": poussee_croisiere_facteur, "All_Thrust_Factor": pousee_totale_facteur,
            "Zero_Lift_Drag_Factor": trainee_zeroportance_facteur, "Induced_Drag_Factor": trainee_induite_facteur,
            "Divergence_Mach": mach_divergence_trainee, "All_Drag_Factor": trainee_complete_facteur, "SFC": sfc,
            "FF_Idle": debit_carburant_idle, "FF_App": debit_carburant_approach,
            "FF_Climb": debit_carburant_climbout, "FF_TO": debit_carburant_takeoff,
            "NOx_Idle": emissions_nox_idle, "NOx_App": emissions_nox_approach,
            "NOx_Climb": emissions_nox_climbout, "NOx_TO": emissions_nox_takeoff,
            "HC_Idle": emissions_hc_idle, "HC_App": emissions_hc_approach,
            "HC_Climb": emissions_hc_climbout, "HC_TO": emissions_hc_takeoff,
            "CO_Idle": emissions_co_idle, "CO_App": emissions_co_approach,
            "CO_Climb": emissions_co_climbout, "CO_TO": emissions_co_takeoff,
            "Point_Mach": mach_choisi, "Point_KCAS": kcas_choisie,
            "Point_KEAS": keas_choisie, "Point_KTAS": ktas_choisie,
            "Point_Alt": altitude, "Point_Weight": poids,
            "TO_Weight": poids_decolage, "LD_Weight": poids_atterrissage,
            "TO_Alt": altitude_decolage, "LD_Alt": altitude_atterrissage,
            "TO_Temp_Dev": t_deviation_decolage, "LD_Temp_Dev": t_deviasion_atterrissage
        }

        with open(chemin, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                # CHANGEMENT 5 : Lecture avec point-virgule
                if ";" in ligne:
                    parts = ligne.split(";", 1)
                    if len(parts) == 2:
                        cle, valeur = parts
                        
                        # On ignore la ligne d'en-tête si on tombe dessus
                        if cle == "Attribut": 
                            continue
                            
                        if cle in mapping:
                            widget = mapping[cle]
                            # On vide et on remplit
                            if widget: # Sécurité si widget est None
                                widget.delete(0, tk.END)
                                widget.insert(0, valeur)

        messagebox.showinfo("Succès", "Données importées avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la lecture : {e}")


#------------------------------Fin du .txt-----------------------------------------------

#------------------Frame du "Reserves and allowances"-----------------------------------------------------
frame_Reserves_and_allowances=tk.Frame(main_frame_gauche)

frame_Reserves_and_allowances1=tk.Frame(frame_Reserves_and_allowances)
frame_Reserves_and_allowances2=tk.Frame(frame_Reserves_and_allowances1)

frame_Reserves_and_allowances1.grid(row=2, column=0, columnspan=5)
frame_Reserves_and_allowances2.grid(row=6, column=0, columnspan=6)


tk.Label(frame_Reserves_and_allowances1, text="Diversion Distance (nm)").grid(row=2, column=0)
distance_de_diversion = tk.Entry(frame_Reserves_and_allowances1, width=10)
distance_de_diversion.grid(row=2, column=1)
tk.Label(frame_Reserves_and_allowances1, text="Holding Time (min)").grid(row=3, column=0)
temps_attente = tk.Entry(frame_Reserves_and_allowances1, width=10)
temps_attente.grid(row=3, column=1)
tk.Label(frame_Reserves_and_allowances1, text="Contingency Fuel Rule").grid(row=4, column=0)
carburant_de_reserve = tk.Entry(frame_Reserves_and_allowances1, width=10)
carburant_de_reserve.grid(row=4, column=1)

liste_choix_Fuel_Rule= ["% Of mission fuel", "% Of total fuel", "% Of MTOW", "% Of flight time"]
menu_deroulant_choix_Fuel_Rule=ttk.Combobox(frame_Reserves_and_allowances1, values=liste_choix_Fuel_Rule,state="readonly").grid(row=4, column=2, sticky="w")

tk.Label(frame_Reserves_and_allowances2, text="Allowances:").grid(row=6, column=0)
tk.Label(frame_Reserves_and_allowances2, text="taxi out").grid(row=6, column=1)
t_taxi_out = tk.Entry(frame_Reserves_and_allowances2, width=10)
t_taxi_out.grid(row=7, column=1)
tk.Label(frame_Reserves_and_allowances2, text="takeoff").grid(row=6, column=2)
t_take_off = tk.Entry(frame_Reserves_and_allowances2, width=10)
t_take_off.grid(row=7, column=2)
tk.Label(frame_Reserves_and_allowances2, text="approach").grid(row=6, column=3)
t_approach = tk.Entry(frame_Reserves_and_allowances2, width=10)
t_approach.grid(row=7, column=3)
tk.Label(frame_Reserves_and_allowances2, text="taxi in").grid(row=6, column=4)
t_taxi_in = tk.Entry(frame_Reserves_and_allowances2, width=10)
t_taxi_in.grid(row=7, column=4)
tk.Label(frame_Reserves_and_allowances2, text="miss.app.").grid(row=6, column=5)
t_miis_approach = tk.Entry(frame_Reserves_and_allowances2, width=10)
t_miis_approach.grid(row=7, column=5)
tk.Label(frame_Reserves_and_allowances2, text="Time (min)").grid(row=7, column=0)
#------------------Fin de frame du "Reserves and allowances"-----------------------------------------------------

#------------------Frame du "Basic Design Weights"-----------------------------------------------------
frame_Basic_Design_Weights=tk.Frame(main_frame_gauche)
frame_Basic_Design_Weights.grid_forget()

#def
tk.Label(frame_Basic_Design_Weights, text="Weight (kg)").grid(row=2, column=1)
tk.Label(frame_Basic_Design_Weights, text="Standard Payload").grid(row=2, column=3)

tk.Label(frame_Basic_Design_Weights, text="Max Take Off").grid(row=3,column=0, sticky="e")
m_MTOW = tk.Entry(frame_Basic_Design_Weights, width=10)
m_MTOW.grid(row=3,column=1)
tk.Label(frame_Basic_Design_Weights, text="Operating Empty").grid(row=4,column=0, sticky="e")
m_OWE = tk.Entry(frame_Basic_Design_Weights, width=10)
m_OWE.grid(row=4,column=1)
tk.Label(frame_Basic_Design_Weights, text="Max Zero Fuel").grid(row=5,column=0, sticky="e")
m_MZFW = tk.Entry(frame_Basic_Design_Weights, width=10)
m_MZFW.grid(row=5,column=1)
tk.Label(frame_Basic_Design_Weights, text="Max Landing").grid(row=6,column=0, sticky="e")
m_MLW = tk.Entry(frame_Basic_Design_Weights, width=10)
m_MLW.grid(row=6,column=1)

tk.Label(frame_Basic_Design_Weights, text="passengers").grid(row=3,column=4, sticky="w")
n_passengers = tk.Entry(frame_Basic_Design_Weights, width=10)
n_passengers.grid(row=3,column=3)
tk.Label(frame_Basic_Design_Weights, text="kg each").grid(row=4,column=4, sticky="w")
m_passenger = tk.Entry(frame_Basic_Design_Weights, width=10)
m_passenger.grid(row=4,column=3)
tk.Label(frame_Basic_Design_Weights, text="kg cargo").grid(row=5,column=4, sticky="w")
m_cargo = tk.Entry(frame_Basic_Design_Weights, width=10)
m_cargo.grid(row=5,column=3)
tk.Label(frame_Basic_Design_Weights, text="@").grid(row=4, column=2, sticky="e")
tk.Label(frame_Basic_Design_Weights, text="+").grid(row=5, column=2, sticky="e")

#------------------Fin du frame du "Basic Design Weights"-----------------------------------------------------

#------------------Frame du "Thrust, Drag, Fuel Flow"-----------------------------------------------------
frame_Thrust_Drag_Fuel_Flow=tk.Frame(main_frame_gauche)
frame_Thrust_Drag_Fuel_Flow.grid_forget()

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Factor").grid(row=2, column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Factor").grid(row=2, column=3)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Takeoff Thrust").grid(row=3,column=0, sticky="e")
pousee_takeoff_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
pousee_takeoff_facteur.grid(row=3,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Climb Thrust").grid(row=4,column=0, sticky="e")
pousee_montée_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
pousee_montée_facteur.grid(row=4,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Cruise Thrust").grid(row=5,column=0, sticky="e")
poussee_croisiere_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
poussee_croisiere_facteur.grid(row=5,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="All Thrusts").grid(row=6,column=0, sticky="e")
pousee_totale_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
pousee_totale_facteur.grid(row=6,column=1)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Zero-lift Drag").grid(row=3,column=2, sticky="e")
trainee_zeroportance_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
trainee_zeroportance_facteur.grid(row=3,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Induced Drag").grid(row=4,column=2, sticky="e")
trainee_induite_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
trainee_induite_facteur.grid(row=4,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Divergence_Mach").grid(row=5,column=2, sticky="e")
mach_divergence_trainee = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
mach_divergence_trainee.grid(row=5,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="All Drag").grid(row=6, column=2)
trainee_complete_facteur = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
trainee_complete_facteur.grid(row=6, column=3)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Fuel Flow (SFC)").grid(row=7, column=2, sticky="e")
sfc = tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10)
sfc.grid(row=7, column=3)
#------------------Fin du frame du "Thrust, Drag, Fuel Flow"-----------------------------------------------------

#------------------Frame du "Emission indices"-----------------------------------------------------
frame_Emission_indices=tk.Frame(main_frame_gauche)
frame_Emission_indices.grid_forget()

tk.Label(frame_Emission_indices, text="fuel flow").grid(row=2, column=0)
tk.Label(frame_Emission_indices, text="kg/s").grid(row=3, column=0, sticky="w")
tk.Label(frame_Emission_indices, text="Reference Emissions Indices (grams pollutant per kg fuel):").grid(row=4, column=0, columnspan=5, sticky="w")


tk.Label(frame_Emission_indices, text="idle").grid(row=2, column=1)
debit_carburant_idle = tk.Entry(frame_Emission_indices, width=10)
debit_carburant_idle.grid(row=3, column=1)
tk.Label(frame_Emission_indices, text="approach").grid(row=2, column=2)
debit_carburant_approach = tk.Entry(frame_Emission_indices, width=10)
debit_carburant_approach.grid(row=3, column=2)
tk.Label(frame_Emission_indices, text="climbout").grid(row=2, column=3)
debit_carburant_climbout = tk.Entry(frame_Emission_indices, width=10)
debit_carburant_climbout.grid(row=3, column=3)
tk.Label(frame_Emission_indices, text="takeoff").grid(row=2, column=4)
debit_carburant_takeoff = tk.Entry(frame_Emission_indices, width=10)
debit_carburant_takeoff.grid(row=3, column=4)

tk.Label(frame_Emission_indices, text="NOx").grid(row=5, column=0, sticky="w")
emissions_nox_idle = tk.Entry(frame_Emission_indices, width=10)
emissions_nox_idle.grid(row=5, column=1)
emissions_nox_approach =tk.Entry(frame_Emission_indices, width=10)
emissions_nox_approach.grid(row=5, column=2)
emissions_nox_climbout =tk.Entry(frame_Emission_indices, width=10)
emissions_nox_climbout.grid(row=5, column=3)
emissions_nox_takeoff =tk.Entry(frame_Emission_indices, width=10)
emissions_nox_takeoff.grid(row=5, column=4)
tk.Label(frame_Emission_indices, text="HC").grid(row=6, column=0, sticky="w")
emissions_hc_idle =tk.Entry(frame_Emission_indices, width=10)
emissions_hc_idle.grid(row=6, column=1)
emissions_hc_approach =tk.Entry(frame_Emission_indices, width=10)
emissions_hc_approach.grid(row=6, column=2)
emissions_hc_climbout =tk.Entry(frame_Emission_indices, width=10)
emissions_hc_climbout.grid(row=6, column=3)
emissions_hc_takeoff =tk.Entry(frame_Emission_indices, width=10)
emissions_hc_takeoff.grid(row=6, column=4)
tk.Label(frame_Emission_indices, text="CO").grid(row=7, column=0, sticky="w")
emissions_co_idle =tk.Entry(frame_Emission_indices, width=10)
emissions_co_idle.grid(row=7, column=1)
emissions_co_approach =tk.Entry(frame_Emission_indices, width=10)
emissions_co_approach.grid(row=7, column=2)
emissions_co_climbout =tk.Entry(frame_Emission_indices, width=10)
emissions_co_climbout.grid(row=7, column=3)
emissions_co_takeoff =tk.Entry(frame_Emission_indices, width=10)
emissions_co_takeoff.grid(row=7, column=4)
#------------------Fin du frame du "Emission indices"-----------------------------------------------------

#------------------Frame du "Speed and flight levels"-----------------------------------------------------
frame_optionnel = tk.Frame(main_frame_gauche, bd=1, relief="sunken", padx=10, pady=10)
variable_mach = tk.IntVar()
variable_mach.set(1)
tk.Label(frame_optionnel, text="Cruise Mach :").grid(row=0, column=0, padx=(0, 0))

tk.Radiobutton(frame_optionnel, variable=variable_mach, value = 1).grid(row=0, column=1)
tk.Label(frame_optionnel, text="Economy").grid(row=0, column=2, padx=(0, 0), sticky="w")
tk.Radiobutton(frame_optionnel, variable=variable_mach, value = 2).grid(row=0, column=3)
tk.Label(frame_optionnel, text="Longe Range").grid(row=0, column=4, padx=(0, 0), sticky="w")
tk.Radiobutton(frame_optionnel, variable=variable_mach, value = 3).grid(row=1, column=1)
tk.Label(frame_optionnel, text="High Range").grid(row=1, column=2, padx=(0, 0), sticky="w")
tk.Radiobutton(frame_optionnel, variable=variable_mach, value = 4).grid(row=1, column=3)
tk.Label(frame_optionnel, text="Max(single FL)").grid(row=1, column=4, padx=(0, 0), sticky="w")
tk.Radiobutton(frame_optionnel, variable=variable_mach, value = 5).grid(row=2, column=1)
mach_croisere = tk.Entry(frame_optionnel, **COMMUN)
mach_croisere.grid(row=2, column=2, columnspan= 2,sticky="w")

frame_optionnel.rowconfigure(3, minsize=20)

tk.Label(frame_optionnel, text="Available flight level (ft/100)", font = ("Arial", 8)).grid(row=4, column=0)
niveau_vol_disponible = tk.Entry(frame_optionnel, **COMMUN)
niveau_vol_disponible.grid(row=4, column=2)

frame_optionnel.rowconfigure(5, minsize=20)

variable_speed= tk.IntVar()
tk.Label(frame_optionnel, text="Climb Speed (KCAS)", font = ("Arial", 8)).grid(row=6, column=0)
kcas = tk.Entry(frame_optionnel, **COMMUN)
kcas.grid(row=6, column=2)
tk.Label(frame_optionnel, text="Climb Mach", font = ("Arial", 8)).grid(row=7, column=0)
mach_montee = tk.Entry(frame_optionnel, **COMMUN)
mach_montee.grid(row=7, column=2)
#------------------Fin de frame du "Speed and flight levels"-----------------------------------------------------

#------------------Frame du "Unit preferences"-----------------------------------------------------
frame_unit_preferences = tk.Frame(main_frame_gauche, bd=1, relief="sunken", padx=10, pady=10)
variable_range = tk.IntVar()
variable_range.set(1)
variable_masse = tk.IntVar()
variable_masse.set(1)
variable_altitude = tk.IntVar()
variable_altitude.set(1)
variable_longueur = tk.IntVar()
variable_longueur.set(1)
variable_random_unit = tk.IntVar()
variable_random_unit.set(1)

tk.Label(frame_unit_preferences, text="Distances :").grid(row=0, column=0, padx=(0, 5))
tk.Radiobutton(frame_unit_preferences, variable=variable_range, value = 1).grid(row=0, column=1)
tk.Label(frame_unit_preferences, text="kilomètres").grid(row=0, column=2, padx=(0, 5),  sticky="w")
tk.Radiobutton(frame_unit_preferences, variable=variable_range, value = 2).grid(row=0, column=3)
tk.Label(frame_unit_preferences, text="miles nautiques").grid(row=0, column=4, padx=(0, 5),  sticky="w")

tk.Label(frame_unit_preferences, text="Masses :").grid(row=1, column=0, padx=(0, 5))
tk.Radiobutton(frame_unit_preferences, variable=variable_masse, value = 1).grid(row=1, column=1)
tk.Label(frame_unit_preferences, text="kilogrammes").grid(row=1, column=2, padx=(0, 5),  sticky="w")
tk.Radiobutton(frame_unit_preferences, variable=variable_masse, value = 2).grid(row=1, column=3)
tk.Label(frame_unit_preferences, text="livres").grid(row=1, column=4, padx=(0, 5),  sticky="w")

tk.Label(frame_unit_preferences, text="Altitudes :").grid(row=2, column=0, padx=(0, 5))
tk.Radiobutton(frame_unit_preferences, variable=variable_altitude, value = 1).grid(row=2, column=1)
tk.Label(frame_unit_preferences, text="metres").grid(row=2, column=2, padx=(0, 5),  sticky="w")
tk.Radiobutton(frame_unit_preferences, variable=variable_altitude, value = 2).grid(row=2, column=3)
tk.Label(frame_unit_preferences, text="pieds").grid(row=2, column=4, padx=(0, 5),  sticky="w")

tk.Label(frame_unit_preferences, text="Longueur de piste :").grid(row=3, column=0, padx=(0, 5))
tk.Radiobutton(frame_unit_preferences, variable=variable_longueur, value = 1).grid(row=3, column=1)
tk.Label(frame_unit_preferences, text="metres").grid(row=3, column=2, padx=(0, 5),  sticky="w")
tk.Radiobutton(frame_unit_preferences, variable=variable_longueur, value = 2).grid(row=3, column=3)
tk.Label(frame_unit_preferences, text="pieds").grid(row=3, column=4, padx=(0, 5),  sticky="w")

tk.Label(frame_unit_preferences, text="Les autres unités:").grid(row=4, column=0, padx=(0, 5))
tk.Radiobutton(frame_unit_preferences, variable=variable_random_unit, value = 1).grid(row=4, column=1)
tk.Label(frame_unit_preferences, text="Métriques").grid(row=4, column=2, padx=(0, 5),  sticky="w")
tk.Radiobutton(frame_unit_preferences, variable=variable_random_unit, value = 2).grid(row=4, column=3)
tk.Label(frame_unit_preferences, text="Impériales").grid(row=4, column=4, padx=(0, 5),  sticky="w")


#------------------Fin du frame du "Unit preferences"-----------------------------------------------------
def affichage(event):
    if menu_deroulant_1.get() == "Unit preferences":

        frame_unit_preferences.grid(row=6, column=0, columnspan=6, sticky="ew")
    else :
        frame_unit_preferences.grid_forget()
    if menu_deroulant_1.get() == "Basic Design Weights":

        frame_Basic_Design_Weights.grid(row=6, column=0, columnspan=6, sticky="ew")
    else :
        frame_Basic_Design_Weights.grid_forget()
    if menu_deroulant_1.get() == "Thrust Drag Fuel Flow":

        frame_Thrust_Drag_Fuel_Flow.grid(row=6, column=0, columnspan=6, sticky="ew")
    else :
        frame_Thrust_Drag_Fuel_Flow.grid_forget()

    if menu_deroulant_1.get() == "Emission indices":

        frame_Emission_indices.grid(row=6, column=0, columnspan=6, sticky="ew")
    else :
        frame_Emission_indices.grid_forget()
        
    if menu_deroulant_1.get() == "Speed and flight levels":

        frame_optionnel.grid(row=6, column=0, columnspan=6, sticky="ew")
    else:
        frame_optionnel.grid_forget()
    
    if menu_deroulant_1.get() == "Reserve and Allowances":

        frame_Reserves_and_allowances.grid(row=6, column=0, columnspan=6, sticky="ew")
    else:
        frame_Reserves_and_allowances.grid_forget()

menu_deroulant_1.bind("<<ComboboxSelected>>", affichage)


#-----------------------Partie Fixe en bas de la page-----------------------------------------------------
tk.Button(main_frame_gauche, text = "Sauvegarder", command=sauvegarder_donnees).grid(row=12, column=0, columnspan = 3)
tk.Button(main_frame_gauche, text = "Charger", command = charger_donnees).grid(row=12, column =3, columnspan = 3)
main_frame_gauche.rowconfigure(13, minsize=20)
tk.Frame(main_frame_gauche, height=2, bg="black").grid(row=14, column=0, columnspan=6, sticky="ew")

frame_bas_de_page = tk.Frame(main_frame_gauche)
frame_bas_de_page.grid(row=18, column=0, columnspan=6, sticky="nw")

main_frame_gauche.rowconfigure(15, minsize=20)
tk.Label(main_frame_gauche, text="output:").grid(row=16, column=0, sticky="w")
variable_choisie = tk.StringVar()
menu_deroulant = ttk.Combobox(main_frame_gauche, textvariable = variable_choisie, state="readonly")
menu_deroulant['values'] = ('Block Range Summary', "Detailed Flight Profile", "Block Performance Tables", "Point Performance", "Payload_Range Boundary", "Takeoff/Landing Field Lengths")
menu_deroulant.grid(row=16, column =1,columnspan = 3, sticky= "ew")
menu_deroulant.current(0) 

tk.Button(main_frame_gauche, text ="OK", command = lambda : print ("Sélection :", variable_choisie.get())).grid(row=16, column=4, sticky="w", padx=5)

#----------------------------Frame du "Block Range Summary"-------------------------
frame_Block_range_summary = tk.Frame(frame_bas_de_page, bd = 1, relief = "sunken", padx=10, pady=10)
case_var = tk.IntVar()
case_var.set(1)
tk.Radiobutton(frame_Block_range_summary, variable=case_var, value = 1).grid(row=0, column=1, sticky="w")
tk.Label(frame_Block_range_summary, text="Design range with Standard Payload").grid(row=0, column=2, columnspan=2, sticky="w", padx=(20, 0))
tk.Radiobutton(frame_Block_range_summary, variable=case_var, value = 2).grid(row=1, column=1, sticky="w")
tk.Label(frame_Block_range_summary, text="Range (nm)").grid(row=1, column=2, sticky="w", padx=(20, 0))
tk.Label(frame_Block_range_summary, text="with Payload(kg)").grid(row=1, column=3, sticky="w", padx=(20, 0))
range = tk.Entry(frame_Block_range_summary, **COMMUN)
range.grid(row=2, column =2)
payload = tk.Entry(frame_Block_range_summary, **COMMUN)
payload.grid(row=2, column =3)

#----------------------------Fin du frame du "Block Range Summary"-------------------------

#----------------------------Frame du "Detailed flight profile"-------------------------
frame_Detailed_flight_profile= tk.Frame(frame_bas_de_page, bd = 1, relief = "sunken", padx=10, pady=10)
flight_var = tk.IntVar()
flight_var.set(1)
tk.Radiobutton(frame_Detailed_flight_profile, variable=flight_var, value = 1).grid(row=0, column=1, sticky="w")
tk.Label(frame_Detailed_flight_profile, text="Design range with Standard Payload").grid(row=0, column=2, columnspan=2, sticky="w", padx=(20, 0))
tk.Radiobutton(frame_Detailed_flight_profile, variable=flight_var, value = 2).grid(row=1, column=1, sticky="w")
tk.Label(frame_Detailed_flight_profile, text="Range (nm)").grid(row=1, column=2, sticky="w", padx=(20, 0))
tk.Label(frame_Detailed_flight_profile, text="with Payload(kg)").grid(row=1, column=3, sticky="w", padx=(20, 0))
range = tk.Entry(frame_Detailed_flight_profile, **COMMUN)
range.grid(row=2, column =2)
paylaod = tk.Entry(frame_Detailed_flight_profile, **COMMUN)
payload.grid(row=2, column =3)

#----------------------------Fin du frame du "Detailed flight profile"-------------------------


#-----//------------Frame du "Block performance table"-----------------------------------------------------
frame_Block_performance_table = tk.Frame(frame_bas_de_page, bd=1, relief="sunken", padx=10, pady=10)

tk.Label(frame_Block_performance_table, text="Range(nm)").grid(row=2,column=1, sticky="e")
range = tk.Entry(frame_Block_performance_table, width=10)
range.grid(row=2,column=2, columnspan = 3)
tk.Label(frame_Block_performance_table, text="Payload(kg)").grid(row=3,column=1, sticky="e")
paylaod = tk.Entry(frame_Block_performance_table, width=10)
payload.grid(row=3,column=2, columnspan = 3)

variable_separator = tk.IntVar()
tk.Checkbutton(frame_Block_performance_table, variable=variable_separator).grid(row=4, column=1)
tk.Label(frame_Block_performance_table, text="Use tab separator").grid(row=4, column=2, padx=(0, 5),  sticky="w")

#-----//------------Fin du frame du "Block performance table"-----------------------------------------------------

#----------------------------Frame du "Takeoff/Landing Field Lengths"-------------------------
frame_Takeoff= tk.Frame(frame_bas_de_page, bd = 1, relief = "sunken", padx=10, pady=10)

tk.Label(frame_Takeoff, text="Takeoff").grid(row=18, column=1, padx=(5, 5))
tk.Label(frame_Takeoff, text="Landing").grid(row=18, column=2, padx=(5, 5))
tk.Label(frame_Takeoff, text="Weight (kg)").grid(row=19, column=0, padx=(5, 5))
poids_decolage = tk.Entry(frame_Takeoff, width=10)
poids_decolage.grid(row=19, column=1)
poids_atterrissage = tk.Entry(frame_Takeoff, width=10)
poids_atterrissage.grid(row=19, column=2)
tk.Label(frame_Takeoff, text="Altitude (ft)").grid(row=20, column=0, padx=(5, 5))
altitude_decolage = tk.Entry(frame_Takeoff, width=10)
altitude_decolage.grid(row=20, column=1)
altitude_atterrissage = tk.Entry(frame_Takeoff, width=10)
altitude_atterrissage.grid(row=20, column=2)
tk.Label(frame_Takeoff, text="Temp Deviation").grid(row=21, column=0, padx=(5, 5))
t_deviation_decolage = tk.Entry(frame_Takeoff, width=10)
t_deviation_decolage.grid(row=21, column=1)
t_deviasion_atterrissage = tk.Entry(frame_Takeoff, width=10)
t_deviasion_atterrissage.grid(row=21, column=2)

#----------------------------Fin du frame du "Takeoff/Landing Field Lengths"-------------------------

#-----------------------Frame du Point Performance-----------------------------------------------------
frame_Point_Performance=tk.Frame(frame_bas_de_page)
frame_Point_Performance.grid_forget()
liste_choix_Point_Performance= ["Mach", "KCAS", "KEAS", "KTAS"]
menu_deroulant_choix_Point_Performance = ttk.Combobox(frame_Point_Performance, values=liste_choix_Point_Performance, state="readonly")
menu_deroulant_choix_Point_Performance.grid(row=0, column=1, sticky="w")


 
frame_Point_Performance_Mach=tk.Frame(frame_Point_Performance)
mach_choisi = tk.Entry(frame_Point_Performance_Mach, **COMMUN)
mach_choisi.grid(row=0, column=0)
frame_Point_Performance_KCAS=tk.Frame(frame_Point_Performance)
kcas_choisie = tk.Entry(frame_Point_Performance_KCAS, **COMMUN)
kcas_choisie.grid(row=0, column=0)
frame_Point_Performance_KEAS=tk.Frame(frame_Point_Performance)
keas_choisie = tk.Entry(frame_Point_Performance_KEAS, **COMMUN)
keas_choisie.grid(row=0, column=0)
frame_Point_Performance_KTAS=tk.Frame(frame_Point_Performance)
ktas_choisie = tk.Entry(frame_Point_Performance_KTAS, **COMMUN)
ktas_choisie.grid(row=0, column=0)


 
def affichage_Point_Performance(event):
    if menu_deroulant_choix_Point_Performance.get() == "Mach":
        frame_Point_Performance_Mach.grid(row=0, column=2, sticky="ew")
    else :
        frame_Point_Performance_Mach.grid_forget()
    if menu_deroulant_choix_Point_Performance.get() == "KCAS":
        frame_Point_Performance_KCAS.grid(row=0, column=2, sticky="ew")
    else :
        frame_Point_Performance_KCAS.grid_forget()
    if menu_deroulant_choix_Point_Performance.get() == "KEAS":
        frame_Point_Performance_KEAS.grid(row=0, column=2, sticky="ew")
    else :
        frame_Point_Performance_KEAS.grid_forget()
    if menu_deroulant_choix_Point_Performance.get() == "KTAS":
        frame_Point_Performance_KTAS.grid(row=0, column=2, sticky="ew")
    else :
        frame_Point_Performance_KTAS.grid_forget()


 
menu_deroulant_choix_Point_Performance.bind("<<ComboboxSelected>>", affichage_Point_Performance)
menu_deroulant_choix_Point_Performance.current(0) 
frame_Point_Performance_Mach.grid(row=0, column=2, sticky="ew")


 
tk.Label(frame_Point_Performance, text="Altitude (ft)").grid(row=1, column=1)
altitude = tk.Entry(frame_Point_Performance, **COMMUN)
altitude.grid(row=1, column=2)


 
tk.Label(frame_Point_Performance, text="Weight (kg)").grid(row=2, column=1)
poids = tk.Entry(frame_Point_Performance, **COMMUN)
poids.grid(row=2, column=2)

#-----------------------------------------------

def affichage_du_bas(event):
    if menu_deroulant.get() == "Block Range Summary":

        frame_Block_range_summary.grid(row=18, column=0, columnspan=6, sticky="n")
    else :
        frame_Block_range_summary.grid_forget()
    if menu_deroulant.get() == "Block Performance Tables":

        frame_Block_performance_table.grid(row=18, column=0, columnspan=6, sticky="n")
    else :
        frame_Block_performance_table.grid_forget()
    if menu_deroulant.get() == "Detailed Flight Profile":

        frame_Detailed_flight_profile.grid(row=18, column=0, columnspan=6, sticky="n")
    else :
        frame_Detailed_flight_profile.grid_forget()
    if menu_deroulant.get() == "Takeoff/Landing Field Lengths":

        frame_Takeoff.grid(row=18, column=0, columnspan=6, sticky="n")
    else :
        frame_Takeoff.grid_forget()

    if menu_deroulant.get() == "Point Performance":

        frame_Point_Performance.grid(row=18, column=0, columnspan=6, sticky="ew")
    else :
        frame_Point_Performance.grid_forget()


menu_deroulant.bind("<<ComboboxSelected>>", affichage_du_bas)
main_frame_gauche.grid(row=0, column = 0, sticky="n")
main_frame_droite.grid(row =0, column = 14)
#-----------------------Fin de la partie Fixe en bas de la page-----------------------------------------------------

#-----------------------Page blanche à droite -----------------------------
txt_console = tk.Text(main_frame_droite, font=("Consolas", 9), bd=0)
txt_console.pack(side="left", fill="both", padx=10, pady=10)
#-------------------------Fin de la page blanche à droite






root.mainloop()