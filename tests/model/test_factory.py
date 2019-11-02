"""Test cases for the Factory class."""
from transport.model.factory import Factory
from transport.model.resource import Resource


def test_create_one_resource():
    """One resource shall be created after the specified interval has passed."""
    factory = Factory(creates=Resource.RED, interval=1, max_capacity=1)
    factory.update(1.1)
    assert factory.resources == [Resource.RED]


def test_create_two_resources():
    """Two resources shall be crated after the specified interval has passed twice."""
    factory = Factory(creates=Resource.RED, interval=1, max_capacity=2)
    factory.update(1.1)
    factory.update(1.1)
    assert factory.resources == [Resource.RED, Resource.RED]


def test_max_capacity():
    """The number of resources cannot exceed max capacity."""
    factory = Factory(creates=Resource.RED, interval=1, max_capacity=1)
    factory.update(1.1)
    factory.update(1.1)
    assert factory.resources == [Resource.RED]


def test_no_progress_while_at_max_capacity():
    """While the factory is at max capacity, no work on creating the next resource
    shall be done."""
    factory = Factory(creates=Resource.RED, interval=1, max_capacity=1)
    factory.resources = [Resource.RED]
    factory.update(0.5)
    assert factory.time_to_next_production > 0.99


def test_start_production_when_free_capacity():
    """Once there is free capacity, production shall resume."""
    factory = Factory(creates=Resource.RED, interval=1, max_capacity=1)
    factory.resources = [Resource.RED]
    factory.update(1.1)
    factory.pop()
    factory.update(1.1)
    factory.resources = [Resource.RED]
