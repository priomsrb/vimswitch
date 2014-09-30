from .FileSystemTestCase import FileSystemTestCase
from copy import deepcopy
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.Settings import Settings
from vimswitch.ConfigFile import getConfigFile
from vimswitch.DiskIo import getDiskIo
import vimswitch.six.moves.configparser as configparser


class TestConfigFile(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.app = Application()
        self.configFile = getConfigFile(self.app)

    # ConfigFile.loadSettings()

    def test_loadSettings_allAttributes(self):
        self.copyDataToWorkingDir('vimswitchrc', 'vimswitchrc')
        configFilePath = self.getTestPath('vimswitchrc')
        settings = Settings()

        self.configFile.loadSettings(settings, configFilePath)

        self.assertEqual(settings.currentProfile, Profile('test/vimrc'))

    def test_loadSettings_fileDoesNotExist_settingsUnchanged(self):
        nonExistantPath = self.getTestPath('non_existant')
        settings = Settings()
        settingsCopy = deepcopy(settings)

        self.configFile.loadSettings(settings, nonExistantPath)

        self.assertEqual(settings, settingsCopy)

    def test_loadSettings_emptyFile_raisesError(self):
        diskIo = getDiskIo(self.app)
        emptyConfigFilePath = self.getTestPath('empty_vimswitchrc')
        diskIo.createFile(emptyConfigFilePath, '')
        settings = Settings()

        self.assertRaises(configparser.NoSectionError, self.configFile.loadSettings, settings, emptyConfigFilePath)

    def test_loadSettings_missingSection_raisesError(self):
        diskIo = getDiskIo(self.app)
        incorrectConfigFilePath = self.getTestPath('incorrect_vimswitchrc')
        diskIo.createFile(incorrectConfigFilePath, '[incorrect_section]')
        settings = Settings()

        self.assertRaises(configparser.NoSectionError, self.configFile.loadSettings, settings, incorrectConfigFilePath)

    # ConfigFile.saveSettings()

    def test_saveSettings_allAttributes(self):
        settings = Settings()
        settings.currentProfile = Profile('test/vimrc')
        configFilePath = self.getTestPath('vimswitchrc')

        self.configFile.saveSettings(settings, configFilePath)

        newSettings = Settings()
        self.configFile.loadSettings(newSettings, configFilePath)
        self.assertEqual(newSettings.currentProfile, Profile('test/vimrc'))

    def test_saveSettings_savesNoneValueAttributes(self):
        settings = Settings()
        settings.currentProfile = None
        configFilePath = self.getTestPath('vimswitchrc')

        self.configFile.saveSettings(settings, configFilePath)

        newSettings = Settings()
        self.configFile.loadSettings(newSettings, configFilePath)
        self.assertEqual(newSettings.currentProfile, None)

    def test_saveSettings_savesUnchangedSettings(self):
        settings = Settings()
        configFilePath = self.getTestPath('vimswitchrc')

        self.configFile.saveSettings(settings, configFilePath)

        newSettings = Settings()
        self.configFile.loadSettings(newSettings, configFilePath)
        self.assertEqual(newSettings, settings)
