Démineur — Matplotlib Minesweeper
Un jeu de Démineur entièrement jouable dans une fenêtre Python/Matplotlib, sans dépendances autres que NumPy et Matplotlib.

Prérequis
PaquetVersion testéePython≥ 3.8matplotlib≥ 3.5numpy≥ 1.21
Installation rapide :
bashpip install matplotlib numpy

Lancement
bashpython minesweeper.py
Une fenêtre graphique s'ouvre avec la grille de jeu.

Contrôles
ActionTouche / BoutonRévéler une caseClic gauchePoser / retirer un drapeau Clic droit

Astuce : Le premier clic ne peut jamais tomber sur une mine ni sur une case voisine d'une mine — les mines sont placées après votre premier clic.


Règles

La grille contient des mines cachées.
Révéler une mine → partie perdue (toutes les mines s'affichent).
Révéler toutes les cases sans mine → victoire .
Un chiffre sur une case révélée indique le nombre de mines dans les 8 cases voisines.
Une case vide (0) propage automatiquement la révélation à ses voisines.
Posez des drapeaux sur les cases que vous suspectez de contenir une mine.


Niveaux de difficulté
En bas du fichier minesweeper.py, modifiez la ligne de création du jeu :
python# Débutant
game = Minesweeper(rows=9,  cols=9,  num_mines=10)

# Intermédiaire
game = Minesweeper(rows=16, cols=16, num_mines=40)

# Expert (défaut)
game = Minesweeper(rows=16, cols=30, num_mines=99)

# Personnalisé
game = Minesweeper(rows=20, cols=40, num_mines=120)

Structure du code
minesweeper.py
│
├── Constantes globales
│   ├── ROWS, COLS         — dimensions de la grille
│   ├── NUM_MINES          — nombre de mines
│   ├── NUMBER_COLORS      — couleurs des chiffres 1–8 (standard Démineur)
│   └── COLOR_*            — palette de couleurs de l'interface
│
└── class Minesweeper
    │
    ├── __init__()           — initialise les tableaux NumPy et lance l'UI
    │
    ├── Initialisation de la grille
    │   ├── _place_mines()   — place les mines après le 1er clic (zone sûre garantie)
    │   └── _count_neighbors() — calcule le chiffre de chaque case
    │
    ├── Interface Matplotlib
    │   ├── _build_ui()      — crée la figure, les textes de statut, connecte les événements
    │   ├── _draw_grid()     — redessine toute la grille
    │   └── _draw_cell()     — dessine une case individuelle (fond, emoji, chiffre)
    │
    ├── Gestion des événements
    │   └── _on_click()      — dispatcher : clic gauche → _reveal(), clic droit → drapeau
    │
    └── Logique de jeu
        ├── _reveal()        — révèle une case et propage récursivement si case vide
        ├── _game_over()     — dévoile toutes les mines, bloque les interactions
        ├── _check_victory() — détecte la victoire (cases non révélées == mines)
        └── _update_status() — met à jour le compteur de mines/drapeaux

Points techniques notables
Tableaux NumPy
Trois tableaux booléens (rows × cols) stockent l'état de chaque case :

self.mines — position des mines
self.revealed — cases révélées
self.flagged — cases avec drapeau

Un tableau entier self.numbers stocke le chiffre de chaque case (0–8).
Rendu avec Matplotlib

Chaque case est un FancyBboxPatch (rectangle arrondi).
Les emojis () sont affichés via ax.text().
La méthode _draw_grid() efface et redessine la grille complète à chaque interaction — approche simple et fiable pour une grille de cette taille.

Coordonnées
Matplotlib place l'origine en bas à gauche, alors que la grille est indexée ligne 0 = haut. La conversion est y_matplotlib = rows - 1 - row.
Premier clic garanti sûr
Les mines ne sont placées qu'après le premier clic. La case cliquée et ses 8 voisines sont exclues des positions possibles pour les mines.
Propagation en cascade (flood fill)
Quand une case révélée a 0 mine voisine, _reveal() s'appelle récursivement sur ses 8 voisines. Grâce à la vérification if self.revealed[nr, nc], la récursion se termine naturellement.

Pour rejouer
Fermez la fenêtre et relancez le script :
bashpython minesweeper.py

Développé avec Python 3, NumPy et Matplotlib.
