﻿"""
 deform module 1 pixel = 1mm distance.
convention: ytop is above ybottom so ytop has a bigger y value than y bottom. xright has a bigger x value than xleft. zdown has a smaller value than z.
this is the convention when comparing voxels, so not to get the comparisons mixed up.

"""
import numpy as np

def _find_index(voxel, matrix):
    """
    function that finds a defined voxel position in a matrix

    """
    for i in range(len(matrix)):
        if voxel[0] == matrix[i][0] and voxel[1] == matrix[i][1] and voxel[2] == matrix[i][2]:
            break
    return i


def _deform_right(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the Right (in x) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]
    if (candidate[0] - sponsor[0]) < minimum:
        candidate[0] = sponsor[0] + minimum
    elif (candidate[0] - sponsor[0]) > maximum:
        candidate[0] = sponsor[1] + maximum

    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] - shear
    elif (candidate[1] - sponsor[1]) > shear:
        candidate[1] = sponsor[1] + shear

    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear

    if candidate == compare:
        return 0
    else:
        return candidate


def _deform_left(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the Left (in x) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]    
    if (candidate[0] - sponsor[0]) < -maximum:
        candidate[0] = sponsor[0] - maximum
    elif (candidate[0] - sponsor[0]) > -minimum:
        candidate[0] = sponsor[1] - minimum

    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] + shear
    elif (candidate[1] - sponsor[1]) > shear:
        candidate[1] = sponsor[1] + shear

    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear

    if candidate == compare:
        return 0
    else:
        return candidate


def _deform_top(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the Top (in y) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]
    if (candidate[1] - sponsor[1]) < minimum:       
        candidate[1] = sponsor[1] + minimum
    elif (candidate[1] - sponsor[1]) > maximum:
        candidate[1] = sponsor[1] + maximum

    if (candidate[0] - sponsor[0]) < -shear:
        candidate[0] = sponsor[0] + shear
    elif (candidate[0] - sponsor[0]) > shear:
        candidate[0] = sponsor[1] + shear

    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear

    if candidate == compare:
        return 0
    else:   
        return candidate


def _deform_lower(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the Bottom (in y) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]
    if (candidate[1] - sponsor[1]) > -minimum:       
        candidate[1] = sponsor[1] - minimum
    elif (candidate[1] - sponsor[1]) < -maximum:
        candidate[1] = sponsor[1] - maximum   

    if (candidate[0] - sponsor[0]) < -shear:
        candidate[0] = sponsor[0] + shear
    elif (candidate[0] - sponsor[0]) > shear:
        candidate[0] = sponsor[1] + shear

    if (candidate[2] - sponsor[2]) < -shear:
        candidate[2] = sponsor[2] - shear
    elif (candidate[2] - sponsor[2]) > shear:
        candidate[2] = sponsor[2] + shear

    if candidate == compare:
        return 0
    else:
        return candidate


def _deform_down(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the DOWN (in z) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]

    if (candidate[2] - sponsor[2]) > -minimum:
        candidate[2] = sponsor[2] - minimum         
    elif (candidate[2] - sponsor[2]) < -maximum:     
        candidate[2] = sponsor[2] - maximum

    if (candidate[0] - sponsor[0]) < -shear:
        candidate[0] = sponsor[0] + shear
    elif (candidate[0] - sponsor[0]) > shear:
        candidate[0] = sponsor[0] + shear

    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] - shear
    elif (candidate[1] - sponsor[1]) > shear:
        candidate[1] = sponsor[1] + shear

    if candidate == compare:
        return 0
    else:
        return candidate

def _deform_up(sponsor, candidate, step, stiffness_coef):
    """
    Deforms the UP (in z) neighbor of the sponsor

    """
    minimum = step - stiffness_coef
    maximum = step + stiffness_coef
    shear = stiffness_coef
    compare = candidate[:]

    if (candidate[2] - sponsor[2]) > minimum:
        candidate[2] = sponsor[2] + minimum
    elif (candidate[2] - sponsor[2]) > maximum:
        candidate[2] = sponsor[2] + maximum

    if (candidate[0] - sponsor[0]) < -shear:
        candidate[0] = sponsor[0] + shear
    elif (candidate[0] - sponsor[0]) > shear:
        candidate[0] = sponsor[0] + shear

    if (candidate[1] - sponsor[1]) < -shear:
        candidate[1] = sponsor[1] - shear
    elif (candidate[1] - sponsor[1]) > shear:
        candidate[1] = sponsor[1] + shear

    if candidate == compare:
        return 0
    else:
        return candidate


# this matrix selects the neighbour against the sponsor and sends them
# to the correct function it returns the modified value of the neighbor
def _deform_neighbour(sponsor, neighbor, step, stiffness_coef):

    if neighbor[3] == 0:
        return _deform_right(sponsor, neighbor, step, stiffness_coef)
    elif neighbor[3] == 1:
        return _deform_left(sponsor, neighbor, step, stiffness_coef)
    elif neighbor[3] == 2:
        return _deform_top(sponsor, neighbor, step, stiffness_coef)
    elif neighbor[3] == 3:
        return _deform_lower(sponsor, neighbor, step, stiffness_coef)
    elif neighbor[3] == 4:
        return _deform_down(sponsor, neighbor, step, stiffness_coef)
    elif neighbor[3] == 5:
        return _deform_up(sponsor, neighbor, step, stiffness_coef)


# this updates the matrix with the new deformed position
def _update_matrix(sponsor_list, new_matrix):
    for el in sponsor_list:
        new_matrix[el[3]] = el

    return new_matrix


# creates the history of all the sponsor positions so they cannot be deformed
def _build_history(sponsor_list):
    sponsor_history = []
    for el in sponsor_list:
        sponsor_history.append(el[3])

    return sponsor_history


def _find_neighbors(sponsor, matrix, sponsor_hist, side, step, surface_only):
    """
    this functions finds all the neighbors of the sponsor, it requires the variable step and side variables
    add previous sponsors, gets the original value of the sponsor to find the neighbors
    it also will not add values outside the cube as neighbors, and it will not

    """
    neighbors = []

    # the right neighbor value=0 ; left =1; top =2; bottom = 3 down = 4.
    if sponsor[0] + step < side * step:
        rn = [sponsor[0] + step, sponsor[1], sponsor[2], 0]
        # if the right neighbor is not a previous sponsor, it adds the value to the neighbor list
        if not _find_index(rn, matrix) in sponsor_hist:
            neighbors.append(rn)

    if sponsor[0] - step >= 0:
        ln = [sponsor[0] - step, sponsor[1], sponsor[2], 1]
        if not _find_index(ln, matrix) in sponsor_hist:
            neighbors.append(ln)

    if sponsor[1] + step < side * step:
        tn = [sponsor[0], sponsor[1] + step, sponsor[2], 2]
        if not _find_index(tn, matrix) in sponsor_hist:
            neighbors.append(tn)

    if sponsor[1] - step >= 0:
        bn = [sponsor[0], sponsor[1] - step, sponsor[2], 3]
        if not _find_index(bn, matrix) in sponsor_hist:
            neighbors.append(bn)

    # find z neighbors only if not finding surface neighbors
    if sponsor[2] - step >= 0 and not surface_only:
        dn = [sponsor[0], sponsor[1], sponsor[2] - step, 4]
        if not _find_index(dn, matrix) in sponsor_hist:
            neighbors.append(dn)

    if sponsor[2] + step < side * step and not surface_only:
        dn = [sponsor[0], sponsor[1], sponsor[2] + step, 5]
        if not _find_index(dn, matrix) in sponsor_hist:
            neighbors.append(dn)

    return neighbors


def _deform_surface(displacement_vector, surface_list):
    """
    Deforms the surface found (all the neighbors) according to the vector of deformation applied to the sponsor

    """
    # applies the deformation to the entire surface list of sponsor/neighbors
    for el in surface_list:
        el[0] = el[0] + displacement_vector[0]
        el[1] = el[1] + displacement_vector[1]
        el[2] = el[2] + displacement_vector[2]

    return surface_list


def deform(sponsor_list, original_cube, side, step, stiffness_coef):
    """
    deform matrix from a sponsor list

    """

    # copies the original matrix in the new matrix that will be deformed
    new_matrix = original_cube[:]
    # updates the new matrix with the positions that are not sponsors
    new_matrix = _update_matrix(sponsor_list, new_matrix)
    sponsor_history = _build_history(sponsor_list)
    # the loop will execute as long as there is an active sponsor
    while len(sponsor_list) > 0:
        use_sponsor = sponsor_list.pop(0)
        sponsor = original_cube[use_sponsor[3]]
        neighbors = _find_neighbors(sponsor, original_cube, sponsor_history, side, step, False)

        while len(neighbors) > 0:
            use_neighbor = neighbors.pop(0)
            neighbor_position = _find_index(use_neighbor, original_cube)
            use_neighbor = _deform_neighbour(use_sponsor, use_neighbor, step, stiffness_coef)
            sponsor_history.append(neighbor_position)

            if use_neighbor != 0:
                # adds the position value instead of the neighbor value
                use_neighbor[3] = neighbor_position
                sponsor_list.append(use_neighbor)
                new_matrix[neighbor_position] = np.array(use_neighbor[:3])

    return new_matrix

def find_surface_sponsors(displacement_dst, displacement_src, original_cube, side, step, displacement_area):
    """
    Find all surface sponsors, depending on the displacement area

    """
    # position of the original modified voxel
    sponsor_index = _find_index(displacement_src, original_cube)
    # the list of sponsors to include in the deform function, includes the sponsor position also [3]
    surface_sponsors = [np.append(displacement_dst, sponsor_index)]

    # the list of neighbors at the layer of the radius function.  Ex for radius 1, the layer neighbor is the sponsor
    outside_layer = surface_sponsors

    # the sponsor_history list for a radius of 2, the new layer neighbors are the neighbors added for a radius of 1.
    # puts the sponsor position in a list so that it adds the sponsors when it looks for it
    sponsor_history = [sponsor_index]

    for i in range(displacement_area):
        # empty storage layer of neighbors
        storage_layer = []
        while len(outside_layer) > 0:
            index = outside_layer.pop(0)[3]
            sponsor = original_cube[index]
            neighbors = _find_neighbors(sponsor, original_cube, sponsor_history, side, step, True)
            storage_layer.extend(neighbors)

            # Find and add the position of the new neighbors to the history list
            for el in storage_layer:
                el[3] = _find_index(el, original_cube)
                sponsor_history.append(el[3])

        surface_sponsors.extend(storage_layer)
        outside_layer.extend(storage_layer)

    displacement_vector = np.subtract(displacement_dst, displacement_src)
    surface_sponsors = _deform_surface(displacement_vector, surface_sponsors)
    return surface_sponsors

