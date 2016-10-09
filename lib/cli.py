#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from lib.core.data import paths, conf, logger
from lib.core.common import getUnicode
from lib.core.common import setPaths

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
    print os.path.dirname(os.path.realpath(__file__))
    print os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    try:
        paths.SHEEP_ROOT_PATH = modulePath()
        setPaths()
        print "success"
    except Exception:
        print "出错了"


if __name__ == "__main__":
    main()
