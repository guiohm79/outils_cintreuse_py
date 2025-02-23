import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ParametresTube:
    diametre: float
    epaisseur: float
    longueur: float
    
@dataclass
class ParametresCintrage:
    angle: float
    rayon: float
    position: float  # Distance depuis le début du tube jusqu'au point de cintrage
    
class CalculMultiCintrage:
    def __init__(self):
        self.cintrages: List[ParametresCintrage] = []
        
    def ajouter_cintrage(self, params: ParametresCintrage):
        # Vérifier que la nouvelle position est valide par rapport aux cintrages existants
        for cintrage in self.cintrages:
            if abs(cintrage.position - params.position) < 10:  # minimum 10mm entre les cintrages
                raise ValueError("Les cintrages sont trop proches")
        self.cintrages.append(params)
        self.cintrages.sort(key=lambda x: x.position)  # Trier par position
        
    def supprimer_cintrage(self, index: int):
        if 0 <= index < len(self.cintrages):
            self.cintrages.pop(index)
    
class CalculateurCintrage:
    def __init__(self):
        self.coefficient_retour_elastique = 0.975  # Facteur de correction pour le retour élastique
        self.multi_cintrage = CalculMultiCintrage()
        
    def calculer_points_tube(self, params_tube: ParametresTube, params_cintrage: ParametresCintrage = None) -> List[Tuple[float, float]]:
        """
        Calcule les points de contrôle pour dessiner le tube cintré
        Retourne une liste de tuples (x, y) représentant les points du tube
        """
        if params_cintrage:
            # Mode cintrage unique
            return self._calculer_points_cintrage_unique(params_tube, params_cintrage)
        else:
            # Mode multi-cintrage
            return self._calculer_points_multi_cintrage(params_tube)
            
    def _calculer_points_cintrage_unique(self, params_tube: ParametresTube, params_cintrage: ParametresCintrage) -> List[Tuple[float, float]]:
        points = []
        x_courant = 0
        y_courant = 0
        angle_courant = 0  # en radians, 0 = horizontal vers la droite
        
        # Point de départ
        points.append((x_courant, y_courant))
        
        # Segment droit avant le cintrage
        if params_cintrage.position > 0:
            x_courant = params_cintrage.position
            points.append((x_courant, y_courant))
        
        # Calcul de l'arc de cintrage
        angle_rad = math.radians(params_cintrage.angle)
        rayon_effectif = params_cintrage.rayon / self.coefficient_retour_elastique
        
        # Points de l'arc
        nb_points = 40  # Plus de points pour un arc plus lisse
        
        # Centre de rotation pour l'arc
        centre_x = x_courant - rayon_effectif * math.sin(angle_courant)
        centre_y = y_courant + rayon_effectif * math.cos(angle_courant)
        
        for j in range(nb_points + 1):
            t = j / nb_points
            angle_arc = angle_rad * t
            
            # Rotation autour du centre
            x = centre_x + rayon_effectif * (math.sin(angle_courant + angle_arc))
            y = centre_y - rayon_effectif * (math.cos(angle_courant + angle_arc))
            points.append((x, y))
        
        # Mise à jour de la position finale
        x_courant = points[-1][0]
        y_courant = points[-1][1]
        angle_courant += angle_rad
        
        # Segment final
        longueur_restante = params_tube.longueur - params_cintrage.position
        if longueur_restante > 0:
            x_final = x_courant + longueur_restante * math.cos(angle_courant)
            y_final = y_courant + longueur_restante * math.sin(angle_courant)
            points.append((x_final, y_final))
            
        return points
        
    def _calculer_points_multi_cintrage(self, params_tube: ParametresTube) -> List[Tuple[float, float]]:
        if not self.multi_cintrage.cintrages:
            # Si pas de cintrage, retourner un tube droit
            return [(0, 0), (params_tube.longueur, 0)]
            
        points = []
        x_courant = 0
        y_courant = 0
        angle_courant = 0  # en radians, 0 = horizontal vers la droite
        
        # Point de départ
        points.append((x_courant, y_courant))
        
        for i, cintrage in enumerate(self.multi_cintrage.cintrages):
            # Segment droit jusqu'au point de cintrage
            distance_segment = cintrage.position - (0 if i == 0 else self.multi_cintrage.cintrages[i-1].position)
            if distance_segment > 0:
                x_courant += distance_segment * math.cos(angle_courant)
                y_courant += distance_segment * math.sin(angle_courant)
                points.append((x_courant, y_courant))
            
            # Calcul de l'arc de cintrage
            angle_rad = math.radians(cintrage.angle)
            rayon_effectif = cintrage.rayon / self.coefficient_retour_elastique
            
            # Points de l'arc
            nb_points = 40  # Plus de points pour un arc plus lisse
            
            # Centre de rotation pour l'arc
            centre_x = x_courant - rayon_effectif * math.sin(angle_courant)
            centre_y = y_courant + rayon_effectif * math.cos(angle_courant)
            
            for j in range(nb_points + 1):
                t = j / nb_points
                angle_arc = angle_rad * t
                
                # Rotation autour du centre
                x = centre_x + rayon_effectif * (math.sin(angle_courant + angle_arc))
                y = centre_y - rayon_effectif * (math.cos(angle_courant + angle_arc))
                points.append((x, y))
            
            # Mise à jour de la position et de l'angle
            x_courant = points[-1][0]
            y_courant = points[-1][1]
            angle_courant += angle_rad
        
        # Segment final
        longueur_restante = params_tube.longueur - (self.multi_cintrage.cintrages[-1].position if self.multi_cintrage.cintrages else 0)
        if longueur_restante > 0:
            x_final = x_courant + longueur_restante * math.cos(angle_courant)
            y_final = y_courant + longueur_restante * math.sin(angle_courant)
            points.append((x_final, y_final))
            
        return points
        
    def calculer_longueur_developpee(self, params_tube: ParametresTube, params_cintrage: ParametresCintrage = None) -> float:
        """
        Calcule la longueur totale développée nécessaire pour le tube
        """
        if params_cintrage:
            # Mode cintrage unique
            angle_rad = math.radians(params_cintrage.angle)
            longueur_arc = angle_rad * params_cintrage.rayon
            return params_tube.longueur + (longueur_arc - 2 * params_cintrage.rayon * math.sin(angle_rad/2))
        else:
            # Mode multi-cintrage
            longueur_totale = params_tube.longueur
            for cintrage in self.multi_cintrage.cintrages:
                angle_rad = math.radians(cintrage.angle)
                longueur_arc = angle_rad * cintrage.rayon
                longueur_totale += (longueur_arc - 2 * cintrage.rayon * math.sin(angle_rad/2))
            return longueur_totale
        
    def calculer_retour_elastique(self, angle_desire: float) -> float:
        """
        Calcule l'angle de cintrage nécessaire pour compenser le retour élastique
        """
        return angle_desire / self.coefficient_retour_elastique
        
    def calculer_valeur_A(self, rayon: float, angle: float) -> float:
        """
        Calcule la valeur A à retrancher pour obtenir la dimension désirée.
        Cette valeur est théoriquement égale à 0,215 x R pour un angle de 90°.
        
        Args:
            rayon: Le rayon de cintrage
            angle: L'angle de cintrage en degrés
            
        Returns:
            La valeur A à retrancher
        """
        if abs(angle - 90) < 0.1:  # On vérifie si l'angle est proche de 90°
            return 0.215 * rayon
        return 0  # Pour les autres angles, à implémenter selon les besoins
