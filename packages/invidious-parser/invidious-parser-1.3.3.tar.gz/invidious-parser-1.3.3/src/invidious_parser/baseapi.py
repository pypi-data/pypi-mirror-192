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

class BaseAPI:
    def __init__(self, config, url):
        self.__config = config
        self.__url = url

    def get_json(self, id: str, fields=None, url=None) -> dict:
        """
        Return the video JSON as dictionary.
        """
        url_args = [self.__url, id] if url is None else [url, id]
        
        return self.__config.get_api().get(self.__config, url_args, fields)

    def get_field(self, id:str, field:str, fields=None, default_value=None):
        """
        Return a field value from JSON.
        If no field, then return default value.
        """
        return dict.pop(self.get_json(id, fields), field, default_value)

    def get_title(self, id: str) -> str|None:
        return self.get_field(id, 'title', ['title'])

    def get_author_id(self, id: str) -> str|None:
        return self.get_field(id, 'authorId', ['authorId'])

    def get_description(self, id: str) -> str|None:
        return self.get_field(id, 'description', ['description'])

    def get_description_html(self, id: str) -> str|None:
        return self.get_field(id, 'descriptionHtml', ['descriptionHtml'])

    def get_config(self):
        return self.__config
