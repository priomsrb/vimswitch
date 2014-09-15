import os
import re
import urllib
import datetime
from mimetools import Message
from StringIO import StringIO
from urlparse import urlparse
from Settings import getSettings
from DiskIo import getDiskIo


class FileDownloader:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def download(self, url, path):
        """
        Downloads the file at `url` saves it into `path`. If `path` is a directory,
        the file is saved inside that directory. If path points to a file then
        we save the download as that file. Returns the filename of the
        downloaded file.
        """
        temporaryFilename = 'download_' + self._getTimestamp() + '.tmp'
        temporaryFilePath = os.path.join(self.settings.downloadsPath, temporaryFilename)
        (_, headers) = self.UrlOpener().retrieve(url, temporaryFilePath)
        filename = self._getDownloadFilename(url, headers)

        # If we are saving to a directory, then we add the file's basename to
        # the directory to get the full path
        if self.diskIo.dirExists(path):
            if filename != '':
                filePath = os.path.join(path, os.path.basename(filename))
            else:
                # TODO: shouldn't filePath be inside path?
                filePath = temporaryFilePath
        else:
            # If we are saving to a file, just use that filename
            filePath = path

        # Move the temporary file to it's final name and destination
        self.diskIo.move(temporaryFilePath, filePath)

        return filePath

    def _getTimestamp(self):
        """
        Returns a sortable timestamp.
        For example on Dec 31 2014 at 1:00:59pm this would return:
            20141231_130059
        """
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def _getDownloadFilename(self, url, headersString):
        """
        Returns the filename of the download by first parsing the header and if
        unsuccessful, then parsing the url. If both fail, then returns an empty
        string.
        """
        headers = Message(StringIO(headersString))
        if 'content-disposition' in headers:
            regex = 'attachment; filename=(.*)'
            contentDisposition = headers['content-disposition']
            match = re.match(regex, contentDisposition)
            if match is not None:
                filename = match.group(1)
                return filename

        urlPath = urlparse(url).path
        filename = os.path.basename(urlPath)
        return filename

    class UrlOpener(urllib.FancyURLopener):
        "A URLOpener that raises an error when there is a http error"
        def http_error_default(self, url, fp, errcode, errmsg, headers):
            errorMessage = 'Error when accessing %s: %s %s' % (url, errcode, errmsg)
            raise IOError(errorMessage)


def getFileDownloader(app):
    return app.get('fileDownloader', createFileDownloader(app))


def createFileDownloader(app):
    settings = getSettings(app)
    diskIo = getDiskIo(app)
    fileDownloader = FileDownloader(settings, diskIo)
    return fileDownloader
