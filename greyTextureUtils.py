#!/usr/bin/env python3.10

from PIL import Image
import numpy as np
import os
import itertools
import utilities
DST_EXTENSION = ".bin"


def convert_image_to_bin_80x50(input_img, num_of_cols=32, num_of_rows=26):
    pixels = np.array(list(input_img.getdata())).reshape((num_of_rows, num_of_cols))[:num_of_rows]
    # print("pixels raw = {}".format(pixels))
    screen_buffer_pixels = []
    color_buffer_pixels = []

    for r in range(0, len(pixels), 2):
        for c in range(0, len(pixels[r]), 2):
            screen_buffer_pixels.append((pixels[r + 1][c] << 4) | pixels[r + 1][c + 1])
            color_buffer_pixels.append(pixels[r][c + 1])

    sb = np.array(screen_buffer_pixels).reshape(num_of_rows // 2, num_of_cols // 2)
    cb = np.array(color_buffer_pixels).reshape(num_of_rows // 2, num_of_cols // 2)
    # print("separated: \n{}\n\n{}".format(sb, cb))

    bin_screen_buffer = sb.transpose().flatten().tolist()
    bin_color_buffer = cb.transpose().flatten().tolist()

    return bin_screen_buffer, bin_color_buffer


def save_sr_cr_bins_to_file_common(src_path, dst_path, bins):
    head, tail = os.path.split(src_path)
    fn, ext = os.path.splitext(tail)
    out_file_name_stem = os.path.join(dst_path, fn)

    sbf, cbf = bins
    # print("saving bins: \n {} \n {}".format(sbf, cbf))

    utilities.write_to_bin_file(out_file_name_stem + "_screenRam" + DST_EXTENSION, sbf)
    utilities.write_to_bin_file(out_file_name_stem + "_colorRam" + DST_EXTENSION, cbf)


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
    
        if ans[light_cr[i]] == light_cr[i]:
            ans[light_cr[i]] = dark_cr[i]
        elif ans[light_cr[i]] != dark_cr[i]:
            raise RuntimeError("Inconsistent light-dark texture relation. Can't generate a dark transition vector")

    return ans


NUM_OF_WALL_TEXTURES_IN_MAIN_RAM = 3


# textures
#   bin
#       door_sr.bin
#       common_light_sr.bin
#       common_dark_sr.bin
#       level1_0_light_sr.bin
#       level1_0_dark_sr.bin
#       level1_1_light_sr.bin
#       level1_1_dark_sr.bin
#       door_cr.bin
#
#       common_light_cr.bin         + level2_0_cr
#       common_dark_cr.bin          + level2_1_cr
#       level1_0_light_cr.bin       + level3_0_cr
#       level1_0_dark_cr.bin        + level3_1_cr
#       level1_1_light_cr.bin       + level4_0_cr
#       level1_1_dark_cr.bin        + level4_1_cr
#
#       levels234_compressed.bin
#   common
#   level1
#   level2
#   level3
#   level4
#
def read_and_convert_to_bin_all_textures(path, stripes_cols, stripes_rows, tex_cols, tex_rows):
    root_dir = path

    door_stripes_path = os.path.join(root_dir, "common", "keyDoorColorStripes.tga")
    paths = [
        os.path.join(root_dir, "common", "doorTexture.tga"),
        os.path.join(root_dir, "common", "commonTextureLight.tga"),
        os.path.join(root_dir, "common", "commonTextureDark.tga"),

        os.path.join(root_dir, "level1", "level1Texture0Light.tga"),  # 3
        os.path.join(root_dir, "level1", "level1Texture0Dark.tga"),
        os.path.join(root_dir, "level1", "level1Texture1Light.tga"),
        os.path.join(root_dir, "level1", "level1Texture1Dark.tga"),

        os.path.join(root_dir, "level2", "level2Texture0Light.tga"),  # 7
        os.path.join(root_dir, "level2", "level2Texture0Dark.tga"),
        os.path.join(root_dir, "level2", "level2Texture1Light.tga"),
        os.path.join(root_dir, "level2", "level2Texture1Dark.tga"),

        os.path.join(root_dir, "level3", "level3Texture0Light.tga"),  # 11
        os.path.join(root_dir, "level3", "level3Texture0Dark.tga"),
        os.path.join(root_dir, "level3", "level3Texture1Light.tga"),
        os.path.join(root_dir, "level3", "level3Texture1Dark.tga"),

        os.path.join(root_dir, "level4", "level4Texture0Light.tga"),  # 15
        os.path.join(root_dir, "level4", "level4Texture0Dark.tga"),
        os.path.join(root_dir, "level4", "level4Texture1Light.tga"),
        os.path.join(root_dir, "level4", "level4Texture1Dark.tga")
    ]

    try:
        door_stripes_image = Image.open(door_stripes_path)
        images = [Image.open(path) for path in paths]
    except (FileNotFoundError, IOError, OSError) as e:
        print("Error: ", e)
    else:
        door_stripes_bin = convert_image_to_bin_80x50(door_stripes_image, stripes_cols, stripes_rows)
        bins = [convert_image_to_bin_80x50(img, tex_cols, tex_rows) for img in images]
        output_path = os.path.join(root_dir, "bin")

        # door stripes sr & cr
        save_sr_cr_bins_to_file_common(door_stripes_path, output_path, door_stripes_bin)
        # door sr
        darkening_luts = generate_darkening_luts([
            (bins[i], bins[i + 1]) for i in range(1, 18, 2)
        ])

        if tex_cols == 16 and tex_rows == 13:
            door_cr_merged_with_rec_vect = merge_two_color_ram_data_segments(
                bins[0][1], list(itertools.chain(*darkening_luts)) + [0] * 64)
            save_sr_cr_bins_to_file_common(paths[0], output_path, (bins[0][0], door_cr_merged_with_rec_vect))
        else:
            save_sr_cr_bins_to_file_common(paths[0], output_path, bins[0])

        # common light sr
        cl_sr, cl_cr = bins[1]
        l20l_sr, l20l_cr = bins[7]
        save_sr_cr_bins_to_file_common(paths[1], output_path,
                                       (cl_sr, merge_two_color_ram_data_segments(cl_cr, l20l_cr)))

        # common dark sr
        cd_sr, cd_cr = bins[2]
        l21l_sr, l21l_cr = bins[9]
        save_sr_cr_bins_to_file_common(paths[2], output_path,
                                       (cd_sr, merge_two_color_ram_data_segments(cd_cr, l21l_cr)))

        # level 1 0 light sr
        l10l_sr, l10l_cr = bins[3]
        l30l_sr, l30l_cr = bins[11]
        save_sr_cr_bins_to_file_common(paths[3], output_path,
                                       (l10l_sr, merge_two_color_ram_data_segments(l10l_cr, l30l_cr)))

        # level 1 0 dark sr
        l10d_sr, l10d_cr = bins[4]
        l31l_sr, l31l_cr = bins[13]
        save_sr_cr_bins_to_file_common(paths[4], output_path,
                                       (l10d_sr, merge_two_color_ram_data_segments(l10d_cr, l31l_cr)))

        # level 1 1 light sr
        l11l_sr, l11l_cr = bins[5]
        l40l_sr, l40l_cr = bins[15]
        save_sr_cr_bins_to_file_common(paths[5], output_path,
                                       (l11l_sr, merge_two_color_ram_data_segments(l11l_cr, l40l_cr)))

        # level 1 1 dark sr
        l11d_sr, l11d_cr = bins[6]
        l41l_sr, l41l_cr = bins[17]
        save_sr_cr_bins_to_file_common(paths[6], output_path,
                                       (l11d_sr, merge_two_color_ram_data_segments(l11d_cr, l41l_cr)))

        # add tex_pack generator here + darkening luts
        first_tex_start_offset = 3 + 12
        texture_pack = [
            2, 3, 4,
            first_tex_start_offset & 0xff,
            (first_tex_start_offset >> 8) & 0xff,

            (first_tex_start_offset + 208) & 0xff,
            ((first_tex_start_offset + 208) >> 8) & 0xff,

            (first_tex_start_offset + 208 * 2) & 0xff,
            ((first_tex_start_offset + 208 * 2) >> 8) & 0xff,

            (first_tex_start_offset + 208 * 3) & 0xff,
            ((first_tex_start_offset + 208 * 3) >> 8) & 0xff,

            (first_tex_start_offset + 208 * 4) & 0xff,
            ((first_tex_start_offset + 208 * 4) >> 8) & 0xff,

            (first_tex_start_offset + 208 * 5) & 0xff,
            ((first_tex_start_offset + 208 * 5) >> 8) & 0xff,
        ] + bins[7][0] + bins[9][0] + bins[11][0] + bins[13][0] + bins[15][0] + bins[17][0]

        # print(texture_pack, len(texture_pack))
        utilities.write_to_bin_file(os.path.join(output_path, "texturePack" + DST_EXTENSION), texture_pack)

#     3             12                       208 * 6 = 1248         1263
#   order | tex starting offsets    | textures data           |
#   2 3 4 | L H L H L H L H L H L H | L20 L21 L30 L31 L40 L41 |
#


def generate_darkening_luts(texture_pairs):
    ans = []
    for light, dark in texture_pairs:
        ans.append(generate_texture_dark_transition_map(light, dark))

    # for x in ans:
    #     print(x)
    return ans


DOOR_STRIPES_NO_OF_COLUMNS = 6
DOOR_STRIPES_NO_OF_ROWS = 26
TEXTURE_NO_OF_COLUMNS = 32
TEXTURE_NO_OF_ROWS = 26


if __name__ == '__main__':
    read_and_convert_to_bin_all_textures("./greyTextureUtilsTestData", DOOR_STRIPES_NO_OF_COLUMNS,
                                         DOOR_STRIPES_NO_OF_ROWS, TEXTURE_NO_OF_COLUMNS, TEXTURE_NO_OF_ROWS)
