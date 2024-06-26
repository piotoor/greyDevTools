from utilities import greyLogger
import utilities
from PIL import Image
import os
import argparse
import logging


def convert_sprite_to_indexed_palette(raw_sprite):
    greyLogger.debug("start")
    ans = []
    for x in raw_sprite:
        # print("{:x} = {} {} {} {}".format(x, x >> 6, ))
        ans.append(x >> 6)
        ans.append((x & 0b00110000) >> 4)
        ans.append((x & 0b00001100) >> 2)
        ans.append(x & 0b00000011)
    return ans


def convert_indices_to_sprite(raw_pixels, width, height):
    greyLogger.debug("start")
    as_ints = []
    ans = []
    num_of_scaled_pixels_to_padding = {
        20: 4,
        54: 3,
        88: 2,
        120: 2,
        170: 1,
        228: 0,
        252: 0
    }

    padding = num_of_scaled_pixels_to_padding[len(raw_pixels)]

    # for i in range(0, len(raw_pixels) - 4, 4):
    #     a = raw_pixels[i]
    #     b = raw_pixels[i + 1]
    #     c = raw_pixels[i + 2]
    #     d = raw_pixels[i + 3]
    #     ans.append((a << 6) | (b << 4) | (c << 2) | d)
    k = 0
    for i in range(0, len(raw_pixels), width):
        as_ints += [0 for _ in range(padding)] + raw_pixels[i: i + width] + [0 for _ in range(padding)]
    greyLogger.debug(as_ints)

    for i in range(0, len(as_ints), 4):
        a = as_ints[i]
        b = as_ints[i + 1]
        c = as_ints[i + 2]
        d = as_ints[i + 3]
        ans.append((a << 6) | (b << 4) | (c << 2) | d)

    greyLogger.debug("Indices to sprite: {}".format(ans))
    return ans


def generate_sprite_scaled_frames(path):
    greyLogger.debug("start")
    frame_data = utilities.read_from_bin_file(path)
    greyLogger.debug("frame_data = {}".format(frame_data))
    multicolor_pixels = convert_sprite_to_indexed_palette(frame_data[0:63])
    width = 12
    height = 21
    img = Image.new(mode="P", size=(width, height))
    # pixels = [x % 4 for x in range(width * height)]
    img.putdata(multicolor_pixels)
    greyLogger.debug("multicolor_pixels = {}".format(multicolor_pixels))

    idx = 0
    sprite_frame_set = []
    for x in utilities.scaledFrameDataResolution:
        img_tmp = img.resize(x)
        raw_pixels = list(img_tmp.getdata())
        greyLogger.debug("raw_pixels = {} len = {}".format(raw_pixels, len(raw_pixels)))
        sprite_frame_raw = convert_indices_to_sprite(raw_pixels, x[0], x[1])
        padding = (63 - utilities.scaledFrameData[idx][1]) // 2
        sprite = [0 for _ in range(padding)] + sprite_frame_raw + [0 for _ in range(padding)]
        greyLogger.debug("sprite resized to {} x {} = {}".format(x[0], x[1], sprite))
        sprite_frame_set += sprite
        sprite_frame_set.append(0)  # 64th byte
        idx += 1

    filename = os.path.splitext(path)
    output_path = filename[0] + "_generated.bin"
    greyLogger.debug("output_path = {}".format(output_path))
    utilities.write_to_bin_file(os.path.join(".", output_path), bytes(sprite_frame_set))


if __name__ == '__main__':
    greyLogger.debug("start")
    greyLogger.setLevel(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()

    # try:
    generate_sprite_scaled_frames(args.path)
    # except (FileNotFoundError, PermissionError, IOError, OSError) as e:
    #     greyLogger.error("Couldn't read sprite file {}".format(e))
    # else:
    #     greyLogger.debug("Generated sprite scaled frames successfully")
