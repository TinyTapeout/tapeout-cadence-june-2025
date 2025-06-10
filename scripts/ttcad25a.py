# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025 Tiny Tapeout LTD
# Author: Uri Shaked

import os
import klayout.db as pya
from map_fill import map_fill_layers

SHUTTLE_ID = "ttcad25a"
SEAL_RING_CELL = "advSeal_6um_gen"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp")
FINAL_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../oas"))

# GDS run: https://github.com/TinyTapeout/tinytapeout-cad-25a/actions/runs/15550104754
# Precheck run: https://github.com/TinyTapeout/tinytapeout-cad-25a/actions/runs/15551439891
commit_hash = "734c1d4e"

top_cell_name = f"{SHUTTLE_ID}_{commit_hash}"
temp_oas = os.path.join(TEMP_DIR, f"{top_cell_name}.oas")
final_oas = os.path.join(FINAL_DIR, f"{top_cell_name}.oas")

print(f"Commit hash: {commit_hash}")

print(f"Reading {temp_oas}...")
layout = user_layout = pya.Layout()
user_layout.read(temp_oas)
top_cell = layout.top_cell()
top_cell.name = top_cell_name

# Remove the seal ring
print(f"Removing {SEAL_RING_CELL} from {temp_oas}")
seal_ring_cell = layout.cell(SEAL_RING_CELL)
assert seal_ring_cell is not None, f"Cell {SEAL_RING_CELL} not found in {temp_oas}"
seal_ring_cell.prune_cell()

print(f"Mapping fill layers...")
map_fill_layers(layout)

# Write the modified library
print(f"Writing modified library to {final_oas}")
layout.write(final_oas)
