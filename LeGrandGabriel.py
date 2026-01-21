import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("PIE COA26")
root.geometry("1200x1000")


COMMUN = {"font": ("Arial", 10)}
#-------------------Normalement tu l'as déjà---------------------------
tk.Label(root, text="Adjust:").grid(row=1, column=0, sticky="w")
entree_choisie = tk.StringVar()
menu_deroulant_1 = ttk.Combobox(root, textvariable = entree_choisie, state="readonly")
menu_deroulant_1['values'] = ('Basic Design Weights', "Thrust Drag Fuel Flow", "Emission indices", "Speed and flight levels", "Reserve and Allowances", "Unit preferences")
menu_deroulant_1.grid(row=1, column =1,columnspan = 3, sticky= "ew")
#-------------------Fin du normalement tu l'as déjà----------------------------


#------------------Frame du "Reserves and allowances"-----------------------------------------------------
frame_Reserves_and_allowances=tk.Frame(root)

frame_Reserves_and_allowances1=tk.Frame(frame_Reserves_and_allowances)
frame_Reserves_and_allowances2=tk.Frame(frame_Reserves_and_allowances1)

frame_Reserves_and_allowances1.grid(row=2, column=0, columnspan=5)
frame_Reserves_and_allowances2.grid(row=6, column=0, columnspan=6)


tk.Label(frame_Reserves_and_allowances1, text="Diversion Distance (nm)").grid(row=2, column=0)
tk.Entry(frame_Reserves_and_allowances1, width=10).grid(row=2, column=1)
tk.Label(frame_Reserves_and_allowances1, text="Holding Time (min)").grid(row=3, column=0)
tk.Entry(frame_Reserves_and_allowances1, width=10).grid(row=3, column=1)
tk.Label(frame_Reserves_and_allowances1, text="Contingency Fuel Rule").grid(row=4, column=0)
tk.Entry(frame_Reserves_and_allowances1, width=10).grid(row=4, column=1)

liste_choix_Fuel_Rule= ["% Of mission fuel", "% Of total fuel", "% Of MTOW", "% Of flight time"]
menu_deroulant_choix_Fuel_Rule=ttk.Combobox(frame_Reserves_and_allowances1, values=liste_choix_Fuel_Rule,state="readonly").grid(row=4, column=2, sticky="w")

tk.Label(frame_Reserves_and_allowances2, text="Allowances:").grid(row=6, column=0)
tk.Label(frame_Reserves_and_allowances2, text="taxi out").grid(row=6, column=1)
tk.Entry(frame_Reserves_and_allowances2, width=10).grid(row=7, column=1)
tk.Label(frame_Reserves_and_allowances2, text="takeoff").grid(row=6, column=2)
tk.Entry(frame_Reserves_and_allowances2, width=10).grid(row=7, column=2)
tk.Label(frame_Reserves_and_allowances2, text="approach").grid(row=6, column=3)
tk.Entry(frame_Reserves_and_allowances2, width=10).grid(row=7, column=3)
tk.Label(frame_Reserves_and_allowances2, text="taxi in").grid(row=6, column=4)
tk.Entry(frame_Reserves_and_allowances2, width=10).grid(row=7, column=4)
tk.Label(frame_Reserves_and_allowances2, text="miss.app.").grid(row=6, column=5)
tk.Entry(frame_Reserves_and_allowances2, width=10).grid(row=7, column=5)
tk.Label(frame_Reserves_and_allowances2, text="Time (min)").grid(row=7, column=0)
#------------------Fin de frame du "Reserves and allowances"-----------------------------------------------------

#------------------Frame du "Basic Design Weights"-----------------------------------------------------
frame_Basic_Design_Weights=tk.Frame(root)
frame_Basic_Design_Weights.grid_forget()

#def
tk.Label(frame_Basic_Design_Weights, text="Weight (kg)").grid(row=2, column=1)
tk.Label(frame_Basic_Design_Weights, text="Standard Payload").grid(row=2, column=3)

tk.Label(frame_Basic_Design_Weights, text="Max Take Off").grid(row=3,column=0, sticky="e")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=3,column=1)
tk.Label(frame_Basic_Design_Weights, text="Operating Empty").grid(row=4,column=0, sticky="e")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=4,column=1)
tk.Label(frame_Basic_Design_Weights, text="Max Zero Fuel").grid(row=5,column=0, sticky="e")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=5,column=1)
tk.Label(frame_Basic_Design_Weights, text="Max Landing").grid(row=6,column=0, sticky="e")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=6,column=1)

tk.Label(frame_Basic_Design_Weights, text="passengers").grid(row=3,column=4, sticky="w")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=3,column=3)
tk.Label(frame_Basic_Design_Weights, text="kg each").grid(row=4,column=4, sticky="w")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=4,column=3)
tk.Label(frame_Basic_Design_Weights, text="kg cargo").grid(row=5,column=4, sticky="w")
tk.Entry(frame_Basic_Design_Weights, width=10).grid(row=5,column=3)
tk.Label(frame_Basic_Design_Weights, text="@").grid(row=4, column=2, sticky="e")
tk.Label(frame_Basic_Design_Weights, text="+").grid(row=5, column=2, sticky="e")

#------------------Fin du frame du "Basic Design Weights"-----------------------------------------------------

#------------------Frame du "Thrust, Drag, Fuel Flow"-----------------------------------------------------
frame_Thrust_Drag_Fuel_Flow=tk.Frame(root)
frame_Thrust_Drag_Fuel_Flow.grid_forget()

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Factor").grid(row=2, column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Factor").grid(row=2, column=3)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Takeoff Thrust").grid(row=3,column=0, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=3,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Climb Thrust").grid(row=4,column=0, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=4,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Cruise Thrust").grid(row=5,column=0, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=5,column=1)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="All Thrusts").grid(row=6,column=0, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=6,column=1)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Zero-lift Drag").grid(row=3,column=2, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=3,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Induced Drag").grid(row=4,column=2, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=4,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Divergence_M").grid(row=5,column=2, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=5,column=3)
tk.Label(frame_Thrust_Drag_Fuel_Flow, text="All Drag").grid(row=6, column=2)
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=6, column=3)

tk.Label(frame_Thrust_Drag_Fuel_Flow, text="Fuel Flow (SFC)").grid(row=7, column=2, sticky="e")
tk.Entry(frame_Thrust_Drag_Fuel_Flow, width=10).grid(row=7, column=3)
#------------------Fin du frame du "Thrust, Drag, Fuel Flow"-----------------------------------------------------

#------------------Frame du "Emission indices"-----------------------------------------------------
frame_Emission_indices=tk.Frame(root)
frame_Emission_indices.grid_forget()

tk.Label(frame_Emission_indices, text="fuel flow").grid(row=2, column=0)
tk.Label(frame_Emission_indices, text="kg/s").grid(row=3, column=0, sticky="w")
tk.Label(frame_Emission_indices, text="Reference Emissions Indices (grams pollutant per kg fuel):").grid(row=4, column=0, columnspan=5, sticky="w")


tk.Label(frame_Emission_indices, text="idle").grid(row=2, column=1)
tk.Entry(frame_Emission_indices, width=10).grid(row=3, column=1)
tk.Label(frame_Emission_indices, text="approach").grid(row=2, column=2)
tk.Entry(frame_Emission_indices, width=10).grid(row=3, column=2)
tk.Label(frame_Emission_indices, text="climbout").grid(row=2, column=3)
tk.Entry(frame_Emission_indices, width=10).grid(row=3, column=3)
tk.Label(frame_Emission_indices, text="takeoff").grid(row=2, column=4)
tk.Entry(frame_Emission_indices, width=10).grid(row=3, column=4)

tk.Label(frame_Emission_indices, text="NOx").grid(row=5, column=0, sticky="w")
tk.Entry(frame_Emission_indices, width=10).grid(row=5, column=1)
tk.Entry(frame_Emission_indices, width=10).grid(row=5, column=2)
tk.Entry(frame_Emission_indices, width=10).grid(row=5, column=3)
tk.Entry(frame_Emission_indices, width=10).grid(row=5, column=4)
tk.Label(frame_Emission_indices, text="HC").grid(row=6, column=0, sticky="w")
tk.Entry(frame_Emission_indices, width=10).grid(row=6, column=1)
tk.Entry(frame_Emission_indices, width=10).grid(row=6, column=2)
tk.Entry(frame_Emission_indices, width=10).grid(row=6, column=3)
tk.Entry(frame_Emission_indices, width=10).grid(row=6, column=4)
tk.Label(frame_Emission_indices, text="CO").grid(row=7, column=0, sticky="w")
tk.Entry(frame_Emission_indices, width=10).grid(row=7, column=1)
tk.Entry(frame_Emission_indices, width=10).grid(row=7, column=2)
tk.Entry(frame_Emission_indices, width=10).grid(row=7, column=3)
tk.Entry(frame_Emission_indices, width=10).grid(row=7, column=4)
#------------------Fin du frame du "Emission indices"-----------------------------------------------------

#------------------Frame du "Speed and flight levels"-----------------------------------------------------
frame_optionnel = tk.Frame(root, bd=1, relief="sunken", padx=10, pady=10)
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
tk.Entry(frame_optionnel, **COMMUN).grid(row=2, column=2, columnspan= 2,sticky="w")

frame_optionnel.rowconfigure(3, minsize=20)

tk.Label(frame_optionnel, text="Available flight level (ft/100)", font = ("Arial", 8)).grid(row=4, column=0)
tk.Entry(frame_optionnel, **COMMUN).grid(row=4, column=2)

frame_optionnel.rowconfigure(5, minsize=20)

variable_speed= tk.IntVar()
tk.Label(frame_optionnel, text="Climb Speed (KCAS)", font = ("Arial", 8)).grid(row=6, column=0)
tk.Entry(frame_optionnel, **COMMUN).grid(row=6, column=2)
tk.Label(frame_optionnel, text="Climb Mach", font = ("Arial", 8)).grid(row=7, column=0)
tk.Entry(frame_optionnel, **COMMUN).grid(row=7, column=2)
#------------------Fin de frame du "Speed and flight levels"-----------------------------------------------------

#------------------Frame du "Unit preferences"-----------------------------------------------------
frame_unit_preferences = tk.Frame(root, bd=1, relief="sunken", padx=10, pady=10)
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
tk.Button(root, text = "Sauvegarder").grid(row=12, column=0, columnspan = 3)
tk.Button(root, text = "Charger").grid(row=12, column =3, columnspan = 3)
root.rowconfigure(13, minsize=20)
tk.Frame(root, height=2, bg="black").grid(row=14, column=0, columnspan=6, sticky="ew")
root.rowconfigure(15, minsize=20)
tk.Label(root, text="output:").grid(row=16, column=0, sticky="w")
variable_choisie = tk.StringVar()
menu_deroulant = ttk.Combobox(root, textvariable = variable_choisie, state="readonly")
menu_deroulant['values'] = ('Block Range Summary', "Detailed Flight Profile", "Block Performance Tables", "Point Performance", "Payload_Range Boundary", "Takeoff/Landing Field Lengths")
menu_deroulant.grid(row=16, column =1,columnspan = 3, sticky= "ew")
menu_deroulant.current(0) 

tk.Button(root, text ="OK", command = lambda : print ("Sélection :", variable_choisie.get())).grid(row=16, column=4, sticky="w", padx=5)
case_var = tk.IntVar()
case_var.set(1)
tk.Radiobutton(root, variable=case_var, value = 1).grid(row=17, column=1, sticky="w")
tk.Label(root, text="Design range with Standard Payload").grid(row=17, column=2, columnspan=2, sticky="w", padx=(20, 0))
tk.Radiobutton(root, variable=case_var, value = 2).grid(row=18, column=1, sticky="w")
tk.Label(root, text="Range (nm)").grid(row=18, column=2, sticky="w", padx=(20, 0))
tk.Label(root, text="with Payload(kg)").grid(row=18, column=3, sticky="w", padx=(20, 0))
tk.Entry(root, **COMMUN).grid(row=19, column =2)
tk.Entry(root, **COMMUN).grid(row=19, column =3)
#-----------------------Fin de la partie Fixe en bas de la page-----------------------------------------------------

root.mainloop()