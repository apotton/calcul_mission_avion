import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk

def rien():
    messagebox.showinfo("Fontion en cours d'éxécution")

COMMUN = {"font": ("Garamond", 10)}

# --- CONFIGURATION PRINCIPALE ---

root = tk.Tk()
root.title("PIE COA26")
root.geometry("1200x1000")


# --- CONSTRUCTION DE L'INTERFACE (Layout GRID) ---
# Choix de l'avion
liste_avion= ["A320", "A350", "Boeing 777X", "tapis volant d'Aladin"]
lbl_avion = tk.Label(root, text="Plane:").grid(row=0, column=0, sticky="w")
menu_deroulant_avion=ttk.Combobox(root, values=liste_avion)
menu_deroulant_avion.state(["readonly"])
menu_deroulant_avion.grid(row=0, column=1, padx=0, pady=5, sticky="w")

# Choix des paramètres de mesure
liste_choix= ["Basic design weights", "Thrust, Drag, Fuel Flow", "Emission indices", "Speeds and flight levels", "Reserves and allowances", "Unit preferences"]
lbl_choix = tk.Label(root, text="Adjust:").grid(row=1, column=0, sticky="w")
menu_deroulant_choix=ttk.Combobox(root, values=liste_choix)
menu_deroulant_choix.state(["readonly"])
menu_deroulant_choix.grid(row=1, column=1, padx=0, pady=5, sticky="w")


#------------------Frame du "Basic Design Weights"-----------------------------------------------------
frame_Basic_Design_Weights=tk.Frame(root)
frame_Basic_Design_Weights.grid_forget()

#def
lbl_weight=tk.Label(frame_Basic_Design_Weights, text="Weight (kg)")
lbl_standard_payload=tk.Label(frame_Basic_Design_Weights, text="Standard Payload")

lbl_MaxTakeOff=tk.Label(frame_Basic_Design_Weights, text="Max Take Off")
max_take_off = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_OperatingEmpty=tk.Label(frame_Basic_Design_Weights, text="Operating Empty")
operating_empty = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_MaxZeroFuel=tk.Label(frame_Basic_Design_Weights, text="Max Zero Fuel")
max_zero_fuel = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_Landing=tk.Label(frame_Basic_Design_Weights, text="Max Landing")
max_landing = tk.Entry(frame_Basic_Design_Weights, width=10)

lbl_passengers=tk.Label(frame_Basic_Design_Weights, text="passengers")
passengers = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_kgEach=tk.Label(frame_Basic_Design_Weights, text="kg each")
kg_each = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_kgCargo=tk.Label(frame_Basic_Design_Weights, text="kg cargo")
kg_cargo = tk.Entry(frame_Basic_Design_Weights, width=10)
lbl_at = tk.Label(frame_Basic_Design_Weights, text="@")
lbl_plus = tk.Label(frame_Basic_Design_Weights, text="+")

# Positions 
lbl_weight.grid(row=2, column=1)
lbl_standard_payload.grid(row=2, column=3)

lbl_MaxTakeOff.grid(row=3,column=0, sticky="e")
max_take_off.grid(row=3,column=1)
lbl_OperatingEmpty.grid(row=4,column=0, sticky="e")
operating_empty.grid(row=4,column=1)
lbl_MaxZeroFuel.grid(row=5,column=0, sticky="e")
max_zero_fuel.grid(row=5,column=1)
lbl_Landing.grid(row=6,column=0, sticky="e")
max_landing.grid(row=6,column=1)

lbl_passengers.grid(row=3,column=4, sticky="w")
passengers.grid(row=3,column=3)
lbl_kgEach.grid(row=4,column=4, sticky="w")
kg_each.grid(row=4,column=3)
lbl_kgCargo.grid(row=5,column=4, sticky="w")
kg_cargo.grid(row=5,column=3)
lbl_at.grid(row=4, column=2, sticky="e")
lbl_plus.grid(row=5, column=2, sticky="e")






#------------------Frame du "Emission indices"-----------------------------------------------------
frame_Emission_indices=tk.Frame(root)
frame_Emission_indices.grid_forget()

lbl_fuel_flow=tk.Label(frame_Emission_indices, text="fuel flow")
lbl_kg_s=tk.Label(frame_Emission_indices, text="kg/s")
lbl_Reference_Emissions_Indices=tk.Label(frame_Emission_indices, text="Reference Emissions Indices (grams pollutant per kg fuel):")

lbl_idle=tk.Label(frame_Emission_indices, text="idle")
idle = tk.Entry(frame_Emission_indices, width=10)
lbl_approach=tk.Label(frame_Emission_indices, text="approach")
approach = tk.Entry(frame_Emission_indices, width=10)
lbl_climbout=tk.Label(frame_Emission_indices, text="climbout")
climbout = tk.Entry(frame_Emission_indices, width=10)
lbl_takeoff=tk.Label(frame_Emission_indices, text="takeoff")
takeoff = tk.Entry(frame_Emission_indices, width=10)

lbl_NOx=tk.Label(frame_Emission_indices, text="NOx")
NOx_idle = tk.Entry(frame_Emission_indices, width=10)
NOx_approach = tk.Entry(frame_Emission_indices, width=10)
NOx_climbout = tk.Entry(frame_Emission_indices, width=10)
NOx_takeoff = tk.Entry(frame_Emission_indices, width=10)
lbl_HC=tk.Label(frame_Emission_indices, text="HC")
HC_idle = tk.Entry(frame_Emission_indices, width=10)
HC_approach = tk.Entry(frame_Emission_indices, width=10)
HC_climbout = tk.Entry(frame_Emission_indices, width=10)
HC_takeoff = tk.Entry(frame_Emission_indices, width=10)
lbl_CO=tk.Label(frame_Emission_indices, text="CO")
CO_idle = tk.Entry(frame_Emission_indices, width=10)
CO_approach = tk.Entry(frame_Emission_indices, width=10)
CO_climbout = tk.Entry(frame_Emission_indices, width=10)
CO_takeoff = tk.Entry(frame_Emission_indices, width=10)

# Positions
lbl_fuel_flow.grid(row=2, column=0)
lbl_kg_s.grid(row=3, column=0, sticky="w")
lbl_Reference_Emissions_Indices.grid(row=4, column=0, columnspan=5, sticky="w")

lbl_idle.grid(row=2, column=1)
idle.grid(row=3, column=1)
lbl_approach.grid(row=2, column=2)
approach.grid(row=3, column=2)
lbl_climbout.grid(row=2, column=3)
climbout.grid(row=3, column=3)
lbl_takeoff.grid(row=2, column=4)
takeoff.grid(row=3, column=4)

lbl_NOx.grid(row=5, column=0, sticky="w")
NOx_idle.grid(row=5, column=1)
NOx_approach.grid(row=5, column=2)
NOx_climbout.grid(row=5, column=3)
NOx_takeoff.grid(row=5, column=4)
lbl_HC.grid(row=6, column=0, sticky="w")
HC_idle.grid(row=6, column=1)
HC_approach.grid(row=6, column=2)
HC_climbout.grid(row=6, column=3)
HC_takeoff.grid(row=6, column=4)
lbl_CO.grid(row=7, column=0, sticky="w")
CO_idle.grid(row=7, column=1)
CO_approach.grid(row=7, column=2)
CO_climbout.grid(row=7, column=3)
CO_takeoff.grid(row=7, column=4)



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
tk.Entry(frame_optionnel, **COMMUN).grid(row=2, column=2, columnspan= 2)

frame_optionnel.rowconfigure(3, minsize=20)

tk.Label(frame_optionnel, text="Available flight level (ft/100)", font = ("Arial", 8)).grid(row=4, column=1, columnspan = 3)
tk.Entry(frame_optionnel, **COMMUN).grid(row=4, column=0)

frame_optionnel.rowconfigure(5, minsize=20)

variable_speed= tk.IntVar()
tk.Label(frame_optionnel, text="Climb Speed (KCAS)", font = ("Arial", 8)).grid(row=6, column=1, columnspan = 3, sticky="w")
tk.Entry(frame_optionnel, **COMMUN).grid(row=6, column=0)
tk.Label(frame_optionnel, text="Climb Mach", font = ("Arial", 8)).grid(row=7, column=1, columnspan = 3 , sticky="w")
tk.Entry(frame_optionnel, **COMMUN).grid(row=7, column=0)





#------------------Frame du "Reserves and allowances"-----------------------------------------------------
frame_Reserves_and_allowances=tk.Frame(root)
frame_Reserves_and_allowances.grid_forget()

frame_Reserves_and_allowances1=tk.Frame(frame_Reserves_and_allowances)
frame_Reserves_and_allowances2=tk.Frame(frame_Reserves_and_allowances1)

lbl_Diversion_Distance=tk.Label(frame_Reserves_and_allowances1, text="Diversion Distance (nm)")
Diversion_Distance = tk.Entry(frame_Reserves_and_allowances1, width=10)
lbl_Holding_Time=tk.Label(frame_Reserves_and_allowances1, text="Holding Time (min)")
Holding_Time = tk.Entry(frame_Reserves_and_allowances1, width=10)
lbl_Contingency_Fuel_Rule=tk.Label(frame_Reserves_and_allowances1, text="Contingency Fuel Rule")
Contingency_Fuel_Rule = tk.Entry(frame_Reserves_and_allowances1, width=10)

liste_choix_Fuel_Rule= ["% Of mission fuel", "% Of total fuel", "% Of MTOW", "% Of flight time"]
menu_deroulant_choix_Fuel_Rule=ttk.Combobox(frame_Reserves_and_allowances1, values=liste_choix_Fuel_Rule)
menu_deroulant_choix_Fuel_Rule.state(["readonly"])

lbl_Allowances=tk.Label(frame_Reserves_and_allowances2, text="Allowances:")
lbl_taxi_out=tk.Label(frame_Reserves_and_allowances2, text="taxi out")
taki_out=tk.Entry(frame_Reserves_and_allowances2, width=10)
lbl_takeoff2=tk.Label(frame_Reserves_and_allowances2, text="takeoff")
takeoff2=tk.Entry(frame_Reserves_and_allowances2, width=10)
lbl_approach=tk.Label(frame_Reserves_and_allowances2, text="approach")
approach=tk.Entry(frame_Reserves_and_allowances2, width=10)
lbl_taxi_in=tk.Label(frame_Reserves_and_allowances2, text="taxi in")
taxi_in=tk.Entry(frame_Reserves_and_allowances2, width=10)
lbl_miss_app=tk.Label(frame_Reserves_and_allowances2, text="miss.app.")
miss_app=tk.Entry(frame_Reserves_and_allowances2, width=10)
lbl_Time=tk.Label(frame_Reserves_and_allowances2, text="Time (min)")

# Positions
frame_Reserves_and_allowances1.grid(row=2, column=0, columnspan=5)
frame_Reserves_and_allowances2.grid(row=6, column=0, columnspan=6)

lbl_Diversion_Distance.grid(row=2, column=0)
Diversion_Distance.grid(row=2, column=1)
lbl_Holding_Time.grid(row=3, column=0)
Holding_Time.grid(row=3, column=1)
lbl_Contingency_Fuel_Rule.grid(row=4, column=0)
Contingency_Fuel_Rule.grid(row=4, column=1)

menu_deroulant_choix_Fuel_Rule.grid(row=4, column=2, sticky="w")

lbl_Allowances.grid(row=6, column=0)
lbl_taxi_out.grid(row=6, column=1)
taki_out.grid(row=7, column=1)
lbl_takeoff2.grid(row=6, column=2)
takeoff2.grid(row=7, column=2)
lbl_approach.grid(row=6, column=3)
approach.grid(row=7, column=3)
lbl_taxi_in.grid(row=6, column=4)
taxi_in.grid(row=7, column=4)
lbl_miss_app.grid(row=6, column=5)
miss_app.grid(row=7, column=5)
lbl_Time.grid(row=7, column=0)


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



def mettre_a_jour_affichage(event):
    if menu_deroulant_choix.get() == "Basic design weights":
        frame_Basic_Design_Weights.grid(row=2, column=0, columnspan=5)
    else:
        frame_Basic_Design_Weights.grid_forget()
    if menu_deroulant_choix.get() == "Thrust, Drag, Fuel Flow":
        frame_Thrust_Drag_Fuel_Flow.grid(row=2, column=0, columnspan=5)
    else:
        frame_Thrust_Drag_Fuel_Flow.grid_forget()
    if menu_deroulant_choix.get() == "Emission indices":
        frame_Emission_indices.grid(row=2, column=0, columnspan=5)
    else :
        frame_Emission_indices.grid_forget()
    if menu_deroulant_choix.get() == "Speeds and flight levels":
        frame_optionnel.grid(row=2, column=0, columnspan=5)
    else :
        frame_optionnel.grid_forget()
    if menu_deroulant_choix.get() == "Reserves and allowances":
        frame_Reserves_and_allowances.grid(row=2, column=0, columnspan=5)
    else :
        frame_Reserves_and_allowances.grid_forget()
    if menu_deroulant_choix.get() == "Unit preferences":
        frame_unit_preferences.grid(row=2, column=0, columnspan=5)
    else :
        frame_unit_preferences.grid_forget()
   


menu_deroulant_choix.bind("<<ComboboxSelected>>", mettre_a_jour_affichage) # Lance la fonction de mise à jour d'affichage


#-----------------------Partie Fixe en bas de la page-----------------------------------------------------
frame_button_bottom = tk.Frame(root).grid(row=12, column=0, columnspan=6)
tk.Button(frame_button_bottom, text = "Sauvegarder").grid(row=12, column=0, columnspan = 3, sticky="w", padx=[10,10])
tk.Button(frame_button_bottom, text = "Charger").grid(row=12, column =3, columnspan = 3, sticky="e", padx=[10,10])

root.rowconfigure(13, minsize=20)
tk.Frame(frame_button_bottom, height=2, bg="black").grid(row=14, column=0, columnspan=6, sticky="ew")
root.rowconfigure(15, minsize=20)
tk.Label(frame_button_bottom, text="output:").grid(row=16, column=0, sticky="w")

frame_bottom = tk.Frame(root).grid(row=16, column=0, columnspan=6)
variable_choisie = tk.StringVar()
menu_deroulant = ttk.Combobox(frame_bottom, textvariable = variable_choisie, state="readonly")
menu_deroulant['values'] = ('Block Range Summary', "Detailed Flight Profile", "Block Performance Tables", "Point Performance", "Payload_Range Boundary", "Takeoff/Landing Field Lengths")
menu_deroulant.grid(row=16, column =1,columnspan = 3, sticky= "ew")
menu_deroulant.current(0) 

tk.Button(frame_bottom, text ="OK", command = lambda : print ("Sélection :", variable_choisie.get())).grid(row=16, column=4, sticky="w", padx=5)
case_var = tk.IntVar()
case_var.set(1)
tk.Radiobutton(frame_bottom, variable=case_var, value = 1).grid(row=17, column=1, sticky="w")
tk.Label(frame_bottom, text="Design range with Standard Payload").grid(row=17, column=2, columnspan=2, sticky="w")
tk.Radiobutton(frame_bottom, variable=case_var, value = 2).grid(row=18, column=1, sticky="w")
tk.Label(frame_bottom, text="Range (nm)").grid(row=18, column=2, sticky="w")
tk.Label(frame_bottom, text="with Payload(kg)").grid(row=18, column=3, sticky="w")
tk.Entry(frame_bottom, **COMMUN).grid(row=19, column =2)
tk.Entry(frame_bottom, **COMMUN).grid(row=19, column =3)


#-----------------------Fin de la partie Fixe en bas de la page-----------------------------------------------------

root.mainloop()
