# -*- coding: utf-8 -*-
"""
This algorithm shows the deformation of a 3d cube according to a force applied on the cube.
The logic is based on the 3D chainmail algorithm paper called "3D ChainMail: a Fast Algorithm for
Deforming Volumetric Objects" by Sarah F. F. Gibson (1996).
First, a 3d cube is build, then a force is applied to a selected sponsor voxel.
The new cube, deformed as a result of the force is shown in matplotlib

"""
import utility_functions
import deform
import numpy as np


def main():
    """
    Entry point for the application

    """
    stiffness_coef = 0.4
    voxel_spacing = 1  # the distance between the voxels pf the cube.
    cube_side_length = 10  # the side of the cube
    displacement_area = 3
    displacement_src = np.array([5, 5, 0])  # the voxel that will be displaced
    displacement_vector = np.array([0, 0, -3])  # the final destination of the source voxel

    # Generate the cube
    x_range = y_range = z_range = np.arange(cube_side_length)
    original_cube = np.array(np.meshgrid(x_range, y_range, z_range)).T.reshape(-1, 3)

    # Generate the deformed cube using the chainmail algorithm
    new_matrix = deform.deform(displacement_src, displacement_area, displacement_vector, original_cube, voxel_spacing, stiffness_coef)

    force_vector = np.array(original_cube) - np.array(new_matrix)

    displacement_dst = displacement_src + displacement_vector
    utility_functions.show_3d_plot(displacement_dst, force_vector, new_matrix)


if __name__ == '__main__':
    main()
