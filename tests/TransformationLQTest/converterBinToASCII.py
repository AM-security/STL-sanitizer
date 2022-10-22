import stl
from stl import mesh
import numpy

your_mesh = mesh.Mesh.from_file('untitled.stl')
your_mesh.save('3dascii.stl',mode=stl.Mode.ASCII)