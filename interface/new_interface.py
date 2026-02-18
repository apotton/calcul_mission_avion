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


frame_Mission = tk.Frame(notebook)
frame_pasdetemps = tk.Frame(notebook)
notebook.add(frame_Mission, text="  Mission  ")
notebook.add(frame_pasdetemps, text="  Pas de temps  ")


#--------------Frame Mission -----------------------------
frame_Montee = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_Croisiere = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_generale = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_descente = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_generale1= tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_diversion = tk.Frame(frame_Mission, bd = 2, relief = "sunken")
frame_autre = tk.Frame(frame_Mission, bd = 2, relief = "sunken")

frame_generale.grid(row=0, column=2, padx=10, pady=10)
frame_generale1.grid(row=0, column = 0, padx=10, pady=10)
frame_Montee.grid(row=7, column=0, padx=10, pady=10)
frame_Croisiere.grid(row=7, column=2, padx=10, pady=10)
frame_descente.grid(row=7, column=4, padx= 10, pady = 10)
frame_diversion.grid(row =15, column=2, padx=10, pady=10)
frame_autre.grid(row =15, column=4, padx=10, pady=10)





# ----------Partie générale (Payload Distance)------------------------
frame_generale.rowconfigure(0, minsize=20)

tk.Label(frame_generale, text="Payload", **COMMUN).grid(row=2, column=0, sticky="e")
payload = tk.Entry(frame_generale, width=10)
payload.grid(row=2, column=1)
tk.Label(frame_generale, text="kg", **COMMUN).grid(row=2, column=3, sticky="w")

tk.Label(frame_generale, text="Ditance", **COMMUN).grid(row=3, column=0, sticky="e")
distance_de_diversion = tk.Entry(frame_generale, width=10)
distance_de_diversion.grid(row=3, column=1)
tk.Label(frame_generale, text="nm", **COMMUN).grid(row=3, column=3, sticky="w")


#--------Fin de payload distance -------------

#-----------Partie générale 1 (Avion Moteur)-------------------------
frame_generale1.rowconfigure(0, minsize=20)
tk.Label(frame_generale1, text="Avion", **COMMUN).grid(row=2, column=0, sticky="e")

avion_choisi = tk.StringVar()
menu_deroulant_avion = ttk.Combobox(frame_generale1, textvariable = avion_choisi, state="readonly")
menu_deroulant_avion['values'] = ('A320', "A321", "A350", "A380")
menu_deroulant_avion.grid(row=2, column =1,columnspan = 2, sticky= "ew")

tk.Label(frame_generale1, text="Moteur", **COMMUN).grid(row=3, column=0, sticky="e")

moteur_choisi = tk.StringVar()
menu_deroulant_moteur = ttk.Combobox(frame_generale1, textvariable = moteur_choisi, state="readonly")
menu_deroulant_moteur['values'] = ('CFM56', "M88")
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
#-----------Fin subframe Mach_Sar--------------------------

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



tk.Label(frame_diversion, text="KCAS holding", **COMMUN).grid(row=13, column=0, sticky="e")
KCAS_holding = tk.Entry(frame_diversion, width=10)
KCAS_holding.grid(row=13, column=1)
tk.Label(frame_diversion, text="kt", **COMMUN).grid(row=13, column=2, sticky="w")

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

#--------------Fin de la partie Autre----------------------


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