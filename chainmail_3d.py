# -*- coding: utf-8 -*-
"""
This algorithm shows the deformation of a 3d cube according to a force applied on the cube.
The logic is based on the 3D chainmail algorithm paper called "3D ChainMail: a Fast Algorithm for
Deforming Volumetric Objects" by Sarah F. F. Gibson (1996).
First, a 3d cube is build, then a force is applied to a selected sponsor voxel.
The new cube, deformed as a result of the force is shown in matplotlib

"""
#from visual import * #imports the 3Dvisual Module
from deform import * #imports the deform module
from surfaceSponsors import * #imports the surfaceSponsors module

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def main():
    """
    Entry point for the application

    """
    stiffness_coef = 1 # "Enter stiffness level [0 : " + str(self.step) + "]"
    voxel_distance = 1
    cube_side_length = 3

    displacement_area = 1
    displacement_src = np.array([0, 0, 0])
    displacement_dst = np.array([5, 0, 0]) # "Enter new x position of sponsor: [" + str(self.posx - get_cube.step) + ":" + str(self.posx + get_cube.step) + "]"

    original_cube = _get_cube_coordinates(cube_side_length, voxel_distance)

    # position of the original modified voxel
    sponsor_position = find([displacement_src[0], displacement_src[1], displacement_src[2]], original_cube)

    # modified sponsor value with position and radius values
    sponsor = [displacement_dst[0], displacement_dst[1], displacement_dst[2], sponsor_position, displacement_area]
    surface_sponsors = findSurfaceSponsors(sponsor, original_cube, cube_side_length, voxel_distance)

    new_matrix = deform(surface_sponsors, original_cube, cube_side_length, voxel_distance, stiffness_coef)

    force_vector = _get_displacement_force(original_cube, new_matrix)

    #pointer = arrow(pos=(get_force.x,get_force.y,get_force.z), axis=(force_vector[0],force_vector[1],force_vector[2]), shaftwidth=0.1)

def _get_cube_coordinates(side, step=1):
    """
    Gets the xyz coordinates of a cube of selected side

    """
    matrix_voxel = []
    side = side * step
    for z in range(0, side, step):
        step_matrix = []
        for y in range(0, side, step):
            for x in range(0, side, step):
                matrix_voxel.append([x, y, z])
                step_matrix.append([x, y, z])

    return matrix_voxel


def _get_displacement_force(original_cube, deformed_cube):
    """
    Return force according to the sum of all the small displacements
    Goes through both matrices and compares the distances between the voxels and multiplies by the elastic coeff.

    """
    diff = np.array([0, 0, 0])
    for i in range(len(original_cube)):
        for j in range(3):
            if j == 0:
                diff[0] = diff[0] + (original_cube[i][j] - deformed_cube[i][j])
            elif j == 1:
                diff[1] = diff[1] + (original_cube[i][j] - deformed_cube[i][j])
            elif j == 2:
                diff[2] = diff[2] + (original_cube[i][j] - deformed_cube[i][j])

    return diff

if __name__ == '__main__':
    main()
    _get_cube_coordinates()
    _get_displacement_force()
