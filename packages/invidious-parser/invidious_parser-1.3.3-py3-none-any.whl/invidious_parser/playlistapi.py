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
This module fetch information about a playlist from the invidious.
"""
from .baseapi import BaseAPI

class PlaylistAPI(BaseAPI):
    def __init__(self, config):
        super().__init__(config, '/api/v1/playlists/')

    def get_video_count(self, id: str) -> int|None:
        return self.get_field(id, 'videoCount', ['videoCount'])

    def get_videos(self, id: str) -> int|None:
        return self.get_field(id, 'videos', ['videos'])
