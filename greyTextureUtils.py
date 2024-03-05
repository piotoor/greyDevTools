#!/usr/bin/env python3.10

from PIL import Image
import numpy as np
import os
import argparse

DST_EXTENSION = ".bin"


def convert_image_to_bin_80x50(input_img, num_of_cols=32, num_of_rows=26):
    pixels = np.array(list(input_img.getdata())).reshape((num_of_rows, num_of_cols))[:num_of_rows]
    print("pixels raw = {}".format(pixels))
    screen_buffer_pixels = []
    color_buffer_pixels = []

    for r in range(0,len(pixels), 2):
        for c in range(0, len(pixels[r]), 2):
            screen_buffer_pixels.append((pixels[r + 1][c] << 4) | pixels[r + 1][c + 1])
            color_buffer_pixels.append(pixels[r][c + 1])

    sb = np.array(screen_buffer_pixels).reshape(num_of_rows // 2, num_of_cols // 2)
    cb = np.array(color_buffer_pixels).reshape(num_of_rows // 2, num_of_cols // 2)
    print("separated: \n{}\n\n{}".format(sb, cb))

    bin_screen_buffer = sb.transpose().flatten().tolist()
    bin_color_buffer = cb.transpose().flatten().tolist()

    return bin_screen_buffer, bin_color_buffer


def save_image_to_bin_files_80x50(file_path, num_of_cols, num_of_rows):
    print("Processing {}".format(file_path))
    curr_img = Image.open(file_path)
    head, tail = os.path.split(file_path)
    src_file_name, ext = os.path.splitext(tail)

    sbf, cbf = convert_image_to_bin_80x50(curr_img, num_of_cols, num_of_rows)
    print("bins: \n {} \n {}".format(sbf, cbf))
    sbf_bin_file_path = os.path.join(head, "..", src_file_name) + DST_EXTENSION
    cbf_bin_file_path = os.path.join(head, "..", src_file_name + "_b") + DST_EXTENSION

    with open(sbf_bin_file_path, 'wb') as bin_file:
        print("Saving {}...".format(sbf_bin_file_path))
        bin_file.write(bytearray(sbf))

    with open(cbf_bin_file_path, 'wb') as bin_file:
        print("Saving {}...".format(cbf_bin_file_path))
        bin_file.write(bytearray(cbf))


def merge_two_color_ram_data_segments(main, stash):
    return [m | (s << 4) for m, s in zip(main, stash)]


def generate_texture_dark_transition_map(light, dark):
    light_sr, light_cr = light
    dark_sr, dark_cr = dark

    ans = [i for i in range(16)]

    for i in range(len(light_sr)):
        lo_nibble_light = light_sr[i] & 0x0f
        hi_nibble_light = light_sr[i] >> 4
        lo_nibble_dark = dark_sr[i] & 0x0f
        hi_nibble_dark = dark_sr[i] >> 4

        if ans[lo_nibble_light] == lo_nibble_light:
            ans[lo_nibble_light] = lo_nibble_dark
        elif ans[lo_nibble_light] != lo_nibble_dark:
            raise RuntimeError("Inconsistent light-dark texture relation. Can't generate a dark transition vector")

        if ans[hi_nibble_light] == hi_nibble_light:
            ans[hi_nibble_light] = hi_nibble_dark
        elif ans[hi_nibble_light] != hi_nibble_dark:
            raise RuntimeError("Inconsistent light-dark texture relation. Can't generate a dark transition vector")
    
        if ans[light_cr] == light_cr:
            ans[light_cr] = dark_cr
        elif ans[light_cr] != dark_cr:
            raise RuntimeError("Inconsistent light-dark texture relation. Can't generate a dark transition vector")

    return ans


NUM_OF_WALL_TEXTURES_IN_MAIN_RAM = 3


def create_textures_bin_data(start_address_in_io, srs_common_wall, srs_level_walls, srs_door, crs_common_wall, crs_level_walls, crs_door):
    # srs & crs walls = L00, L01, L10, L11, L20, L21
    # compressedScreenRamLevel234Textures.bin format:
    # levels| lev sr start addr | data
    # 2 3 4 | LB HB LB HB LB HB | screen ram data

    


    level1_screen_ram_textures = [srs_walls[i] for i in range(6)]
    level1_color_ram_textures_merged_with_stash = []
    level234_bin = [2, 3, 4, ]

    for i in range(3):
        level1_color_ram_textures_merged_with_stash.append(merge_two_color_ram_data_segments(crs_walls[i], crs_walls[i + NUM_OF_WALL_TEXTURES_IN_MAIN_RAM]))

    return level1_screen_ram_textures, srs_door, level1_color_ram_textures_merged_with_stash, crs_door, level234_bin


def save_textures_bin_data(data, path):
    pass

# def save_images_to_bin_files_80x50(textures_dir, extension):
#     files_in_path = [x for x in os.listdir(textures_dir) if x.endswith(extension)]
#     for src_file in files_in_path:
#         full_src_file_path = os.path.join(textures_dir, src_file)
#         save_image_to_bin_files_80x50(full_src_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-F', '--fli',
    #                     required=False,
    #                     dest='fli',
    #                     action='store_true')
    # parser.add_argument('-q', '--hi-res',
    #                     required=False,
    #                     dest='hires',
    #                     action='store_true')
    # parser.add_argument('-s', '--single-file',
    #                     required=False,
    #                     dest='single',
    #                     action='store_true')
    # parser.add_argument('-f', '--full_size',
    #                     required=False,
    #                     dest='full_size',
    #                     action='store_true')
    parser.add_argument('path',
                        type=str)
    # parser.add_argument('-c', '--key-door-columns',
    #                     required=False,
    #                     action='store_true')
    args = parser.parse_args()

    save_image_to_bin_files_80x50(args.path, 32, 26)
