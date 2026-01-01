"""
Unit tests for spatial planning models.
"""

import pytest
from pydantic import ValidationError
from spatial_planning.models import Dimensions, Position, Room, Constraint, Space, Layout


def test_dimensions_creation():
    """Test creating dimensions."""
    dims = Dimensions(width=10, height=8)
    assert dims.width == 10
    assert dims.height == 8
    assert dims.area == 80


def test_dimensions_invalid():
    """Test that invalid dimensions raise errors."""
    with pytest.raises(ValidationError):
        Dimensions(width=-5, height=8)
    with pytest.raises(ValidationError):
        Dimensions(width=5, height=0)


def test_position_creation():
    """Test creating position."""
    pos = Position(x=5.5, y=3.2)
    assert pos.x == 5.5
    assert pos.y == 3.2


def test_room_creation():
    """Test creating a room."""
    room = Room(
        id="room1",
        name="Living Room",
        dimensions=Dimensions(width=5, height=4),
        room_type="living",
        priority=8
    )
    assert room.id == "room1"
    assert room.name == "Living Room"
    assert room.area == 20
    assert room.priority == 8


def test_room_with_position():
    """Test room with position."""
    room = Room(
        id="room1",
        name="Bedroom",
        dimensions=Dimensions(width=4, height=3),
        position=Position(x=2, y=1)
    )
    assert room.position.x == 2
    assert room.position.y == 1


def test_constraint_creation():
    """Test creating constraints."""
    constraint = Constraint(
        type="min_distance",
        params={"room1": "r1", "room2": "r2", "distance": 3.0},
        description="Min distance between rooms"
    )
    assert constraint.type == "min_distance"
    assert constraint.params["distance"] == 3.0


def test_space_creation():
    """Test creating a space."""
    room1 = Room(id="r1", name="Room 1", dimensions=Dimensions(width=5, height=4))
    room2 = Room(id="r2", name="Room 2", dimensions=Dimensions(width=3, height=3))
    
    space = Space(
        dimensions=Dimensions(width=10, height=10),
        rooms=[room1, room2]
    )
    
    assert space.area == 100
    assert space.total_room_area == 29
    assert space.utilization == 0.29
    assert len(space.rooms) == 2


def test_layout_creation():
    """Test creating a layout."""
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[]
    )
    
    layout = Layout(
        space=space,
        placed_rooms=[],
        score=95.5,
        violations=[]
    )
    
    assert layout.score == 95.5
    assert layout.is_valid
    assert len(layout.violations) == 0


def test_layout_with_violations():
    """Test layout with violations."""
    space = Space(dimensions=Dimensions(width=10, height=8))
    
    layout = Layout(
        space=space,
        violations=["Room exceeds boundary", "Rooms overlap"]
    )
    
    assert not layout.is_valid
    assert len(layout.violations) == 2


def test_layout_to_json_dict():
    """Test converting layout to JSON dict."""
    room = Room(
        id="r1",
        name="Living Room",
        dimensions=Dimensions(width=5, height=4),
        position=Position(x=0, y=0)
    )
    
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[room]
    )
    
    layout = Layout(
        space=space,
        placed_rooms=[room],
        score=100.0
    )
    
    json_dict = layout.to_json_dict()
    
    assert json_dict["dimensions"]["width"] == 10
    assert json_dict["dimensions"]["height"] == 8
    assert len(json_dict["rooms"]) == 1
    assert json_dict["rooms"][0]["name"] == "Living Room"
    assert json_dict["metrics"]["score"] == 100.0
