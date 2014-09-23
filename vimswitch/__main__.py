from .VimSwitch import VimSwitch
import sys


if __name__ == '__main__':
    vimSwitch = VimSwitch()
    exitCode = vimSwitch.main(sys.argv)
    sys.exit(exitCode)
