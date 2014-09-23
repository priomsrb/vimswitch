import os
from vimswitch.six.moves.SimpleHTTPServer import SimpleHTTPRequestHandler
import vimswitch.six.moves.socketserver as socketserver
import threading
from time import sleep
from vimswitch.six.moves import input


class SimpleServer(threading.Thread):
    def __init__(self, pathToServe, address='127.0.0.1', port=8001):
        self.pathToServe = pathToServe
        self.address = address
        self.port = port
        self.httpd = None
        threading.Thread.__init__(self)

    def run(self):
        self.httpd = socketserver.TCPServer((self.address, self.port),
                                            self.SimpleRequestHandler)
        self.httpd.pathToServe = self.pathToServe
        self.httpd.serve_forever()

    def stop(self):
        # Stop may be called before run(). So we wait up to 2 seconds for the
        # TCP server to show up
        for _ in range(20):
            if self.httpd is not None:
                self.httpd.shutdown()
                self.httpd.socket.close()
                break
            sleep(0.1)

    class SimpleRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

        def translate_path(self, path):
            # TODO: prevent path traversal
            path = path[1:]  # Remove starting slash
            pathToServe = self.server.pathToServe
            #print('path (%s), pathToServe (%s)' % (path, pathToServe))
            #print('Serving (%s)' % os.path.relpath(path, pathToServe))
            #return os.path.relpath(path, pathToServe)
            return os.path.join(pathToServe, path)

        def log_message(self, format, *args):
            # Disable logging
            pass


if __name__ == '__main__':
    try:
        s = SimpleServer(os.path.abspath(''))
        s.start()
        input('Press Enter to stop server...\n')
    finally:
        s.stop()
