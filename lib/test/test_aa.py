#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import time
import unicodedata
#from script.test import test
from lib.core.settings import IS_WIN
from lib.core.common import banner, importModule
from thirdparty.prettytable.prettytable import PrettyTable

readme = {
    "target": "1.1.1.1",
    "port": "22",
    "user": "user.txt",
    "pass": "pass.txt"
}

mod = importModule("script.exploits.bruteForce_mutith_ssh")


mod.run(readme)

