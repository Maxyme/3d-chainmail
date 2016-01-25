#this module builds the cube, and creates a list(matrixVoxel) of all the voxels positions
class Cube:
    def __init__(self):
        self.side = int(input("Enter side length of the cube (number of voxels on one side)"))
        self.step = int(input("Enter the distance between each voxel of the cube"))
        self.matrix = get_matrix(self.side, self.step)
        self.elast = float(input("Enter elasticity constant of the cube? (kr) "))
        self.stiff = float(input("Enter stiffness level [0 : " + str(self.step) + "]"))
        

def get_matrix(side, step):
    matrix_voxel = []        #initializes the list
    side = side * step       #to keep the number of voxels as the distance changes
    for z in range(0, side, step):
        step_matrix = []     #this is the floor representation of the matrix
        for y in range(0, side, step):
            for x in range(0, side, step):
                matrix_voxel.append([x, y, z])
                step_matrix.append([x, y, z])
    return matrix_voxel
