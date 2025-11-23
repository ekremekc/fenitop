import numpy as np
from mpi4py import MPI

from fenitop.topopt import topopt
from fenitop.io_utils import XDMFReader
import dolfinx
# Read mesh 
filename = 'Model_updated_V2_meters'
Topology = XDMFReader("MeshDir/"+filename)
mesh, subdomains, facet_tags = Topology.getAll()
Topology.getInfo()

if MPI.COMM_WORLD.rank == 0:
    with dolfinx.io.XDMFFile(MPI.COMM_SELF, "MeshDir/"+filename+".xdmf", "r") as xdmf:
        mesh_serial = xdmf.read_mesh(name="Grid")
else:
    mesh_serial = None

from ufl import Measure
from dolfinx.fem import form
from dolfinx.fem.assemble import assemble_scalar

# bottom_tag = 5 # 5 for domain, 29 for domain2
# ds = Measure('ds', domain=mesh, subdomain_data=facet_tags)
# bottom_area_form = form(1 * ds(bottom_tag))
# bottom_area = assemble_scalar(bottom_area_form)
# print(bottom_area)

F_bottom = 220 #N
F_point = np.array([[0.54], [-0.066], [0.052]])
load_traction = F_bottom

rho = 1010 #kg/m^3

fem = {  # FEA parameters
    "mesh": mesh,
    "mesh_serial": mesh_serial,
    "young's modulus": 2.4E6,
    "poisson's ratio": 0.25,
    "disp_bc": lambda x: np.less_equal(x[0], 0.007147328651994162),
    "traction_bcs": [[(-4318, 823.8, 863.6),
                     lambda x, tol=1e-2: np.isclose(x, F_point, atol=tol).all(axis=0)]],
    "body_force": (0, 0, 0),
    "quadrature_degree": 2,
    "petsc_options": {
        "ksp_type": "cg",
        "pc_type": "gamg",
    },
}

opt = {  # Topology optimization parameters
    "max_iter": 10,
    "opt_tol": 1e-5,
    "vol_frac": 0.2,
    "solid_zone": lambda x: np.less(x[0], 0.01),
    "void_zone": lambda x: np.full(x.shape[1], False),
    "penalty": 3.0,
    "epsilon": 1e-6,
    "filter_radius": 0.006,
    "beta_interval": 50,
    "beta_max": 128,
    "use_oc": True,
    "move": 0.02,
    "opt_compliance": True,
}

if __name__ == "__main__":
    topopt(fem, opt)

# Execute the code in parallel:
# mpirun -n 8 python3 scripts/beam_3d.py
