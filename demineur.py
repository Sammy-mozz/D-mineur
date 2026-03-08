import matplotlib.pyplot as plt
import random

# Paramètres de base
hauteur, largeur = 16, 30
nb_mines_total = 99
couleurs_chiffres = {1:'blue', 2:'green', 3:'red', 4:'darkblue', 5:'darkred', 6:'teal', 7:'black', 8:'gray'}

class Demineur:
    def __init__(self):
        self.h = hauteur
        self.w = largeur
        
        # Initialisation des grilles avec des boucles simples
        self.champ = []     # 1 si mine, 0 sinon
        self.visible = []   # True si révélé
        self.drapeaux = []  # True si drapeau posé
        self.compte = []    # Nombre de mines autour
        
        for y in range(self.h):
            ligne_mines = []
            ligne_visible = []
            ligne_drapeaux = []
            ligne_compte = []
            
            for x in range(self.w):
                ligne_mines.append(0)
                ligne_visible.append(False)
                ligne_drapeaux.append(False)
                ligne_compte.append(0)
            
            self.champ.append(ligne_mines)
            self.visible.append(ligne_visible)
            self.drapeaux.append(ligne_drapeaux)
            self.compte.append(ligne_compte)
        
        self.perdu = False
        self.gagne = False
        
        # Placement des mines
        mines_posees = 0
        while mines_posees < nb_mines_total:
            ry = random.randint(0, self.h - 1)
            rx = random.randint(0, self.w - 1)
            if self.champ[ry][rx] == 0:
                self.champ[ry][rx] = 1
                mines_posees = mines_posees + 1

        # Calcul des chiffres (voisins)
        for y in range(self.h):
            for x in range(self.w):
                if self.champ[y][x] == 0:
                    somme = 0
                    # On regarde les 8 cases autour
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            v_y = y + dy
                            v_x = x + dx
                            # On vérifie qu'on ne sort pas du plateau
                            if v_y >= 0 and v_y < self.h and v_x >= 0 and v_x < self.w:
                                if self.champ[v_y][v_x] == 1:
                                    somme = somme + 1
                    self.compte[y][x] = somme

        # Lancement de la fenêtre
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event', self.quand_on_clique)
        self.dessiner()
        plt.show()

    def reveler(self, y, x):
        # Sécurités de base
        if y < 0 or y >= self.h or x < 0 or x >= self.w:
            return
        if self.visible[y][x] == True or self.drapeaux[y][x] == True:
            return
            
        self.visible[y][x] = True
        
        # Si c'est une mine
        if self.champ[y][x] == 1:
            self.perdu = True
            return
            
        # Si la case est vide (0 mine autour), on propage
        if self.compte[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveler(y + dy, x + dx)

    def quand_on_clique(self, event):
        if event.inaxes != self.ax or self.perdu or self.gagne:
            return
            
        # Conversion des coordonnées du clic en index de liste
        clic_x = int(event.xdata)
        clic_y = int(event.ydata)
        
        if event.button == 1: # Clic gauche
            self.reveler(clic_y, clic_x)
        elif event.button == 3: # Clic droit
            if self.visible[clic_y][clic_x] == False:
                # Inverse l'état du drapeau
                if self.drapeaux[clic_y][clic_x] == True:
                    self.drapeaux[clic_y][clic_x] = False
                else:
                    self.drapeaux[clic_y][clic_x] = True
        
        # Vérification de la victoire
        total_cache = 0
        for y in range(self.h):
            for x in range(self.w):
                if self.visible[y][x] == False:
                    total_cache = total_cache + 1
        
        if total_cache == nb_mines_total and self.perdu == False:
            self.gagne = True
            
        self.dessiner()

    def dessiner(self):
        self.ax.clear()
        for y in range(self.h):
            for x in range(self.w):
                if self.visible[y][x] == True:
                    if self.champ[y][x] == 1:
                        # Dessin de la mine
                        rect = plt.Rectangle((x, y), 1, 1, color='red')
                        self.ax.add_patch(rect)
                    else:
                        # Dessin de la case vide
                        rect = plt.Rectangle((x, y), 1, 1, color='lightgray')
                        self.ax.add_patch(rect)
                        chiffre = self.compte[y][x]
                        if chiffre > 0:
                            couleur = couleurs_chiffres.get(chiffre, 'black')
                            self.ax.text(x + 0.5, y + 0.5, str(chiffre), color=couleur,
                                         ha='center', va='center')
                else:
                    # Case non cliquée
                    rect = plt.Rectangle((x, y), 1, 1, color='gray', ec='white')
                    self.ax.add_patch(rect)
                    if self.drapeaux[y][x] == True:
                        self.ax.text(x + 0.5, y + 0.5, 'P', color='red', ha='center', va='center')
        
        if self.perdu:
            self.ax.set_title("Perdu !")
        elif self.gagne:
            self.ax.set_title("Gagné !")
        
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        self.fig.canvas.draw()

# On lance le jeu
Demineur()