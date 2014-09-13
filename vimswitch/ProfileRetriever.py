import os
from zipfile import ZipFile
from ProfileUrlResolver import getProfileUrl


class ProfileRetriever:
    def __init__(self, settings, fileDownloader, profileCache, diskIo):
        self.settings = settings
        self.fileDownloader = fileDownloader
        self.profileCache = profileCache
        self.diskIo = diskIo

    def retrieve(self, profile):
        url = getProfileUrl(profile)
        downloadsPath = self.settings.downloadsPath
        downloadedFilePath = self.fileDownloader.download(url, downloadsPath)
        extractionDir = os.path.splitext(downloadedFilePath)[0]
        ZipFile(downloadedFilePath).extractall(extractionDir)

        if self.profileCache.contains(profile):
            self.profileCache.delete(profile)

        profileDir = self.profileCache.getLocation(profile)
        self.diskIo.move(extractionDir, profileDir)
