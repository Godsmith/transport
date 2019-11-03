"""Contains the FactoryView object."""
from typing import List

from kivy.core.text import Label as CoreLabel
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle

from transport.model.factory import Factory
from transport.view.constants import COLOR_FROM_RESOURCE
from transport.view.grid_properties import GridProperties


class FactoryView:
    """A visualization of a Factory object."""

    def __init__(self, factory: Factory, grid_properties: GridProperties):
        self._top_color = COLOR_FROM_RESOURCE[factory.consumes]
        self._bottom_color = COLOR_FROM_RESOURCE[factory.creates]
        self._resource_count = len(factory.resources)
        self._x, self._y = grid_properties.to_pixels(factory.x, factory.y)
        self._cell_width = grid_properties.cell_width
        self._cell_height = grid_properties.cell_height

        self.instruction_groups: List[InstructionGroup] = []
        self._paint_divided_square()
        self._paint_digit()

    def _paint_divided_square(self):
        instruction_group = InstructionGroup()
        bottom_left_x = self._x - self._cell_width / 2
        bottom_left_y = self._y - self._cell_height / 2
        instruction_group.add(self._bottom_color)
        instruction_group.add(
            Rectangle(
                pos=(bottom_left_x, bottom_left_y),
                size=(self._cell_width, self._cell_height / 2),
            )
        )
        self.instruction_groups.append(instruction_group)

        instruction_group2 = InstructionGroup()
        middle_left_y = self._y
        instruction_group2.add(self._top_color)
        instruction_group2.add(
            Rectangle(
                pos=(bottom_left_x, middle_left_y),
                size=(self._cell_width, self._cell_height / 2),
            )
        )
        self.instruction_groups.append(instruction_group2)

    def _paint_digit(self):
        label = CoreLabel(text=str(self._resource_count), font_size=20)
        label.refresh()
        text = label.texture

        instruction_group = InstructionGroup()
        instruction_group.add(Color(1, 1, 1))
        instruction_group.add(
            Rectangle(size=text.size, pos=(self._x, self._y), texture=text)
        )

        self.instruction_groups.append(instruction_group)
