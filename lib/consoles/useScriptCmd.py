#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string
from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from thirdparty.prettytable.prettytable import PrettyTable
from lib.core.data import scr, logger, paths
from lib.core.common import systemQuit, getUnicode
from lib.core.enums import EXIT_STATUS

class useScriptCmd(baseCmd):
    """UseScriptCmd consoles"""
    def __init__(self, module = None):
        baseCmd.__init__(self)
        if IS_WIN:
            colorInit()
        self.shellPrompt = "sheep>script>use>"
        self.module = module
        self.readme = module.readme
        self.run = module.run
        self.defaultRun = module.defaultRun
        self.config = {}
        for key in self.readme:
            self.config[key] = None
        print self.config


    def show_options(self):
        """Show option by table"""
        id = 1
        table = PrettyTable()
        table.field_names = ["Id", "argName", "argValue", "description"]
        for k, v in self.readme.items():
            argValue= self.config[k]
            des =   getUnicode(v)
            table.add_row([id, k, argValue, v])
        print table
        return



    def do_show(self, line):
        """Main show options"""
        if line == "" or line != "options":
            print "usage: show options"
            return
        else:
            self.show_options()

