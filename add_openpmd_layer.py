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
series.write_iterations()[1]
series.close()

# Now link the NeXus data into the openPMD structure
with h5.File(target, "r+") as f:
    openpmd_data = f["data"]["1"]
    openpmd_data["nexus_data"] = f["shot_001"]

# Reopen in openPMD, openPMD now sees the NeXus data and can use it
series = opmd.Series(target, opmd.Access.read_write)
iteration = series.iterations[1]


def print_hierarchy(obj, indent=""):
    for key in obj:
        print("{}{}".format(indent, key))
        print_hierarchy(obj[key], "\t" + indent)


def copy_field(name):
    field_o = iteration.meshes[name]
    field_i = iteration["nexus_data"][name]["data"].as_container_of_datasets()["image"]

    field_o.reset_dataset(opmd.Dataset(field_i.dtype, field_i.shape))
    field_o.axis_labels = ["x", "y"]
    field_o.unit_dimension = {opmd.Unit_Dimension.M: 1, opmd.Unit_Dimension.T: -1}
    field_o.grid_global_offset = [0, 0]
    field_o.grid_spacing = [1, 1]
    field_o.grid_unit_SI = 1
    field_o.position = [0.5, 0.5]
    field_o.unit_SI = 1

    # copy data for now, far goal: use links in openPMD

    # read data
    chunk = field_i[:, :]
    series.flush()

    # write data
    field_o[:, :] = chunk[:, :]
    series.flush()


for field in ["GCCD", "MCP", "Nearfield", "Probe1", "Probe2", "Transmission"]:
    copy_field(field)
