# Démineur — Matplotlib Minesweeper

Un jeu de Démineur entièrement jouable dans une fenêtre Python/Matplotlib, sans dépendances autres que Matplotlib.

## Prérequis

| Paquet | Version testée |
|--------|----------------|
| Python | ≥ 3.8 |
| matplotlib | ≥ 3.5 |

Installation rapide :
```bash
pip install matplotlib
```

## Lancement

```bash
python demineur.py
```

Une fenêtre graphique s'ouvre avec la grille de jeu.

## Contrôles

| Action | Touche / Bouton |
|--------|-----------------|
| Révéler une case | Clic gauche |
| Poser / retirer un drapeau | Clic droit |

## Règles

- La grille contient des mines cachées.
- Révéler une mine → partie perdue.
- Révéler toutes les cases sans mine → victoire ✓
- Un chiffre sur une case révélée indique le nombre de mines dans les 8 cases voisines.
- Une case vide (0) propage automatiquement la révélation à ses voisines.
- Posez des drapeaux (affichés `P`) sur les cases que vous suspectez de contenir une mine.

## Niveaux de difficulté

En haut du fichier `demineur.py`, modifiez les constantes globales :

```python
# Débutant
hauteur, largeur = 9, 9
nb_mines_total = 10

# Intermédiaire
hauteur, largeur = 16, 16
nb_mines_total = 40

# Expert (défaut)
hauteur, largeur = 16, 30
nb_mines_total = 99
```

## Structure du code

```
demineur.py
│
├── Constantes globales
│   ├── hauteur, largeur      — dimensions de la grille
│   ├── nb_mines_total        — nombre de mines
│   └── couleurs_chiffres     — couleurs des chiffres 1–8 (standard Démineur)
│
└── class Demineur
    │
    ├── __init__()            — initialise les grilles et place les mines aléatoirement
    │
    ├── Initialisation de la grille
    │   └── calcul des voisins — compte les mines autour de chaque case (self.compte)
    │
    ├── Interface Matplotlib
    │   ├── dessiner()        — redessine toute la grille à chaque interaction
    │   └── connexion événements — clic souris via mpl_connect
    │
    ├── Gestion des événements
    │   └── quand_on_clique() — clic gauche → reveler(), clic droit → drapeau
    │
    └── Logique de jeu
        └── reveler()         — révèle une case et propage récursivement si case vide
```

## Points techniques notables

**Grilles en listes Python**
Quatre listes 2D stockent l'état du jeu :
- `self.champ` — position des mines (1 ou 0)
- `self.visible` — cases révélées (True/False)
- `self.drapeaux` — cases avec drapeau (True/False)
- `self.compte` — nombre de mines voisines (0–8)

**Rendu avec Matplotlib**
Chaque case est un `plt.Rectangle`. Les chiffres et drapeaux sont affichés via `ax.text()`. La méthode `dessiner()` efface et redessine la grille complète à chaque interaction.

**Gestion des événements**
Les clics de souris sont interceptés via `mpl_connect('button_press_event', ...)`. La méthode `quand_on_clique()` traduit les coordonnées graphiques en index de matrice, puis dispatche vers `reveler()` ou la logique de drapeau.

**Propagation en cascade (flood fill)**
Quand une case révélée a 0 mine voisine, `reveler()` s'appelle récursivement sur ses 8 voisines. La vérification `if self.visible[y][x] == True` arrête la récursion naturellement.

## Limites actuelles

- **Premier clic non protégé** — les mines sont placées avant toute interaction, le premier clic peut donc tomber directement sur une mine.
- **Grille fixe** — les dimensions et le nombre de mines sont définis par des constantes globales ; il n'y a pas de menu de sélection de difficulté intégré.

## Pour rejouer

Fermez la fenêtre et relancez le script :

```bash
python demineur.py
```

---

Développé avec Python 3 et Matplotlib.
