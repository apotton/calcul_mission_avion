class Constantes:
    '''
    Classe statique qui gère les nombre constants, utilisés régulièrement à travers le code.
    '''
    g = 9.80665 # Gravité (m/s²)
        
    # Constantes Atmosphère
    rho0  = 1.225    # Masse volumique (kg/m^3)
    rho11 = 0.364    # Masse volumique à 11000m
    p0_Pa = 101325   # Pression au niveau de la mer (Pa)
    T0_K  = 288.15   # Température au niveau de la mer (K)

    Th_Kparm = -6.5e-3     # Gradients de température (entre 0 et 11km d'altitude)

    r = 8.31446261815324 / 0.02896442488  # Constante des gaz parfait (J/kg/K)
    gamma = 1.4                           # Indice adiabatique

    # Constantes émissions
    EI_H2O  = 1.2351017         # Constante humidité (Indice d'émission ?)
    Cp      = 1004              # J/Kg/K
    epsilon = 0.622             # Rapport des masses molaires (eau/air sec)
    Q       = 43124000          # J/Kg (Chaleur latente ou pouvoir calorifique)

    # Constantes de conversion
    conv_kt_mps = 0.514666666   # Conversion kt vers m/s
    conv_ft_m   = 0.3048        # Conversion ft vers m
    conv_NM_m   = 1852          # Conversion Nm vers m
    conv_lb_kg  = 0.453592      # Conversion lb vers kg
