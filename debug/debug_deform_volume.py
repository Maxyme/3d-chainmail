from volume import Volume
import numpy as np


def deform_volume():
    data = np.random.random((7, 7, 7, 3))  # random RGB colors
    volume = Volume(data=data, deformation_range=(0.6, 0.6, 0.6), spacing=(2, 2, 2))
    deformation = np.asarray([6, 6, 5])
    deformation_index = (3, 3, 6)
    volume.deform(deformation_index, deformation)
    volume.show()
    volume.show(scatter=False)


if __name__ == '__main__':
    deform_volume()
