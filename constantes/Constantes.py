class Constantes:
        
    # --- Constantes Atmosphère ---
    rho0_kgm3   = 1.225    # Masse volumique (kg/m^3)
    p0_Pa       = 101325   # Pression (Pa)
    T0_K        = 288.15   # Température (K)

    Th_Kparm = -6.5e-3     # Gradients de température (entre 0 et 11km d'altitude)

    r = 8.31446261815324 / 0.02896442488  # Constante des gaz parfait (J/kg/K)
    gamma = 1.4                           # Indice adiabatique

    g = 9.80665 # Gravité (m/s²)

    EI_H2O  = 1.2351017         # Constante humidité (Indice d'émission ?)
    Cp      = 1004              # J/Kg/K
    epsilon = 0.622             # Rapport des masses molaires (eau/air sec)
    Q       = 43124000          # J/Kg (Chaleur latente ou pouvoir calorifique)

    # Constantes de conversion
    conv_kt_mps = 0.514666666   # Conversion kt en m/s
    conv_ft_m   = 0.3048        # Conversion ft en m
    conv_NM_m   = 1852          # Conversion Nm en m
    conv_lb_kg  = 0.453592      # Conversion lb en kg


    # Coefficients pour le calcul de la SFC

    # Coefficients Troposphère
    a1_troposphere_1 = -7.44e-13  # 0.000000000001673685489809980000
    a1_troposphere_2 = 6.54e-7    # 0.000000271973216373792000000000
    a2_troposphere_1 = -3.32e-10  # -0.000000000050392752180622600000
    a2_troposphere_2 = 8.54e-6    # 0.000012264573143726900000000000
    b1_troposphere_1 = -3.47e-11  # -0.000000000007256995083984370000
    b1_troposphere_2 = -6.58e-7   # -0.000000207867787329130000000000
    b2_troposphere_1 = 4.23e-10   # 0.000000000085471019929081500000
    b2_troposphere_2 = 1.32e-5    # 0.000010593476302983000000000000
    c_troposphere    = -1.05e-7   # -0.000000023325594999116000000000

    # Coefficients Stratosphère (Calculés)
    a1_stratosphere = a1_troposphere_1 * 11000 + a1_troposphere_2 # 6.45e-7
    a2_stratosphere = a2_troposphere_1 * 11000 + a2_troposphere_2 # 4.89e-6
    b1_stratosphere = b1_troposphere_1 * 11000 + b1_troposphere_2 # -1.04e-6
    b2_stratosphere = b2_troposphere_1 * 11000 + b2_troposphere_2 # 1.79e-5
    c_stratosphere  = c_troposphere                               # -1.05e-7

    # Coefficients Surface
    coef_SFC1 = 7.4e-13            # 0.000000000000117760232145255000
    coef_SFC  = 0.663573705252024  # 0.000000000000000000000000000000


    const_SFCmin         = 0.998  # 1.001241429
    coef_alt_SFCmin      = 0      # -0.003092577
    coef_mach_SFCmin     = 0      # -0.015688604
    coef_alt_mach_SFCmin = 0      # 0.015770772

    const_Fi             = 0.85   # 1.040417117
    coef_alt_Fi          = 0      # 0.002494591
    coef_mach_Fi         = 0      # -0.099775754
    coef_alt_mach_Fi1    = 0      # 2.369599459
    coef_alt_mach_Fi2    = 0      # -2.385063906

    coef_fpr_SFCmin      = 0      # 0.001739837
    coef_fpr_Fi          = 0      # 0.048060427