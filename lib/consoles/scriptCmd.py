#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string
from lib.consoles.baseCmd import baseCmd
from lib.consoles.useScriptCmd import useScriptCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from lib.core.data import scr, logger, paths
from lib.core.common import initScr, systemQuit, importModule
from lib.core.enums import EXIT_STATUS



class scriptCmd(baseCmd):
    """"""
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "sheep>script>"
        self.current_scrid = 1
        self.scr = scr
        self.scr.all = {}
        self.scr.allpath = {}
        self.import_script_dir(paths.SCRIPT_PATH)


    def import_script(self, scriptFile):
        """Import a scipt from a directory"""
        try:
            if scriptFile and os.path.isfile(scriptFile):
                _ = os.path.split(scriptFile)[1].split('.')
                scriptName = _[0]
                if scriptName.startswith('__init__') or _[1] == 'pyc':
                    return
                self.scr.all.update({self.current_scrid: scriptName})
                self.scr.allpath.update({self.current_scrid: scriptFile})
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


    def do_use(self, line):
        """Select a script to use"""
        if line == "":
            logger.warning("Please select a script's ID.")
            return
        try:
            id = int(line)
            if id < 1 or id >= self.current_scrid:
                logger.warning("Invalid ID!")
                return
            modulepath = 'script.' + scr.all.get(id)
            print "11"
            module = importModule(modulepath)
            print "22"
            print type(module)
            Use = useScriptCmd(module)
            Use.cmdloop()
        except TypeError:
            logger.warning("Please select a script's ID.")
        except ValueError:
            logger.warning("Please select a script's ID.")
        except Exception:
            logger.error("Use error!")






    def do_list(self, line):
        """Show all available scripts"""
        msg_format = "   {:>12}  {:<32}  "
        print
        print(msg_format.format('SCRIPT-ID', 'SCR_NAME'))
        print(msg_format.format('=========', '========'))
        for i in self.scr.all.items():
            print(msg_format.format(*i))
        print
        """
        print(msg_format.format('SCRIPT-ID', 'SCR_PATH'))
        print(msg_format.format('=========', '========'))
        for i in scr.allpath.items():
            print(msg_format.format(*i))
        print
        """


if __name__ == "__main__":
    test = useScriptCmd()
    test.cmdloop()
