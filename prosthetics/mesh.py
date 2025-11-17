import gmsh
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))

filename = "domain2"

geomDir = os.path.join(dir_path, 'GeomDir')
meshDir = os.path.join(dir_path, 'MeshDir')

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add(filename)
gmsh.option.setString("Geometry.OCCTargetUnit", "M")


gmsh.model.occ.importShapes(os.path.join(geomDir, filename + ".step"))
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

# lc = 0.0080
lc = 0.003

# led_tag = 2

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

sur_tags = gmsh.model.getEntities(dim=2)

vol_tags = gmsh.model.getEntities(dim=3)

for surface in sur_tags:
    gmsh.model.addPhysicalGroup(2, [surface[1]], tag=surface[1])

for volume in vol_tags:
    gmsh.model.addPhysicalGroup(3, [volume[1]], tag=volume[1])

gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.write("{}.msh".format(meshDir + "/" + filename))
gmsh.write("{}.stl".format(meshDir + "/" + filename))

gmsh.finalize()

from fenitop.io_utils import write_xdmf_mesh

write_xdmf_mesh(meshDir+"/"+filename, dimension=3)