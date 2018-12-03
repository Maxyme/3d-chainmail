import numpy.testing as npt
import numpy as np

from volume import Volume


def test_get_center_neighbors():
    """test the get neighbor function"""
    volume = Volume(data=np.random.random((3, 3, 3)))
    neighbors = volume._get_neighbors((1, 1, 1))
    actual_neighbors = [(0, 1, 1), (2, 1, 1), (1, 2, 1), (1, 0, 1), (1, 1, 0), (1, 1, 2)]
    npt.assert_array_equal(neighbors.sort(), actual_neighbors.sort())


def test_get_edge_neighbors():
    """test the get neighbor function"""
    volume = Volume(data=np.random.random((3, 3, 3)))
    neighbors = volume._get_neighbors((0, 0, 2))
    actual_neighbors = [(0, 1, 2), (0, 0, 1), (1, 0, 2)]
    npt.assert_array_equal(neighbors.sort(), actual_neighbors.sort())


def test_get_edge_neighbors_with_history():
    """test the get neighbor function"""
    volume = Volume(data=np.random.random((3, 3, 3)))
    sponsor_history = [(0, 0, 1)]
    neighbors = volume._get_neighbors((0, 0, 2), sponsor_history)
    actual_neighbors = [(0, 1, 2), (1, 0, 2)]
    npt.assert_array_equal(neighbors.sort(), actual_neighbors.sort())
