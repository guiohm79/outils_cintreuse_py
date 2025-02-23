import math
from typing import List, Tuple
import xml.etree.ElementTree as ET
from dataclasses import dataclass

@dataclass
class ExportConfig:
    echelle: float = 1.0
    marge: float = 10.0
    couleur_ligne: str = "#000000"
    epaisseur_ligne: float = 1.0

class ExporteurPlans:
    def __init__(self):
        self.config = ExportConfig()
    
    def exporter_svg(self, points: List[Tuple[float, float]], nom_fichier: str):
        """
        Exporte le dessin du tube en format SVG
        """
        # Calcul des dimensions
        x_min = min(p[0] for p in points)
        x_max = max(p[0] for p in points)
        y_min = min(p[1] for p in points)
        y_max = max(p[1] for p in points)
        
        largeur = (x_max - x_min) * self.config.echelle + 2 * self.config.marge
        hauteur = (y_max - y_min) * self.config.echelle + 2 * self.config.marge
        
        # Création du document SVG
        svg = ET.Element('svg')
        svg.set('width', str(largeur))
        svg.set('height', str(hauteur))
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        
        # Création du chemin
        path_data = f"M {self.config.marge},{self.config.marge}"
        for x, y in points:
            x_scaled = x * self.config.echelle + self.config.marge
            y_scaled = y * self.config.echelle + self.config.marge
            path_data += f" L {x_scaled},{y_scaled}"
        
        path = ET.SubElement(svg, 'path')
        path.set('d', path_data)
        path.set('stroke', self.config.couleur_ligne)
        path.set('stroke-width', str(self.config.epaisseur_ligne))
        path.set('fill', 'none')
        
        # Sauvegarde du fichier
        tree = ET.ElementTree(svg)
        tree.write(nom_fichier)
    
    def exporter_dxf(self, points: List[Tuple[float, float]], nom_fichier: str):
        """
        Exporte le dessin du tube en format DXF
        """
        with open(nom_fichier, 'w') as f:
            # En-tête DXF
            f.write("0\nSECTION\n2\nENTITIES\n")
            
            # Écriture des lignes
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Ligne DXF
                f.write("0\nLINE\n")
                f.write("8\n0\n")  # Calque 0
                f.write(f"10\n{x1}\n")  # Point de départ X
                f.write(f"20\n{y1}\n")  # Point de départ Y
                f.write("30\n0\n")      # Point de départ Z
                f.write(f"11\n{x2}\n")  # Point d'arrivée X
                f.write(f"21\n{y2}\n")  # Point d'arrivée Y
                f.write("31\n0\n")      # Point d'arrivée Z
            
            # Fin du fichier DXF
            f.write("0\nENDSEC\n0\nEOF\n")
