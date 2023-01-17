import stl
from stl import mesh
import numpy

your_mesh = mesh.Mesh.from_file('../models/original/ninja_test.stl')
your_mesh.save('ninja_test_new.stl',mode=stl.Mode.ASCII)