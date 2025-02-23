import tkinter as tk
from tkinter import ttk, messagebox
import math
from modules.calculs import ParametresTube, ParametresCintrage

class Interface:
    def __init__(self, master, calculateur):
        self.master = master
        self.calculateur = calculateur
        
        # Configuration du style
        self.setup_style()
        
        # Frame principale avec bordure et padding
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(expand=True, fill='both')
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
        self.status_bar = ttk.Label(self.master, textvariable=self.status_var, 
                                  style='Status.TLabel', relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
        
        # Zone de dessin avec grille de fond
        self.canvas_frame = ttk.LabelFrame(self.main_frame, text="Visualisation", padding="5")
        self.canvas_frame.pack(side='left', expand=True, fill='both', padx=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=1024, height=600)
        self.canvas.pack(expand=True, fill='both', padx=5, pady=5)
        self.dessiner_grille()
        
        # Panneau de contrôle
        self.setup_control_panel()
        
    def setup_style(self):
        style = ttk.Style()
        
        # Style général
        style.configure('TLabelframe', padding=5)
        style.configure('Info.TLabel', foreground='#666666', font=('Arial', 9, 'italic'))
        
        # Style des boutons
        style.configure('Action.TButton', 
                       padding=10,
                       font=('Arial', 10, 'bold'))
        style.configure('Secondary.TButton', 
                       padding=8)
                       
        # Style pour la barre de statut
        style.configure('Status.TLabel',
                       padding=5,
                       background='#f0f0f0',
                       font=('Arial', 9))
        
    def dessiner_grille(self):
        # Dessiner une grille légère pour mieux visualiser les dimensions
        for i in range(0, 801, 50):
            # Lignes verticales
            self.canvas.create_line(i, 0, i, 600, fill='#d0d0d0')
            # Lignes horizontales
            self.canvas.create_line(0, i, 800, i, fill='#d0d0d0')
        
    def setup_control_panel(self):
        # Frame de contrôle avec style
        control_frame = ttk.LabelFrame(self.main_frame, text="Paramètres", padding="10")
        control_frame.pack(side='right', fill='y', padx=5)
        
        # Liste des cintrages
        cintrages_frame = ttk.LabelFrame(control_frame, text="Liste des cintrages", padding="5")
        cintrages_frame.pack(fill='x', pady=5)
        
        # Treeview pour afficher les cintrages
        self.cintrages_tree = ttk.Treeview(cintrages_frame, columns=('Position', 'Angle', 'Rayon', 'A'), 
                                         show='headings', height=5)
        self.cintrages_tree.heading('Position', text='Position (mm)')
        self.cintrages_tree.heading('Angle', text='Angle (°)')
        self.cintrages_tree.heading('Rayon', text='Rayon (mm)')
        self.cintrages_tree.heading('A', text='A (mm)')
        self.cintrages_tree.pack(fill='x', pady=2)
        
        # Boutons pour gérer les cintrages
        btn_frame = ttk.Frame(cintrages_frame)
        btn_frame.pack(fill='x', pady=2)
        ttk.Button(btn_frame, text="Ajouter", command=self.ajouter_cintrage).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Supprimer", command=self.supprimer_cintrage).pack(side='left', padx=2)
        
        # Section Paramètres du tube
        tube_frame = ttk.LabelFrame(control_frame, text="Tube", padding="5")
        tube_frame.pack(fill='x', pady=5)
        
        # Création d'une grille pour aligner les éléments
        for i, (label, var, default, tooltip) in enumerate([
            ("Diamètre (mm)", "diametre_var", "20", "Diamètre extérieur du tube"),
            ("Épaisseur (mm)", "epaisseur_var", "1.5", "Épaisseur de la paroi du tube"),
            ("Longueur (mm)", "longueur_var", "1000", "Longueur totale du tube avant cintrage")
        ]):
            ttk.Label(tube_frame, text=label).grid(row=i, column=0, sticky='w', pady=2)
            setattr(self, var, tk.StringVar(value=default))
            entry = ttk.Entry(tube_frame, textvariable=getattr(self, var), width=10)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.create_tooltip(entry, tooltip)
            
        # Section Paramètres de cintrage
        cintrage_frame = ttk.LabelFrame(control_frame, text="Cintrage", padding="5")
        cintrage_frame.pack(fill='x', pady=5)
        
        for i, (label, var, default, tooltip) in enumerate([
            ("Position (mm)", "position_var", "200", "Distance depuis le début du tube jusqu'au point de cintrage"),
            ("Angle (degrés)", "angle_var", "90", "Angle de cintrage désiré"),
            ("Rayon (mm)", "rayon_var", "50", "Rayon de cintrage intérieur")
        ]):
            ttk.Label(cintrage_frame, text=label).grid(row=i, column=0, sticky='w', pady=2)
            setattr(self, var, tk.StringVar(value=default))
            entry = ttk.Entry(cintrage_frame, textvariable=getattr(self, var), width=10)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.create_tooltip(entry, tooltip)
        
        # Frame pour les boutons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', pady=10)
        
        # Boutons avec icônes (symboles unicode)
        ttk.Button(button_frame, text="▶ Simuler", command=self.simuler_cintrage, style='Action.TButton').pack(fill='x', pady=2)
        ttk.Button(button_frame, text="↺ Réinitialiser", command=self.reinitialiser).pack(fill='x', pady=2)
        
        # Section informations
        info_frame = ttk.LabelFrame(control_frame, text="Informations", padding="5")
        info_frame.pack(fill='x', pady=5)
        
        # Label pour les informations générales
        self.info_label = ttk.Label(info_frame, 
                                  text="Les dimensions sont en millimètres.\nLe retour élastique est automatiquement compensé.",
                                  style='Info.TLabel', wraplength=200)
        self.info_label.pack(pady=(0, 5))
        
        # Label pour les informations de cintrage
        self.cintrages_info = ttk.Label(info_frame, text="", style='Info.TLabel', wraplength=200)
        self.cintrages_info.pack()
                 
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief='solid', padding=2)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)
        
    def ajouter_cintrage(self):
        try:
            params_cintrage = ParametresCintrage(
                angle=float(self.angle_var.get()),
                rayon=float(self.rayon_var.get()),
                position=float(self.position_var.get())
            )
            
            self.calculateur.multi_cintrage.ajouter_cintrage(params_cintrage)
            self.mettre_a_jour_liste_cintrages()
            
        except ValueError as e:
            tk.messagebox.showerror("Erreur", str(e))
            
    def supprimer_cintrage(self):
        selection = self.cintrages_tree.selection()
        if selection:
            index = self.cintrages_tree.index(selection[0])
            self.calculateur.multi_cintrage.supprimer_cintrage(index)
            self.mettre_a_jour_liste_cintrages()
            
    def mettre_a_jour_liste_cintrages(self):
        # Effacer la liste actuelle
        for item in self.cintrages_tree.get_children():
            self.cintrages_tree.delete(item)
            
        # Ajouter les cintrages
        for cintrage in self.calculateur.multi_cintrage.cintrages:
            if abs(cintrage.angle - 90) < 0.1:
                valeur_a = f"{self.calculateur.calculer_valeur_A(cintrage.rayon, cintrage.angle):.1f}"
            else:
                valeur_a = "-"
            self.cintrages_tree.insert('', 'end', values=(
                f"{cintrage.position:.1f}",
                f"{cintrage.angle:.1f}",
                f"{cintrage.rayon:.1f}",
                valeur_a
            ))
            
    def simuler_cintrage(self):
        try:
            self.status_var.set("Calcul en cours...")
            self.master.update()
            
            # Récupération des paramètres du tube
            params_tube = ParametresTube(
                diametre=float(self.diametre_var.get()),
                epaisseur=float(self.epaisseur_var.get()),
                longueur=float(self.longueur_var.get())
            )
            
            # Calcul des points du tube (mode multi-cintrage)
            points = self.calculateur.calculer_points_tube(params_tube)
            
            # Dessin du tube
            self.reinitialiser(False)  # False pour ne pas effacer la liste des cintrages
            self.dessiner_tube(points)
            
            # Préparation des informations de cintrage
            info = "Cintrages:\n"
            
            # Informations pour chaque cintrage
            for i, cintrage in enumerate(self.calculateur.multi_cintrage.cintrages):
                angle_reel = self.calculateur.calculer_retour_elastique(cintrage.angle)
                valeur_a = self.calculateur.calculer_valeur_A(cintrage.rayon, cintrage.angle)
                info += f"#{i+1}: pos={cintrage.position:.0f}, "
                info += f"angle={angle_reel:.1f}°"
                if abs(cintrage.angle - 90) < 0.1:
                    info += f", A={valeur_a:.1f}mm"
                info += "\n"
                
            # Ajout de la longueur développée totale
            longueur_dev = self.calculateur.calculer_longueur_developpee(params_tube)
            info += f"\nLongueur développée:\n{longueur_dev:.1f} mm"
            
            # Mise à jour du label des informations de cintrage
            self.cintrages_info.configure(text=info)
            
            self.status_var.set("Simulation terminée")
            
        except ValueError as e:
            self.status_var.set("Erreur: valeurs invalides")
            tk.messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")
        
    def reinitialiser(self, tout=True):
        self.canvas.delete("all")
        if tout:
            self.calculateur.multi_cintrage.cintrages.clear()
            self.mettre_a_jour_liste_cintrages()
        else:
            self.dessiner_grille()
        
    def dessiner_tube(self, points):
        if not points:
            return
            
        self.dessiner_grille()
            
        # Facteur d'échelle et décalage pour centrer le dessin
        x_min = min(p[0] for p in points)
        x_max = max(p[0] for p in points)
        y_min = min(p[1] for p in points)
        y_max = max(p[1] for p in points)
        
        largeur_dessin = x_max - x_min
        hauteur_dessin = y_max - y_min
        
        # Calcul de l'échelle pour utiliser 90% de l'espace disponible
        echelle_x = (self.canvas.winfo_width() * 0.9) / largeur_dessin if largeur_dessin > 0 else 1
        echelle_y = (self.canvas.winfo_height() * 0.9) / hauteur_dessin if hauteur_dessin > 0 else 1
        echelle = min(echelle_x, echelle_y)
        
        # Décalage pour centrer
        dx = (self.canvas.winfo_width() - largeur_dessin * echelle) / 2 - x_min * echelle
        dy = (self.canvas.winfo_height() - hauteur_dessin * echelle) / 2 - y_min * echelle
        
        # Conversion des points en coordonnées canvas
        points_canvas = [(x * echelle + dx, y * echelle + dy) for x, y in points]
        
        # Dessin du tube avec effet 3D amélioré
        
        # Ombre portée
        for i in range(len(points_canvas) - 1):
            x1, y1 = points_canvas[i]
            x2, y2 = points_canvas[i + 1]
            self.canvas.create_line(x1+4, y1+4, x2+4, y2+4, 
                                  width=10, 
                                  fill="#90CAF9",  # Bleu plus prononcé pour l'ombre
                                  capstyle="round", 
                                  joinstyle="round")
        
        # Tube principal - contour
        for i in range(len(points_canvas) - 1):
            x1, y1 = points_canvas[i]
            x2, y2 = points_canvas[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, 
                                  width=10, 
                                  fill="#0D47A1",  # Bleu plus foncé pour plus de contraste
                                  capstyle="round", 
                                  joinstyle="round")
            
        # Tube principal - effet de brillance
        for i in range(len(points_canvas) - 1):
            x1, y1 = points_canvas[i]
            x2, y2 = points_canvas[i + 1]
            self.canvas.create_line(x1-1, y1-1, x2-1, y2-1, 
                                  width=6, 
                                  fill="#42A5F5",  # Bleu brillant plus vif
                                  capstyle="round", 
                                  joinstyle="round")
            
        # Points de cintrage avec effet métallique
        for i, cintrage in enumerate(self.calculateur.multi_cintrage.cintrages):
            for j in range(len(points_canvas) - 1):
                x1, y1 = points_canvas[j]
                if abs(x1 - cintrage.position * echelle - dx) < 1:
                    # Ombre du point
                    self.canvas.create_oval(x1-7, y1-7, x1+7, y1+7, 
                                         fill="#F57C00",  # Orange plus foncé
                                         outline="#E65100", 
                                         width=2)
                    # Effet de brillance
                    self.canvas.create_oval(x1-5, y1-5, x1+5, y1+5, 
                                         fill="#FFB74D",  # Orange plus chaud
                                         outline="")
                    # Point central
                    self.canvas.create_oval(x1-2, y1-2, x1+2, y1+2, 
                                         fill="#FFFFFF",  # Blanc
                                         outline="")
                    break
        
        # Affichage des dimensions
        self.afficher_dimensions(points_canvas, points)
        
        
    def afficher_cote_a(self, point, valeur_a):
        """Affiche la cote A sur le dessin"""
        x, y = point
        
        # Style de la ligne de cote
        style_ligne = {"fill": "#FF5722", "width": 2, "dash": (6, 2)}
        style_texte = {"font": ("Arial", 9, "bold"), "fill": "#FF5722"}
        
        # Dessin de la ligne de cote
        fleche_longueur = 40
        self.canvas.create_line(x, y, x + fleche_longueur, y, **style_ligne)
        
        # Flèches aux extrémités
        taille_fleche = 8
        self.canvas.create_line(x, y, x + taille_fleche, y - taille_fleche/2, **style_ligne)
        self.canvas.create_line(x, y, x + taille_fleche, y + taille_fleche/2, **style_ligne)
        self.canvas.create_line(x + fleche_longueur, y, x + fleche_longueur - taille_fleche, y - taille_fleche/2, **style_ligne)
        self.canvas.create_line(x + fleche_longueur, y, x + fleche_longueur - taille_fleche, y + taille_fleche/2, **style_ligne)
        
        # Texte de la cote
        self.canvas.create_text(x + fleche_longueur/2, y - 15,
                              text=f"A = {valeur_a:.1f} mm",
                              anchor="s",
                              **style_texte)
    
    def afficher_dimensions(self, points_canvas, points_reels):
        """Affiche les dimensions principales du tube"""
        if len(points_canvas) < 2:
            return
            
        # Style du texte
        style_texte = {"font": ("Arial", 8), "fill": "#666666"}
        
        # Dimensions réelles
        longueur_reelle = math.sqrt((points_reels[-1][0] - points_reels[0][0])**2 + 
                                  (points_reels[-1][1] - points_reels[0][1])**2)
        
        # Point de départ
        x0, y0 = points_canvas[0]
        self.canvas.create_text(x0-10, y0-10, 
                              text="Début", 
                              anchor="se",
                              **style_texte)
        
        # Point final
        xn, yn = points_canvas[-1]
        self.canvas.create_text(xn+10, yn+10, 
                              text=f"Fin\n{longueur_reelle:.1f}mm", 
                              anchor="nw",
                              **style_texte)
