class InvalidArgsAction():
    def execute(self):
        message = """
Invalid Arguments. Use `vimswitch <profile>` to switch profiles.
"""
        print(message.strip())
