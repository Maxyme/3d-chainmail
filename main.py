# 13 Avril 2009 - Maxime Jacques
# variation of original code where this takes into account multiple sponsor
# it works by asking the user a radius of action

from visual import * #imports the 3Dvisual Module
from genVisual  import * #import the 3d visual module
from force import * #imports the forcefeedback module
from cube import * #import the cube creation module
from deform import * #imports the deform module
from surfaceSponsors import * #imports the surfaceSponsors module


get_cube=Cube()   #creates the cube : get_cube.side=side value get_cube.step = step value get_cube.matrix = matrix of data

get_force = Force(get_cube)   #creates the force : get_force.x=x displacement (same for y and z) get_force.posx = (original x position on top surface) (same for y)

sponsorpos = find([get_force.posx,get_force.posy,get_force.posz],get_cube.matrix)   #position of the original modified voxel

sponsor = [get_force.x,get_force.y,get_force.z,sponsorpos,get_force.rad]  #modified sponsor value with position and radius values

surface_sponsors = findSurfaceSponsors(sponsor,get_cube.matrix,get_cube.side,get_cube.step)

new_matrix = deform(surface_sponsors,get_cube.matrix,get_cube.side,get_cube.step,get_cube.stiff)   #deforms the cube matrix

genDisplay(new_matrix)        #shows the cube in 3D

force_vector = forcefeedback(get_cube.matrix,new_matrix,get_cube.elast) #display the forcefeedback 3d vector using the forcefeedback module

pointer = arrow(pos=(get_force.x,get_force.y,get_force.z), axis=(force_vector[0],force_vector[1],force_vector[2]), shaftwidth=0.1) #displays the force in a 3d vector form
