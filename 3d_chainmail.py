# -*- coding: utf-8 -*-
"""
This algorithm shows the deformation of a 3d cube according to a force applied on the cube.
The logic is based on the 3D chainmail algorithm paper called "3D ChainMail: a Fast Algorithm for
Deforming Volumetric Objects" by Sarah F. F. Gibson (1996).
First, a 3d cube is build, then a force is applied to a selected sponsor voxel.
The new cube, deformed as a result of the force is shown in matplotlib

"""

#from visual import * #imports the 3Dvisual Module
from genVisual import * #import the 3d visual module
from force import * #imports the forcefeedback module
from cube import * #import the cube creation module
from deform import * #imports the deform module
from surfaceSponsors import * #imports the surfaceSponsors module

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#This algorithm shows a cube deformation based on the 3D chainmail algorithm.
#A cube is build, then a force is applied to a specific "sponsor" voxel.
#To show compression a hard surface is declared under the cube.


get_cube = Cube()
get_force = Force(get_cube)

sponsorpos = find([get_force.posx, get_force.posy, get_force.posz], get_cube.matrix)   #position of the original modified voxel
sponsor = [get_force.x, get_force.y, get_force.z, sponsorpos, get_force.rad]  #modified sponsor value with position and radius values
surface_sponsors = findSurfaceSponsors(sponsor, get_cube.matrix, get_cube.side, get_cube.step)

new_matrix = deform(surface_sponsors, get_cube.matrix, get_cube.side, get_cube.step, get_cube.stiff)   #deforms the cube matrix

#genDisplay(new_matrix)        #shows the cube in 3D
#force_vector = forcefeedback(get_cube.matrix,new_matrix,get_cube.elast) #display the forcefeedback 3d vector using the forcefeedback module
#pointer = arrow(pos=(get_force.x,get_force.y,get_force.z), axis=(force_vector[0],force_vector[1],force_vector[2]), shaftwidth=0.1)
