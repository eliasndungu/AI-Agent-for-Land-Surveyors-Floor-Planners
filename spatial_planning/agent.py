"""
Main AI agent for spatial planning.
Provides a high-level interface for generating layout suggestions.
"""

import json
from typing import Dict, Any, List, Optional
from .models import Space, Room, Dimensions, Constraint, Layout
from .optimizer import LayoutOptimizer


class SpatialPlanningAgent:
    """
    AI Agent for generating optimized spatial layouts.
    
    This agent takes land or floor dimensions and constraints,
    and generates optimized 2D layout suggestions.
    """
    
    def __init__(self):
        """Initialize the spatial planning agent."""
        self.current_space: Optional[Space] = None
        self.current_layout: Optional[Layout] = None
    
    def create_space(
        self,
        width: float,
        height: float,
        rooms: Optional[List[Dict[str, Any]]] = None,
        constraints: Optional[List[Dict[str, Any]]] = None
    ) -> Space:
        """
        Create a space definition from dimensions, rooms, and constraints.
        
        Args:
            width: Width of the space in meters
            height: Height of the space in meters
            rooms: List of room definitions (dicts with id, name, width, height, etc.)
            constraints: List of constraint definitions
        
        Returns:
            Space object
        """
        dimensions = Dimensions(width=width, height=height)
        
        # Parse rooms
        room_objects = []
        if rooms:
            for room_data in rooms:
                room = Room(
                    id=room_data.get("id", f"room_{len(room_objects)}"),
                    name=room_data["name"],
                    dimensions=Dimensions(
                        width=room_data["width"],
                        height=room_data["height"]
                    ),
                    room_type=room_data.get("type", "general"),
                    priority=room_data.get("priority", 5)
                )
                room_objects.append(room)
        
        # Parse constraints
        constraint_objects = []
        if constraints:
            for constraint_data in constraints:
                constraint = Constraint(
                    type=constraint_data["type"],
                    params=constraint_data.get("params", {}),
                    description=constraint_data.get("description")
                )
                constraint_objects.append(constraint)
        
        self.current_space = Space(
            dimensions=dimensions,
            rooms=room_objects,
            constraints=constraint_objects
        )
        
        return self.current_space
    
    def generate_layout(self, space: Optional[Space] = None) -> Layout:
        """
        Generate an optimized layout for the given space.
        
        Args:
            space: Space object (uses current_space if not provided)
        
        Returns:
            Layout object with positioned rooms
        """
        if space is None:
            space = self.current_space
        
        if space is None:
            raise ValueError("No space provided. Call create_space() first or pass a Space object.")
        
        optimizer = LayoutOptimizer(space)
        layout = optimizer.generate_layout()
        
        self.current_layout = layout
        return layout
    
    def generate_from_dict(self, data: Dict[str, Any]) -> Layout:
        """
        Generate a layout from a dictionary specification.
        
        Args:
            data: Dictionary with 'dimensions', 'rooms', and optionally 'constraints'
        
        Returns:
            Layout object
        """
        dimensions = data["dimensions"]
        space = self.create_space(
            width=dimensions["width"],
            height=dimensions["height"],
            rooms=data.get("rooms", []),
            constraints=data.get("constraints", [])
        )
        
        return self.generate_layout(space)
    
    def generate_from_json(self, json_str: str) -> Layout:
        """
        Generate a layout from a JSON string.
        
        Args:
            json_str: JSON string with space specification
        
        Returns:
            Layout object
        """
        data = json.loads(json_str)
        return self.generate_from_dict(data)
    
    def export_layout_json(self, layout: Optional[Layout] = None, pretty: bool = True) -> str:
        """
        Export a layout to JSON string.
        
        Args:
            layout: Layout to export (uses current_layout if not provided)
            pretty: Whether to format JSON with indentation
        
        Returns:
            JSON string representation of the layout
        """
        if layout is None:
            layout = self.current_layout
        
        if layout is None:
            raise ValueError("No layout available. Generate a layout first.")
        
        data = layout.to_json_dict()
        
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)
    
    def get_layout_summary(self, layout: Optional[Layout] = None) -> str:
        """
        Get a human-readable summary of the layout.
        
        Args:
            layout: Layout to summarize (uses current_layout if not provided)
        
        Returns:
            Summary string
        """
        if layout is None:
            layout = self.current_layout
        
        if layout is None:
            raise ValueError("No layout available. Generate a layout first.")
        
        summary_lines = [
            "=" * 60,
            "SPATIAL LAYOUT SUMMARY",
            "=" * 60,
            f"Space: {layout.space.dimensions.width}m × {layout.space.dimensions.height}m "
            f"({layout.space.area:.2f} m²)",
            f"Score: {layout.score:.2f}",
            f"Valid: {'Yes' if layout.is_valid else 'No'}",
            f"Utilization: {layout.space.utilization * 100:.1f}%",
            "",
            f"Rooms Placed: {len(layout.placed_rooms)}/{len(layout.space.rooms)}",
            "-" * 60
        ]
        
        for room in layout.placed_rooms:
            pos_str = f"at ({room.position.x:.1f}, {room.position.y:.1f})" if room.position else "unplaced"
            summary_lines.append(
                f"  {room.name:20s} [{room.dimensions.width}m × {room.dimensions.height}m] {pos_str}"
            )
        
        if layout.violations:
            summary_lines.extend([
                "",
                "Constraint Violations:",
                "-" * 60
            ])
            for violation in layout.violations:
                summary_lines.append(f"  ⚠ {violation}")
        
        summary_lines.append("=" * 60)
        
        return "\n".join(summary_lines)
