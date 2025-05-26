# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025 Tiny Tapeout LTD
# Author: Uri Shaked

import requests

def get_shuttle_info(shuttle_id: str):
  """
  Get the shuttle info for a given shuttle id.
  """
  shuttle_index = requests.get("https://index.tinytapeout.com/").json()
  shuttle_entry = next(filter(lambda x: x["id"] == shuttle_id, shuttle_index["shuttles"]))
  return shuttle_entry

def parse_rom_data(rom_data: str) -> dict[str, str]:
  """
  Parse the rom_data string into a dictionary of {key: value} pairs.
  """
  rom_data = rom_data.split("\n")
  rom_data = [line.split("=") for line in rom_data if "=" in line]
  rom_data = {key: value for key, value in rom_data}
  return rom_data


