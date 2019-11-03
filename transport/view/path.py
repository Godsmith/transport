"""Contains the PathView class."""

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Ellipse, Rectangle

from transport.model.path import Path
from transport.view.constants import COLOR_FROM_RESOURCE
from transport.view.grid_properties import GridProperties


class PathView:
    """A visual representation of a Path."""

    def __init__(self, grid_path: Path, grid_properties: GridProperties):
        self._grid_properties = grid_properties
        self._grid_path = grid_path

        container_instruction_group = InstructionGroup()
        container_instruction_group.add(Color(1, 0, 0))
        points = [grid_properties.to_pixels(*point) for point in grid_path]
        container_instruction_group.add(Line(points=points))

        d = 15
        x, y = self._agent_position
        container_instruction_group.add(
            Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))
        )

        self.instruction_groups = [container_instruction_group]

        rectangle_diameter = 10
        for resource in grid_path.resources:
            resource_instruction_group = InstructionGroup()
            resource_instruction_group.add(COLOR_FROM_RESOURCE[resource])
            resource_instruction_group.add(
                Rectangle(
                    pos=(x - rectangle_diameter / 2, y - rectangle_diameter / 2),
                    size=(rectangle_diameter, rectangle_diameter),
                )
            )
            self.instruction_groups.append(resource_instruction_group)

    @property
    def _agent_position(self):
        x1, y1 = self._grid_properties.to_pixels(
            *self._grid_path.point_agent_is_leaving
        )
        x2, y2 = self._grid_properties.to_pixels(
            *self._grid_path.point_agent_is_approaching
        )
        fraction = self._grid_path.distance_to_next_square
        return x1 + (x2 - x1) * fraction, y1 + (y2 - y1) * fraction
