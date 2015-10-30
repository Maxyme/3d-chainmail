#this module finds the voxels composing the surface to be deplaced. It uses a radius of neighbors to limit the surface space.
#the surface cannot be larger than the side of the cube. Also, it only gets the neighbors on the same level, not in depth (z variation)
# 14 Apr 09: Reservation on a surface with an an angle; idea is that all the neighbors follow the same movement as the sponsor.

def find(voxel,matrix):                    #function that finds a defined voxel position in a matrix
    for i in range(len(matrix)):           #from 0 to the end of the matrix
        if (voxel[0] == matrix[i][0] and voxel[1] == matrix[i][1] and voxel[2] == matrix[i][2]):
            break
    return i

def findNeighbors(sponsorpos,matrix,sponsorhist,side,step):         #this functions finds all the neighbors of the sponsor, it requires
                                                                    #the variable step and side variables
    neighborlist = []                                                 #it also will not add values
                                                                      #outside the cube as
                                                                      #neighbors, and it will not
                                                                      #add previous sponsors
    sponsor = matrix[sponsorpos]                                      #gets the original value of the sponsor
                                                                      #to find the neighbors

    if (sponsor[0] + step < side * step):
        rn = [sponsor[0] + step,sponsor[1],sponsor[2],0]                #the right neighbor value=0 ; left =1; top =2; bottom = 3 down
                                                                        #= 4.
        if (find(rn,matrix) in sponsorhist) == False:                          #if the right neighbor is not a previous sponsor, it
                                                                               #adds the value to the neighbor list
            neighborlist.append(rn)
            
    if (sponsor[0] - step >= 0):
        ln = [sponsor[0] - step,sponsor[1],sponsor[2],1]
        if (find(ln,matrix) in sponsorhist) == False:
            neighborlist.append(ln)
            
    if (sponsor[1] + step < side * step):
        tn = [sponsor[0],sponsor[1] + step,sponsor[2],2]
        if (find(tn,matrix) in sponsorhist) == False:
            neighborlist.append(tn)
            
    if (sponsor[1] - step >= 0):
        bn = [sponsor[0],sponsor[1] - step,sponsor[2],3]
        if (find(bn,matrix) in sponsorhist) == False:
            neighborlist.append(bn)
            
    return neighborlist

def deformSurface(surface_list,matrix):  #this deforms the surface found (all the neighbors) according to the vector
                                         #of deformation applied to the sponso#

    sponsor = surface_list[0]
    del surface_list[0]
    
    original_sponsor = matrix[sponsor[3]]       #this is the original value of the sponsor
    vectorx = sponsor[0] - original_sponsor[0] 
    vectory = sponsor[1] - original_sponsor[1]  
    vectorz = sponsor[2] - original_sponsor[2]  

    for i in range(len(surface_list)):                      #applies the deformation to the entire surface list of
                                                            #sponsor/neighbors
        surface_list[i][0] = surface_list[i][0] + vectorx
        surface_list[i][1] = surface_list[i][1] + vectory
        surface_list[i][2] = surface_list[i][2] + vectorz

    surface_list.insert(0,sponsor)            #adds the surface sponsor to the list again
    
    return surface_list
    


def findSurfaceSponsors(sponsor,matrix,side,step):       #the radius value is included in the sponsor [4]
    surface_sponsors = []          #the list of sponsors to include in the deform function
    outside_layer = []            #the list of neighbors at the layer of the radius function.  Ex,
                                  #for radius 1, the layer neighbor is the sponsor
    sponsor_history = []            #the sponsor_history list
                                    #for a radius of 2, the new layer neighbors
                                                            #are the neighbors added for a radius of 1.
    radius = sponsor[4]
    del sponsor[4]
    
    surface_sponsors.append(sponsor) #includes the sponsor position also [3]
    outside_layer.extend(surface_sponsors)
    sponsor_history.append(sponsor[3]) #puts the sponsor position in a list so that it adds the sponsors when it
                                       #looks for it.
    
    if radius != 0:                         # if the radius = 0, it returns only the first
                                            # sponsor.
        for i in range(radius):
            storage_layer = []                              #empty storage layer of neighbors
            while len(outside_layer) > 0:
                use_sponsor = outside_layer.pop(0)
                storage_layer.extend(findNeighbors(use_sponsor[3],matrix,sponsor_history,side,step))

                for j in range(len(storage_layer)):
                    neighbor_position = find(storage_layer[j],matrix)
                    storage_layer[j][3] = neighbor_position
                    sponsor_history.append(neighbor_position)   #adds the position of the newneighbors to the history list

            surface_sponsors.extend(storage_layer)

            outside_layer.extend(storage_layer)
            #print "outside_layer", i, outside_layer

    surface_sponsors = deformSurface(surface_sponsors,matrix)             
    return surface_sponsors






##                for i in range(len(radius)-1):    #for i in the range of radius-1; if radius = 1 it only goes once
##
##                        use_sponsor = outside_layer.pop[0]
##                        layer_neighbors.extend(findNeighbors(use_sponsor[3],matrix,sponsor_history,side,step))
##                        surface_neighbors.extend(layer_neighbors)
##
##                        for j in layer_neighbors:
##                                sponsor_history.extend(layer_neighbors[j][3])   #adds the position of the newneighbors to the history list
##                                
##                        if i < (radius - 1):            #if there are neighbors of neighbors to add
##                                layer_list2 = []
##                                while len(range(layer_neighbors)) < 0:
##                                        use_neighbor = layer_neighbors.pop[0]
##                                        layer_list2.extend(findNeighbors(use_neighbor[3],matrix,sponsor_history,side,step)
##                                                           
##                                layer_neighbors = layer_list2[:]
##                                layer_list2 = []
##                        else
##                                return surface_neighbors
##        return surface_neighbors
                                        
                        
#------------------ ------------------ ------------------ ------------------ ------------------ ------------------
#test variables 3x3

#sponsor = [4,4,6,22,1]    #x,y,z deformed, position radius

#radius = 0   #with a radius of 0, it only gets the first sponsor, no neighbors. 1 is the 4 nearby voxels.

#side = 3

#step = 2

#matrix = [[0.0, 0.0, 0.0], [2, 0, 0], [4, 0, 0], [0, 2, 0], [2, 2, 0], [4, 2, 0], [0, 4, 0], [2, 4, 0], [4, 4, 0], [0, 0, 2], [2, 0, 2], [4, 0, 2],
#          [0, 2, 2], [2, 2, 2], [4, 2, 2], [0, 4, 2], [2, 4, 2], [4, 4, 2], [0, 0, 4], [2, 0, 4], [4, 0, 4], [0, 2, 4], [2, 2, 4], [4, 2, 4], [0, 4, 4], [2, 4, 4], [4, 4, 4]]


#surface_list = [[4, 4, 6, 22], [4, 2, 4, 23], [0, 2, 4, 21], [2, 4, 4, 25], [2, 0, 4, 19]]

#------------------------------------------------------------------------------------------------------------

#test variables 5x5

##matrix = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0], [3, 1, 0], [4, 1, 0], [0, 2, 0], [1, 2, 0], [2, 2, 0], [3, 2, 0], [4, 2, 0], [0, 3, 0],
##[1, 3, 0], [2, 3, 0], [3, 3, 0], [4, 3, 0], [0, 4, 0], [1, 4, 0], [2, 4, 0], [3, 4, 0], [4, 4, 0], [0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1],
##[0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 1, 1], [0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1], [4, 2, 1], [0, 3, 1], [1, 3, 1], [2, 3, 1], [3, 3, 1],
##[4, 3, 1], [0, 4, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1], [0, 0, 2], [1, 0, 2], [2, 0, 2], [3, 0, 2], [4, 0, 2], [0, 1, 2], [1, 1, 2], [2, 1, 2], [3, 1, 2], [4, 1, 2],
##[0, 2, 2], [1, 2, 2], [2, 2, 2], [3, 2, 2], [4, 2, 2], [0, 3, 2], [1, 3, 2], [2, 3, 2], [3, 3, 2], [4, 3, 2], [0, 4, 2], [1, 4, 2], [2, 4, 2], [3, 4, 2], [4, 4, 2],
##[0, 0, 3], [1, 0, 3], [2, 0, 3], [3, 0, 3], [4, 0, 3], [0, 1, 3], [1, 1, 3], [2, 1, 3], [3, 1, 3], [4, 1, 3], [0, 2, 3], [1, 2, 3], [2, 2, 3], [3, 2, 3], [4, 2, 3], [0, 3, 3], [1, 3, 3],
##[2, 3, 3], [3, 3, 3], [4, 3, 3], [0, 4, 3], [1, 4, 3], [2, 4, 3], [3, 4, 3], [4, 4, 3], [0, 0, 4], [1, 0, 4], [2, 0, 4], [3, 0, 4], [4, 0, 4], [0, 1, 4], [1, 1, 4], [2, 1, 4],
##[3, 1, 4], [4, 1, 4], [0, 2, 4], [1, 2, 4], [2, 2, 4], [3, 2, 4], [4, 2, 4], [0, 3, 4], [1, 3, 4], [2, 3, 4], [3, 3, 4], [4, 3, 4], [0, 4, 4], [1, 4, 4], [2, 4, 4],
##[3, 4, 4], [4, 4, 4]]
##
##sponsor = [2,2,4,0,3]
##
##position = find(sponsor,matrix)
##
##sponsor[3] = position
##
##print "sponsor", sponsor
##
##vector = [2,2,2]
##
##sponsor[0]=sponsor[0]+vector[0]
##sponsor[1]=sponsor[1]+vector[1]
##sponsor[2]=sponsor[2]+vector[2]
##
##side = 5
##
##step = 1
##
##print "new_sponsor", sponsor
##
##print findNeighbors(sponsor[3],matrix,[0],side,step)
##surface_list = findSurfaceSponsors(sponsor,matrix,side,step)
##
##print deformSurface(surface_list,matrix)


