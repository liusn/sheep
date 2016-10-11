#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
#from script.test import test
from lib.core.settings import IS_WIN
from lib.core.common import banner, importModule
from thirdparty.prettytable.prettytable import PrettyTable


test = importModule('script.test')
print test.readme
test.run(11)
test.run(test.readme)
test.defaultRun()

x = PrettyTable()
x.field_names = ["id", "ss"]
u = test.readme["user"]
x.add_row([1, u])
print x
