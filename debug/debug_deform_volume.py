from volume import Volume
import numpy as np


def deform_volume():
    volume = Volume(data=np.random.random((7, 7, 7)), deformation_range=(0.6, 0.6, 0.6), spacing=(2, 2, 2))
    deformation = np.asarray([6, 6, 5])
    deformation_index = (3, 3, 6)
    volume.deform(deformation_index, deformation)
    volume.show()


if __name__ == '__main__':
    deform_volume()
