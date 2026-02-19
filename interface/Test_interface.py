import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
root = tk.Tk()
root.title("PIE COA26")
root.geometry("1400x1000")

#le zoom de vieux
root.tk.call('tk', 'scaling', 2.2)


COMMUN = {"font": ("Helvetica", 10)}
COMMUNTITRE = {"font": ("Helvetica", 16)}


style = ttk.Style()
style.configure('TNotebook.Tab', **COMMUN)


main_frame_gauche = tk.Frame(root)
main_frame_gauche.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

DOSSIER_SORTIE = Path(__file__).parent

notebook = ttk.Notebook(main_frame_gauche)
notebook.grid(row=0, column=0, sticky="nsew")

frame_Caracteristiques = tk.Frame(notebook)
frame_Mission = tk.Frame(notebook)
frame_diversion = tk.Frame(notebook)
frame_pasdetemps = tk.Frame(notebook)
notebook.add(frame_Caracteristiques, text="  Caractéristiques  ")
notebook.add(frame_Mission, text="  Mission  ")
notebook.add(frame_diversion, text="  Diversion  ")
notebook.add(frame_pasdetemps, text="  Pas de temps  ")


#--------------Frame Caracteristiques -----------------------------
def obtenir_noms_fichiers():
    """
    Scanne le dossier du script pour trouver les fichiers .csv
    et retourne une liste de noms sans l'extension.
    """
    # Chemin du dossier où se trouve ce script
    dossier_courant = Path(__file__).parent.parent / "data" / "avions"
    # On cherche tous les fichiers .csv
    fichiers = dossier_courant.glob("*.csv")
    # On garde seulement le nom du fichier (stem) sans le .csv
    noms = [f.stem for f in fichiers]
    print(noms)
    return sorted(noms) # On trie par ordre alphabétique

def mettre_a_jour_menu():
    """
    Fonction appelée juste avant l'ouverture du menu.
    Elle met à jour les valeurs possibles.
    """
    choix_avions = []
    nouveaux_choix = obtenir_noms_fichiers()
    menu_avions['values'] = nouveaux_choix

menu_avions = ttk.Combobox(frame_Caracteristiques, postcommand=mettre_a_jour_menu, state="readonly")
menu_avions.grid(row=0, column=0)

#--------------Fin du Frame Caracteristiques -----------------------------




#--------------Frame Mission -----------------------------
frame_Montee = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_Croisiere = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_generale = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_descente = tk.Frame(frame_Mission, bd = 2, relief = "sunken")

frame_generale.grid(row=0, column=2, padx=10, pady=10)
frame_Montee.grid(row=7, column=0, padx=10, pady=10)
frame_Croisiere.grid(row=7, column=2, padx=10, pady=10)
frame_descente.grid(row=7, column=4, padx= 10, pady = 10)





# ---Partie générale ---
frame_generale.rowconfigure(0, minsize=20)
tk.Label(frame_generale, text="Payload", **COMMUN).grid(row=2, column=0, sticky="e")
distance_de_diversion = tk.Entry(frame_generale, width=10)
distance_de_diversion.grid(row=2, column=1)
tk.Label(frame_generale, text="kg", **COMMUN).grid(row=2, column=3, sticky="w")

tk.Label(frame_generale, text="Holding Time", **COMMUN).grid(row=3, column=0, sticky="e")
temps_attente = tk.Entry(frame_generale, width=10)
temps_attente.grid(row=3, column=1)
tk.Label(frame_generale, text="min", **COMMUN).grid(row=3, column=3, sticky="w")

tk.Label(frame_generale, text="Contingency Fuel Rule", **COMMUN).grid(row=4, column=0, sticky="e")
carburant_de_reserve = tk.Entry(frame_generale, width=10)
carburant_de_reserve.grid(row=4, column=1)

tk.Label(frame_generale, text="KCAS holding", **COMMUN).grid(row=5, column=0, sticky="e")
KCAS_holding = tk.Entry(frame_generale, width=10)
KCAS_holding.grid(row=5, column=1)
tk.Label(frame_generale, text="kt", **COMMUN).grid(row=5, column=3, sticky="w")
frame_generale.rowconfigure(6, minsize=20)


# --- Partie Montée ---

tk.Label(frame_Montee, text="Montée", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_Montee, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_initial_ft = tk.Entry(frame_Montee, width=10)
h_initial_ft.grid(row=8, column=1)
tk.Label(frame_Montee, text="ft", **COMMUN).grid(row=8, column=3,sticky="w")

tk.Label(frame_Montee, text="Altitude d'accélération", **COMMUN).grid(row=9, column=0, sticky="e")
h_accel_ft = tk.Entry(frame_Montee, width=10)
h_accel_ft.grid(row=9, column=1)
tk.Label(frame_Montee, text="ft", **COMMUN).grid(row=9, column=3, sticky="w")

tk.Label(frame_Montee, text="CAS < 10000 ft", **COMMUN).grid(row=10, column=0, sticky="e")
CAS_below_10000_mont_kt = tk.Entry(frame_Montee, width=10)
CAS_below_10000_mont_kt.grid(row=10, column=1)
tk.Label(frame_Montee, text="kt", **COMMUN).grid(row=10, column=3, sticky="w")


tk.Label(frame_Montee, text="Mach de montée", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_climb = tk.Entry(frame_Montee, width=10)
Mach_climb.grid(row=12, column=1)

frame_Montee.rowconfigure(13, minsize=20)
# --- Partie Croisière ---

croisiere_choisie = tk.StringVar()
menu_deroulant_croisiere = ttk.Combobox(frame_Croisiere, textvariable = croisiere_choisie, state="readonly")
menu_deroulant_croisiere['values'] = ('Mach SAR', "Alt SAR", "Alt Mach", "CI")
menu_deroulant_croisiere.grid(row=0, column =0,columnspan = 3, sticky= "ew")

#-----SubFrame Mach_Sar------------
frame_mach_sar = tk.Frame(frame_Croisiere)

tk.Label(frame_mach_sar, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_mach_sar, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init = tk.Entry(frame_mach_sar, width=10)
h_cruise_init.grid(row=8, column=1)
tk.Label(frame_mach_sar, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_mach_sar, width=10)
step_climb_ft.grid(row=9, column=1)
tk.Label(frame_mach_sar, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Borne Inf montée", **COMMUN).grid(row=10, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_mach_sar, width=10)
step_climb_ft.grid(row=10, column=1)
tk.Label(frame_mach_sar, text="% distance mission", **COMMUN).grid(row=10, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Borne Sup déscente", **COMMUN).grid(row=11, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_mach_sar, width=10)
step_climb_ft.grid(row=11, column=1)
tk.Label(frame_mach_sar, text="% distance mission", **COMMUN).grid(row=11, column=2, sticky="w")



tk.Label(frame_mach_sar, text="Vitesse montée min", **COMMUN).grid(row=12, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_mach_sar, width=10)
RRoC_min_ft_min.grid(row=12, column=1)
tk.Label(frame_mach_sar, text="ft/min", **COMMUN).grid(row=12, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Mach de croisière", **COMMUN).grid(row=13, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_mach_sar, width=10)
Mach_cruise.grid(row=13, column=1)

frame_mach_sar.rowconfigure(14, minsize=20)
#-----------Fin subframe Mach_Sar

#-----SubFrame Alt_Sar------------
frame_alt_sar = tk.Frame(frame_Croisiere)

tk.Label(frame_alt_sar, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_alt_sar, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init = tk.Entry(frame_alt_sar, width=10)
h_cruise_init.grid(row=8, column=1)
tk.Label(frame_alt_sar, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_alt_sar, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_alt_sar, width=10)
step_climb_ft.grid(row=9, column=1)
tk.Label(frame_alt_sar, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_alt_sar, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_alt_sar, width=10)
RRoC_min_ft_min.grid(row=11, column=1)
tk.Label(frame_alt_sar, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_alt_sar, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_alt_sar, width=10)
Mach_cruise.grid(row=12, column=1)

frame_alt_sar.rowconfigure(13, minsize=20)
#-------------Fin Subframe alt Sar ------------------------------------

#-----SubFrame Alt_Mach------------
frame_alt_mach = tk.Frame(frame_Croisiere)

tk.Label(frame_alt_mach, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_alt_mach, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init = tk.Entry(frame_alt_mach, width=10)
h_cruise_init.grid(row=8, column=1)
tk.Label(frame_alt_mach, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_alt_mach, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_alt_mach, width=10)
step_climb_ft.grid(row=9, column=1)
tk.Label(frame_alt_mach, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_alt_mach, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_alt_mach, width=10)
RRoC_min_ft_min.grid(row=11, column=1)
tk.Label(frame_alt_mach, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_alt_mach, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_alt_mach, width=10)
Mach_cruise.grid(row=12, column=1)

frame_alt_mach.rowconfigure(13, minsize=20)
#-----------Fin subframe Alt Mach --------------------------

#-----SubFrame CI------------
frame_ci = tk.Frame(frame_Croisiere)

tk.Label(frame_ci, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_ci, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init = tk.Entry(frame_ci, width=10)
h_cruise_init.grid(row=8, column=1)
tk.Label(frame_ci, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_ci, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_ci, width=10)
step_climb_ft.grid(row=9, column=1)
tk.Label(frame_ci, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_ci, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_ci, width=10)
RRoC_min_ft_min.grid(row=11, column=1)
tk.Label(frame_ci, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_ci, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_ci, width=10)
Mach_cruise.grid(row=12, column=1)

frame_ci.rowconfigure(13, minsize=20)
#-----------Fin subframe CI --------------------------

#-----------Partie descente----------------------
tk.Label(frame_descente, text="Descente", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_descente, text="Altitude de décélération", **COMMUN).grid(row=8, column=0, sticky="e")
h_decel_ft = tk.Entry(frame_descente, width=10)
h_decel_ft.grid(row=8, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_descente, text="Altitude finale", **COMMUN).grid(row=9, column=0, sticky="e")
h_final_ft = tk.Entry(frame_descente, width=10)
h_final_ft.grid(row=9, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")

tk.Label(frame_descente, text="CAS < 10000 pieds", **COMMUN).grid(row=10, column=0, sticky="e")
CAS_below_10000_desc_kt = tk.Entry(frame_descente, width=10)
CAS_below_10000_desc_kt.grid(row=10, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=10, column=2, sticky="w")

tk.Label(frame_descente, text="CAS max de descente", **COMMUN).grid(row=11, column=0, sticky="e")
CAS_max_descent_kt = tk.Entry(frame_descente, width=10)
CAS_max_descent_kt.grid(row=11, column=1)
tk.Label(frame_descente, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_descente, text="Rien", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_descente, width=10)
Mach_cruise.grid(row=12, column=1)

frame_descente.rowconfigure(13, minsize=20)

#---------------Fin de l'onglet Mission -------------------------------


#------------------------Onglet Diversion-----------------------
tk.Label(frame_diversion, text="Altitude finale montée diversion", **COMMUN).grid(row=0, column=0, pady=5)
Final_climb_altitude_diversion_ft = tk.Entry(frame_diversion, width=10)
Final_climb_altitude_diversion_ft.grid(row=0, column=1)
tk.Label(frame_diversion, text="ft", **COMMUN).grid(row=0, column=2, sticky="w")

tk.Label(frame_diversion, text="Distance max en diversion", **COMMUN).grid(row=1, column=0, pady=5)
Range_diversion_NM = tk.Entry(frame_diversion, width=10)
Range_diversion_NM.grid(row=1, column=1)
tk.Label(frame_diversion, text="nm", **COMMUN).grid(row=1, column=2, sticky="w")

tk.Label(frame_diversion, text="Mach de croisière en diversion", **COMMUN).grid(row=2, column=0, pady=5)
Mach_cruise_div = tk.Entry(frame_diversion, width=10)
Mach_cruise_div.grid(row=2, column=1)
# Note: j'ai corrigé "nm" en sans unité ou Mach ici si c'est un Mach
tk.Label(frame_diversion, text="", **COMMUN).grid(row=2, column=2) 

#-------------------------Fin de l'onglet Diversion-------------------------


#-----------------------------Onglet pas de temps------------------------
tk.Label(frame_pasdetemps, text="Pas de temps montée", **COMMUN).grid(row=0, column=0, pady=5)
dt_climb = tk.Entry(frame_pasdetemps, width=10)
dt_climb.grid(row=0, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=0, column=2, sticky="w")

tk.Label(frame_pasdetemps, text="Pas de temps croisière", **COMMUN).grid(row=1, column=0, pady=5)
dt_cruise = tk.Entry(frame_pasdetemps, width=10)
dt_cruise.grid(row=1, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=1, column=2, sticky="w")

tk.Label(frame_pasdetemps, text="Pas de temps descente", **COMMUN).grid(row=2, column=0, pady=5)
dt_descent = tk.Entry(frame_pasdetemps, width=10)
dt_descent.grid(row=2, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=2, column=2, sticky="w")

#-----------------------Fin de l'onglet pas de temps--------------------------

def affichage_croisiere(event):
    if menu_deroulant_croisiere.get() == "Mach SAR":
        frame_mach_sar.grid(row=1, column=2, sticky="ew")
    else :
        frame_mach_sar.grid_forget()
    if menu_deroulant_croisiere.get() == "Alt SAR":
        frame_alt_sar.grid(row=1, column=2, sticky="ew")
    else :
        frame_alt_sar.grid_forget()
    if menu_deroulant_croisiere.get() == "Alt Mach":
        frame_alt_mach.grid(row=1, column=2, sticky="ew")
    else :
        frame_alt_mach.grid_forget()
    if menu_deroulant_croisiere.get() == "CI":
        frame_ci.grid(row=1, column=2, sticky="ew")
    else :
        frame_ci.grid_forget()
menu_deroulant_croisiere.bind("<<ComboboxSelected>>", affichage_croisiere)
menu_deroulant_croisiere.current(0) 
affichage_croisiere(None)
root.mainloop()