import tkinter as tk
from tkinter import ttk, messagebox
from modules.interface import Interface
from modules.calculs import CalculateurCintrage, ParametresTube, ParametresCintrage
from modules.export import ExporteurPlans

class ApplicationCintrage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulateur de Cintrage")
        self.root.geometry("1280x1024")
        
        self.calculateur = CalculateurCintrage()
        self.interface = Interface(self.root, self.calculateur)
        self.exporteur = ExporteurPlans()
        
        self.setup_menu()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau projet", command=self.nouveau_projet)
        file_menu.add_command(label="Exporter en DXF", command=self.exporter_dxf)
        file_menu.add_command(label="Exporter en SVG", command=self.exporter_svg)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)

    def nouveau_projet(self):
        self.interface.reinitialiser()
        
    def exporter_dxf(self):
        try:
            params_tube = ParametresTube(
                diametre=float(self.interface.diametre_var.get()),
                epaisseur=float(self.interface.epaisseur_var.get()),
                longueur=float(self.interface.longueur_var.get())
            )
            params_cintrage = ParametresCintrage(
                angle=float(self.interface.angle_var.get()),
                rayon=float(self.interface.rayon_var.get()),
                position=float(self.interface.position_var.get())
            )
            points = self.calculateur.calculer_points_tube(params_tube, params_cintrage)
            self.exporteur.exporter_dxf(points, "tube_cintre.dxf")
            tk.messagebox.showinfo("Succès", "Le fichier DXF a été créé avec succès")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Erreur lors de l'export DXF: {str(e)}")
            
    def exporter_svg(self):
        try:
            params_tube = ParametresTube(
                diametre=float(self.interface.diametre_var.get()),
                epaisseur=float(self.interface.epaisseur_var.get()),
                longueur=float(self.interface.longueur_var.get())
            )
            params_cintrage = ParametresCintrage(
                angle=float(self.interface.angle_var.get()),
                rayon=float(self.interface.rayon_var.get()),
                position=float(self.interface.position_var.get())
            )
            points = self.calculateur.calculer_points_tube(params_tube, params_cintrage)
            self.exporteur.exporter_svg(points, "tube_cintre.svg")
            tk.messagebox.showinfo("Succès", "Le fichier SVG a été créé avec succès")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Erreur lors de l'export SVG: {str(e)}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ApplicationCintrage()
    app.run()
