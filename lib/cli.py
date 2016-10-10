#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from lib.core.data import paths, conf, logger
from lib.core.common import getUnicode, setPaths
from lib.consoles.mainCmd import mainCmd

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
        print "success"
    except Exception:
        print "出错了"


if __name__ == "__main__":
    main()
