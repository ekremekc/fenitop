import numpy as np
from mpi4py import MPI

from fenitop.topopt import topopt
from fenitop.io_utils import XDMFReader
import dolfinx
# Read mesh 
Micca = XDMFReader("MeshDir/domain")
mesh, subdomains, facet_tags = Micca.getAll()
Micca.getInfo()

if MPI.COMM_WORLD.rank == 0:
    with dolfinx.io.XDMFFile(MPI.COMM_SELF, "MeshDir/domain.xdmf", "r") as xdmf:
        mesh_serial = xdmf.read_mesh(name="Grid")

bottom_tag = 5
from ufl import Measure
from dolfinx.fem import form
from dolfinx.fem.assemble import assemble_scalar
ds = Measure('ds', domain=mesh, subdomain_data=facet_tags)
bottom_area_form = form(1 * ds(bottom_tag))
bottom_area = assemble_scalar(bottom_area_form)

print(bottom_area)
F_bottom = 220 #N
load_traction = F_bottom/bottom_area 


fem = {  # FEA parameters
    "mesh": mesh,
    "mesh_serial": mesh_serial,
    "young's modulus": 100E6,
    "poisson's ratio": 0.25,
    "disp_bc": lambda x: np.isclose(x[2], 0.336),
    "traction_bcs": [[(0, 0, load_traction),
                     lambda x: np.isclose(x[2], 0.0)]],
    "body_force": (0, 0, 0),
    "quadrature_degree": 2,
    "petsc_options": {
        "ksp_type": "cg",
        "pc_type": "gamg",
    },
}

opt = {  # Topology optimization parameters
    "max_iter": 100,
    "opt_tol": 1e-5,
    "vol_frac": 0.08,
    "solid_zone": lambda x: np.full(x.shape[1], False),
    "void_zone": lambda x: np.full(x.shape[1], False),
    "penalty": 3.0,
    "epsilon": 1e-6,
    "filter_radius": 0.6,
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
