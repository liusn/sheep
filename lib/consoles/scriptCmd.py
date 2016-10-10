#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from lib.core.data import scr, logger, paths
from lib.core.common import initScr, systemQuit
from lib.core.enums import EXIT_STATUS


class scriptCmd(baseCmd):
    """"""
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "sheep>script>"
        self.current_scrid = 1
        initScr()
        print paths.SCRIPT_PATH
        self.import_script_dir(paths.SCRIPT_PATH)
        print scr.all[5]


    def import_script(self, scriptFile):
        """Import a scipt from a directory"""
        try:
            if scriptFile and os.path.isfile(scriptFile):
                scriptName = os.path.split(scriptFile)[1]
                if scriptName.startswith('__init__'):
                    return
                scr.all.update({self.current_scrid: scriptName})
                self.current_scrid += 1
        except Exception:
            logger.warning("Import script file error!")


    def import_script_dir(self, scriptDir):
        """Import  scripts from a directory"""
        try:

            if scriptDir and os.path.isdir(scriptDir):
                for sname in os.listdir(scriptDir):
                    sname = os.path.join(scriptDir, sname)
                    self.import_script(sname)
            else:
                logger.error("script's directory error")
                systemQuit(EXIT_STATUS.ERROR_EXIT)
        except Exception:
            logger.warning("Import script dir error!")


    def do_list(self, line):
        """Show all available scripts"""
        msg_format = "   {:>12}  {:<32}  "
        print
        print(msg_format.format('IMPORTED-ID', 'SCR_PATH'))
        print(msg_format.format('===========', '========'))
        for i in scr.all.items():
            print(msg_format.format(*i))
        print


if __name__ == "__main__":
    test = scriptCmd()
    test.cmdloop()
