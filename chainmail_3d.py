# -*- coding: utf-8 -*-
"""
This algorithm shows the deformation of a 3d cube according to a force applied on the cube.
The logic is based on the 3D chainmail algorithm paper called "3D ChainMail: a Fast Algorithm for
Deforming Volumetric Objects" by Sarah F. F. Gibson (1996).
First, a 3d cube is build, then a force is applied to a selected sponsor voxel.
The new cube, deformed as a result of the force is shown in matplotlib

"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from deform import find_surface_sponsors, deform

def main():
    """
    Entry point for the application

    """
    stiffness_coef = 0.4
    voxel_distance = 1  # the distance between the voxels pf the cube.
    cube_side_length = 10  # the side of the cube
    displacement_area = 3
    displacement_src = np.array([5, 5, 0])  # the voxel that will be displaced
    displacement_dst = np.array([5, 5, -3])  # the final destination of the source voxel

    original_cube = _get_cube_coordinates(cube_side_length, voxel_distance)

    surface_sponsors = find_surface_sponsors(displacement_dst, displacement_src, original_cube, cube_side_length, voxel_distance, displacement_area)

    new_matrix = deform(surface_sponsors, original_cube, cube_side_length, voxel_distance, stiffness_coef)

    force_vector = _get_displacement_force(original_cube, new_matrix)

    _show_3d_plot(displacement_dst, force_vector, new_matrix)


def _show_3d_plot(displacement_dst, force_vector, new_matrix):
    """
    Shows the displacement on a 3d chart

    """
    # get x, y, z for matplotlib
    x, y, z = zip(*new_matrix)
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    # show the force vector
    ax.quiver(displacement_dst[0], displacement_dst[1], displacement_dst[2],
              force_vector[0], force_vector[1], force_vector[2])

    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    plt.waitforbuttonpress()


def _get_cube_coordinates(side, step=1):
    """
    Gets the xyz coordinates of a cube of selected side

    """
    matrix_voxel = []
    side = side * step
    for z in range(0, side, step):
        for y in range(0, side, step):
            for x in range(0, side, step):
                matrix_voxel.append(np.array([x, y, z]))

    return matrix_voxel


def _get_displacement_force(original_cube, deformed_cube):
    """
    Return force according to the sum of all the small displacements
    Goes through both matrices and compares the distances between the voxels and multiplies by the elastic coeff.

    """
    diff = np.array([0, 0, 0])
    for i in range(len(original_cube)):
        diff[0] = diff[0] + (original_cube[i][0] - deformed_cube[i][0])
        diff[1] = diff[1] + (original_cube[i][1] - deformed_cube[i][1])
        diff[2] = diff[2] + (original_cube[i][2] - deformed_cube[i][2])

    return diff

if __name__ == '__main__':
    main()
    _get_cube_coordinates()
    _get_displacement_force()
