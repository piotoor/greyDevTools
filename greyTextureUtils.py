#!/usr/bin/env python3.10

from PIL import Image
import numpy as np
import os
import argparse

DST_EXTENSION = ".bin"


def convert_image_to_bin_80x50(input_img, num_of_cols=32):
    pixels = np.array(list(input_img.getdata())).reshape((26, num_of_cols))[:26]
    print("pixels raw = {}".format(pixels))
    screen_buffer_pixels = []
    color_buffer_pixels = []

    for r in range(0,len(pixels), 2):
        for c in range(0, len(pixels[r]), 2):
            screen_buffer_pixels.append((pixels[r + 1][c] << 4) | pixels[r + 1][c + 1])
            color_buffer_pixels.append(pixels[r][c + 1])

    sb = np.array(screen_buffer_pixels).reshape(13, num_of_cols // 2)
    cb = np.array(color_buffer_pixels).reshape(13, num_of_cols // 2)
    print("separated: \n{}\n\n{}".format(sb, cb))

    bin_screen_buffer = sb.transpose().flatten().tolist()
    bin_color_buffer = cb.transpose().flatten().tolist()

    return bin_screen_buffer, bin_color_buffer


def save_image_to_bin_files_80x50(file_path, num_of_cols):
    print("Processing {}".format(file_path))
    curr_img = Image.open(file_path)
    head, tail = os.path.split(file_path)
    src_file_name, ext = os.path.splitext(tail)

    sbf, cbf = convert_image_to_bin_80x50(curr_img, num_of_cols)
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


def create_campaign_bin_files(start_address_in_io, start_address_in_color_ram_textures, srs, crs):
    # returns both campaign.bin file and level1 textures in folders, color ram data merged
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

    save_image_to_bin_files_80x50(args.path, 6)
