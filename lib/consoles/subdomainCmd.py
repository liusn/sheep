#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from thirdparty.prettytable.prettytable import PrettyTable
from lib.core.data import logger
from lib.api.subDomainsBrute import run


class subdomainCmd(baseCmd):
    """Subdomain detection class"""
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "\033[01;35msheep>detect>subdomain>\033[0m"
        self.domain = ""
        self.full_scan = False
        self.i = False
        self.output = None


    def do_run(self, line):
        """Detect this domain, usage: run"""
        if self.domain == "":
            logger.warning("Please set  a domain name to detect!")
            return
        args = {}
        args["domain"] = self.domain
        args["i"] = self.i
        args["full_scan"] = self.full_scan
        args["output"] = self.output
        run(args)


    def do_set(self, line):
        """Set domain options. usage:set domain = baidu.com"""
        if line == "" or line.find('=') == -1:
            print "usage:set domain = baidu.com"
            return
        _ = line.split('=', 1)
        k = _[0].strip()
        v = _[1].strip()
        if k == "domain":
            self.domain = v
        elif k == "i":
            self.i = True
        elif k == "full_scan":
            self.full_scan = True
        elif k == "output":
            self.output = v
        else:
            print "usage:set domain = baidu.com"


    def show_options(self):
        """Show option by table"""
        table = PrettyTable()
        print "\033[01;33m            =====Detect subdomain=====    \033[0m"
        table.field_names = ["Id", "argName", "argValue", "description"]
        table.add_row([1, "domain", self.domain, "To detect for a domain name"])
        table.add_row([2, "full_scan", self.full_scan, "Full scan, a large NAMES FILE will be used during the scan, default=False"])
        table.add_row([3, "i", self.i, "Ignore domains pointed to private IPs, default=False"])
        table.add_row([4, "output", self.output, "Output file name. default is  data/subdomain/{target}.txt"])
        print table


    def do_show(self, line):
        """Main show options"""
        if line == "" or line != "options":
            print "usage: show options"
            return
        else:
            self.show_options()

"""
if __name__ == "__main__":
    test = subdomainCmd()
    test.cmdloop()
"""