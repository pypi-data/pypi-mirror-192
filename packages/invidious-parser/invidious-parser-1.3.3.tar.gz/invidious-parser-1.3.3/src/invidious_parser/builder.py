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

class Builder:
    """The helper to build a url."""
    @staticmethod
    def url(args: list) -> str:
        return ''.join(args)

    @staticmethod
    def url_base(base:str, args: list) -> str:
        return f"{base}{Builder.url(args)}"

    @staticmethod
    def url_fields(url:str, fields: list|None = None) -> str:
        if fields is None:
            return url
        return f"{url}?fields={','.join(fields)}"
