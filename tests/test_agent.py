"""
Unit tests for the spatial planning agent.
"""

import json
import pytest
from spatial_planning import SpatialPlanningAgent
from spatial_planning.models import Dimensions


def test_agent_creation():
    """Test creating an agent."""
    agent = SpatialPlanningAgent()
    assert agent is not None
    assert agent.current_space is None
    assert agent.current_layout is None


def test_create_space():
    """Test creating a space through the agent."""
    agent = SpatialPlanningAgent()
    
    space = agent.create_space(
        width=10,
        height=8,
        rooms=[
            {"name": "Room 1", "width": 5, "height": 4}
        ]
    )
    
    assert space.dimensions.width == 10
    assert space.dimensions.height == 8
    assert len(space.rooms) == 1
    assert space.rooms[0].name == "Room 1"
    assert agent.current_space == space


def test_generate_layout_basic():
    """Test generating a basic layout."""
    agent = SpatialPlanningAgent()
    
    space = agent.create_space(
        width=10,
        height=8,
        rooms=[
            {"name": "Room 1", "width": 5, "height": 4, "priority": 10},
            {"name": "Room 2", "width": 3, "height": 3, "priority": 5}
        ]
    )
    
    layout = agent.generate_layout(space)
    
    assert layout is not None
    assert len(layout.placed_rooms) == 2
    assert layout.placed_rooms[0].position is not None
    assert layout.score > 0


def test_generate_layout_uses_current_space():
    """Test that generate_layout can use current_space."""
    agent = SpatialPlanningAgent()
    
    agent.create_space(
        width=10,
        height=8,
        rooms=[{"name": "Room 1", "width": 5, "height": 4}]
    )
    
    # Don't pass space, should use current_space
    layout = agent.generate_layout()
    
    assert layout is not None
    assert len(layout.placed_rooms) == 1


def test_generate_layout_no_space_raises():
    """Test that generating layout without space raises error."""
    agent = SpatialPlanningAgent()
    
    with pytest.raises(ValueError, match="No space provided"):
        agent.generate_layout()


def test_generate_from_dict():
    """Test generating layout from dictionary."""
    agent = SpatialPlanningAgent()
    
    data = {
        "dimensions": {"width": 10, "height": 8},
        "rooms": [
            {"name": "Living Room", "width": 5, "height": 4, "priority": 9},
            {"name": "Bedroom", "width": 4, "height": 3, "priority": 7}
        ]
    }
    
    layout = agent.generate_from_dict(data)
    
    assert layout is not None
    assert len(layout.placed_rooms) == 2


def test_generate_from_json():
    """Test generating layout from JSON string."""
    agent = SpatialPlanningAgent()
    
    json_str = json.dumps({
        "dimensions": {"width": 10, "height": 8},
        "rooms": [
            {"name": "Room 1", "width": 5, "height": 4}
        ]
    })
    
    layout = agent.generate_from_json(json_str)
    
    assert layout is not None
    assert len(layout.placed_rooms) == 1


def test_export_layout_json():
    """Test exporting layout to JSON."""
    agent = SpatialPlanningAgent()
    
    space = agent.create_space(
        width=10,
        height=8,
        rooms=[{"name": "Room 1", "width": 5, "height": 4}]
    )
    
    layout = agent.generate_layout(space)
    json_output = agent.export_layout_json(layout)
    
    # Should be valid JSON
    data = json.loads(json_output)
    
    assert "dimensions" in data
    assert "rooms" in data
    assert "metrics" in data
    assert data["dimensions"]["width"] == 10


def test_get_layout_summary():
    """Test getting layout summary."""
    agent = SpatialPlanningAgent()
    
    space = agent.create_space(
        width=10,
        height=8,
        rooms=[
            {"name": "Living Room", "width": 5, "height": 4},
            {"name": "Bedroom", "width": 4, "height": 3}
        ]
    )
    
    layout = agent.generate_layout(space)
    summary = agent.get_layout_summary(layout)
    
    assert "SPATIAL LAYOUT SUMMARY" in summary
    assert "Living Room" in summary
    assert "Bedroom" in summary
    assert "10.0m × 8.0m" in summary


def test_layout_with_constraints():
    """Test generating layout with constraints."""
    agent = SpatialPlanningAgent()
    
    space = agent.create_space(
        width=10,
        height=10,
        rooms=[
            {"id": "r1", "name": "Room 1", "width": 3, "height": 3},
            {"id": "r2", "name": "Room 2", "width": 3, "height": 3}
        ],
        constraints=[
            {
                "type": "adjacency",
                "params": {"room1": "r1", "room2": "r2", "max_distance": 10.0}
            }
        ]
    )
    
    layout = agent.generate_layout(space)
    
    # Should place both rooms
    assert len(layout.placed_rooms) == 2
