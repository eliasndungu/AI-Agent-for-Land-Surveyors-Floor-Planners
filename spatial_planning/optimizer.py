"""
Layout optimization engine using rule-based and greedy algorithms.
"""

from typing import List, Optional
from .models import Room, Space, Layout, Position
from .constraints import ConstraintValidator


class LayoutOptimizer:
    """Generates optimized layouts for spatial planning."""
    
    def __init__(self, space: Space):
        self.space = space
        self.validator = ConstraintValidator(space)
    
    def generate_layout(self) -> Layout:
        """
        Generate an optimized layout using a greedy placement algorithm.
        Rooms are placed by priority, using a grid-based approach.
        """
        # Sort rooms by priority (higher priority first)
        sorted_rooms = sorted(self.space.rooms, key=lambda r: r.priority, reverse=True)
        
        placed_rooms = []
        
        for room in sorted_rooms:
            position = self._find_best_position(room, placed_rooms)
            if position:
                # Create a new room instance with the assigned position
                placed_room = Room(
                    id=room.id,
                    name=room.name,
                    dimensions=room.dimensions,
                    room_type=room.room_type,
                    priority=room.priority,
                    position=position
                )
                placed_rooms.append(placed_room)
        
        # Validate the layout
        violations = self.validator.validate_layout(placed_rooms)
        
        # Calculate score
        score = self._calculate_score(placed_rooms, violations)
        
        # Create metadata
        metadata = {
            "total_rooms": len(self.space.rooms),
            "placed_rooms": len(placed_rooms),
            "placement_rate": len(placed_rooms) / len(self.space.rooms) if self.space.rooms else 0,
            "algorithm": "greedy_priority"
        }
        
        return Layout(
            space=self.space,
            placed_rooms=placed_rooms,
            score=score,
            violations=violations,
            metadata=metadata
        )
    
    def _find_best_position(self, room: Room, placed_rooms: List[Room]) -> Optional[Position]:
        """
        Find the best position for a room using a grid search.
        Returns None if no valid position is found.
        """
        # Grid resolution for position search
        grid_step = 0.5  # meters
        
        best_position = None
        best_score = -float('inf')
        
        # Try positions from top-left, moving right then down
        y = 0.0
        while y + room.dimensions.height <= self.space.dimensions.height:
            x = 0.0
            while x + room.dimensions.width <= self.space.dimensions.width:
                position = Position(x=x, y=y)
                
                # Create temporary room with this position
                temp_room = Room(
                    id=room.id,
                    name=room.name,
                    dimensions=room.dimensions,
                    room_type=room.room_type,
                    priority=room.priority,
                    position=position
                )
                
                # Check if this position is valid (no overlaps)
                if not self._has_overlap(temp_room, placed_rooms):
                    # Calculate position score (prefer top-left positions)
                    pos_score = self._score_position(position)
                    
                    if pos_score > best_score:
                        best_score = pos_score
                        best_position = position
                
                x += grid_step
            y += grid_step
        
        return best_position
    
    def _has_overlap(self, room: Room, placed_rooms: List[Room]) -> bool:
        """Check if a room overlaps with any placed rooms."""
        if not room.position:
            return False
        
        for placed in placed_rooms:
            if not placed.position:
                continue
            
            r1_x1 = room.position.x
            r1_y1 = room.position.y
            r1_x2 = r1_x1 + room.dimensions.width
            r1_y2 = r1_y1 + room.dimensions.height
            
            r2_x1 = placed.position.x
            r2_y1 = placed.position.y
            r2_x2 = r2_x1 + placed.dimensions.width
            r2_y2 = r2_y1 + placed.dimensions.height
            
            # Check if rectangles overlap
            if not (r1_x2 <= r2_x1 or r2_x2 <= r1_x1 or 
                   r1_y2 <= r2_y1 or r2_y2 <= r1_y1):
                return True
        
        return False
    
    def _score_position(self, position: Position) -> float:
        """
        Score a position. Prefer positions closer to origin (top-left).
        """
        # Simple scoring: negative distance from origin
        # This encourages compact layouts starting from top-left
        return -(position.x + position.y)
    
    def _calculate_score(self, placed_rooms: List[Room], violations: List[str]) -> float:
        """
        Calculate overall layout score.
        Higher is better.
        """
        score = 0.0
        
        # Reward for placing all rooms
        placement_ratio = len(placed_rooms) / len(self.space.rooms) if self.space.rooms else 0
        score += placement_ratio * 100
        
        # Penalty for violations
        score -= len(violations) * 10
        
        # Bonus for good space utilization (60-80% is ideal)
        utilization = sum(r.area for r in placed_rooms) / self.space.area if self.space.area > 0 else 0
        if 0.6 <= utilization <= 0.8:
            score += 20
        elif utilization > 0.8:
            score += 10  # Slight bonus but not ideal (too cramped)
        
        # Bonus for compact layout (rooms closer to origin)
        if placed_rooms:
            avg_distance = sum(
                (r.position.x + r.position.y) for r in placed_rooms if r.position
            ) / len(placed_rooms)
            # Normalize and invert (closer to origin is better)
            max_distance = self.space.dimensions.width + self.space.dimensions.height
            compactness = 1 - (avg_distance / max_distance)
            score += compactness * 10
        
        return score
