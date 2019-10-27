from main import GridWidget


def test_index_of_closest():
    assert 2 == GridWidget._index_of_closest(3.2, [1, 2, 3, 4, 5])
