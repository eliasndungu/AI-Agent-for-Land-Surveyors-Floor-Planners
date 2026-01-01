"""
Data models for spatial planning.
Represents spaces, rooms, constraints, and layouts.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    """2D dimensions for spaces and rooms."""
    width: float = Field(gt=0, description="Width in meters")
    height: float = Field(gt=0, description="Height in meters")
    
    @property
    def area(self) -> float:
        """Calculate area."""
        return self.width * self.height


class Position(BaseModel):
    """2D position coordinates."""
    x: float = Field(ge=0, description="X coordinate")
    y: float = Field(ge=0, description="Y coordinate")


class Room(BaseModel):
    """Represents a room or furniture item to be placed."""
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Room/item name")
    dimensions: Dimensions
    room_type: str = Field(default="general", description="Type of room (bedroom, kitchen, etc.)")
    position: Optional[Position] = Field(default=None, description="Assigned position")
    priority: int = Field(default=5, ge=1, le=10, description="Placement priority (1-10)")
    
    @property
    def area(self) -> float:
        """Get room area."""
        return self.dimensions.area


class Constraint(BaseModel):
    """Represents a constraint for layout planning."""
    type: str = Field(description="Constraint type (min_distance, adjacency, etc.)")
    params: Dict[str, Any] = Field(default_factory=dict, description="Constraint parameters")
    description: Optional[str] = Field(default=None, description="Human-readable description")


class Space(BaseModel):
    """Represents the total available space for planning."""
    dimensions: Dimensions
    rooms: List[Room] = Field(default_factory=list, description="Rooms to place")
    constraints: List[Constraint] = Field(default_factory=list, description="Layout constraints")
    
    @property
    def area(self) -> float:
        """Get total space area."""
        return self.dimensions.area
    
    @property
    def total_room_area(self) -> float:
        """Calculate total area of all rooms."""
        return sum(room.area for room in self.rooms)
    
    @property
    def utilization(self) -> float:
        """Calculate space utilization ratio."""
        return self.total_room_area / self.area if self.area > 0 else 0


class Layout(BaseModel):
    """Represents a generated layout solution."""
    space: Space
    placed_rooms: List[Room] = Field(default_factory=list, description="Rooms with assigned positions")
    score: float = Field(default=0.0, description="Layout quality score")
    violations: List[str] = Field(default_factory=list, description="Constraint violations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @property
    def is_valid(self) -> bool:
        """Check if layout has no violations."""
        return len(self.violations) == 0
    
    def to_json_dict(self) -> Dict[str, Any]:
        """Convert layout to JSON-serializable dictionary."""
        return {
            "dimensions": {
                "width": self.space.dimensions.width,
                "height": self.space.dimensions.height,
                "area": self.space.area
            },
            "rooms": [
                {
                    "id": room.id,
                    "name": room.name,
                    "type": room.room_type,
                    "dimensions": {
                        "width": room.dimensions.width,
                        "height": room.dimensions.height,
                        "area": room.area
                    },
                    "position": {
                        "x": room.position.x,
                        "y": room.position.y
                    } if room.position else None
                }
                for room in self.placed_rooms
            ],
            "metrics": {
                "score": self.score,
                "utilization": self.space.utilization,
                "is_valid": self.is_valid,
                "violations": self.violations
            },
            "metadata": self.metadata
        }
