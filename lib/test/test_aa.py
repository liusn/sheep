#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import time
import unicodedata
import requests
#from script.test import test
from lib.core.settings import IS_WIN
from lib.core.common import banner, importModule
from thirdparty.prettytable.prettytable import PrettyTable

r = requests.get("http://github.com")
r.encoding = 'utf-8'
print r.url
print r.cookies
print r.history


