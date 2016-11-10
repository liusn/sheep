#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lib.consoles.baseCmd import baseCmd
from lib.consoles.subdomainCmd import subdomainCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit


class detectCmd(baseCmd):
    """All detection function of entrance class"""
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "\033[01;35msheep>detect>\033[0m"


    def do_subdomain(self, line):
        """Call probe subdomain functions"""
        sub = subdomainCmd()
        sub.cmdloop()


