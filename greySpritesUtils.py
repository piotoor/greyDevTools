#!/usr/bin/env python3.10

import argparse
import os
import utilities
from utilities import greyLogger
import logging


def compress_sprite_set_empty_removal(sprite_set, skip_initial_frame):
    greyLogger.debug("start")
    raw_sprite_set = list(sprite_set)
    sprite_set_size = len(raw_sprite_set)
    parsed_size = 64 if skip_initial_frame else 0
    frame_id = 1 if skip_initial_frame else 0
    compressed_sprites = []

    while parsed_size < sprite_set_size:
        # print("test = {}".format(scaledFrameData[frame_id % 7]))
        curr_frame = raw_sprite_set[parsed_size:parsed_size + 64]
        start, length = utilities.scaledFrameData[frame_id % 7]
        compressed_sprites += curr_frame[start:start + length]
        # print("currFrame[{}:{}] = {}".format(start, length, curr_frame[start:start + length]))
        parsed_size += 64
        frame_id += 1

    greyLogger.debug("end")
    return compressed_sprites


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
