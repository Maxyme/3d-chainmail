"""
 deform module 1 pixel = 1mm distance.
convention: ytop is above ybottom so ytop has a bigger y value than y bottom. xright has a bigger x value than xleft. zdown has a smaller value than z.
this is the convention when comparing voxels, so not to get the comparisons mixed up.

"""


def find(voxel, matrix):
    """
    function that finds a defined voxel position in a matrix

    """
    for i in range(len(matrix)):
        if voxel[0] == matrix[i][0] and voxel[1] == matrix[i][1] and voxel[2] == matrix[i][2]:
            break
    return i


def deformRN(sponsor, candidate):                #function that deforms the right neighbor of the sponsor
    compare = candidate[:]
    if (candidate[0] - sponsor[0]) < minimum:       #[0] is for x, [1] is for y and [2] is for z
        candidate[0] = sponsor[0] + minimum         #marker is to indicate if there was a change of positions
    elif (candidate[0] - sponsor[0]) > maximum:     #new candidate list, with this candidate becoming the sponsor
        candidate[0] = sponsor[1] + maximum
    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] - shear
    elif (candidate[1] - sponsor[1]) > shear:   #here, z and y behave in the same way.
        candidate[1] = sponsor[1] + shear
    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear
    if candidate == compare:
        return 0
    else:
        return candidate


def deformLN(sponsor, candidate):                #function that deforms the LEFT neighbor of the sponsor
    compare = candidate[:]    
    if (candidate[0] - sponsor[0]) < -maximum:     #[0] is for x, [1] is for y and [2] is for z
        candidate[0] = sponsor[0] - maximum        #marker is to indicate if there was a change of positions
    elif (candidate[0] - sponsor[0]) > -minimum:    #new candidate list, with this candidate becoming the sponsor
        candidate[0] = sponsor[1] - minimum
    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] + shear
    elif (candidate[1] - sponsor[1]) > shear:   #here, z and y behave in the same way
        candidate[1] = sponsor[1] + shear
    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear
    if candidate == compare:
        return 0
    else:
        return candidate


def deformTN(sponsor, candidate):                #function that deforms the TOP neighbor of the sponsor
    compare = candidate[:]    
    if (candidate[1] - sponsor[1]) < minimum:       
        candidate[1] = sponsor[1] + minimum
    elif (candidate[1] - sponsor[1]) > maximum: #here, z and x behave in the same way (shear)
        candidate[1] = sponsor[1] + maximum  
    if (candidate[0] - sponsor[0]) < -shear:        #[0] is for x, [1] is for y and [2] is for z
        candidate[0] = sponsor[0] + shear           #marker is to indicate if there was a change of positions
    elif (candidate[0] - sponsor[0]) > shear:       #new candidate list, with this candidate becoming the sponsor
        candidate[0] = sponsor[1] + shear
    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear
    if candidate == compare:
        return 0
    else:   
        return candidate


def deformBN(sponsor, candidate):                #function that deforms the Bottom neighbor of the sponsor
    compare = candidate[:]
    if (candidate[1] - sponsor[1]) > -minimum:       
        candidate[1] = sponsor[1] - minimum
    elif (candidate[1] - sponsor[1]) < -maximum:    #here, z and x behave in the same way (shear)
        candidate[1] = sponsor[1] - maximum   
    if (candidate[0] - sponsor[0]) < -shear:        #[0] is for x, [1] is for y and [2] is for z
        candidate[0] = sponsor[0] + shear           #marker is to indicate if there was a change of positions
    elif (candidate[0] - sponsor[0]) > shear:       #new candidate list, with this candidate becoming the sponsor
        candidate[0] = sponsor[1] + shear
    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear
    if candidate == compare:
        return 0
    else:
        return candidate


def deformDN(sponsor, candidate):                #function that deforms the DOWN (in z) neighbor of the sponsor
    compare = candidate[:]    
    if (candidate[2] - sponsor[2]) > -minimum:       #[0] is for x, [1] is for y and [2] is for z
        candidate[2] = sponsor[2] - minimum         
    elif (candidate[2] - sponsor[2]) < -maximum:     
        candidate[2] = sponsor[2] - maximum
    if (candidate[0] - sponsor[0]) < -shear:
        candidate[0] = sponsor[0] + shear
    elif (candidate[0] - sponsor[0]) > shear:   #here, x and y behave in the same way
        candidate[0] = sponsor[0] + shear
    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] - shear
    elif (candidate[1] - sponsor[1]) > shear:
        candidate[1] = sponsor[1] + shear
    if candidate == compare:
        return 0
    else:
        return candidate

def findneighbors(sponsorpos,matrix,sponsorhist,side,step):
    """
    #this functions finds all the neighbors of the sponsor

    """

    neighborlist = []                                                 #it also will not add values
                                                                      #outside
                                                                                           #the cube
                                                                                           #as
                                                                                           #neighbors,
                                                                                           #and it
                                                                                           #will not
                                                                                           #add
                                                                                           #previous
                                                                                           #sponsors
    sponsor = matrix[sponsorpos]                                      #gets the original value of the sponsor
                                                                      #to find
                                                                                                      #the
                                                                                                      #neighbors
    if (sponsor[0] + step < side * step):
        rn = [sponsor[0] + step,sponsor[1],sponsor[2],0]                #the right neighbor value=0 ; left =1; top =2; bottom = 3 down
                                                                        #= 4.
        if find(rn,matrix) in sponsorhist:                          #if the right neighbor is not a previous sponsor, it
                                                                    #adds the
                                                                                                              #value to
                                                                                                              #the
                                                                                                              #neighbor
                                                                                                              #list
            1 #do nothing
        else:
            neighborlist.append(rn)                             
    if (sponsor[0] - step >= 0):
        ln = [sponsor[0] - step,sponsor[1],sponsor[2],1]
        if find(ln,matrix) in sponsorhist:
            1
        else:
            neighborlist.append(ln)                                 
    if (sponsor[1] + step < side * step):
        tn = [sponsor[0],sponsor[1] + step,sponsor[2],2]
        if find(tn,matrix) in sponsorhist:
            1
        else:
            neighborlist.append(tn)                                 
    if (sponsor[1] - step >= 0):
        bn = [sponsor[0],sponsor[1] - step,sponsor[2],3]
        if find(bn,matrix) in sponsorhist:
            1
        else:
            neighborlist.append(bn)                                 
    if (sponsor[2] - step >= 0):
        dn = [sponsor[0],sponsor[1],sponsor[2] - step,4]
        if find(dn,matrix) in sponsorhist:
            1
        else:
            neighborlist.append(dn)                                 
    return neighborlist


# this matrix selects the neighbour against the sponsor and sends them
# to the correct function it returns the modified value of the neighbor
def deform_neighbour(sponsor, neighbor):
    if neighbor[3] == 0:
        return deformRN(sponsor, neighbor)
    if neighbor[3] == 1:                            
        return deformLN(sponsor, neighbor)
    if neighbor[3] == 2:                            
        return deformTN(sponsor, neighbor)
    if neighbor[3] == 3:                            
        return deformBN(sponsor, neighbor)
    if neighbor[3] == 4:                            
        return deformDN(sponsor, neighbor)


# this updates the matrix with the new deformed position
def update_matrix(sponsor_list, new_matrix):
    for i in range(len(sponsor_list)):
        use_sponsor = sponsor_list[i]
        new_matrix[use_sponsor[3]] = use_sponsor
    return new_matrix


# creates the history of all the sponsor positions so they cannot be deformed
def build_history(sponsor_list):
    sponsor_history = []
    for i in range(len(sponsor_list)):
        sponsor_history.append(sponsor_list[i][3])
    return sponsor_history


# defines the global variables to be used in the module, in this case, the
# shear and the maximum and minimum distances of the chain.
def deform(sponsor_list, matrix, side, step, stiff):
    global minimum, maximum, shear
    minimum = step - stiff
    maximum = step + stiff
    shear = stiff

    # copies the original matrix in the new matrix that will be deformed
    new_matrix = matrix[:]
    # updates the new matrix with the positions that are not sponsors
    new_matrix = update_matrix(sponsor_list, new_matrix)
    sponsor_history = build_history(sponsor_list)
    # the loop will execute as long as there is an active sponsor
    while len(sponsor_list) > 0:
        # this takes the first element of the sponsor list and pops it out to use
        use_sponsor = sponsor_list.pop(0)
        # this function finds the neighbor voxels of the sponsor
        neighbors = (findneighbors(use_sponsor[3], matrix, sponsor_history, side, step))
        while len(neighbors) > 0:
            use_neighbor = neighbors.pop(0)
            neighbor_position = find(use_neighbor, matrix)
            use_neighbor = deform_neighbour(use_sponsor, use_neighbor)
            # this makes sure that the neighbor is not being worked on again.
            sponsor_history.append(neighbor_position)
            if use_neighbor != 0:
                # adds the position value instead of the neighbor value
                use_neighbor[3] = neighbor_position
                sponsor_list.append(use_neighbor)
                new_matrix[neighbor_position] = use_neighbor[:3]

    return new_matrix
