#Gets data from the user such as the position of the displacement and the
#(x,y,z) values of the displacement vector as well as the original position of the displacement vector.

class Force:
    def __init__(self,get_cube):
        self.posx = int(input("Enter x position of the force (according to matrix positions given)"))
        self.posy = int(input("Enter y position of the force"))
        self.posz = int(input("Enter Z position of the force = " + str(get_cube.side*get_cube.step-get_cube.step)))  #to be modified if deformation inside cubic volume are allowed
        self.x = float(input("Enter new x position of sponsor: [" + str(self.posx-get_cube.step)+ ":" + str(self.posx+get_cube.step)+ "]"))
        self.y = float(input("Enter new y position of sponsor: [" + str(self.posy-get_cube.step)+ ":" + str(self.posy+get_cube.step)+ "]"))
        self.z = float(input("Enter new z position of sponsor: [" + str(self.posz-get_cube.step)+ ":" + str(self.posz+get_cube.step)+ "]"))
        self.rad = int(input("Enter the radius of action [0 : "+ str(get_cube.side)))
        
def forcefeedback(oldmatrix,newmatrix,elast): #this function calculates the force according to the sum of all the small displacements
    diff_x = 0.0
    diff_y = 0.0
    diff_z = 0.0
    for i in range(len(oldmatrix)):     #this goes through both matrices and compares the distances between the voxels
        for j in range(3):              #goes through 0:x,1:y,2:z
            if j == 0:
                diff_x = diff_x + (oldmatrix[i][j]-newmatrix[i][j])
            elif j == 1:
                diff_y = diff_y + (oldmatrix[i][j]-newmatrix[i][j])
            elif j == 2:
                diff_z = diff_z + (oldmatrix[i][j]-newmatrix[i][j])
    diff_x = diff_x * elast
    diff_y = diff_y * elast
    diff_z = diff_z * elast
    force_vector = [diff_x,diff_y,diff_z]
    return force_vector
