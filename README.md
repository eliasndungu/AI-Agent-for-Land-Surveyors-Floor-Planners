# AI Agent for Land Surveyors & Floor Planners

An AI-powered spatial planning agent that generates optimized 2D layout suggestions for land surveyors and floor planners.

## Overview

This agent takes land or floor dimensions along with room/structure specifications and constraints, then generates optimized layout suggestions using rule-based algorithms and spatial optimization techniques.

## Features

- **2D Spatial Planning**: Generate layouts for floor plans or land plots
- **Rule-Based Optimization**: Uses greedy algorithms with priority-based placement
- **Constraint Support**: Define spatial constraints (minimum distance, adjacency, etc.)
- **JSON Input/Output**: Easy integration with other tools
- **Layout Validation**: Automatic checking for overlaps and boundary violations
- **Scoring System**: Quantitative evaluation of layout quality

## Installation

```bash
# Clone the repository
git clone https://github.com/eliasndungu/AI-Agent-for-Land-Surveyors-Floor-Planners.git
cd AI-Agent-for-Land-Surveyors-Floor-Planners

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from spatial_planning import SpatialPlanningAgent

# Create agent
agent = SpatialPlanningAgent()

# Define space and rooms
space = agent.create_space(
    width=10,
    height=8,
    rooms=[
        {"name": "Living Room", "width": 5, "height": 4, "priority": 9},
        {"name": "Bedroom", "width": 4, "height": 3, "priority": 8},
        {"name": "Kitchen", "width": 3, "height": 3, "priority": 7},
    ]
)

# Generate optimized layout
layout = agent.generate_layout(space)

# Print summary
print(agent.get_layout_summary(layout))

# Export to JSON
json_output = agent.export_layout_json(layout)
```

### Using JSON Input

```python
import json
from spatial_planning import SpatialPlanningAgent

agent = SpatialPlanningAgent()

# Load from JSON file
with open('examples/apartment_floor_plan.json', 'r') as f:
    data = json.load(f)

layout = agent.generate_from_dict(data)
print(agent.get_layout_summary(layout))
```

## Input Format

The agent accepts JSON input with the following structure:

```json
{
  "dimensions": {
    "width": 10,
    "height": 8
  },
  "rooms": [
    {
      "id": "living",
      "name": "Living Room",
      "width": 5,
      "height": 4,
      "type": "living_room",
      "priority": 9
    }
  ],
  "constraints": [
    {
      "type": "adjacency",
      "params": {
        "room1": "kitchen",
        "room2": "living",
        "max_distance": 5.0
      },
      "description": "Kitchen should be adjacent to living room"
    }
  ]
}
```

### Room Properties

- `id` (optional): Unique identifier for the room
- `name` (required): Display name
- `width` (required): Width in meters
- `height` (required): Height in meters
- `type` (optional): Room type (bedroom, kitchen, etc.)
- `priority` (optional): Placement priority 1-10 (default: 5, higher = placed first)

### Constraint Types

1. **min_distance**: Minimum distance between two rooms
   ```json
   {
     "type": "min_distance",
     "params": {"room1": "id1", "room2": "id2", "distance": 3.0}
   }
   ```

2. **adjacency**: Rooms should be next to each other
   ```json
   {
     "type": "adjacency",
     "params": {"room1": "id1", "room2": "id2", "max_distance": 2.0}
   }
   ```

## Output Format

The agent produces JSON output with positioned rooms:

```json
{
  "dimensions": {
    "width": 10,
    "height": 8,
    "area": 80
  },
  "rooms": [
    {
      "id": "living",
      "name": "Living Room",
      "type": "living_room",
      "dimensions": {"width": 5, "height": 4, "area": 20},
      "position": {"x": 0.0, "y": 0.0}
    }
  ],
  "metrics": {
    "score": 95.5,
    "utilization": 0.75,
    "is_valid": true,
    "violations": []
  }
}
```

## Examples

Run the demo script to see various examples:

```bash
python examples/demo.py
```

Example files are provided in the `examples/` directory:
- `apartment_floor_plan.json`: Residential apartment layout
- `land_survey_plot.json`: Land plot with buildings

## Architecture

The system consists of several components:

1. **Models** (`models.py`): Data structures for spaces, rooms, constraints, and layouts
2. **Optimizer** (`optimizer.py`): Greedy algorithm for room placement
3. **Constraints** (`constraints.py`): Validation and constraint checking
4. **Agent** (`agent.py`): Main interface for the planning system

## Optimization Algorithm

The agent uses a priority-based greedy algorithm:

1. Sort rooms by priority (highest first)
2. For each room, search for the best valid position using a grid
3. Place room at position that maximizes layout quality
4. Validate constraints and calculate final score

The scoring system considers:
- Placement success rate
- Space utilization (60-80% ideal)
- Constraint violations
- Layout compactness

## Limitations (MVP Scope)

- 2D planning only (no 3D support)
- Text/JSON-based output (no visual rendering)
- Basic rule-based optimization (not ML-based)
- Rectangular rooms only
- Grid-based positioning

## Future Enhancements

Potential improvements beyond MVP:
- 3D layout generation
- Visual rendering of layouts
- Machine learning-based optimization
- Interactive web interface
- Support for irregular shapes
- Advanced constraint types
- Multi-floor planning

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
