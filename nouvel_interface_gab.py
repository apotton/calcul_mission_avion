import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
root = tk.Tk()
root.title("PIE COA26")
root.geometry("1300x900")

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
frame_diversion = tk.Frame(notebook)
frame_pasdetemps = tk.Frame(notebook)
notebook.add(frame_Mission, text="  Mission  ")
notebook.add(frame_diversion, text="  Diversion  ")
notebook.add(frame_pasdetemps, text="  Pas de temps  ")


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

tk.Label(frame_Montee, text="CAS de montée", **COMMUN).grid(row=11, column=0, sticky="e")
CAS_climb_kt = tk.Entry(frame_Montee, width=10)
CAS_climb_kt.grid(row=11, column=1)
tk.Label(frame_Montee, text="kt", **COMMUN).grid(row=11, column=3, sticky="w")

tk.Label(frame_Montee, text="Mach de montée", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_climb = tk.Entry(frame_Montee, width=10)
Mach_climb.grid(row=12, column=1)

frame_Montee.rowconfigure(13, minsize=20)
# --- Partie Croisière ---

tk.Label(frame_Croisiere, text="Croisière", **COMMUNTITRE).grid(row=7, column=0, columnspan=3, sticky= "ew")

tk.Label(frame_Croisiere, text="Altitude initiale", **COMMUN).grid(row=8, column=0, sticky="e")
h_cruise_init = tk.Entry(frame_Croisiere, width=10)
h_cruise_init.grid(row=8, column=1)
tk.Label(frame_Croisiere, text="ft", **COMMUN).grid(row=8, column=2, sticky="w")

tk.Label(frame_Croisiere, text="Step climb", **COMMUN).grid(row=9, column=0, sticky="e")
step_climb_ft = tk.Entry(frame_Croisiere, width=10)
step_climb_ft.grid(row=9, column=1)
tk.Label(frame_Croisiere, text="ft", **COMMUN).grid(row=9, column=2, sticky="w")

tk.Label(frame_Croisiere, text="Plafond pressurisation", **COMMUN).grid(row=10, column=0, sticky="e")
pressurisation_ceiling_ft = tk.Entry(frame_Croisiere, width=10)
pressurisation_ceiling_ft.grid(row=10, column=1)
tk.Label(frame_Croisiere, text="ft", **COMMUN).grid(row=10, column=2, sticky="w")

tk.Label(frame_Croisiere, text="Vitesse montée min", **COMMUN).grid(row=11, column=0, sticky="e")
RRoC_min_ft_min = tk.Entry(frame_Croisiere, width=10)
RRoC_min_ft_min.grid(row=11, column=1)
tk.Label(frame_Croisiere, text="ft/min", **COMMUN).grid(row=11, column=2, sticky="w")

tk.Label(frame_Croisiere, text="Mach de croisière", **COMMUN).grid(row=12, column=0, sticky="e")
Mach_cruise = tk.Entry(frame_Croisiere, width=10)
Mach_cruise.grid(row=12, column=1)

frame_Croisiere.rowconfigure(13, minsize=20)

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

root.mainloop()