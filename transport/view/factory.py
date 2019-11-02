"""Contains the FactoryView object."""
from typing import List

from kivy.core.text import Label as CoreLabel
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle

from transport.model.factory import Factory
from transport.model.resource import Resource

COLOR_FROM_RESOURCE = {
    Resource.BLUE: Color(0, 1, 1),
    Resource.RED: Color(1, 0, 0),
    None: Color(0.2, 0.2, 0.2),
}


class FactoryView:
    """A visualization of a Factory object."""

    def __init__(
        self,
        factory: Factory,
        x: float,
        y: float,
        cell_width: float,
        cell_height: float,
    ):
        self._top_color = COLOR_FROM_RESOURCE[factory.consumes]
        self._bottom_color = COLOR_FROM_RESOURCE[factory.creates]
        self._resource_count = len(factory.resources)
        self._x = x
        self._y = y
        self._cell_width = cell_width
        self._cell_height = cell_height

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
