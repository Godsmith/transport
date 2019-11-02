"""Test cases for the path.py modules."""


from transport.model.path import Path, Point


def test_moving():
    """Test that the agent is at the right location after moving normally"""
    path = Path(Point(0, 0))
    path.append(Point(0, 1))
    path.append(Point(0, 2))

    path.update(1.1)

    assert path.point_agent_is_leaving == Point(0, 1)
    assert path.point_agent_is_approaching == Point(0, 2)


def test_reversing():
    """Test that the agent is at the right location after reaching the end of the line
    and reversing"""
    path = Path(Point(0, 0))
    path.append(Point(0, 1))
    path.append(Point(0, 2))

    path.update(1.1)
    path.update(1.1)

    assert path.point_agent_is_leaving == Point(0, 2)
    assert path.point_agent_is_approaching == Point(0, 1)


def test_single_point_path_not_crashing():
    """Previously, creating a single-point path crashed the program after one second."""
    path = Path(Point(0, 0))

    path.update(1.1)

    assert path.point_agent_is_leaving == Point(0, 0)
    assert path.point_agent_is_approaching == Point(0, 0)
