# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025 Tiny Tapeout LTD
# Author: Uri Shaked

import os
import requests
import klayout.db as pya
from shuttles import parse_rom_data, get_shuttle_info

SHUTTLE_ID = "tt06"
SEAL_RING_CELL = "advSeal_6um_gen"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp")
FINAL_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../oas"))

# Fetching the shuttle info from the index
shuttle_entry = get_shuttle_info(SHUTTLE_ID)
oas_url = shuttle_entry["gds_url"]
rom_data = parse_rom_data(shuttle_entry["rom_data"])
commit_hash = rom_data["commit"]

top_cell_name = f"{SHUTTLE_ID}_{commit_hash}"
temp_oas = os.path.join(TEMP_DIR, f"{top_cell_name}.oas")
final_oas = os.path.join(FINAL_DIR, f"{top_cell_name}.oas")

print(f"OAS URL: {oas_url}")
print(f"Commit hash: {commit_hash}")

# Download the original OAS file
response = requests.get(oas_url)
with open(temp_oas, "wb") as f:
   f.write(response.content)

print(f"Reading {temp_oas}...")
layout = user_layout = pya.Layout()
user_layout.read(temp_oas)
top_cell = layout.top_cell()
top_cell.name = top_cell_name

# Cadence won't allow "/" in cell names, so we need to rename them:
for cell in layout.each_cell():
   if "/" in cell.name:
      new_name = cell.name.replace("/", "__")
      print(f"Cell {cell.name} has '/' in its name")
      print(f"  => renaming to {new_name}")
      cell.name = new_name

# Remove the seal ring
print(f"Removing {SEAL_RING_CELL} from {temp_oas}")
seal_ring_cell = layout.cell(SEAL_RING_CELL)
assert seal_ring_cell is not None, f"Cell {SEAL_RING_CELL} not found in {temp_oas}"
seal_ring_cell.prune_cell()

# Write the modified library
print(f"Writing modified library to {final_oas}")
layout.write(final_oas)
