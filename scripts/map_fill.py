# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025 Tiny Tapeout LTD
# Author: Uri Shaked

fill_layer_map = {
    "cfom.fill": ((23, 28), (65, 99)),
    "cp1m.fill": ((28, 28), (66, 99)),
    "cli1m.fill": ((56, 28), (67, 99)),
    "cmm1.fill": ((36, 28), (68, 99)),
    "cmm2.fill": ((41, 28), (69, 99)),
    "cmm3.fill": ((34, 28), (70, 99)),
    "cmm4.fill": ((51, 28), (71, 99)),
    "cmm5.fill": ((59, 28), (72, 99)),
}


def map_fill_layers(layout):
    for fill_layer, (original_layer, new_layer) in fill_layer_map.items():
        print(f"Moving {fill_layer} from {original_layer} to {new_layer}")

        orig_layer_num, orig_datatype = original_layer
        orig_layer_idx = layout.layer(orig_layer_num, orig_datatype)
        if not layout.is_valid_layer(orig_layer_idx):
            print(f"  Warning: Original layer {original_layer} not found, skipping...")
            continue

        new_layer_num, new_datatype = new_layer
        new_layer_idx = layout.layer(new_layer_num, new_datatype)
        layout.move_layer(orig_layer_idx, new_layer_idx)

    print("Layer mapping completed!")
