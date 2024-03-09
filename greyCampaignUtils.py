#!/usr/bin/env python3.10

import utilities
import argparse
import os
from utilities import greyLogger
import logging

# campaign format:
# N SL SH LHLHLH LHLHLH LHLHLH LH LEVEL_DATA
#
# N - num of levels
# SL, SH - low and high bytes of campaign size in bytes
# LHLHLH - level segments starting addresses
# LH - LEVEL_DATA upper bound (for easy calculations


MAX_CAMPAIGN_FILE_SIZE = 2000


class CampaignTooLargeError(Exception):
    def __init__(self, campaign_size):
        self.salary = campaign_size
        self.message = "Campaign size {} too large. maxSize = {}".format(campaign_size, MAX_CAMPAIGN_FILE_SIZE)
        super().__init__(self.message)


def compress_map(game_map):
    greyLogger.debug("start")
    # campaign = []
    compressed_segments = []

    map_size = len(game_map)
    greyLogger.debug("map_size = {}".format(map_size))
    parsed_size = 0
    game_map_list = list(map(int, game_map))
    full_level_size = 256 * 3 + 16

    level_idx = 0
    while parsed_size < map_size:
        # print("level {}".format(level_idx))
        curr_level = game_map_list[parsed_size: parsed_size + full_level_size]
        # level_header = curr_level[0:16]     # for now ignored. reserved for texture set data etc.
        raw_level = curr_level[16:]

        level_segments = []
        segment_size = 256
        parsed_level_size = 0
        segment_idx = 0
        while parsed_level_size < segment_size * 3:
            greyLogger.debug("\tsegment_idx = {}".format(segment_idx))
            level_segments.append(raw_level[parsed_level_size: parsed_level_size + segment_size])
            parsed_level_size += segment_size
            segment_idx += 1

        greyLogger.debug("level_idx = {}".format(level_idx))
        for seg in level_segments:
            compressed_segments.append(compress_map_segment(seg))

        level_idx += 1
        parsed_size += full_level_size

    num_of_levels = len(compressed_segments) // 3
    greyLogger.debug("num_of_levels = {}".format(num_of_levels))
    num_of_levels_byte = 1
    num_of_segment_addr_bytes = 6
    num_of_campaign_size_bytes = 2
    num_of_campaign_upper_bound_addr_bytes = 2
    start_address = (0xd000 + num_of_levels_byte + num_of_levels * num_of_segment_addr_bytes
                     + num_of_campaign_size_bytes + num_of_campaign_upper_bound_addr_bytes)
    campaign_size_l = 0
    campaign_size_h = 0
    campaign_data = ([num_of_levels, campaign_size_l, campaign_size_h]
                     + [-1 for _ in range(num_of_levels * num_of_segment_addr_bytes
                        + num_of_campaign_upper_bound_addr_bytes)])  # segment start addr. -1 means no seg

    seg_l_idx = 3
    seg_h_idx = 4
    greyLogger.debug("Compressed segments:")
    for seg in compressed_segments:
        greyLogger.debug("\tseg = {}".format(seg))
        # print(seg)
        # print()
        # print("start addr = {0:x}".format(start_address))
        if seg != [0, -256]:
            # print(len(seg))
            campaign_data += seg
            campaign_data[seg_l_idx] = start_address & 0xff
            campaign_data[seg_h_idx] = start_address >> 8
            greyLogger.debug("\tsegment address L: {:02x} H: {:02x}".format(start_address & 0xff, start_address >> 8))
            start_address += len(seg)
        seg_l_idx += 2
        seg_h_idx += 2
    campaign_data[seg_l_idx] = start_address & 0xff      # campaign upper bound
    campaign_data[seg_h_idx] = start_address >> 8        # campaign upper bound
    greyLogger.debug("\tcampaign upperBound L: {:02x} H: {:02x}".format(start_address & 0xff, start_address >> 8))

    size_l_idx = 1
    size_h_idx = 2
    campaign_data[size_l_idx] = len(campaign_data) & 0xff
    campaign_data[size_h_idx] = len(campaign_data) >> 8

    campaign_normalized = list(map(lambda x: 256 + x if x < 0 else x, campaign_data))

    campaign_size = len(campaign_normalized)
    greyLogger.debug("campaign = {}".format(campaign_normalized))
    greyLogger.debug("campaign_size = {0} original_size = {1}, compression_ratio = {2:.2f}".format(
        campaign_size, map_size, map_size / campaign_size ))

    if campaign_size > MAX_CAMPAIGN_FILE_SIZE:
        greyLogger.error("Campaign size {} too large. maxSize = {}".format(campaign_size, MAX_CAMPAIGN_FILE_SIZE))
        raise CampaignTooLargeError(len(campaign_normalized))
    else:
        greyLogger.debug("end")
        return campaign_normalized


def compress_map_segment(game_map_segment):
    greyLogger.debug("start")
    ans = []

    for x in game_map_segment:
        if len(ans) == 0 or x != ans[-2]:
            ans.append(x)
            ans.append(-1)
        else:
            ans[-1] -= 1

    post_processed = []

    for x in ans:
        if x != -1:
            post_processed.append(x)

    greyLogger.debug("end")
    return post_processed


# if __name__ == '__main__':
#     greyLogger.debug("start")
#     parser = argparse.ArgumentParser()
#
#     group = parser.add_mutually_exclusive_group()
#     # group.add_argument('-c', action='store_true', help="campaign compression")
#     parser.add_argument('-d', action='store_true', help="enables debugging")
#     parser.add_argument("path", type=str)
#     args = parser.parse_args()
#
#     if args.d:
#         greyLogger.setLevel(level=logging.DEBUG)
#     try:
#         data = utilities.read_from_bin_file(args.path)
#     except (FileNotFoundError, PermissionError, IOError, OSError) as e:
#         greyLogger.error("Couldn't read campaign file {}".format(e))
#     else:
#         # print(data)
#         filename = os.path.splitext(args.path)
#         out_path = filename[0] + "_compressed" + filename[1]
#         try:
#             campaign = compress_map(data)
#         except CampaignTooLargeError as e:
#             greyLogger.error("{}".format(e))
#         else:
#             utilities.write_to_bin_file(out_path, campaign)
#             greyLogger.debug("end")
