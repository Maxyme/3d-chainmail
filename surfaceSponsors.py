"""
this module finds the voxels composing the surface to be deplaced. It uses a radius of neighbors to limit the surface space.
the surface cannot be larger than the side of the cube. Also, it only gets the neighbors on the same level, not in depth (z variation)
14 Apr 09: Reservation on a surface with an an angle; idea is that all the neighbors follow the same movement as the sponsor.

"""
def find(voxel, matrix):
    for i in range(len(matrix)):
        if voxel[0] == matrix[i][0] and voxel[1] == matrix[i][1] and voxel[2] == matrix[i][2]:
            break
    return i


def findNeighbors(sponsorpos, matrix, sponsorhist, side, step):
    """
    this functions finds all the neighbors of the sponsor, it requires the variable step and side variables
    add previous sponsors, gets the original value of the sponsor to find the neighbors
    it also will not add values outside the cube as neighbors, and it will not

    """

    neighborlist = []

    sponsor = matrix[sponsorpos]
    # the right neighbor value=0 ; left =1; top =2; bottom = 3 down = 4.
    if sponsor[0] + step < side * step:
        rn = [sponsor[0] + step, sponsor[1], sponsor[2], 0]
        # if the right neighbor is not a previous sponsor, it adds the value to the neighbor list
        if find(rn, matrix) in sponsorhist == False:
            neighborlist.append(rn)

    if sponsor[0] - step >= 0:
        ln = [sponsor[0] - step, sponsor[1], sponsor[2], 1]
        if find(ln, matrix) in sponsorhist == False:
            neighborlist.append(ln)

    if sponsor[1] + step < side * step:
        tn = [sponsor[0], sponsor[1] + step, sponsor[2], 2]
        if find(tn, matrix) in sponsorhist == False:
            neighborlist.append(tn)

    if sponsor[1] - step >= 0:
        bn = [sponsor[0], sponsor[1] - step, sponsor[2], 3]
        if find(bn, matrix) in sponsorhist == False:
            neighborlist.append(bn)

    return neighborlist


def deformSurface(surface_list, matrix):
    """
    this deforms the surface found (all the neighbors) according to the vector of deformation applied to the sponsor

    """

    sponsor = surface_list[0]
    del surface_list[0]

    # original value of the sponsor
    original_sponsor = matrix[sponsor[3]]
    vectorx = sponsor[0] - original_sponsor[0] 
    vectory = sponsor[1] - original_sponsor[1]  
    vectorz = sponsor[2] - original_sponsor[2]  

    # applies the deformation to the entire surface list of sponsor/neighbors
    for i in range(len(surface_list)):

        surface_list[i][0] = surface_list[i][0] + vectorx
        surface_list[i][1] = surface_list[i][1] + vectory
        surface_list[i][2] = surface_list[i][2] + vectorz

    # adds the surface sponsor to the list again
    surface_list.insert(0, sponsor)
    
    return surface_list
    


def findSurfaceSponsors(sponsor,matrix,side,step):
    """
    the radius value is included in the sponsor [4]

    """

    # the list of sponsors to include in the deform function
    surface_sponsors = []
    # the list of neighbors at the layer of the radius function.  Ex for radius 1, the layer neighbor is the sponsor
    outside_layer = []
    # the sponsor_history list for a radius of 2, the new layer neighbors are the neighbors added for a radius of 1.
    sponsor_history = []
    radius = sponsor[4]
    del sponsor[4]

    # includes the sponsor position also [3]
    surface_sponsors.append(sponsor)
    outside_layer.extend(surface_sponsors)
    # puts the sponsor position in a list so that it adds the sponsors when it looks for it
    sponsor_history.append(sponsor[3])

    # if the radius = 0, it returns only the first sponsor
    if radius != 0:
        for i in range(radius):
            # empty storage layer of neighbors
            storage_layer = []
            while len(outside_layer) > 0:
                use_sponsor = outside_layer.pop(0)
                storage_layer.extend(findNeighbors(use_sponsor[3], matrix, sponsor_history, side, step))

                for j in range(len(storage_layer)):
                    neighbor_position = find(storage_layer[j],matrix)
                    storage_layer[j][3] = neighbor_position
                    # adds the position of the newneighbors to the history list
                    sponsor_history.append(neighbor_position)

            surface_sponsors.extend(storage_layer)

            outside_layer.extend(storage_layer)
    surface_sponsors = deformSurface(surface_sponsors,matrix)             
    return surface_sponsors
