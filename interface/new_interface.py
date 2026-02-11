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
main_frame_gauche.grid(row=0, column=0, sticky="nw", padx=10, pady=10) 
main_frame_droite.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
tk.Label(main_frame_gauche, text="Adjust:").grid(row=1, column=0, sticky="w")
entree_choisie = tk.StringVar()
menu_deroulant_1 = ttk.Combobox(main_frame_gauche, textvariable = entree_choisie, state="readonly")
menu_deroulant_1['values'] = ("Mission","Diversion")
menu_deroulant_1.grid(row=1, column =1,columnspan = 3, sticky= "ew")

DOSSIER_SORTIE = Path(__file__).parent



#------------------Frame de la Mission-----------------------------------------------------
frame_Mission=tk.Frame(main_frame_gauche)

frame_Montee=tk.Frame(frame_Mission)
frame_Croisiere=tk.Frame(frame_Mission)

frame_Montee.grid(row=2, column=0, columnspan=5)
frame_Croisiere.grid(row=6, column=0, columnspan=6)


tk.Label(frame_Montee, text="Payload").grid(row=2, column=0)
distance_de_diversion = tk.Entry(frame_Montee, width=10)
distance_de_diversion.grid(row=2, column=1)
tk.Label(frame_Montee, text="Holding Time (min)").grid(row=3, column=0)
temps_attente = tk.Entry(frame_Montee, width=10)
temps_attente.grid(row=3, column=1)
tk.Label(frame_Montee, text="Contingency Fuel Rule").grid(row=4, column=0)
carburant_de_reserve = tk.Entry(frame_Montee, width=10)
carburant_de_reserve.grid(row=4, column=1)

liste_choix_Fuel_Rule= ["% Of mission fuel", "% Of total fuel", "% Of MTOW", "% Of flight time"]
menu_deroulant_choix_Fuel_Rule=ttk.Combobox(frame_Montee, values=liste_choix_Fuel_Rule,state="readonly").grid(row=4, column=2, sticky="w")

tk.Label(frame_Croisiere, text="Allowances:").grid(row=6, column=0)
tk.Label(frame_Croisiere, text="taxi out").grid(row=6, column=1)
t_taxi_out = tk.Entry(frame_Croisiere, width=10)
t_taxi_out.grid(row=7, column=1)
tk.Label(frame_Croisiere, text="takeoff").grid(row=6, column=2)
t_take_off = tk.Entry(frame_Croisiere, width=10)
t_take_off.grid(row=7, column=2)
tk.Label(frame_Croisiere, text="approach").grid(row=6, column=3)
t_approach = tk.Entry(frame_Croisiere, width=10)
t_approach.grid(row=7, column=3)
tk.Label(frame_Croisiere, text="taxi in").grid(row=6, column=4)
t_taxi_in = tk.Entry(frame_Croisiere, width=10)
t_taxi_in.grid(row=7, column=4)
tk.Label(frame_Croisiere, text="miss.app.").grid(row=6, column=5)
t_miis_approach = tk.Entry(frame_Croisiere, width=10)
t_miis_approach.grid(row=7, column=5)
tk.Label(frame_Croisiere, text="Time (min)").grid(row=7, column=0)
#------------------Fin de frame du "Reserves and allowances"-----------------------------------------------------


def affichage(event):
    if menu_deroulant_1.get() == "Mission":

        frame_Mission.grid(row=6, column=0, columnspan=6, sticky="ew")
    else :
        frame_Mission.grid_forget()

menu_deroulant_1.bind("<<ComboboxSelected>>", affichage)


root.mainloop()