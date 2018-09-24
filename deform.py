"""
Deform module where 1 pixel = 1mm distance.
This is the convention when comparing voxels, so not to get the comparisons mixed up:
    ytop is above ybottom so ytop has a bigger y value than y bottom.
    xright has a bigger x value than xleft. zdown has a smaller value than z.

"""
import numpy as np


def deform(disp_src, disp_area, disp_vector, original_cube, voxel_spacing, stiffness_coef):
    """
    Deform matrix from a sponsor list

    """
    disp_dst = disp_src + disp_vector

    # Get the original sponsors
    original_sponsors = find_original_sponsors(disp_dst, disp_src, original_cube, voxel_spacing, disp_area)

    # creates the history of all the sponsor positions so they cannot be deformed
    sponsor_index_history = original_sponsors[:, -1]

    # copies the original matrix in the new matrix that will be deformed
    deformed_cube = np.copy(original_cube)

    # Updates the cube with the new deformed position
    for el in original_sponsors:
        deformed_cube[el[3]] = el[:3]

    # execute as long as there is an active sponsor
    while len(original_sponsors) > 0:
        use_sponsor = original_sponsors[0]
        original_sponsors = np.delete(original_sponsors, 0, axis=0)

        sponsor_index = use_sponsor[3]
        sponsor = original_cube[np.int(sponsor_index)]
        neighbors = find_neighbors(sponsor, original_cube, sponsor_index_history, voxel_spacing, False)

        while len(neighbors) > 0:
            use_neighbor = neighbors.pop(0)
            neighbor_index = find_index(use_neighbor[:3], original_cube)
            sponsor_index_history = np.append(sponsor_index_history, neighbor_index)

            neighbor = deform_neighbour(use_sponsor, use_neighbor[:3], use_neighbor[3], voxel_spacing, stiffness_coef)

            if neighbor:
                original_sponsors = np.vstack((original_sponsors, np.append(neighbor, neighbor_index)))
                deformed_cube[neighbor_index] = np.array(neighbor)

    return deformed_cube


def find_original_sponsors(displacement_dst, displacement_src, original_cube, step, displacement_area):
    """
    Find all original sponsors, depending on the displacement area

    """
    displacement_vector = displacement_dst - displacement_src

    # position of the original modified voxel
    sponsor_index = find_index(displacement_src, original_cube)

    # the list of sponsors to include in the deform function, includes the sponsor position also [3]
    original_sponsors = np.expand_dims(np.append(displacement_dst, sponsor_index), axis=0)

    # the list of neighbors at the layer of the radius function.  Ex for radius 1, the layer neighbor is the sponsor
    outside_layer = list(original_sponsors)

    # the sponsor_history list for a radius of 2, the new layer neighbors are the neighbors added for a radius of 1.
    # puts the sponsor position in a list so that it adds the sponsors when it looks for it
    sponsor_history = [sponsor_index]

    for i in range(displacement_area):
        storage_layer = []
        while len(outside_layer) > 0:
            index = outside_layer.pop(0)[3]
            sponsor = original_cube[index]
            neighbors = find_neighbors(sponsor, original_cube, sponsor_history, step)
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


def deform_neighbour(sponsor, neighbor, position, step, shear):
    """
    Selects the neighbour against the sponsor and returns the modified value of the neighbor
    """
    minimum = step - shear
    maximum = step + shear
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


def find_neighbors(sponsor, cube_matrix, sponsor_hist, step, surface_only=True):
    """
    Find all the neighbors of the sponsor. Will not add values outside the cube as neighbors.
    Right neighbor value=0 ; left =1; top =2; bottom = 3 down = 4, up = 5.
    Find z neighbors if not only surface neighbors
    """
    side_length = np.ceil(np.power(cube_matrix.shape[0], 1 / 3) * step)
    neighbors = []

    if sponsor[0] + step < side_length:
        rn = [sponsor[0] + step, sponsor[1], sponsor[2], 0]
        if not find_index(rn[:3], cube_matrix) in sponsor_hist:
            neighbors.append(rn)

    if sponsor[0] - step >= 0:
        ln = [sponsor[0] - step, sponsor[1], sponsor[2], 1]
        if not find_index(ln[:3], cube_matrix) in sponsor_hist:
            neighbors.append(ln)

    if sponsor[1] + step < side_length:
        tn = [sponsor[0], sponsor[1] + step, sponsor[2], 2]
        if not find_index(tn[:3], cube_matrix) in sponsor_hist:
            neighbors.append(tn)

    if sponsor[1] - step >= 0:
        bn = [sponsor[0], sponsor[1] - step, sponsor[2], 3]
        if not find_index(bn[:3], cube_matrix) in sponsor_hist:
            neighbors.append(bn)

    if not surface_only:
        if sponsor[2] - step >= 0:
            dn = [sponsor[0], sponsor[1], sponsor[2] - step, 4]
            if not find_index(dn[:3], cube_matrix) in sponsor_hist:
                neighbors.append(dn)

        if sponsor[2] + step < side_length:
            un = [sponsor[0], sponsor[1], sponsor[2] + step, 5]
            if not find_index(un[:3], cube_matrix) in sponsor_hist:
                neighbors.append(un)

    return neighbors
