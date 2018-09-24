"""
Deform module where 1 pixel = 1mm distance.
This is the convention when comparing voxels, so not to get the comparisons mixed up:
    ytop is above ybottom so ytop has a bigger y value than y bottom.
    xright has a bigger x value than xleft. zdown has a smaller value than z.

"""
import numpy as np


def deform(disp_src, disp_area, disp_vector, original_cube, spacing, stiffness_coef):
    """
    Deform matrix from a sponsor list

    """
    # Get the displacement sponsor voxels
    sponsors = find_sponsors(disp_src, disp_vector, original_cube, spacing, disp_area)

    # creates the history of all the sponsor positions so they cannot be deformed
    sponsor_index_history = sponsors[:, -1]

    # copies the original matrix in the new matrix that will be deformed
    deformed_cube = np.copy(original_cube)

    # Updates the cube with the new deformed position
    for el in sponsors:
        deformed_cube[el[3]] = el[:3]

    # execute as long as there is an active sponsor
    while len(sponsors) > 0:
        use_sponsor = sponsors[0]
        sponsors = np.delete(sponsors, 0, axis=0)

        sponsor_index = use_sponsor[3]
        sponsor = original_cube[np.int(sponsor_index)]
        neighbors = find_neighbors(sponsor, original_cube, sponsor_index_history, spacing)

        while len(neighbors) > 0:
            use_neighbor = neighbors.pop(0)
            neighbor_index = find_index(use_neighbor[:3], original_cube)
            sponsor_index_history = np.append(sponsor_index_history, neighbor_index)

            neighbor = deform_neighbour(use_sponsor, use_neighbor[:3], use_neighbor[3], spacing, stiffness_coef)

            if neighbor:
                sponsors = np.vstack((sponsors, np.append(neighbor, neighbor_index)))
                deformed_cube[neighbor_index] = np.array(neighbor)

    return deformed_cube


def find_sponsors(displacement_src, displacement_vector, original_cube, spacing, displacement_area):
    """
    Find all original sponsors, depending on the displacement area

    """
    # position of the original modified voxel
    sponsor_index = find_index(displacement_src, original_cube)

    # the list of sponsors to include in the deform function, includes the sponsor position also [3]
    displacement_dst = displacement_src + displacement_vector
    original_sponsors = np.expand_dims(np.append(displacement_dst, sponsor_index), axis=0)

    # the list of neighbors at the layer of the radius function.  Ex for radius 1, the layer neighbor is the sponsor
    outside_layer = list(original_sponsors)

    # the sponsor_history list for a radius of 2, the new layer neighbors are the neighbors added for a radius of 1.
    # puts the sponsor position in a list so that it adds the sponsors when it looks for it
    sponsor_history = [sponsor_index]

    for i in range(displacement_area):
        storage_layer = []
        while outside_layer:
            index = outside_layer.pop(0)[3]
            sponsor = original_cube[index]
            neighbors = find_neighbors(sponsor, original_cube, sponsor_history, spacing)
            storage_layer = storage_layer + neighbors

            # Find and add the position of the new neighbors to the history list
            for el in storage_layer:
                el[3] = find_index(el[:3], original_cube)
                sponsor_history.append(el[3])

        original_sponsors = np.append(storage_layer, original_sponsors, axis=0)
        outside_layer.extend(storage_layer)

    # apply displacement vector to sponsors
    original_sponsors[:, :3] += displacement_vector

    return original_sponsors


def find_index(voxel, matrix):
    """
    function that finds a defined voxel position in a matrix

    """
    return np.where(np.all(matrix == voxel, axis=1))[0][0]


def deform_neighbour(sponsor, neighbor, position, spacing, shear):
    """
    Selects the neighbour against the sponsor and returns the modified value of the neighbor
    """
    minimum = spacing - shear
    maximum = spacing + shear
    compare = sponsor[:]
    
    if position == 0:  # Deforms the right (in x) neighbor of the sponsor
        if neighbor[0] - sponsor[0] < minimum:
            neighbor[0] = sponsor[0] + minimum
        elif neighbor[0] - sponsor[0] > maximum:
            neighbor[0] = sponsor[1] + maximum

        if neighbor[1] - sponsor[1] < -shear:
            neighbor[1] = sponsor[1] - shear
        elif neighbor[1] - sponsor[1] > shear:
            neighbor[1] = sponsor[1] + shear

        if neighbor[2] - sponsor[2] < -shear:
            neighbor[2] = sponsor[2] - shear
        elif neighbor[2] - sponsor[2] > shear:
            neighbor[2] = sponsor[2] + shear

    elif position == 1:  # Deforms the left (in x) neighbor of the sponsor
        if neighbor[0] - sponsor[0] < -maximum:
            neighbor[0] = sponsor[0] - maximum
        elif neighbor[0] - sponsor[0] > -minimum:
            neighbor[0] = sponsor[1] - minimum

        if neighbor[1] - sponsor[1] < -shear:
            neighbor[1] = sponsor[1] + shear
        elif neighbor[1] - sponsor[1] > shear:
            neighbor[1] = sponsor[1] + shear

        if neighbor[2] - sponsor[2] < -shear:
            neighbor[2] = sponsor[2] - shear
        elif neighbor[2] - sponsor[2] > shear:
            neighbor[2] = sponsor[2] + shear
    
    elif position == 2:  # Deforms the top (in y) neighbor of the sponsor
        if neighbor[1] - sponsor[1] < minimum:
            neighbor[1] = sponsor[1] + minimum
        elif neighbor[1] - sponsor[1] > maximum:
            neighbor[1] = sponsor[1] + maximum

        if neighbor[0] - sponsor[0] < -shear:
            neighbor[0] = sponsor[0] + shear
        elif neighbor[0] - sponsor[0] > shear:
            neighbor[0] = sponsor[1] + shear

        if neighbor[2] - sponsor[2] < -shear:
            neighbor[2] = sponsor[2] - shear
        elif neighbor[2] - sponsor[2] > shear:
            neighbor[2] = sponsor[2] + shear
            
    elif position == 3:  # Deforms the bottom (in y) neighbor of the sponsor
        if neighbor[1] - sponsor[1] > -minimum:
            neighbor[1] = sponsor[1] - minimum
        elif neighbor[1] - sponsor[1] < -maximum:
            neighbor[1] = sponsor[1] - maximum

        if neighbor[0] - sponsor[0] < -shear:
            neighbor[0] = sponsor[0] + shear
        elif neighbor[0] - sponsor[0] > shear:
            neighbor[0] = sponsor[1] + shear

        if neighbor[2] - sponsor[2] < -shear:
            neighbor[2] = sponsor[2] - shear
        elif neighbor[2] - sponsor[2] > shear:
            neighbor[2] = sponsor[2] + shear
            
    elif position == 4:  # # Deforms the down (in z) neighbor of the sponsor
        if neighbor[2] - sponsor[2] > -minimum:
            neighbor[2] = sponsor[2] - minimum
        elif neighbor[2] - sponsor[2] < -maximum:
            neighbor[2] = sponsor[2] - maximum

        if neighbor[0] - sponsor[0] < -shear:
            neighbor[0] = sponsor[0] + shear
        elif neighbor[0] - sponsor[0] > shear:
            neighbor[0] = sponsor[0] + shear

        if neighbor[1] - sponsor[1] < -shear:
            neighbor[1] = sponsor[1] - shear
        elif neighbor[1] - sponsor[1] > shear:
            neighbor[1] = sponsor[1] + shear
    
    elif position == 5:  # Deforms the up (in z) neighbor of the sponsor
        if neighbor[2] - sponsor[2] > minimum:
            neighbor[2] = sponsor[2] + minimum
        elif neighbor[2] - sponsor[2] > maximum:
            neighbor[2] = sponsor[2] + maximum

        if neighbor[0] - sponsor[0] < -shear:
            neighbor[0] = sponsor[0] + shear
        elif neighbor[0] - sponsor[0] > shear:
            neighbor[0] = sponsor[0] + shear

        if neighbor[1] - sponsor[1] < -shear:
            neighbor[1] = sponsor[1] - shear
        elif neighbor[1] - sponsor[1] > shear:
            neighbor[1] = sponsor[1] + shear

    return 0 if np.array_equal(compare, neighbor) else neighbor


def find_neighbors(sponsor, cube_matrix, sponsor_hist, spacing):
    """
    Find all the neighbors of the sponsor. Will not add values outside the cube as neighbors.
    Right neighbor value=0 ; left =1; top =2; bottom = 3 down = 4, up = 5.
    """
    side_length = np.ceil(np.power(cube_matrix.shape[0], 1 / 3) * spacing)
    neighbors = []

    if sponsor[0] + spacing < side_length:
        rn = [sponsor[0] + spacing, sponsor[1], sponsor[2], 0]
        try:
            if not find_index(rn[:3], cube_matrix) in sponsor_hist:
                neighbors.append(rn)
        except IndexError:
            pass

    if sponsor[0] - spacing >= 0:
        ln = [sponsor[0] - spacing, sponsor[1], sponsor[2], 1]
        try:
            if not find_index(ln[:3], cube_matrix) in sponsor_hist:
                neighbors.append(ln)
        except IndexError:
            pass

    if sponsor[1] + spacing < side_length:
        tn = [sponsor[0], sponsor[1] + spacing, sponsor[2], 2]
        try:
            if not find_index(tn[:3], cube_matrix) in sponsor_hist:
                neighbors.append(tn)
        except IndexError:
            pass

    if sponsor[1] - spacing >= 0:
        bn = [sponsor[0], sponsor[1] - spacing, sponsor[2], 3]
        try:
            if not find_index(bn[:3], cube_matrix) in sponsor_hist:
                neighbors.append(bn)
        except IndexError:
            pass

    if sponsor[2] - spacing >= 0:
        dn = [sponsor[0], sponsor[1], sponsor[2] - spacing, 4]
        try:
            if not find_index(dn[:3], cube_matrix) in sponsor_hist:
                neighbors.append(dn)
        except IndexError:
            pass

    if sponsor[2] + spacing < side_length:
        un = [sponsor[0], sponsor[1], sponsor[2] + spacing, 5]
        try:
            if not find_index(un[:3], cube_matrix) in sponsor_hist:
                neighbors.append(un)
        except IndexError:
            pass

    return neighbors
