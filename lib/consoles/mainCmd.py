#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lib.consoles.baseCmd import baseCmd
from lib.consoles.scriptCmd import scriptCmd
from lib.consoles.detectCmd import detectCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from lib.core.common import banner


class mainCmd(baseCmd):
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "\033[01;35msheep>\033[0m"
        banner()

    def do_script(self, line):
        """Execute pocs and exploits script"""
        scrCmd = scriptCmd()
        scrCmd.cmdloop()

    def do_detect(self, line):
        """All detection function of entrance order"""
        detect = detectCmd()
        detect.cmdloop()

if __name__ == "__main__":
    test = mainCmd()
    test.cmdloop()


