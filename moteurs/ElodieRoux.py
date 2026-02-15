from moteurs.Moteur import Moteur

class ElodieRoux(Moteur):
    def __init__(self, Avion, BPR=0, OPR=0):
        super().__init__(Avion)
        # Pas de Donnees_moteur ici, peut-être d'autres constantes spécifiques

    def Calculate_F(self):
        print("Calcul Poussée via méthode analytique (Elodie Roux)")
        # Ici tu mets tes équations mathématiques
        # self.F_t = ... formule mathématique ...

    def Calculate_SFC(self, F_engine_N=None):
        print("Calcul SFC via méthode analytique (Elodie Roux)")
        # Ici tu mets tes équations mathématiques
        # self.SFC_t = ... formule mathématique ...



# Dans cruise_mach_SAR.py
# 
# else % mode analytique
#     F_MCL_cruise_step=2*CalculateFmax(F_0_uni_ref*dx_MCL,Mach_cruise,h_cruise_step);
# end

# else % Modèle Elodie Roux
#     F_MCL_cruise_step_up=2*CalculateFmax(F_0_uni_ref*dx_MCL,Mach_cruise,h_cruise_step+2000*conv_ft_m);
# end


# else % Analytique 
#     [F_N_AEO_cruise_step]=CalculateFmax(F_0*dx_MCL,Mach_cruise_step,h_cruise_step);
#     [SFC_cruise_step]=CalculateSFC(F_N_AEO_cruise_step,F_N_AEO_cruise_step,T_cruise_step,Mach_cruise_step,h_cruise_step);
# end 


# Climb ops 
# else
#     [F_N_AEO_climb_ops]=CalculateFmax(F_0*dx_MCL,Mach_climb_ops,h_climb_ops);
#     [SFC_climb_ops]=CalculateSFC(F_N_AEO_climb_ops,F_N_AEO_climb_ops,T_climb_ops,Mach_climb_ops,h_climb_ops);
# end

# else
#     [F_N_AEO_climb_ops]=CalculateFmax(F_0*dx_MCL,Mach_climb_ops,h_climb_ops);
#     [SFC_climb_ops]=CalculateSFC(F_N_AEO_climb_ops,F_N_AEO_climb_ops,T_climb_ops,Mach_climb_ops,h_climb_ops);
# end