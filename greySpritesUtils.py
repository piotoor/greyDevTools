#!/usr/bin/env python3.10

import argparse
import os
import utilities
from utilities import greyLogger
import logging

scaledFrameData = (
    (0, 63),
    (3, 57),
    (6, 51),
    (9, 45),
    (15, 33),
    (18, 27),
    (24, 15),
)

scaledFrameDataResolution = (
    (12, 21),
    (12, 19),
    (10, 17),
    (8, 15),
    (8, 11),
    (6, 9),
    (4, 5)
)


def compress_sprite_set_empty_removal(sprite_set, skip_initial_frame):
    greyLogger.debug("start")
    raw_sprite_set = list(sprite_set[3:])
    sprite_set_size = len(raw_sprite_set)
    parsed_size = 64 if skip_initial_frame else 0
    frame_id = 1 if skip_initial_frame else 0
    compressed_sprites = []

    while parsed_size < sprite_set_size:
        # print("test = {}".format(scaledFrameData[frame_id % 7]))
        curr_frame = raw_sprite_set[parsed_size:parsed_size + 64]
        start, length = scaledFrameData[frame_id % 7]
        compressed_sprites += curr_frame[start:start + length]
        # print("currFrame[{}:{}] = {}".format(start, length, curr_frame[start:start + length]))
        parsed_size += 64
        frame_id += 1

    greyLogger.debug("end")
    return compressed_sprites


# def convert_sprite_to_indexed_palette(raw_sprite):
#     ans = []
#     for x in raw_sprite:
#         # print("{:x} = {} {} {} {}".format(x, x >> 6, ))
#         ans.append(x >> 6)
#         ans.append((x & 0b00110000) >> 4)
#         ans.append((x & 0b00001100) >> 2)
#         ans.append(x & 0b00000011)
#     return ans
#
#
# def convert_indices_to_sprite(raw_pixels, width, height):
#     as_ints = []
#     ans = []
#     num_of_scaled_pixels_to_padding = {
#         20: 4,
#         54: 3,
#         88: 2,
#         120: 2,
#         170: 1,
#         228: 0,
#         252: 0
#     }
#
#     padding = num_of_scaled_pixels_to_padding[len(raw_pixels)]
#
#     # for i in range(0, len(raw_pixels) - 4, 4):
#     #     a = raw_pixels[i]
#     #     b = raw_pixels[i + 1]
#     #     c = raw_pixels[i + 2]
#     #     d = raw_pixels[i + 3]
#     #     ans.append((a << 6) | (b << 4) | (c << 2) | d)
#     k = 0
#     for i in range(0, len(raw_pixels), width):
#         as_ints += [0 for _ in range(padding)] + raw_pixels[i: i + width] + [0 for _ in range(padding)]
#     # print(as_ints)
#
#     for i in range(0, len(as_ints), 4):
#         a = as_ints[i]
#         b = as_ints[i + 1]
#         c = as_ints[i + 2]
#         d = as_ints[i + 3]
#         ans.append((a << 6) | (b << 4) | (c << 2) | d)
#
#     return ans
#
#
# def generate_sprite_scaled_frames(path):
#     frame_data_with_header = read_data(path)
#     spd_header = frame_data_with_header[0:3]
#     frame_data = frame_data_with_header[3:]
#     print("frame_data = {}".format(frame_data))
#     multicolor_pixels = convert_sprite_to_indexed_palette(frame_data[0:63])
#     width = 12
#     height = 21
#     img = Image.new(mode="P", size=(width, height))
#     # pixels = [x % 4 for x in range(width * height)]
#     img.putdata(multicolor_pixels)
#     print("multicolor_pixels = {}".format(multicolor_pixels))
#     print()
#
#     idx = 0
#     sprite_frame_set = []
#     for x in scaledFrameDataResolution:
#         img_tmp = img.resize(x)
#         raw_pixels = list(img_tmp.getdata())
#         print("raw_pixels = {} len = {}".format(raw_pixels, len(raw_pixels)))
#         sprite_frame_raw = convert_indices_to_sprite(raw_pixels, x[0], x[1])
#         padding = (63 - scaledFrameData[idx][1]) // 2
#         sprite = [0 for _ in range(padding)] + sprite_frame_raw + [0 for _ in range(padding)]
#         print("sprite resized to {} x {} = {}".format(x[0], x[1], sprite))
#         print()
#         sprite_frame_set += sprite
#         sprite_frame_set.append(0)  # 64th byte
#         idx += 1
#
#     filename = os.path.splitext(path)
#     print(filename)
#     print(sprite_frame_set)
#     output_path = filename[0] + "_generated.spd"
#     save_data(spd_header + bytes(sprite_frame_set), output_path)


if __name__ == '__main__':
    greyLogger.debug("start")
    parser = argparse.ArgumentParser()
    # group.add_argument('-e', action='store_true', help="sprite compression remove empty bytes")
    parser.add_argument("path", type=str)
    parser.add_argument('-s', action='store_true', help="skip first frame")
    parser.add_argument('-d', action='store_true', help="enables debugging")
    args = parser.parse_args()

    if args.d:
        greyLogger.setLevel(level=logging.DEBUG)
    try:
        data = utilities.read_from_bin_file(args.path)
    except (FileNotFoundError, PermissionError, IOError, OSError) as e:
        greyLogger.error("Couldn't read sprites data {}".format(e))
    else:
        filename = os.path.splitext(args.path)
        compressed_sprite_set = compress_sprite_set_empty_removal(data, args.s)
        output_path = filename[0] + "_compressed.bin"
        utilities.write_to_bin_file(output_path, compressed_sprite_set)
        greyLogger.debug("end")
