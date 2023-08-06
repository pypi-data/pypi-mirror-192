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

from invidious_parser.invidious_api import InvidiousAPI
from invidious_parser.invidious_instance import InvidiousInstance
from invidious_parser.connection_config import ConnectionConfig
from invidious_parser.builder import Builder
from invidious_parser.receiver import Receiver

class InvidiousConfig:
    """
    The handler of the configuration information.
    """
    def __init__(self, connection_config = None, instance = None, API = None, builder = None, receiver = None):
        """
        Initialaze the configuration.
        """
        self.set_connection_config(connection_config)
        self.__instance = InvidiousInstance() if instance is None else instance
        self.__API = InvidiousAPI() if API is None else API
        self.__builder = Builder() if builder is None else builder
        self.__receiver = Receiver() if receiver is None else receiver

    def set_connection_config(self, connection_config = None):
        if connection_config is None:
            self.__connection_config = ConnectionConfig()
        else:
            self.__connection_config = connection_config

    def set_receiver(self, receiver = None):
        self.__receiver = Receiver() if receiver is None else receiver

    def get_connection_config(self):
        return self.__connection_config

    def get_instance(self):
        return self.__instance

    def get_api(self):
        return self.__API

    def get_builder(self):
        return self.__builder

    def get_receiver(self):
        return self.__receiver
