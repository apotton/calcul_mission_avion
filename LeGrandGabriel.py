import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("PIE COA26")
root.geometry("1200x1000")
#root.columnconfigure(0, weight=1) 
#root.rowconfigure(0, weight=1)
COMMUN = {"font": ("Arial", 6), "borderwidth": 1, "relief": "solid"}

#tk.Label(root, text = "Mach de vol:", width=18, height=2, **COMMUN).grid(row = 0, column = 0) 
# entry_mach = tk.Entry(root, **COMMUN).grid(row=0, column =1, columnspan = 1)
# tk.Label(root, text = "/", width=5, height=2, **COMMUN).grid(row = 0, column= 2)

# tk.Label(root, text = "Distance:", width=18, height=2, **COMMUN).grid(row = 1, column = 0) 
# entry_mach = tk.Entry(root, **COMMUN).grid(row=1, column =1, columnspan = 1)
# tk.Label(root, text = "m", width=5, height=2, **COMMUN).grid(row = 1, column= 2)

# tk.Label(root, text = "Masse:", width=18, height=2, **COMMUN).grid(row = 2, column = 0) 
# entry_mach = tk.Entry(root, **COMMUN).grid(row=2, column =1, columnspan = 1)
# tk.Label(root, text = "kg", width=5, height=2, **COMMUN).grid(row = 2, column= 2)

# tk.Button(root, text = "Appuie").grid(row=3, column =0, columnspan = 2)
# tk.Entry(root, width=20).grid(row=4, column =0, columnspan = 2)

tk.Label(root, text="Adjust:").grid(row=1, column=0, sticky="w")
entree_choisie = tk.StringVar()
menu_deroulant_1 = ttk.Combobox(root, textvariable = entree_choisie, state="readonly")
menu_deroulant_1['values'] = ('Basic Design Weights', "Thrust Drag Fuel FLow", "Emission indices", "Speed and flight levels", "Reserve and Allowances", "Unit preferences")
menu_deroulant_1.grid(row=1, column =1,columnspan = 3, sticky= "ew")
menu_deroulant_1.current(0) 

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


def gerer_affichage(event):
    if menu_deroulant_1.get() == "Speed and flight levels":

        frame_optionnel.grid(row=6, column=0, columnspan=6, sticky="ew")
    else:
        frame_optionnel.grid_forget()

menu_deroulant_1.bind("<<ComboboxSelected>>", gerer_affichage)
#------------------Fin de frame du "Speed and flight levels"-----------------------------------------------------



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
#-----------------------Fin de la artie Fixe en bas de la page-----------------------------------------------------

root.mainloop()