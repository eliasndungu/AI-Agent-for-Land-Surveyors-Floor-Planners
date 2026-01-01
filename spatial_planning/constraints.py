"""
Constraint validation and checking for spatial layouts.
"""

from typing import List, Tuple
from .models import Room, Space, Constraint, Position


class ConstraintValidator:
    """Validates layout constraints."""
    
    def __init__(self, space: Space):
        self.space = space
    
    def validate_layout(self, rooms: List[Room]) -> List[str]:
        """
        Validate all constraints for a layout.
        Returns list of violation messages.
        """
        violations = []
        
        # Check bounds
        violations.extend(self._check_bounds(rooms))
        
        # Check overlaps
        violations.extend(self._check_overlaps(rooms))
        
        # Check custom constraints
        violations.extend(self._check_custom_constraints(rooms))
        
        return violations
    
    def _check_bounds(self, rooms: List[Room]) -> List[str]:
        """Check if all rooms fit within space boundaries."""
        violations = []
        
        for room in rooms:
            if not room.position:
                continue
                
            max_x = room.position.x + room.dimensions.width
            max_y = room.position.y + room.dimensions.height
            
            if max_x > self.space.dimensions.width:
                violations.append(
                    f"Room '{room.name}' exceeds space width boundary "
                    f"({max_x} > {self.space.dimensions.width})"
                )
            
            if max_y > self.space.dimensions.height:
                violations.append(
                    f"Room '{room.name}' exceeds space height boundary "
                    f"({max_y} > {self.space.dimensions.height})"
                )
        
        return violations
    
    def _check_overlaps(self, rooms: List[Room]) -> List[str]:
        """Check if any rooms overlap."""
        violations = []
        
        for i, room1 in enumerate(rooms):
            if not room1.position:
                continue
                
            for room2 in rooms[i + 1:]:
                if not room2.position:
                    continue
                
                if self._rooms_overlap(room1, room2):
                    violations.append(
                        f"Rooms '{room1.name}' and '{room2.name}' overlap"
                    )
        
        return violations
    
    def _rooms_overlap(self, room1: Room, room2: Room) -> bool:
        """Check if two rooms overlap."""
        if not room1.position or not room2.position:
            return False
        
        r1_x1 = room1.position.x
        r1_y1 = room1.position.y
        r1_x2 = r1_x1 + room1.dimensions.width
        r1_y2 = r1_y1 + room1.dimensions.height
        
        r2_x1 = room2.position.x
        r2_y1 = room2.position.y
        r2_x2 = r2_x1 + room2.dimensions.width
        r2_y2 = r2_y1 + room2.dimensions.height
        
        # Check if rectangles overlap
        return not (r1_x2 <= r2_x1 or r2_x2 <= r1_x1 or 
                   r1_y2 <= r2_y1 or r2_y2 <= r1_y1)
    
    def _check_custom_constraints(self, rooms: List[Room]) -> List[str]:
        """Check custom constraints defined in the space."""
        violations = []
        
        for constraint in self.space.constraints:
            if constraint.type == "min_distance":
                violations.extend(self._check_min_distance(rooms, constraint))
            elif constraint.type == "adjacency":
                violations.extend(self._check_adjacency(rooms, constraint))
        
        return violations
    
    def _check_min_distance(self, rooms: List[Room], constraint: Constraint) -> List[str]:
        """Check minimum distance constraint between rooms."""
        violations = []
        room1_id = constraint.params.get("room1")
        room2_id = constraint.params.get("room2")
        min_dist = constraint.params.get("distance", 0)
        
        room1 = next((r for r in rooms if r.id == room1_id), None)
        room2 = next((r for r in rooms if r.id == room2_id), None)
        
        if room1 and room2 and room1.position and room2.position:
            dist = self._calculate_distance(room1, room2)
            if dist < min_dist:
                violations.append(
                    f"Minimum distance constraint violated between '{room1.name}' "
                    f"and '{room2.name}' ({dist:.2f} < {min_dist})"
                )
        
        return violations
    
    def _check_adjacency(self, rooms: List[Room], constraint: Constraint) -> List[str]:
        """Check adjacency constraint (rooms should be next to each other)."""
        violations = []
        room1_id = constraint.params.get("room1")
        room2_id = constraint.params.get("room2")
        max_dist = constraint.params.get("max_distance", 1.0)
        
        room1 = next((r for r in rooms if r.id == room1_id), None)
        room2 = next((r for r in rooms if r.id == room2_id), None)
        
        if room1 and room2 and room1.position and room2.position:
            dist = self._calculate_distance(room1, room2)
            if dist > max_dist:
                violations.append(
                    f"Adjacency constraint violated between '{room1.name}' "
                    f"and '{room2.name}' ({dist:.2f} > {max_dist})"
                )
        
        return violations
    
    def _calculate_distance(self, room1: Room, room2: Room) -> float:
        """Calculate minimum distance between two rooms."""
        if not room1.position or not room2.position:
            return float('inf')
        
        # Calculate center points
        r1_cx = room1.position.x + room1.dimensions.width / 2
        r1_cy = room1.position.y + room1.dimensions.height / 2
        r2_cx = room2.position.x + room2.dimensions.width / 2
        r2_cy = room2.position.y + room2.dimensions.height / 2
        
        # Euclidean distance between centers
        return ((r1_cx - r2_cx) ** 2 + (r1_cy - r2_cy) ** 2) ** 0.5
