import unittest
from parameterized import parameterized
import greyTextureUtils
from PIL import Image
import os
import logging
from utilities import greyLogger

greyLogger.setLevel(level=logging.ERROR)

class GreyTextureUtilsTests(unittest.TestCase):
    @parameterized.expand([
        (
            "texture 1",
            "./greyTextureUtilsTestData/commonTextureDark.tga",
            (
                [255, 188, 187, 155, 0, 0, 0, 9, 155, 155, 187, 187, 187, 252, 187, 203, 155, 0, 0, 9, 155, 187, 187,
                 155, 187, 187, 204, 176, 0, 184, 0, 9, 153, 185, 185, 185, 187, 187, 187, 204, 9, 153, 207, 0, 144,
                 144, 153, 153, 185, 187, 187, 187, 204, 155, 188, 251, 0, 0, 0, 0, 144, 153, 185, 185, 187, 207, 188,
                 188, 185, 0, 0, 0, 9, 153, 155, 187, 187, 187, 204, 203, 187, 155, 0, 0, 153, 153, 185, 185, 187, 187,
                 187, 204, 176, 0, 184, 0, 0, 153, 155, 155, 187, 187, 187, 187, 204, 9, 153, 207, 0, 153, 153, 185,
                 185, 187, 187, 187, 187, 207, 155, 188, 251, 0, 144, 153, 155, 187, 187, 187, 187, 187, 255, 188, 187,
                 185, 0, 0, 144, 155, 155, 155, 187, 187, 187, 255, 187, 155, 155, 0, 0, 9, 153, 187, 187, 187, 187,
                 187, 252, 176, 0, 184, 0, 9, 153, 153, 153, 185, 155, 187, 187, 204, 9, 153, 207, 0, 144, 153, 155,
                 187, 187, 187, 187, 187, 204, 155, 188, 251, 0, 0, 144, 153, 185, 187, 187, 187, 187, 207, 188, 188,
                 185, 0, 0, 0, 144, 185, 185, 187, 187, 187],
                [15, 12, 11, 11, 0, 0, 0, 0, 9, 9, 11, 11, 11, 15, 12, 11, 11, 9, 0, 0, 9, 11, 11, 11, 11, 11, 15, 11,
                 0, 9, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 0, 11, 9, 0, 9, 9, 9, 9, 11, 11, 11, 15, 11, 12, 15, 9,
                 0, 0, 0, 0, 0, 9, 11, 11, 15, 12, 11, 11, 0, 0, 0, 0, 9, 9, 11, 11, 11, 15, 11, 11, 11, 9, 0, 0, 9, 9,
                 11, 11, 11, 11, 15, 11, 0, 9, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 0, 11, 9, 0, 9, 9, 11, 11, 11,
                 11, 11, 15, 12, 12, 15, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 12, 11, 11, 9, 0, 0, 9, 11, 9, 11, 11, 11,
                 15, 12, 11, 11, 0, 0, 0, 9, 11, 11, 11, 11, 11, 15, 12, 0, 9, 9, 0, 9, 9, 9, 9, 11, 11, 11, 15, 11, 0,
                 11, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 12, 15, 9, 0, 0, 9, 9, 11, 11, 11, 11, 15, 12, 11, 11, 0,
                 0, 0, 0, 9, 11, 11, 11, 11]
            )
        )
    ])
    def test_convert_image_to_bin_80x50_texture(self, _, path, expected):
        curr_img = Image.open(path)
        self.assertEqual(expected, greyTextureUtils.convert_image_to_bin_80x50(curr_img))

    @parameterized.expand([
        (
            "colorDoorStripes 1",
            "./greyTextureUtilsTestData/keyDoorColorStripes.tga",
            (
                 [34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85,
                  85, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102],
                 [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
                  13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
            )
        )
    ])
    def test_convert_image_to_bin_80x50_colorDoorStripes(self, _, path, expected):
        curr_img = Image.open(path)
        self.assertEqual(expected, greyTextureUtils.convert_image_to_bin_80x50(curr_img, 6))

    @parameterized.expand([
        (
            "test1",
            (
                 [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
                  6,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                 [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
                  13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
            ),
            [0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xab, 0xd6, 0xd6, 0xd6, 0xd6, 0xd6,
             0xd6, 0xd6, 0xd6, 0xd6, 0xd6, 0xd6, 0xd6, 0xd6, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1, 0xe1,
             0xe1, 0xe1, 0xe1]
        )
    ])
    def test_merge_two_color_ram_data_segments(self, _, data, expected):
        self.assertEqual(expected, greyTextureUtils.merge_two_color_ram_data_segments(data[0], data[1]))

    @parameterized.expand([
        (
            "correct",
            (
                 "./greyTextureUtilsTestData/commonTextureLight.tga",
                 "./greyTextureUtilsTestData/commonTextureDark.tga",
            ),
            [0, 15, 2, 3, 4, 5, 6, 15, 11, 0, 8, 9, 11, 13, 14, 12]
        )
    ])
    def test_merge_two_color_ram_data_segments(self, _, data, expected):
        light_path, dark_path = data
        light_image = Image.open(light_path)
        dark_image = Image.open(dark_path)
        light_bin = greyTextureUtils.convert_image_to_bin_80x50(light_image)
        dark_bin = greyTextureUtils.convert_image_to_bin_80x50(dark_image)

        self.assertEqual(expected, greyTextureUtils.generate_texture_dark_transition_map(light_bin, dark_bin))

    @parameterized.expand([
        (
            "exception",
            (
                    "./greyTextureUtilsTestData/commonTextureLight.tga",
                    "./greyTextureUtilsTestData/commonTextureDark_invalid.tga",
            ),
            "Inconsistent light-dark texture relation. Can't generate a dark transition vector"
        ),
    ])
    def test_merge_two_color_ram_data_segments_exception(self, _, data, expected):
        light_path, dark_path = data
        light_image = Image.open(light_path)
        dark_image = Image.open(dark_path)
        light_bin = greyTextureUtils.convert_image_to_bin_80x50(light_image)
        dark_bin = greyTextureUtils.convert_image_to_bin_80x50(dark_image)

        with self.assertRaises(RuntimeError) as context:
            _ = greyTextureUtils.generate_texture_dark_transition_map(light_bin, dark_bin)

        self.assertTrue(expected in str(context.exception))

    def test_read_and_convert_to_bin_all_textures(self):
        raised = False
        try:
            greyTextureUtils.read_and_convert_to_bin_all_textures(
                "./greyTextureUtilsTestData", 2, 4, 4, 4)
        except RuntimeError as e:
            print("Error: ", e)
            raised = True
        else:
            filenames = [
                "commonTextureDark_colorRam.bin",
                "commonTextureDark_screenRam.bin",
                "commonTextureLight_colorRam.bin",
                "commonTextureLight_screenRam.bin",
                "doorTexture_colorRam.bin",
                "doorTexture_screenRam.bin",
                "keyDoorColorStripes_colorRam.bin",
                "keyDoorColorStripes_screenRam.bin",
                "level1Texture0Dark_colorRam.bin",
                "level1Texture0Dark_screenRam.bin",
                "level1Texture0Light_colorRam.bin",
                "level1Texture0Light_screenRam.bin",
                "level1Texture1Dark_colorRam.bin",
                "level1Texture1Dark_screenRam.bin",
                "level1Texture1Light_colorRam.bin",
                "level1Texture1Light_screenRam.bin",
                "texturePack.bin"
            ]
            expects = [
                [0xe2, 0xe2, 0xef, 0xef],
                [0xb2, 0xb2, 0xbf, 0xbf],
                [0xda, 0xda, 0x31, 0x31],
                [0xfa, 0xfa, 0xf1, 0xf1],
                [0x02, 0x02, 0x01, 0x02],
                [0x22, 0x22, 0x11, 0x11],
                [0x02, 0x02],
                [0x25, 0x25],
                [0xa2, 0xa2, 0xa3, 0xa3],
                [0x33, 0x33, 0x22, 0x22],
                [0x8a, 0x8a, 0x8e, 0x8e],
                [0xee, 0xee, 0xaa, 0xaa],
                [0xf2, 0xb2, 0xb2, 0xf2],
                [0x33, 0x33, 0x33, 0x33],
                [0xea, 0xea, 0xaa, 0xaa],
                [0x33, 0x33, 0x33, 0x33],
                [
                    2, 3, 4,
                    15, 0, 223, 0, 175, 1, 127, 2, 79, 3, 31, 4,
                    221, 221, 51, 51, 235, 235, 235, 235, 17, 24,
                    129, 17, 170, 170, 170, 170, 218, 218, 218, 218, 255, 187, 187, 255
                ]
            ]
            try:
                for filename, expected in zip(filenames, expects):
                    with open(os.path.join("greyTextureUtilsTestData", "bin", filename), mode="rb") as f:
                        try:
                            data = list(f.read())
                            self.assertEqual(expected, data)
                        except (IOError, OSError) as e:
                            print("Error: ", e)
                            raised = True
                        else:
                            pass
            except (FileNotFoundError, PermissionError, OSError) as e:
                print("Error opening file: ", e)
                raised = True
        self.assertFalse(raised, 'Exception raised')
