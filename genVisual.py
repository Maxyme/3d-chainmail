#this modules displays the voxels in a 3d window

from visual import * #imports the 3Dvisual Module

def genDisplay(matrix):
    for i in range(len(matrix)):
        voxel=sphere(pos=(matrix[i][0],matrix[i][1],matrix[i][2]), radius=1, color=color.red)
