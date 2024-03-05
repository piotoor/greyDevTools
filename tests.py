import unittest
from parameterized import parameterized
import greyTextureUtils
from PIL import Image


class GreyTextureUtilsTests(unittest.TestCase):
    @parameterized.expand([
        (
            "texture 1",
            "./greyTextureUtilsTestData/commonTextureDark.tga",
            (
                [255, 188, 187, 155, 0, 0, 0, 9, 155, 155, 187, 187, 187, 252, 187, 203, 155, 0, 0, 9, 155, 187, 187, 155, 187, 187, 204, 176, 0, 184, 0, 9, 153, 185, 185, 185, 187, 187, 187, 204, 9, 153, 207, 0, 144, 144, 153, 153, 185, 187, 187, 187, 204, 155, 188, 251, 0, 0, 0, 0, 144, 153, 185, 185, 187, 207, 188, 188, 185, 0, 0, 0, 9, 153, 155, 187, 187, 187, 204, 203, 187, 155, 0, 0, 153, 153, 185, 185, 187, 187, 187, 204, 176, 0, 184, 0, 0, 153, 155, 155, 187, 187, 187, 187, 204, 9, 153, 207, 0, 153, 153, 185, 185, 187, 187, 187, 187, 207, 155, 188, 251, 0, 144, 153, 155, 187, 187, 187, 187, 187, 255, 188, 187, 185, 0, 0, 144, 155, 155, 155, 187, 187, 187, 255, 187, 155, 155, 0, 0, 9, 153, 187, 187, 187, 187, 187, 252, 176, 0, 184, 0, 9, 153, 153, 153, 185, 155, 187, 187, 204, 9, 153, 207, 0, 144, 153, 155, 187, 187, 187, 187, 187, 204, 155, 188, 251, 0, 0, 144, 153, 185, 187, 187, 187, 187, 207, 188, 188, 185, 0, 0, 0, 144, 185, 185, 187, 187, 187],
                [15, 12, 11, 11, 0, 0, 0, 0, 9, 9, 11, 11, 11, 15, 12, 11, 11, 9, 0, 0, 9, 11, 11, 11, 11, 11, 15, 11, 0, 9, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 0, 11, 9, 0, 9, 9, 9, 9, 11, 11, 11, 15, 11, 12, 15, 9, 0, 0, 0, 0, 0, 9, 11, 11, 15, 12, 11, 11, 0, 0, 0, 0, 9, 9, 11, 11, 11, 15, 11, 11, 11, 9, 0, 0, 9, 9, 11, 11, 11, 11, 15, 11, 0, 9, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 0, 11, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 12, 12, 15, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 12, 11, 11, 9, 0, 0, 9, 11, 9, 11, 11, 11, 15, 12, 11, 11, 0, 0, 0, 9, 11, 11, 11, 11, 11, 15, 12, 0, 9, 9, 0, 9, 9, 9, 9, 11, 11, 11, 15, 11, 0, 11, 9, 0, 9, 9, 11, 11, 11, 11, 11, 15, 11, 12, 15, 9, 0, 0, 9, 9, 11, 11, 11, 11, 15, 12, 11, 11, 0, 0, 0, 0, 9, 11, 11, 11, 11]
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
                 [34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102],
                 [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
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
