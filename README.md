Python chainmail algorithm 3d visualizer
=======

Python application for visualizing the deformation of a 3d cube using the chainmail algorithm. 

Requirements
-------------
* numpy
* matplotlib

Installation
-------------
### Install requirements with Conda
`conda env create -f environment.yml`

Running
-------
##### Change the parameters in main.py first (cube side, length, etc.) then,
`source activate chainmail`
`python debug_deform_volume.py`

Documentation
-------------
#### 3D ChainMail: a Fast Algorithm for Deforming Volumetric Objects
http://www.merl.com/publications/docs/TR96-22.pdf