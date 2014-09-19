class InvalidArgsAction():
    def execute(self):
        message = """
Invalid arguments. Use `vimswitch myuser/myrepo` to switch profiles.
"""
        print(message.strip())
