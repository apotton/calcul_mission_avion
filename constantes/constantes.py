class Constantes:
        
    # --- Constantes Atmosphère ---
    rho0_kgm3 = 1.225  # Masse volumique (kg/m^3)
    p0_Pa = 101325   # Pression (Pa)
    T0_K = 288.15   # Température (K)

    a_h = -0.11e-3    # Approximation exponentielle Coefficient a (approx. exp)
    b_h = -0.136e-3   # Approximation exponentielle Coefficient b (approx. exp)

    Th_Kparm = -6.5e-3     # Gradients de température (entre 0 et 11km d'altitude)

    r = 8.31446261815324 / 0.02896442488  # Constante des gaz parfait (J/kg/K)
    gamma = 1.4                              # Indice adiabatique

    g=9.80665 # Gravité (m/s²)

    EI_H2O = 1.2351017  # Constante humidité (Indice d'émission ?)
    Cp = 1004           # J/Kg/K
    epsilon = 0.622     # Rapport des masses molaires (eau/air sec)
    Q = 43124000        # J/Kg (Chaleur latente ou pouvoir calorifique)



    # --- Constantes de conversion ---
    conv_kt_mps=0.514666666 # Conversion kt en m/s
    conv_ft_m=0.3048 # Conversion ft en m
    conv_NM_m=1852 # Conversion Nm en m
    conv_lb_kg=0.453592 # Conversion lb en kg