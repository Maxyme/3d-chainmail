Python 2.7 DICOM Viewer
=======

Python 2.7 DICOM Viewer is a python application for reading and annotating [DICOM](http://medical.nema.org/) files. 

The annotations created with the application can be saved to a JSON file for analysis.  

Requirements
-------------
* numpy

* pydicom

Limitations
-------------
File export is limited to .ps files (ghostscript) for the time being.

Installation
-------------
### Install pydicom with conda
#### Linux 64
conda install -c https://conda.anaconda.org/lukepfister pydicom
#### Win 64
conda install -c https://conda.anaconda.org/eelcohoogendoorn pydicom
** if this doesn't work, copy the pydicom installation folder (included as zip) to your python site-package folder

### Install dateutil which includes an installation of six
conda install dateutil

Documentation
-------------
pydicom [documentation](https://pydicom.readthedocs.org/en/latest/).
