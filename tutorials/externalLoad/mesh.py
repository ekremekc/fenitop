import gmsh
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))

filename = "domain"

meshDir = os.path.join(dir_path, 'MeshDir')

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add(filename)

# lc = 0.0080
lc = 0.5

Lx = 45
Ly = 30

rectangle = gmsh.model.occ.addRectangle(0,0,0, Lx, Ly)
hole = gmsh.model.occ.addDisk(Ly/2, Lx/3, 0, Ly/3, Ly/3)

print(rectangle)
print(hole)
geometry = gmsh.model.occ.cut([(2, rectangle)], [(2, hole)])

gmsh.model.occ.synchronize()

# Mesh refinement
# gmsh.model.mesh.field.add("Constant", 1)
# gmsh.model.mesh.field.setNumbers(1, "VolumesList", [led_tag])
# gmsh.model.mesh.field.setNumber(1, "VIn", lc / 10)
# gmsh.model.mesh.field.setNumber(1, "VOut", lc)

# gmsh.model.mesh.field.setAsBackgroundMesh(1)

gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.option.setNumber("Mesh.Algorithm3D", 10)
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)
gmsh.model.mesh.generate(3)

line_tags = gmsh.model.occ.getEntities(dim=1)

surface_tags = gmsh.model.occ.getEntities(dim=2)

for line in line_tags:
    gmsh.model.addPhysicalGroup(1, [line[1]], tag=line[1])

for surface in surface_tags:
    gmsh.model.addPhysicalGroup(2, [surface[1]], tag=surface[1])

gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.write("{}.msh".format(meshDir + "/" + filename))
gmsh.write("{}.stl".format(meshDir + "/" + filename))

gmsh.finalize()

from fenitop.io_utils import write_xdmf_mesh

write_xdmf_mesh(meshDir+"/"+filename, dimension=2)