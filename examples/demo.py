#!/usr/bin/env python3
"""
Demo script for the Spatial Planning Agent.
Shows basic usage and examples of generating layouts.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from spatial_planning import SpatialPlanningAgent


def demo_basic_usage():
    """Demonstrate basic agent usage."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Floor Plan Layout")
    print("="*70 + "\n")
    
    # Create agent
    agent = SpatialPlanningAgent()
    
    # Define a simple floor plan
    space = agent.create_space(
        width=10,
        height=8,
        rooms=[
            {"name": "Living Room", "width": 5, "height": 4, "priority": 9},
            {"name": "Bedroom", "width": 4, "height": 3, "priority": 8},
            {"name": "Kitchen", "width": 3, "height": 3, "priority": 7},
        ]
    )
    
    # Generate layout
    layout = agent.generate_layout(space)
    
    # Print summary
    print(agent.get_layout_summary(layout))
    
    # Export to JSON
    print("\nJSON Output:")
    print(agent.export_layout_json(layout))


def demo_from_json_file():
    """Demonstrate loading from JSON file."""
    print("\n" + "="*70)
    print("DEMO 2: Apartment Floor Plan from JSON")
    print("="*70 + "\n")
    
    agent = SpatialPlanningAgent()
    
    # Load example file
    examples_dir = Path(__file__).parent
    json_file = examples_dir / "apartment_floor_plan.json"
    
    if json_file.exists():
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        layout = agent.generate_from_dict(data)
        print(agent.get_layout_summary(layout))
    else:
        print(f"Example file not found: {json_file}")


def demo_land_survey():
    """Demonstrate land survey plot planning."""
    print("\n" + "="*70)
    print("DEMO 3: Land Survey Plot Layout")
    print("="*70 + "\n")
    
    agent = SpatialPlanningAgent()
    
    # Load example file
    examples_dir = Path(__file__).parent
    json_file = examples_dir / "land_survey_plot.json"
    
    if json_file.exists():
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        layout = agent.generate_from_dict(data)
        print(agent.get_layout_summary(layout))
        
        # Save output
        output_file = examples_dir / "land_survey_output.json"
        with open(output_file, 'w') as f:
            f.write(agent.export_layout_json(layout))
        print(f"\n✓ Output saved to: {output_file}")
    else:
        print(f"Example file not found: {json_file}")


def demo_custom_constraints():
    """Demonstrate custom constraints."""
    print("\n" + "="*70)
    print("DEMO 4: Layout with Custom Constraints")
    print("="*70 + "\n")
    
    agent = SpatialPlanningAgent()
    
    # Create space with constraints
    space = agent.create_space(
        width=12,
        height=10,
        rooms=[
            {"id": "room1", "name": "Office 1", "width": 4, "height": 3, "priority": 8},
            {"id": "room2", "name": "Office 2", "width": 4, "height": 3, "priority": 8},
            {"id": "meeting", "name": "Meeting Room", "width": 5, "height": 4, "priority": 9},
        ],
        constraints=[
            {
                "type": "min_distance",
                "params": {"room1": "room1", "room2": "room2", "distance": 2.0},
                "description": "Offices should have some separation"
            }
        ]
    )
    
    layout = agent.generate_layout(space)
    print(agent.get_layout_summary(layout))


if __name__ == "__main__":
    print("\n" + "🏠 " * 20)
    print("AI AGENT FOR LAND SURVEYORS & FLOOR PLANNERS - DEMO")
    print("🏠 " * 20)
    
    # Run all demos
    demo_basic_usage()
    demo_from_json_file()
    demo_land_survey()
    demo_custom_constraints()
    
    print("\n" + "="*70)
    print("✓ All demos completed!")
    print("="*70 + "\n")
