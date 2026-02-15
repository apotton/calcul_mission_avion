'''
Fichier qui définit les champs à l'intérieur des Données Moteur
'''

class DonneesMoteur:
    '''
    Classe permettant d'accéder aux données d'un réseau moteur en entrée.
    '''
    def __init__(self, mach_table,
                 alt_table_ft,
                 Fn_MCL_table,
                 Fn_FI_table,
                 SFC_MCL_table,
                 FF_FI_table,
                 mach_table_crl,
                 cruise_data,
                 mach_table_crl_holding,
                 fn_lbf_crl_holding,
                 sfc_crl_holding):
        
        self.mach_table = mach_table
        self.alt_table_ft = alt_table_ft
        self.Fn_MCL_table = Fn_MCL_table
        self.Fn_FI_table = Fn_FI_table
        self.SFC_MCL_table = SFC_MCL_table
        self.FF_FI_table = FF_FI_table
        self.mach_table_crl = mach_table_crl
        self.cruise_data = cruise_data
        self.mach_table_crl_holding = mach_table_crl_holding
        self.fn_lbf_crl_holding = fn_lbf_crl_holding
        self.sfc_crl_holding = sfc_crl_holding


