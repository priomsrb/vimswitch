#!/usr/bin/env python

import sys

def main():
    profile = 'priomsrb/vimrc'

    settings = Settings(sys.argv)

    profile_manager = ProfileManager(settings)

    if !profile_manager.exists(profile):
        profile_manager.retrieve(profile)

    profile_manager.switch_to(profile)


class Settings:
    def init(self, argv):
        self.setup_settings_dir()

    def setup_settings_dir(self):
        self.__check_settings_dir()
        self.__check_default_profile()

class ProfileManager:

    def __init__(self, settings):
        self.settings = settings

    def exists(self, profile):
        pass

    def switch_to(self, profile):
        self.remove_vim_files()
        self.copy_to_home(profile)

main()
