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


class runPocsCmd(baseCmd):
    """runPocsCmd concole."""
    def __init__(self):
        baseCmd.__init__(self)
        if IS_WIN:
            colorInit()
        self.shellPrompt = "sheep>script>runPocs>"
        self.ip = None
        self.file = None
        self.url = None


    def do_set(self, line):
        """Set pocs target options. usage:set ip=1.1.1.1"""
        if line == "" or line.find('=') == -1:
            print "usage:set ip=1.1.1.1"
            return
        _ = line.split('=')
        k = _[0].strip()
        v = _[1].strip()
        if k == 'ip':
            self.ip = v
        elif k == 'file':
            self.file = v
        elif k == 'url':
            self.url = v
        else:
            logger.warning('Not this options, only ip, file, url!')


    def show_options(self):
        """Show option by table"""
        ipDec = "target ip/mask, usage: 127.0.0.1/24"
        fileDec = "target file, ussge: ./data/target.txt"
        urlDec = "target url. usage: www.baidu.com"
        table = PrettyTable()
        print "          ---------------------------------------------"
        print "          *******target(Choose one of the three)*******"
        print "          ---------------------------------------------"
        table.field_names = ["Id", "argName", "argValue", "description"]
        table.add_row([1, 'ip', self.ip, ipDec])
        table.add_row([2, 'file', self.file, fileDec])
        table.add_row([3, 'url', self.url, urlDec])
        print table


    def do_show(self, line):
        """Main show options"""
        if line == "" or line != "options":
            print "usage: show options"
            return
        else:
            self.show_options()


if __name__ == "__main__":
    test = runPocsCmd()
    test.cmdloop()