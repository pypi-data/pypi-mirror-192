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
This module fetch information about a video from the invidious.
"""
from .baseapi import BaseAPI

class VideoAPI(BaseAPI):
    def __init__(self, config):
        super().__init__(config, '/api/v1/videos/')

    def get_thumbnails(self, id: str) -> dict:
        """
        Return JSON as dictionary that contains thumbnails.
        """
        return self.get_json(id, ['videoId','videoThumbnails'])

    def get_recommendations(self, id: str) -> dict:
        """
        Return JSON as dictionary that contains recommended videos.
        """
        return self.get_json(id, ['videoId','recommendedVideos'])
