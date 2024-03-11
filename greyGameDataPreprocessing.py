import greyTextureUtils
import greySpritesUtils
import greyCampaignUtils
import logging
import utilities
from utilities import greyLogger
import os
import argparse

def process_textures():
    greyTextureUtils.read_and_convert_to_bin_all_textures(os.path.join("..", "textures"),
                                                          greyTextureUtils.DOOR_STRIPES_NO_OF_COLUMNS,
                                                          greyTextureUtils.DOOR_STRIPES_NO_OF_ROWS,
                                                          greyTextureUtils.TEXTURE_NO_OF_COLUMNS,
                                                          greyTextureUtils.TEXTURE_NO_OF_ROWS)


def process_campaign():
    campaign_path = os.path.join("..", "gameLevels", "greyTestCampaign.bin")
    try:
        data = utilities.read_from_bin_file(campaign_path)
    except (FileNotFoundError, PermissionError, IOError, OSError) as e:
        greyLogger.error("Couldn't read campaign file {}".format(e))
    else:
        # print(data)
        filename = os.path.splitext(campaign_path)
        out_path = filename[0] + "_compressed" + filename[1]
        try:
            campaign = greyCampaignUtils.compress_map(data)
        except greyCampaignUtils.CampaignTooLargeError as e:
            greyLogger.error("{}".format(e))
        else:
            utilities.write_to_bin_file(out_path, campaign)


def process_sprites(path, skip_first_frame=False):
    try:
        data = utilities.read_from_bin_file(path)
    except (FileNotFoundError, PermissionError, IOError, OSError) as e:
        greyLogger.error("Couldn't read sprites data {}".format(e))
    else:
        filename = os.path.splitext(path)
        compressed_sprite_set = greySpritesUtils.compress_sprite_set_empty_removal(data, skip_first_frame)
        output_path = filename[0] + "_compressed.bin"
        utilities.write_to_bin_file(output_path, compressed_sprite_set)


if __name__ == '__main__':
    greyLogger.debug("start")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true', help="enables debugging")
    args = parser.parse_args()

    if args.d:
        greyLogger.setLevel(level=logging.DEBUG)

    process_textures()
    process_campaign()
    process_sprites(os.path.join("..", "sprites", "barrelDown.spd"))
    process_sprites(os.path.join("..", "sprites", "barrelUp.spd"), True)
    process_sprites(os.path.join("..", "sprites", "mediumEnemy.spd"))
    greyLogger.debug("end")
