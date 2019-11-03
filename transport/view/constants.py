"""Assorted constants used by multiple modules"""
from kivy.graphics.context_instructions import Color

from transport.model.resource import Resource

COLOR_FROM_RESOURCE = {
    Resource.BLUE: Color(0, 1, 1),
    Resource.RED: Color(1, 0, 0),
    None: Color(0.2, 0.2, 0.2),
}
