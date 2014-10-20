from .DiskIo import getDiskIo
from .FileDownloader import getFileDownloader
from .GithubZipballExtractor import getGithubZipballExtractor
from .ProfileCache import getProfileCache
from .ProfileUrlResolver import getProfileUrl
from .Settings import getSettings
import os


class ProfileRetriever:
    def __init__(self, settings, fileDownloader, profileCache, diskIo, githubZipballExtractor):
        self.settings = settings
        self.fileDownloader = fileDownloader
        self.profileCache = profileCache
        self.diskIo = diskIo
        self.githubZipballExtractor = githubZipballExtractor

    def retrieve(self, profile):
        """
        Downloads a profile into the cache. If the profile already exists, then
        it is overwritten.
        """
        url = getProfileUrl(profile)
        print('Downloading profile from %s' % url)
        downloadsPath = self.settings.downloadsPath
        downloadedFilePath = self.fileDownloader.download(url, downloadsPath)
        extractionDir = os.path.splitext(downloadedFilePath)[0]
        self.githubZipballExtractor.extractZipball(downloadedFilePath, extractionDir)

        if self.profileCache.contains(profile):
            self.profileCache.delete(profile)

        profileDir = self.profileCache.getProfileLocation(profile)
        self.diskIo.move(extractionDir, profileDir)


def getProfileRetriever(app):
    return app.get('profileRetriever', createProfileRetriever(app))


def createProfileRetriever(app):
    settings = getSettings(app)
    fileDownloader = getFileDownloader(app)
    profileCache = getProfileCache(app)
    diskIo = getDiskIo(app)
    githubZipballExtractor = getGithubZipballExtractor(app)
    profileRetriever = ProfileRetriever(settings, fileDownloader, profileCache, diskIo, githubZipballExtractor)
    return profileRetriever
