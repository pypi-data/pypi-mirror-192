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
This module fetch information about a channel from the invidious.
"""
from .baseapi import BaseAPI

class ChannelAPI(BaseAPI):
    def __init__(self, config):
        super().__init__(config, '/api/v1/channels/')

    def get_title(self, id: str) -> str|None:
        return dict.pop(self.get_json(id,['author']), 'author', None)

    def get_thumbnails(self, id: str) -> dict:
        """
        Return JSON as dictionary that contains thumbnails.
        """
        return self.get_json(id, ['authorId','authorThumbnails'])

    def get_videos_page(self, id: str, page: str = "") -> dict:
        page_arg = f"?continuation={page}" if page != "" else ""
        url_args = ['/api/v1/channels/videos/', id, page_arg]
        config = super().get_config()
        videos_json = config.get_api().get(config, url_args, None)
        return videos_json

    def get_videos(self, id: str) -> list|None:
        videos, continuation = [], ""
        while continuation != None:
          page_json = self.get_videos_page(id, continuation)
          page_videos = dict.pop(page_json, "videos")
          continuation = dict.pop(page_json, "continuation", None)
          videos += page_videos
        return videos
