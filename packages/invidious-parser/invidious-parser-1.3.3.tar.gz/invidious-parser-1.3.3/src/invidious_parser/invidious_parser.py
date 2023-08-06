################################################################################
# Copyright (C) 2022-2023 Kostiantyn Klochko <kostya_klochko@ukr.net>          #
#                                                                              #
# This file is part of invidious-parser.                                       #
#                                                                              #
# invidious-parser is free software: you can redistribute it and/or modify it  #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# invidious-parser is distributed in the hope that it will be useful, but      #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY   #
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for  #
# more details.                                                                #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# invidious-parser. If not, see <https://www.gnu.org/licenses/>.               #
################################################################################

"""
This module fetch information from invidious using its api.
"""
from invidious_parser.invidious_config import InvidiousConfig
from invidious_parser.videoapi import VideoAPI
from invidious_parser.playlistapi import PlaylistAPI
from invidious_parser.channelapi import ChannelAPI

class Invidious:
    """The helper of fetching information."""
    def __init__(self, config = None):
        self.config = InvidiousConfig() if config is None else config

    def video(self):
        return VideoAPI(self.config)

    def playlist(self):
        return PlaylistAPI(self.config)

    def channel(self):
        return ChannelAPI(self.config)
