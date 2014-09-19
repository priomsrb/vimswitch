class ShortHelpAction():
    def execute(self):
        version = '0.1-alpha'
        message = """
VimSwitch %s
To switch to a profile type:
    vimswitch myuser/myrepo
""" % (version)
        print(message.strip())
