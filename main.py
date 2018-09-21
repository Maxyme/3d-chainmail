"""
This algorithm shows the deformation of a 3d cube according to a force applied on the cube.
The logic is based on the 3D chainmail algorithm paper called "3D ChainMail: a Fast Algorithm for
Deforming Volumetric Objects" by Sarah F. F. Gibson (1996).
First, a 3d cube is build, then a force is applied to a selected sponsor voxel.
Then the force propagates from the sponsor voxel to the neighbourging voxels which become sponsor voxels themselves.
The force stops propagation as a function of the stiffness coefficient.
The new cube, deformed as a result of the force is shown in matplotlib

"""

import deform
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def chainmail_entry(stiffness_coef, voxel_spacing, cube_side_length, disp_area, disp_src, disp_vector):
    """
    Entry point for the application
    stiffness_coef = 0.4
    voxel_spacing = 1  # the distance between the voxels pf the cube.
    cube_side_length = 10  # the side of the cube
    disp_area = 1
    disp_src = np.array([5, 5, 0])  # the voxel that will be displaced
    disp_vector = np.array([0, 0, -3])  # the final destination of the source voxel

    """
    # Generate the cube
    range_array = np.arange(cube_side_length)
    original_cube = np.array(np.meshgrid(range_array, range_array, range_array)).T.reshape(-1, 3)

    # Deform the cube using the chainmail algorithm
    new_matrix = deform.deform(disp_src, disp_area, disp_vector, original_cube, voxel_spacing, stiffness_coef)

    # get x, y, z for matplotlib
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')

    # show the force vector
    force_vector = original_cube - new_matrix
    displacement_dst = disp_src + disp_vector
    ax.quiver(displacement_dst[0], displacement_dst[1], displacement_dst[2],
              force_vector[0], force_vector[1], force_vector[2])

    # show the deformed cube
    x, y, z = zip(*new_matrix)
    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show(block=True)


if __name__ == '__main__':
    chainmail_entry(stiffness_coef=0.4, voxel_spacing=1, cube_side_length=10, disp_area=1, disp_src=np.array([5, 5, 0]),
                    disp_vector=np.array([0, 0, -3]))
