class DonneesMoteur:
    '''
    Classe permettant d'accéder aux données d'un moteur simulé par les formules d'Elodie Roux.
    '''

    def __init__(self, OPR, BPR, F0, T4,
                dT4_climb, dT4_cruise, h_opt,
                fuel_flow_ref,
                EI_HC_ref,
                EI_CO_ref,
                EI_NOx_ref):
            
        self.OPR = OPR
        self.BPR = BPR
        self.F0 = F0
        self.T4 = T4
        self.dT4_climb = dT4_climb
        self.dT4_cruise = dT4_cruise
        self.h_opt = h_opt
        self.fuel_flow_ref = fuel_flow_ref
        self.EI_HC_ref = EI_HC_ref
        self.EI_CO_ref = EI_CO_ref
        self.EI_NOx_ref = EI_NOx_ref


