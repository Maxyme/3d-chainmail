from volume import Volume
import numpy as np


def deform_volume():
    data = np.random.random((9, 9, 9, 3))  # random RGB colors
    volume = Volume(data=data, deformation_range=(0.6, 0.6, 0.6), spacing=(0.2, 0.2, 0.2))
    deformation = np.asarray([1, 1, 3])
    deformation_index = (7, 7, 8)
    volume.deform(deformation_index, deformation)
    volume.show()
    volume.show(scatter=False)


if __name__ == '__main__':
    deform_volume()
