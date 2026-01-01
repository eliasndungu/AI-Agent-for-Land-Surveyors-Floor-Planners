"""
Unit tests for constraint validation.
"""

import pytest
from spatial_planning.models import Space, Room, Dimensions, Position, Constraint
from spatial_planning.constraints import ConstraintValidator


def test_check_bounds_valid():
    """Test that rooms within bounds pass validation."""
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[]
    )
    
    room = Room(
        id="r1",
        name="Room 1",
        dimensions=Dimensions(width=5, height=4),
        position=Position(x=0, y=0)
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_bounds([room])
    
    assert len(violations) == 0


def test_check_bounds_exceeds_width():
    """Test that room exceeding width boundary is detected."""
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[]
    )
    
    room = Room(
        id="r1",
        name="Room 1",
        dimensions=Dimensions(width=5, height=4),
        position=Position(x=6, y=0)  # 6 + 5 = 11 > 10
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_bounds([room])
    
    assert len(violations) == 1
    assert "width boundary" in violations[0]


def test_check_bounds_exceeds_height():
    """Test that room exceeding height boundary is detected."""
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[]
    )
    
    room = Room(
        id="r1",
        name="Room 1",
        dimensions=Dimensions(width=5, height=4),
        position=Position(x=0, y=5)  # 5 + 4 = 9 > 8
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_bounds([room])
    
    assert len(violations) == 1
    assert "height boundary" in violations[0]


def test_check_overlaps_no_overlap():
    """Test that non-overlapping rooms pass validation."""
    space = Space(dimensions=Dimensions(width=10, height=10))
    
    room1 = Room(
        id="r1", name="Room 1",
        dimensions=Dimensions(width=3, height=3),
        position=Position(x=0, y=0)
    )
    
    room2 = Room(
        id="r2", name="Room 2",
        dimensions=Dimensions(width=3, height=3),
        position=Position(x=4, y=0)
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_overlaps([room1, room2])
    
    assert len(violations) == 0


def test_check_overlaps_with_overlap():
    """Test that overlapping rooms are detected."""
    space = Space(dimensions=Dimensions(width=10, height=10))
    
    room1 = Room(
        id="r1", name="Room 1",
        dimensions=Dimensions(width=5, height=5),
        position=Position(x=0, y=0)
    )
    
    room2 = Room(
        id="r2", name="Room 2",
        dimensions=Dimensions(width=5, height=5),
        position=Position(x=3, y=3)  # Overlaps with room1
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_overlaps([room1, room2])
    
    assert len(violations) == 1
    assert "overlap" in violations[0].lower()


def test_min_distance_constraint_satisfied():
    """Test min distance constraint when satisfied."""
    room1 = Room(
        id="r1", name="Room 1",
        dimensions=Dimensions(width=2, height=2),
        position=Position(x=0, y=0)
    )
    
    room2 = Room(
        id="r2", name="Room 2",
        dimensions=Dimensions(width=2, height=2),
        position=Position(x=5, y=5)  # Far enough
    )
    
    constraint = Constraint(
        type="min_distance",
        params={"room1": "r1", "room2": "r2", "distance": 3.0}
    )
    
    space = Space(
        dimensions=Dimensions(width=10, height=10),
        constraints=[constraint]
    )
    
    validator = ConstraintValidator(space)
    violations = validator._check_min_distance([room1, room2], constraint)
    
    assert len(violations) == 0


def test_validate_layout_complete():
    """Test complete layout validation."""
    room1 = Room(
        id="r1", name="Room 1",
        dimensions=Dimensions(width=4, height=3),
        position=Position(x=0, y=0)
    )
    
    room2 = Room(
        id="r2", name="Room 2",
        dimensions=Dimensions(width=3, height=3),
        position=Position(x=5, y=0)
    )
    
    space = Space(
        dimensions=Dimensions(width=10, height=8),
        rooms=[room1, room2]
    )
    
    validator = ConstraintValidator(space)
    violations = validator.validate_layout([room1, room2])
    
    assert len(violations) == 0
