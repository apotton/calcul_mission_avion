import matplotlib.pyplot as plt

# Données calculées (Basées sur votre drapage et materiau)
# Position dans l'épaisseur (mm)
z = [0, 2.75, 2.75, 5.5, 8.25, 8.25, 11]
# Valeurs de Tsai-Hill (Calculées pour Nx = -200 N/mm)
tsai = [0.062, 0.031, 0.002, 0.000, 0.002, 0.031, 0.051]

# Création du graphique
fig, ax = plt.subplots(figsize=(10, 6))

# Couleur de fond grise (pour garder le style de votre image)
ax.set_facecolor('#E0E0E0') 

# --- MODIFICATION ICI : Inversion des variables dans plot() ---
# z est maintenant en X (abscisse), tsai en Y (ordonnée)
ax.plot(z, tsai, color='green', linewidth=1.5, label='TSAIH vs Thickness')

# Étiquettes des axes inversées
ax.set_xlabel('Thickness (mm)', fontsize=10)
ax.set_ylabel('Tsai-Hill Criterion', fontsize=10)

# Ajustement des échelles (Limites inversées aussi)
ax.set_xlim(0, 11)      # L'épaisseur va de 0 à 11 sur l'axe X
ax.set_ylim(0, 0.07)    # Le critère va de 0 à 0.07 sur l'axe Y

# Grille et Titre
ax.grid(True, which='both', color='white', linestyle='-', linewidth=0.5, alpha=0.5)
ax.set_title("Critère de Tsai-Hill le long de l'épaisseur", fontsize=12)

# Afficher le graphique
plt.show()