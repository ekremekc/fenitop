import numpy as np
from mpi4py import MPI
import dolfinx.io
from fenitop.topopt import topopt


with dolfinx.io.XDMFFile(MPI.COMM_WORLD, "MeshDir/domain.xdmf", "r") as xdmf:
    mesh = xdmf.read_mesh(name="Grid")
if MPI.COMM_WORLD.rank == 0:
    with dolfinx.io.XDMFFile(MPI.COMM_SELF, "MeshDir/domain.xdmf", "r") as xdmf:
        mesh_serial = xdmf.read_mesh(name="Grid")
else:
    mesh_serial = None

Lx, Ly = 45, 30

fem = {  # FEM parameters
    "mesh": mesh,
    "mesh_serial": mesh_serial,
    "young's modulus": 1.0,
    "poisson's ratio": 0.3,
    "disp_bc": lambda x: np.isclose(x[0], 0),
    "traction_bcs": [[(0, -1),
                      lambda x: (np.isclose(x[0], Lx) & np.greater_equal(x[1], 0) & np.less(x[1], 3))]],
    "body_force": (0, 0),
    "quadrature_degree": 2,
    "petsc_options": {
        "ksp_type": "cg",
        "pc_type": "gamg",
    },
}

opt = {  # Topology optimization parameters
    "max_iter": 200,
    "opt_tol": 1e-5,
    "vol_frac": 0.5,
    "solid_zone": lambda x: np.full(x.shape[1], False),
    "void_zone": lambda x: np.full(x.shape[1], False),
    "penalty": 3.0,
    "epsilon": 1e-6,
    "filter_radius": 1.5,
    "beta_interval": 50,
    "beta_max": 128,
    "use_oc": True,
    "move": 0.02,
    "opt_compliance": True,
}

if __name__ == "__main__":
    topopt(fem, opt)

# Execute the code in parallel:
# mpirun -n 8 python3 scripts/beam_2d.py
