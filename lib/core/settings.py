#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys


PYVERSION = sys.version.split()[0]

IS_WIN = subprocess.mswindows

REVISION = 1.0

UNICODE_ENCODING = "utf-8"

VERSION = "1.0"

AUTHOR = "liusn"

MAIL = "liuchengsn@163.com"

SITE = 'https://github.com/liusn/sheep'

BANNER = """\033[01;34m
          ,-,
    ,---. | |...  ,---.    ,---.   ,--.,
   (  .-' | .. | | .-. '  | .-. '  |  ; )
   .-'  ` | || |  \  `--.  \  `--  | |''
   `----' '-''-'                   '-'
\033[01;37m{\033[01;m Version %s by %s mail:%s \033[01;37m}\033[0m
\n""" % (VERSION, AUTHOR, MAIL)
