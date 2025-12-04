#!/usr/bin/env python3
import argparse
import json
import sys

import stlmesh
import slicer as slicer_mod  # the slicer module from the repo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stl", required=True, help="Path to STL file")
    parser.add_argument("--layer-height", type=float, required=True, help="Layer height in mm")
    args = parser.parse_args()

    stl_file = args.stl
    delta = args.layer_height

    # 1) Load mesh from STL
    mesh = stlmesh.stlmesh(stl_file)

    # 2) Create slicer
    P = None       # no explicit planes
    srt = False    # planes not pre-sorted
    mesh_slicer = slicer_mod.slicer(mesh.triangles, P, delta, srt)

    # 3) Run slicing
    mesh_slicer.incremental_slicing()

    layers_out = []

    for i, z in enumerate(mesh_slicer.P):
        if i >= len(mesh_slicer.planes):
            continue

        plane_polys = []
        for poly in mesh_slicer.planes[i]:
            coords = []
            for v in poly.vertices:
                c = v.coord  # numpy array [x, y, z]
                coords.append([float(c[0]), float(c[1]), float(c[2])])

            if len(coords) >= 3:
                plane_polys.append(coords)

        layers_out.append({
            "z": float(z),
            "polygons": plane_polys,
        })

    result = {
        "layers": layers_out,
    }

    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
