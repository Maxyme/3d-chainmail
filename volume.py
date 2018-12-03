from dataclasses import dataclass, field
import numpy as np


@dataclass
class Volume(object):
    """Deformable volume object"""
    data: list
    size: tuple = field(init=False)
    deformation_range: tuple = (0.2, 0.2, 0.2)  # x, y and z range of deformation
    min_deformation: tuple = (0.04, 0.04, 0.04)  # point at which deformation is ignored
    spacing: tuple = (1, 1, 1)  # the spacing between the voxels
    x: list = field(init=False)
    y: list = field(init=False)
    z: list = field(init=False)

    def __post_init__(self):
        """initial (x, y, z) positions of the items of the volume"""
        self.data = np.asarray(self.data)
        self.size = self.data.shape[:3]
        self.spacing = np.asarray(self.spacing)
        self.x, self.y, self.z = np.indices(self.size, dtype=float)
        if any(self.spacing > 1):
            self.x *= self.spacing[0]
            self.y *= self.spacing[1]
            self.z *= self.spacing[2]

    def deform(self, index: slice, deformation: list):
        """deform positions by deformation vector starting at index"""
        self._deform_position(index, deformation)
        sponsors = [(index, deformation)]
        sponsor_hist = [index]

        while len(sponsors) > 0:
            sponsor, deformation = sponsors.pop(0)

            # keep the sign for negative values
            sign = np.sign(deformation)
            deformation = np.abs(deformation) - self.deformation_range
            deformation = np.maximum([0, 0, 0], deformation)
            if all(deformation < self.min_deformation):
                continue
            deformation = sign * deformation

            # get and deform neighbors
            neighbors = self._get_neighbors(sponsor, sponsor_hist)
            if len(neighbors) > 0:
                self._deform_positions(neighbors, deformation)
                neighbors_deformation = [(i, deformation) for i in neighbors]
                sponsors.extend(neighbors_deformation)
                sponsor_hist.extend(neighbors)

    def get_position(self, index: slice) -> tuple:
        """return the position of the index"""
        return self.x[index], self.y[index], self.z[index]

    def _deform_position(self, index: slice, deformation: list):
        """deform the position of the provided index"""
        self.x[index] += deformation[0]
        self.y[index] += deformation[1]
        self.z[index] += deformation[2]

    def _deform_positions(self, indices: list, deformation: list):
        """deform the positions of the provided indices"""
        indices = np.asarray(indices)
        self.x[np.asarray(indices)[:, 0], np.asarray(indices)[:, 1], np.asarray(indices)[:, 2]] += deformation[0]
        self.y[np.asarray(indices)[:, 0], np.asarray(indices)[:, 1], np.asarray(indices)[:, 2]] += deformation[1]
        self.z[np.asarray(indices)[:, 0], np.asarray(indices)[:, 1], np.asarray(indices)[:, 2]] += deformation[2]

    def _get_neighbors(self, index: tuple, sponsor_hist: list = None) -> list:
        """return the possible 6 neighbors of the """
        if sponsor_hist is None:
            sponsor_hist = []

        identity = np.eye(3, dtype=int)
        index = np.asarray(index, dtype=int)
        neighbors = []

        for axis in [0, 1, 2]:
            if index[axis] > 0:
                item = index - identity[axis]
                if tuple(item) not in sponsor_hist:
                    neighbors.append(tuple(item))
            if index[axis] < self.size[axis] - 1:
                item = index + identity[axis]
                if tuple(item) not in sponsor_hist:
                    neighbors.append(tuple(item))

        return neighbors

    def show(self, scatter=True):
        """show the volume's voxel positions"""
        import matplotlib.pyplot as plt

        if scatter:
            # show the result in a scatter 3d plot
            from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

            # get x, y, z for matplotlib
            fig = plt.figure(figsize=(15, 15))
            ax = fig.add_subplot(111, projection='3d')

            # show the deformed cube
            ax.scatter(self.x, self.y, self.z, c='r', marker='o')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show(block=True)

        else:
            # show the cubes in 3d for a nicer visualization
            from mpl_toolkits.mplot3d.art3d import Poly3DCollection

            def cuboid_data(p, size=(1, 1, 1)):
                cube = np.array([[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
                                 [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
                                 [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
                                 [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
                                 [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
                                 [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]], dtype=float)

                for i in range(3):
                    cube[:, :, i] *= size[i]

                return cube + np.array(p)

            def plot_cube_at(positions, colors):

                sizes = [(1, 1, 1)] * len(positions)
                g = []
                for p, s in zip(positions, sizes):
                    g.append(cuboid_data(p, size=s))

                return Poly3DCollection(np.concatenate(g), facecolors=colors, edgecolor="k")

            x, y, z = self.x, self.y, self.z
            positions = []
            for i in range(len(self.x)):
                for j in range(len(self.x)):
                    for k in range(len(self.x)):
                        positions.append(self.get_position((i, j, k)))

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_aspect('equal')
            colors = np.repeat(self.data.reshape(self.data.shape[0] * self.data.shape[1] * self.data.shape[2], 3), 6, axis=0)
            pc = plot_cube_at(positions, colors)
            ax.add_collection3d(pc)
            max_range = np.max((x, y, z)) * 1.3
            ax.set_xlim([0, max_range])
            ax.set_ylim([0, max_range])
            ax.set_zlim([0, max_range])
            plt.show(block=True)
