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

class InvidiousAPI:
    @staticmethod
    def get_url(config, url, fields=None) -> dict:
        url = config.get_builder().url_fields(url, fields)
        return config.get_receiver().get(config, url)

    @staticmethod
    def get(config, url_args: list, fields=None) -> dict:
        url:str = config.get_builder().url_base(
            config.get_instance().get_url(), url_args
        )
        if not fields is None:
            return InvidiousAPI.get_url(config, url, fields)
        return config.get_receiver().get(config, url)
