#!/usr/bin/env python

import h5py as h5
import openpmd_api as opmd

# with h5py.File('ShotContainer.hdf5', 'r+') as f:
#     nxdata = f['shot_001']['Farfield']['data']
#     print(list(nxdata.attrs.keys()))
#     # del nxdata.attrs['NX_class']
#     nxdata.attrs['NX_class'] = 'NXdata'

src = "ShotContainer.hdf5"
target = "ShotContainer_openpmd.h5"

from shutil import copyfile

copyfile(src, target)

# First access this with openPMD to add fundamental openPMD structure
series = opmd.Series(target, opmd.Access.append)
# , """iteration_encoding = "variable_based" """

series.openPMD_extension = 0
series.meshes_path = ["meshes/", "/nexus_data/%/data/"]
series.write_iterations()[1]
series.close()

# Now link the NeXus data into the openPMD structure
with h5.File(target, "r+") as f:
    openpmd_data = f["data"]["1"]
    openpmd_data["nexus_data"] = f["shot_001"]

    openpmd_data.create_group("meshes")

    def init_mesh(name):
        mesh = openpmd_data["nexus_data"][name]["data"]["image"]
        dim = len(mesh.shape)
        attrs = mesh.attrs
        attrs["geometry"] = "cartesian"
        attrs["dataOrder"] = "R"
        attrs["axisLabels"] = ["x", "y"] if dim == 2 else ["x"]
        attrs["unitDimension"] = [0, 0, 0, 0, 0, 0, 0]
        attrs["unitSI"] = 1
        attrs["gridUnitSI"] = 1
        attrs["gridSpacing"] = [1 for _ in range(dim)]
        attrs["position"] = [0.5 for _ in range(dim)]
        attrs["gridGlobalOffset"] = [0 for _ in range(dim)]
        attrs["timeOffset"] = 0

        openpmd_data["meshes"][name] = mesh

    for field in ["GCCD", "MCP", "Nearfield", "Farfield", "Probe1", "Probe2", "Transmission"]:
        init_mesh(field)

series = opmd.Series(target, opmd.Access.read_write)
# # Now specify the correct metadata with openPMD
series.iterations[1].meshes["GCCD"].grid_spacing = [0.01, 0.01]
series.close()
# and so on