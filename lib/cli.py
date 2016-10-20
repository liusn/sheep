#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from lib.core.data import paths
from lib.core.common import getUnicode, setPaths, systemQuit
from lib.consoles.mainCmd import mainCmd
from lib.core.enums import EXIT_STATUS

def modulePath():
    """
    the function will get us the program's directory
    :return:
    """
    return getUnicode(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), sys.getfilesystemencoding())

def main():
    """
    Main function of sheep when running from command line.
    :return:
    """
    try:
        paths.SHEEP_ROOT_PATH = modulePath()
        setPaths()
        mainC = mainCmd()
        mainC.cmdloop()
    except KeyboardInterrupt:
        systemQuit(EXIT_STATUS.USER_QUIT)
    except Exception:
        systemQuit(EXIT_STATUS.ERROR_EXIT)


if __name__ == "__main__":
    main()
