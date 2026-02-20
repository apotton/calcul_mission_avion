import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
import random

root = tk.Tk()
root.title("PIE COA26")
root.geometry("1400x1000")

#le zoom de vieux
root.tk.call('tk', 'scaling', 1.5)


COMMUN = {"font": ("Helvetica", 10)}
COMMUNTITRE = {"font": ("Helvetica", 16)}


style = ttk.Style()
style.theme_use('clam') #alt ou clam
style.configure('TNotebook.Tab', 
                background="#30B9F0",   # Couleur de fond (gris clair)
                foreground='black',     # Couleur du texte
                **COMMUN)               # Vos polices
style.map('TNotebook.Tab',
          background=[('selected', "#fffb00")], # Bleu quand sélectionné
          foreground=[('selected', 'red')])   # Texte blanc quand sélectionné


main_frame_gauche = tk.Frame(root)
main_frame_gauche.grid(row = 0, column = 0)
main_frame_droite = tk.Frame(root)
main_frame_droite.grid(row = 0, column = 7, sticky="e")


main_frame_haut = tk.Frame(main_frame_gauche)
main_frame_haut.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

main_frame_bas = tk.Frame(main_frame_gauche)
main_frame_bas.grid(row=7, column =0, padx=10, pady=10)
main_frame_tres_bas = tk.Frame(main_frame_gauche)
main_frame_tres_bas.grid(row=15, column=0, sticky = "s", padx=10, pady=10)

DOSSIER_SORTIE = Path(__file__).parent

notebook = ttk.Notebook(main_frame_bas)
notebook.grid(row=0, column=0, sticky="nsew")


frame_Mission = tk.Frame(notebook, bg = "#fffb00")
onglet_options = tk.Frame(notebook, bg = "#fffb00")
onglet_diversion = tk.Frame(notebook, bg = "#fffb00")
onglet_pointperformance = tk.Frame(notebook, bg = "#fffb00")
notebook.add(frame_Mission, text="  Mission  ")
notebook.add(onglet_options, text=" Options ")
notebook.add(onglet_diversion, text = " Autre ")
notebook.add(onglet_pointperformance, text = "Point Performance")


#--------------Les différentes sous frames -----------------------------
#--------------------------------------------------------------------

frame_generale = tk.Frame(main_frame_haut, bd = 10, relief = "sunken")
frame_generale1= tk.Frame(main_frame_haut, bd = 10, relief = "sunken")
frame_generale.grid(row=0, column=2, padx=10, pady=10)
frame_generale1.grid(row=0, column = 0, padx=10, pady=10)
#---------------Sous Frames de Mission------------------------------------

frame_Montee = tk.Frame(frame_Mission, bd = 10, relief = "sunken")
frame_Croisiere = tk.Frame(frame_Mission, bd = 10, relief = "sunken")
frame_descente = tk.Frame(frame_Mission, bd = 10, relief = "sunken")
frame_Montee.grid(row=7, column=0, padx=10, pady=10)
frame_Croisiere.grid(row=15, column=0, padx=10, pady=10)
frame_descente.grid(row=22, column=0, padx= 10, pady = 10)
#---------------Sous Frame de Autres---------------------------------------------

frame_diversion = tk.Frame(onglet_diversion, bd = 10, relief = "sunken")
frame_autre = tk.Frame(onglet_diversion, bd = 10, relief = "sunken")
frame_coeff = tk.Frame(onglet_diversion, bd = 10, relief = "sunken")
frame_diversion.grid(row =0, column=0, padx=10, pady=10)
frame_autre.grid(row =7, column=0, padx=10, pady=10)
frame_coeff.grid(row = 15, column=0, padx = 10, pady = 10)
#----------------Sous Frame de Options---------------------------------------------------------

frame_pasdetemps = tk.Frame(onglet_options, bd = 10, relief = "sunken")
frame_pasdetemps.grid(row =0, column=0, padx=10, pady=10)
#----------------Sous Frame de Pointperformance---------------------------------------------------------
frame_pp = tk.Frame(onglet_pointperformance, bd = 10, relief = "sunken" )
frame_pp.grid(row = 0, column=0, padx=10, pady=10)

# ----------Partie générale (Payload Distance)------------------------
frame_generale.rowconfigure(0, minsize=20)

tk.Label(frame_generale, text="Payload", **COMMUN).grid(row=2, column=0, sticky="e")
payload = tk.Entry(frame_generale, width=10)
payload.grid(row=2, column=1)
tk.Label(frame_generale, text="kg", **COMMUN).grid(row=2, column=3, sticky="w")

tk.Label(frame_generale, text="Distance", **COMMUN).grid(row=3, column=0, sticky="e")
distance_de_diversion = tk.Entry(frame_generale, width=10)
distance_de_diversion.grid(row=3, column=1)
tk.Label(frame_generale, text="nm", **COMMUN).grid(row=3, column=3, sticky="w")

frame_generale.rowconfigure(4, minsize=20)

#--------Fin de payload distance -------------

#-----------Partie générale 1 (Avion Moteur)-------------------------
frame_generale1.rowconfigure(0, minsize=20)
tk.Label(frame_generale1, text="Avion", **COMMUN).grid(row=2, column=0, sticky="e")

def obtenir_noms_fichiers_avion():
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
    return sorted(noms) # On trie par ordre alphabétique

def mettre_a_jour_menu_avion():
    """
    Fonction appelée juste avant l'ouverture du menu.
    Elle met à jour les valeurs possibles.
    """
    nouveaux_choix = obtenir_noms_fichiers_avion()
    menu_deroulant_avion['values'] = nouveaux_choix

menu_deroulant_avion = ttk.Combobox(frame_generale1, postcommand=mettre_a_jour_menu_avion, state="readonly")
menu_deroulant_avion.grid(row=2, column =1,columnspan = 2, sticky= "ew")

tk.Label(frame_generale1, text="Moteur", **COMMUN).grid(row=3, column=0, sticky="e")

def obtenir_noms_fichiers_moteur():
    """
    Scanne le dossier du script pour trouver les fichiers .csv
    et retourne une liste de noms sans l'extension.
    """
    # Chemin du dossier où se trouve ce script
    dossier_courant = Path(__file__).parent.parent / "data" / "moteurs"
    # On cherche tous les fichiers .csv
    fichiers = dossier_courant.glob("*.py")
    # On garde seulement le nom du fichier (stem) sans le .csv
    noms = [f.stem for f in fichiers]
    return sorted(noms) # On trie par ordre alphabétique

def mettre_a_jour_menu_moteur():
    """
    Fonction appelée juste avant l'ouverture du menu.
    Elle met à jour les valeurs possibles.
    """
    nouveaux_choix = obtenir_noms_fichiers_moteur()
    menu_deroulant_moteur['values'] = nouveaux_choix

moteur_choisi = tk.StringVar()
menu_deroulant_moteur = ttk.Combobox(frame_generale1,postcommand=mettre_a_jour_menu_moteur, state="readonly")
menu_deroulant_moteur.grid(row=3, column =1,columnspan = 2, sticky= "ew")

frame_generale1.rowconfigure(6, minsize=20)


#-----------Fin de Avion et Moteur ---------------------------




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
borne_inf_montee = tk.Entry(frame_mach_sar, width=10)
borne_inf_montee.grid(row=10, column=1)
tk.Label(frame_mach_sar, text="% distance mission", **COMMUN).grid(row=10, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Borne Sup déscente", **COMMUN).grid(row=11, column=0, sticky="e")
borne_sup_montee = tk.Entry(frame_mach_sar, width=10)
borne_sup_montee.grid(row=11, column=1)
tk.Label(frame_mach_sar, text="% distance mission", **COMMUN).grid(row=11, column=2, sticky="w")



tk.Label(frame_mach_sar, text="Vitesse montée min", **COMMUN).grid(row=12, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_mach_sar, width=10)
RRoC_min_ft_min.grid(row=12, column=1)
tk.Label(frame_mach_sar, text="ft/min", **COMMUN).grid(row=12, column=2, sticky="w")

tk.Label(frame_mach_sar, text="Mach de croisière", **COMMUN).grid(row=13, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_mach_sar, width=10)
Mach_cruise.grid(row=13, column=1)

frame_mach_sar.rowconfigure(14, minsize=20)
#-----------Fin subframe Mach_Sar--------------------------

#-----SubFrame Alt_Sar------------
frame_alt_sar = tk.Frame(frame_Croisiere)

tk.Label(frame_alt_sar, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_alt_sar, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init_alt_sar = tk.Entry(frame_alt_sar, width=10)
h_cruise_init_alt_sar.grid(row=8, column=1)
tk.Label(frame_alt_sar, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_alt_sar, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft_alt_sar = tk.Entry(frame_alt_sar, width=10)
step_climb_ft_alt_sar.grid(row=9, column=1)
tk.Label(frame_alt_sar, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_alt_sar, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min_alt_sar = tk.Entry(frame_alt_sar, width=10)
RRoC_min_ft_min_alt_sar.grid(row=11, column=1)
tk.Label(frame_alt_sar, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_alt_sar, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise_alt_sar = tk.Entry(frame_alt_sar, width=10)
Mach_cruise_alt_sar.grid(row=12, column=1)

frame_alt_sar.rowconfigure(13, minsize=20)
#-------------Fin Subframe alt Sar ------------------------------------

#-----SubFrame Alt_Mach------------
frame_alt_mach = tk.Frame(frame_Croisiere)

tk.Label(frame_alt_mach, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_alt_mach, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init_alt_mach = tk.Entry(frame_alt_mach, width=10)
h_cruise_init_alt_mach.grid(row=8, column=1)
tk.Label(frame_alt_mach, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_alt_mach, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft_alt_mach = tk.Entry(frame_alt_mach, width=10)
step_climb_ft_alt_mach.grid(row=9, column=1)
tk.Label(frame_alt_mach, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_alt_mach, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min_alt_mach = tk.Entry(frame_alt_mach, width=10)
RRoC_min_ft_min_alt_mach.grid(row=11, column=1)
tk.Label(frame_alt_mach, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_alt_mach, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise_alt_mach = tk.Entry(frame_alt_mach, width=10)
Mach_cruise_alt_mach.grid(row=12, column=1)

frame_alt_mach.rowconfigure(13, minsize=20)
#-----------Fin subframe Alt Mach --------------------------

#-----SubFrame CI------------
frame_ci = tk.Frame(frame_Croisiere)

tk.Label(frame_ci, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_ci, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init_ci = tk.Entry(frame_ci, width=10)
h_cruise_init_ci.grid(row=8, column=1)
tk.Label(frame_ci, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_ci, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft_ci = tk.Entry(frame_ci, width=10)
step_climb_ft_ci.grid(row=9, column=1)
tk.Label(frame_ci, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_ci, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min_ci = tk.Entry(frame_ci, width=10)
RRoC_min_ft_min_ci.grid(row=11, column=1)
tk.Label(frame_ci, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_ci, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise_ci = tk.Entry(frame_ci, width=10)
Mach_cruise_ci.grid(row=12, column=1)

frame_ci.rowconfigure(13, minsize=20)
#-----------Fin subframe CI --------------------------

#--------Affichage du type de croisière ----------------
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
#------------------------------------

#-----------Partie descente----------------------
tk.Label(frame_descente, text="Descente", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_descente, text="Altitude de décélération", **COMMUN).grid(row=8, column=0, sticky="e")
h_decel_ft = tk.Entry(frame_descente, width=10)
h_decel_ft.grid(row=8, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_descente, text="CAS < 10000 pieds", **COMMUN).grid(row=9, column=0, sticky="e")
CAS_below_10000_desc_kt = tk.Entry(frame_descente, width=10)
CAS_below_10000_desc_kt.grid(row=9, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_descente, text="Altitude finale", **COMMUN).grid(row=10, column=0, sticky="e")
h_final_ft = tk.Entry(frame_descente, width=10)
h_final_ft.grid(row=10, column=1)
tk.Label(frame_descente, text="ft", **COMMUN).grid(row=10, column=2, sticky="w")


frame_descente.rowconfigure(13, minsize=20)

#--------------Fin Partie descente -------------------------

#-----------Partie diversion----------------------
tk.Label(frame_diversion, text="Diversion", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_diversion, text="Altitude finale montée diversion", **COMMUN).grid(row=8, column=0, sticky="e")
Final_climb_altitude_diversion_ft = tk.Entry(frame_diversion, width=10)
Final_climb_altitude_diversion_ft.grid(row=8, column=1)
tk.Label(frame_diversion, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_diversion, text="Distance max en diversion", **COMMUN).grid(row=9, column=0, sticky="e")
Range_diversion_NM = tk.Entry(frame_diversion, width=10)
Range_diversion_NM.grid(row=9, column=1)
tk.Label(frame_diversion, text="nm", **COMMUN).grid(row=9, column=2, sticky="w")


tk.Label(frame_diversion, text="Mach de croisière en diversion", **COMMUN).grid(row=10, column=0, sticky="e")
Mach_cruise_div = tk.Entry(frame_diversion, width=10)
Mach_cruise_div.grid(row=10, column=1)
tk.Label(frame_diversion, text="", **COMMUN).grid(row=10, column=2) 

frame_diversion.rowconfigure(13, minsize=20)

#---------------Fin de la partie diversion -------------------------------

#------------------Partie Autre--------------------------------
tk.Label(frame_autre, text="Autre", **COMMUNTITRE).grid(row=0, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_autre, text="Contingency Fuel Rule", **COMMUN).grid(row=1, column=0, sticky="e")
carburant_de_reserve = tk.Entry(frame_autre, width=10)
carburant_de_reserve.grid(row=1, column=1)
tk.Label(frame_autre, text="%", **COMMUN).grid(row=1, column=2, sticky="w")

tk.Label(frame_autre, text="Holding Time", **COMMUN).grid(row=2, column=0, sticky="e")
temps_attente = tk.Entry(frame_autre, width=10)
temps_attente.grid(row=2, column=1)
tk.Label(frame_autre, text="min", **COMMUN).grid(row=2, column=2, sticky="w")

tk.Label(frame_autre, text="KCAS holding", **COMMUN).grid(row=3, column=0, sticky="e")
KCAS_holding = tk.Entry(frame_autre, width=10)
KCAS_holding.grid(row=3, column=1)
tk.Label(frame_autre, text="kt", **COMMUN).grid(row=3, column=2, sticky="w")

frame_autre.rowconfigure(4, minsize=20)

#--------------Fin de la partie Autre----------------------

#---------------Partie coefficients-----------------------
tk.Label(frame_coeff, text="Coefficients", **COMMUNTITRE).grid(row=0, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_coeff, text="Cx", **COMMUN).grid(row=1, column=0, sticky="e")
cx = tk.Entry(frame_coeff, width=10)
cx.grid(row=1, column=1)
tk.Label(frame_coeff, text="", **COMMUN).grid(row=1, column=2, sticky="w")

tk.Label(frame_coeff, text="Cz", **COMMUN).grid(row=2, column=0, sticky="e")
cz = tk.Entry(frame_coeff, width=10)
cz.grid(row=2, column=1)
tk.Label(frame_coeff, text="", **COMMUN).grid(row=2, column=2, sticky="w")

tk.Label(frame_coeff, text="cFF", **COMMUN).grid(row=3, column=0, sticky="e")
cff = tk.Entry(frame_coeff, width=10)
cff.grid(row=3, column=1)
tk.Label(frame_coeff, text="", **COMMUN).grid(row=3, column=2, sticky="w")

tk.Label(frame_coeff, text="cFn", **COMMUN).grid(row=4, column=0, sticky="e")
cfn = tk.Entry(frame_coeff, width=10)
cfn.grid(row=4, column=1)
tk.Label(frame_coeff, text="", **COMMUN).grid(row=4, column=2, sticky="w")

frame_coeff.rowconfigure(5, minsize=20)


#-------------------Fin de partie coefficients-----------------


#-----------------------------Onglet Options------------------------
tk.Label(frame_pasdetemps, text="Paramètres", **COMMUNTITRE).grid(row=0, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_pasdetemps, text="Pas de temps montée", **COMMUN).grid(row=1, column=0, pady=5, )
dt_climb = tk.Entry(frame_pasdetemps, width=10)
dt_climb.grid(row=1, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=1, column=2, sticky="w")

tk.Label(frame_pasdetemps, text="Pas de temps croisière", **COMMUN).grid(row=2, column=0, pady=5)
dt_cruise = tk.Entry(frame_pasdetemps, width=10)
dt_cruise.grid(row=2, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=2, column=2, sticky="w")

tk.Label(frame_pasdetemps, text="Pas de temps descente", **COMMUN).grid(row=3, column=0, pady=5)
dt_descent = tk.Entry(frame_pasdetemps, width=10)
dt_descent.grid(row=3, column=1)
tk.Label(frame_pasdetemps, text="s", **COMMUN).grid(row=3, column=2, sticky="w")

frame_pasdetemps.rowconfigure(4, minsize=20)

tk.Label(frame_pasdetemps, text="Precision", **COMMUN).grid(row=5, column=0, pady=5)
precision = tk.Entry(frame_pasdetemps, width=10)
precision.grid(row=5, column=1)
tk.Label(frame_pasdetemps, text="%", **COMMUN).grid(row=5, column=2, sticky="w")

#-----------------------Fin de l'onglet Option--------------------------

#------------------Onglet Point Performance ----------------------------

type_vitesse_choisie = tk.StringVar()
menu_deroulant_vitesse = ttk.Combobox(frame_pp, textvariable = type_vitesse_choisie, state="readonly")
menu_deroulant_vitesse['values'] = ("Mach", "TAS", "CAS")
menu_deroulant_vitesse.grid(row=0, column =0,columnspan = 1, sticky= "ew")
vitesse = tk.Entry(frame_pp, width = 10)
vitesse.grid(row = 0, column = 1)

frame_pp.rowconfigure(1, minsize=20)

tk.Label(frame_pp, text="Altitude", **COMMUN).grid(row=2, column=0, pady=5)
altitude = tk.Entry(frame_pp, width=10)
altitude.grid(row=2, column=1)
tk.Label(frame_pp, text="ft", **COMMUN).grid(row=2, column=2, sticky="w")

tk.Label(frame_pp, text="Poids", **COMMUN).grid(row=3, column=0, pady=5)
poids = tk.Entry(frame_pp, width=10)
poids.grid(row=3, column=1)
tk.Label(frame_pp, text="kg", **COMMUN).grid(row=3, column=2, sticky="w")

tk.Label(frame_pp, text="ΔISA", **COMMUN).grid(row=4, column=0, pady=5)
isa = tk.Entry(frame_pp, width=10)
isa.grid(row=4, column=1)
tk.Label(frame_pp, text="", **COMMUN).grid(row=4, column=2, sticky="w")

#-------------Les sous Frame juste pour avoir des unités différentes en fonction du choix dans le menu déroulant-----------------

frame_Mach = tk.Frame(frame_pp)
tk.Label(frame_Mach, text=" ", **COMMUN).grid(row=0, column=2, sticky= "w")

frame_TAS = tk.Frame(frame_pp)
tk.Label(frame_TAS, text="kt", **COMMUN).grid(row=0, column=2, sticky= "w")

frame_CAS = tk.Frame(frame_pp)
tk.Label(frame_CAS, text = 'kt', **COMMUN).grid(row=0, column = 2, sticky = "w")

#------------Fin de ce truc chiant-----------------------------------------------------------



def affichage_type_vitesse(event):

    if menu_deroulant_vitesse.get() == "Mach":
        frame_Mach.grid(row=0, column=2)
    else :
        frame_Mach.grid_forget()
    if menu_deroulant_vitesse.get() == "TAS":
        frame_TAS.grid(row=0, column=2)
    else :
        frame_TAS.grid_forget()
    if menu_deroulant_vitesse.get() == "CAS":
        frame_CAS.grid(row=0, column=2)
    else :
        frame_CAS.grid_forget()

menu_deroulant_vitesse.bind("<<ComboboxSelected>>", affichage_type_vitesse)
menu_deroulant_vitesse.current(0) 
affichage_type_vitesse(None)

#------------------Fin de l'Onglet Point Performance---------------------

#-----------Les fonctions des boutons ----------------------------------------
def sauvegarder_donnees():
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
            # --- Général ---
            "Payload (kg)": payload,
            "Distance de diversion (nm)": distance_de_diversion,
            "Avion": menu_deroulant_avion,
            "Moteur": menu_deroulant_moteur,
            
            # --- Montée ---
            "Altitude initiale montee (ft)": h_initial_ft,
            "Altitude acceleration (ft)": h_accel_ft,
            "CAS < 10000ft montee (kt)": CAS_below_10000_mont_kt,
            "Mach montee": Mach_climb,
            
            # --- Croisière ---
            "Type de croisiere": menu_deroulant_croisiere,
            "Altitude initiale croisiere (ft)": h_cruise_init,
            "Step climb (ft)": step_climb_ft,
            "Borne inf montée (%)" : borne_inf_montee,
            "Borne sup montée (%)" : borne_sup_montee,
            "Vitesse montee min (ft/min)": RRoC_min_ft_min,
            "Mach croisiere": Mach_cruise,
            
            # --- Descente ---
            "Altitude de deceleration (ft)": h_decel_ft,
            "CAS < 10000 pieds descente (kt)": CAS_below_10000_desc_kt,
            "Altitude finale (ft)": h_final_ft,
            
            # --- Diversion ---
            "Altitude finale montee diversion (ft)": Final_climb_altitude_diversion_ft,
            "Distance max en diversion (nm)": Range_diversion_NM,
            "Mach de croisiere en diversion": Mach_cruise_div,
            
            # --- Autre ---
            "Contingency Fuel Rule (%)": carburant_de_reserve,
            "Holding Time (min)": temps_attente,
            "KCAS holding (kt)": KCAS_holding,
            
            # --- Coefficients ---
            "Cx": cx,
            "Cz": cz,
            "cFF": cff,
            "cFn": cfn,
            
            # --- Options ---
            "Pas de temps montee (s)": dt_climb,
            "Pas de temps croisiere (s)": dt_cruise,
            "Pas de temps descente": dt_descent, 
            "Precision" : precision,
            
            
            # --- Point Performance ---
            "Type de vitesse (PP)": menu_deroulant_vitesse,
            "Vitesse (PP)": vitesse,
            "Altitude (PP)": altitude,
            "Poids (PP)": poids,
            "Delta ISA (PP)": isa
        }

        with open(chemin, "w", encoding="utf-8", newline='') as f:
            # On écrit l'en-tête (Titres des colonnes)
            f.write("Attribut;Valeur\n")
            
            for cle, widget in data.items():
                valeur = widget.get() if widget else ""
                # CHANGEMENT 3 : Utilisation du point-virgule
                f.write(f"{cle};{valeur}\n")
        
        messagebox.showinfo("Succès", f"Fichier CSV créé dans :\n{chemin}")
        
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de créer le fichier : {e}")


def charger_donnees(chemin_fichier=None):
    # On vérifie si un chemin est fourni (démarrage) ou non (clic sur le bouton)
    if chemin_fichier is None:
        chemin = filedialog.askopenfilename(
            initialdir=DOSSIER_SORTIE,
            filetypes=[("Fichier CSV", "*.csv"), ("Fichier texte", "*.txt")]
        )
    else:
        chemin = chemin_fichier
        
    # On annule si aucun chemin n'est sélectionné ou si le fichier d'init n'existe pas
    if not chemin or not os.path.exists(chemin):
        return
        
    try:
        mapping = {
            # --- Général ---
            "Payload (kg)": payload,
            "Distance de diversion (nm)": distance_de_diversion,
            "Avion": menu_deroulant_avion,
            "Moteur": menu_deroulant_moteur,
            
            # --- Montée ---
            "Altitude initiale montee (ft)": h_initial_ft,
            "Altitude acceleration (ft)": h_accel_ft,
            "CAS < 10000ft montee (kt)": CAS_below_10000_mont_kt,
            "Mach montee": Mach_climb,
            
            # --- Croisière ---
            "Type de croisiere": menu_deroulant_croisiere,
            "Altitude initiale croisiere (ft)": h_cruise_init,
            "Step climb (ft)": step_climb_ft,
            "Borne inf montée (%)" : borne_inf_montee,
            "Borne sup montée (%)" : borne_sup_montee,
            "Vitesse montee min (ft/min)": RRoC_min_ft_min,
            "Mach croisiere": Mach_cruise,
            
            # --- Descente ---
            "Altitude de deceleration (ft)": h_decel_ft,
            "CAS < 10000 pieds descente (kt)": CAS_below_10000_desc_kt,
            "Altitude finale (ft)": h_final_ft,
            
            # --- Diversion ---
            "Altitude finale montee diversion (ft)": Final_climb_altitude_diversion_ft,
            "Distance max en diversion (nm)": Range_diversion_NM,
            "Mach de croisiere en diversion": Mach_cruise_div,
            
            # --- Autre ---
            "Contingency Fuel Rule (%)": carburant_de_reserve,
            "Holding Time (min)": temps_attente,
            "KCAS holding (kt)": KCAS_holding,
            
            # --- Coefficients ---
            "Cx": cx,
            "Cz": cz,
            "cFF": cff,
            "cFn": cfn,
            
            # --- Options ---
            "Pas de temps montee (s)": dt_climb,
            "Pas de temps croisiere (s)": dt_cruise,
            "Pas de temps descente": dt_descent, 
            "Precision" : precision,
            
            # --- Point Performance ---
            "Type de vitesse (PP)": menu_deroulant_vitesse,
            "Vitesse (PP)": vitesse,
            "Altitude (PP)": altitude,
            "Poids (PP)": poids,
            "Delta ISA (PP)": isa
        }

        with open(chemin, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ";" in ligne:
                    parts = ligne.split(";", 1)
                    if len(parts) == 2:
                        cle, valeur = parts
                        
                        if cle == "Attribut": 
                            continue
                            
                        if cle in mapping:
                            widget = mapping[cle]
                            if widget:
                                # Particularité pour les Combobox (menu déroulant)
                                if isinstance(widget, ttk.Combobox):
                                    widget.set(valeur)
                                else:
                                    widget.delete(0, tk.END)
                                    widget.insert(0, valeur)

        # On affiche le message de succès uniquement si on a cliqué sur le bouton
        if chemin_fichier is None:
            messagebox.showinfo("Succès", "Données importées avec succès.")
            
    except Exception as e:
        if chemin_fichier is None:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture : {e}")
        else:
            print(f"Erreur lors du chargement automatique : {e}")

def surprise():
    # On récupère la taille actuelle de la zone de droite
    largeur = main_frame_droite.winfo_width()
    hauteur = main_frame_droite.winfo_height()
    
    # Sécurité si la fenêtre vient de s'ouvrir et que les tailles sont à 1
    if largeur < 10: largeur = 500
    if hauteur < 10: hauteur = 800

    # Création du calque d'animation par-dessus la console
    canvas_confetti = tk.Canvas(main_frame_droite, bg="white", highlightthickness=0)
    canvas_confetti.place(x=0, y=0, relwidth=1, relheight=1)
    
    couleurs = ["#FF5733", "#33FF57", "#3357FF", "#F033FF", "#FFF033", "#33FFF0"]
    confettis = []

    # Génération de 150 confettis
    for _ in range(150):
        # Position de départ (au-dessus du cadre pour qu'ils tombent)
        x = random.randint(0, largeur)
        y = random.randint(-hauteur, 0) 
        vitesse = random.randint(4, 12)
        taille = random.randint(6, 12)
        couleur = random.choice(couleurs)
        
        # Un mix de carrés et de ronds
        if random.choice([True, False]):
            item = canvas_confetti.create_oval(x, y, x+taille, y+taille, fill=couleur, outline="")
        else:
            item = canvas_confetti.create_rectangle(x, y, x+taille, y+taille, fill=couleur, outline="")
            
        confettis.append({"id": item, "vitesse": vitesse})

    # Fonction interne pour animer image par image
    def animer():
        en_cours = False
        for c in confettis:
            # On déplace chaque confetti vers le bas
            canvas_confetti.move(c["id"], 0, c["vitesse"])
            coords = canvas_confetti.coords(c["id"])
            
            # S'il reste au moins un confetti visible, on continue l'animation
            if coords and coords[1] < hauteur: 
                en_cours = True
        
        if en_cours:
            # On rappelle cette fonction toutes les 20 millisecondes
            root.after(20, animer) 
        else:
            # Quand tout est tombé, on détruit le calque pour revoir la console
            canvas_confetti.destroy()

    # On lance la première image de l'animation
    animer()

def action_go():
   
    txt_console.delete("1.0", tk.END)  # (Optionnel) Effacer la console avant d'écrire la suite
    txt_console.insert(tk.END, "Démarrage de la simulation...\n")
    
    avion = menu_deroulant_avion.get()  
    moteur = menu_deroulant_moteur.get()
    
    #Petit test pour vérifier que les tests fonctionnent 
    if avion and moteur:
        txt_console.insert(tk.END, f"Avion : {avion} | Moteur : {moteur}\n")
    else:
        txt_console.insert(tk.END, "Attention : Avion ou Moteur non sélectionné.\n")
        
    txt_console.insert(tk.END, "Calculs en cours...\n")
    txt_console.insert(tk.END, "Terminé !\n")
    txt_console.insert(tk.END, "-"*40 + "\n") # Ligne de séparation

    surprise()


#---------------------------------------------------------------

#--------------------Frame du bas de page------------------------

tk.Button(main_frame_tres_bas, text = "Sauvegarder", command=sauvegarder_donnees).grid(row=12, column=0, columnspan = 3)
tk.Button(main_frame_tres_bas, text = "Charger", command = charger_donnees).grid(row=12, column =3, columnspan = 3)
tk.Button(main_frame_tres_bas, text = "Go", command=action_go).grid(row=12, column =6, columnspan = 3)

#--------------------------------------------------------------


#-----------------------Page blanche à droite -----------------------------
txt_console = tk.Text(main_frame_droite, font=("Consolas", 9), bd=0)
txt_console.pack(side="left", fill="both", padx=10, pady=10)
#-------------------------Fin de la page blanche à droite


fichier_initialisation = DOSSIER_SORTIE / "init.csv"
charger_donnees(fichier_initialisation)

 #----------------------------------------------------


root.mainloop()