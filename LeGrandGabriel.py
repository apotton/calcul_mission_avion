# Définition de la mission
# Profil de montée
Initial_climb_altitude_ft = 1500
Final_climb_altitude_ft = 35000
KCAS_low_climb = 250

h_lim_climb_ft = 10000
KCAS_high_climb = 280
Mach_climb = 0.78

# Critère de croisière
Mach_cruise = 0.78
RRoC_min = 300  # en fpm
Vw_kt = 0

ECONOMIC = 1
MR = 1
LRC = 0
k_SAR_cruise = 0.99

Cost_Index = 0

# Choix du CI de croisière
CI_cruise = 50  # entre 0 et 50

# Critère de descente
Mach_descent = 0.78
KCAS_high_descent = 280
KCAS_low_descent = 250
h_lim_descent_ft = 10000
Final_descent_altitude_ft = 1500

# Critère de diversion
Final_climb_altitude_diversion_ft = 25000
Range_diversion_NM = 200

# Critère Holding
KCAS_holding = 300  # kt
Time_holding = 30   # min

# Critère contingency (%)
Contingency = 5  # en %

# Conversion finale
Range_diversion = Range_diversion_NM * conv_NM_m

#conditions de calcul
extrapval=1
Reseau_moteur=1
Aero_simplified=0
Weight_limited=1
Method_interp='linear'

precision=0.01
dt=10

#définition de la mission

DISA=0
Relative_humidity_cruise=0
Range_mission_NM=800
m_payload=Max_PL_Weight

ecart_mission=1
ecart_diversion=1
n_boucle=0
l_mission=0
l_descent_ops=0
l_descent_div=0
m_fuel_diversion=0
m_fuel_reserve=0
m_fuel_mission=Max_Fuel_Weight

while (ecart_mission > precision) and (n_boucle < 10) :
    m_fuel=m_fuel_mission, + m_fuel_reserve

    TOW = m_fuel+OEW+m_payload

    if (Weight_limited ==1) :
        if m_fuel>Max_Fuel_Weight :
            m_fuel=Max_Fuel_Weight
            TOW=m_fuel+OEW+m_payload

        if TOW>MTOW :
            m_fuel=m_fuel-(TOW-MTOW)
            TOW=MTOW
#   Mission_computation()
    
    ecart_mission = abs(FB_mission-m_fuel_mission)/m_fuel_mission*100
    m_fuel_mission = FB_mission

    m_fuel_contingency=Contingency*m_fuel_mission/100
    m_fuel_reserve=FB_diversion+FB_holding+m_fuel_contingency

    n_boucle += 1