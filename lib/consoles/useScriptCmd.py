#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from thirdparty.prettytable.prettytable import PrettyTable
from lib.core.data import logger
from lib.core.common import getUnicode


class useScriptCmd(baseCmd):
    """UseScriptCmd consoles"""
    def __init__(self, module = None, name = None):
        baseCmd.__init__(self)
        if IS_WIN:
            colorInit()
        self.shellPrompt = "\033[01;35msheep>script>use>\033[0m"
        self.name = name
        self.module = module
        self.readme = module.readme
        self.run = module.run
        if hasattr(module, 'defaults'):
			self.defaults = module.defaults
        else:
			self.defaults = {}
        self.config = {}
        for key in self.readme:
            if self.defaults.has_key(key):
				self.config[key] = self.defaults[key]
            else:
				self.config[key] = None


    def show_options(self):
        """Show option by table"""
        id = 1
        table = PrettyTable()
        print "\033[01;33m            =====%s=====    \033[0m" % self.name
        table.field_names = ["Id", "argName", "argValue", "description"]
        for k, v in self.readme.items():
            argValue= self.config[k]
            des =   getUnicode(v)
            table.add_row([id, k, argValue, v])
        print table


    def do_show(self, line):
        """Main show options"""
        if line == "" or line != "options":
            print "usage: show options"
            return
        else:
            self.show_options()


    def do_set(self, line):
        """Set script options. usage:set target=1.1.1.1"""
        if line == "" or line.find('=') == -1:
            print "usage:set target=1.1.1.1"
            return
        _ = line.split('=', 1)
        k = _[0].strip()
        v = _[1].strip()
        if self.config.has_key(k):
            self.config[k] = v
        else:
            logger.warning("Without this configuration options. ps: show options")


    def do_run(self, line):
        """Run this script, usage: run"""
        for k, v in self.config.items():
            if v == None:
                ch = "The %s has not been set. ps: set %s = ***" % (k, k)
                logger.warning(ch)
                return
        result = self.run(self.config)


