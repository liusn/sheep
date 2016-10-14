#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string
import Queue
from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit
from thirdparty.prettytable.prettytable import PrettyTable
from thirdparty.oset.pyoset import oset
from thirdparty.IPy import IPy
from lib.core.data import logger, paths, th
from lib.core.common import importModule
from lib.core.theards import runThreads


class runPocsCmd(baseCmd):
    """runPocsCmd concole."""
    def __init__(self, pocs):
        baseCmd.__init__(self)
        if IS_WIN:
            colorInit()
        self.shellPrompt = "sheep>script>runPocs>"
        self.allPocs = pocs
        self.targets = Queue.Queue()
        self.mixTargets = Queue.Queue()
        self.ip = None
        self.file = None
        self.url = None
        self.threadsun = 10
        self.pocModule = {}
        self.results = oset()


    def check_target(self):
        """Check targets and add in queue"""
        ok = 0

        if self.ip != None:
            try:
                _list = IPy.IP(self.ip)
            except Exception, e:
                logger.error('Invalid IP/MASK, %s' % e)
                return False
            for i in _list:
                self.targets.put(str(i))
            ok = 1

        if self.file != None:
            filePath = os.path.join(paths.DATA_PATH, self.file)
            if not os.path.isfile(filePath):
                logger.error('Invalid %s file!' % self.file)
                return False
            for line in open(filePath):
                _ = line.strip()
                if _:
                    self.targets.put(_)
            ok = 1

        if  self.url != None:
            self.targets.put(self.url)
            ok = 1

        if ok == 0:
            logger.warning('Please set target.(ps: show options)')
            return False
        else:
            return True


    def import_pocs(self):
        """Import pocs"""
        _ = 'script.pocs.'
        for k, v in self.allPocs.items():
            modulePath = _ + v
            mod = importModule(modulePath)
            if not hasattr(mod, 'poc') or mod == False:
                logger.warning('Import %s error!' % v)
                continue
            self.pocModule.update({v: mod})


    def mix_targets(self):
        """Mix the targets and the pocs"""
        while not self.targets.empty():
            tar = self.targets.get()
            for k, v in self.pocModule.items():
                self.mixTargets.put((k, tar, v))


    def poc_threads(self):
        """MultiThread executing """
        while not self.mixTargets.empty() and th.threadContinue:
            pocName, tar, module = self.mixTargets.get()
            infoMsg = "Poc : %s    target : %s" % (pocName, tar)
            logger.info(infoMsg)
            result = module.poc(tar)
            output = (pocName, tar, "success" if result == True else result)
            self.results.add(output)


    def do_run(self, line):
        """Run all pocs, usage: run"""
        if self.check_target():
            logger.info('Sheep got a total of %d targets.' % self.targets.qsize())
            self.import_pocs()
            self.mix_targets()
            try:
                runThreads(self.threadsun, self.poc_threads)
            except Exception, e:
                logger.error('Run error! %s' % e)
            table = PrettyTable()
            table.field_names = ["pocNmae", "target", "result"]
            table.padding_width = 1
            if not self.results:
                return
            toNum, sucNum = 0, 0
            for row in self.results:
                table.add_row(list(row))
                toNum += 1
                if row[2] == 'success':
                    sucNum += 1
            print
            logger.info("Result:")
            print table
            print "success : %d / %d " % (sucNum, toNum)
            self.results.clear()


    def do_set(self, line):
        """Set pocs target options. usage:set ip=1.1.1.1"""
        if line == "" or line.find('=') == -1:
            logger.warning("Invalid, usage:set ip=1.1.1.1")
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
        elif k == 'threads':
            self.threadsun = v
        else:
            logger.warning('Not this options, only ip, file, url, threads!')


    def show_options(self):
        """Show option by table"""
        ipDec = "target ip/mask, usage: set = 127.0.0.1/24"
        fileDec = "target file, Please put the DATA directory.  ussge: set file = target.txt"
        urlDec = "target url. usage: set url = www.baidu.com"
        threadDec = "Default thread id 10, usage: set threads = 10"
        table = PrettyTable()
        print "          ---------------------------------------------"
        print "          *******target(Choose one of the three)*******"
        print "          ---------------------------------------------"
        table.field_names = ["Id", "argName", "argValue", "description"]
        table.add_row([1, 'ip', self.ip, ipDec])
        table.add_row([2, 'file', self.file, fileDec])
        table.add_row([3, 'url', self.url, urlDec])
        table.add_row([4, 'threads', self.threadsun, threadDec])
        print table


    def do_show(self, line):
        """Main show options"""
        if line == "" or line != "options":
            print "usage: show options"
            return
        else:
            self.show_options()


if __name__ == "__main__":
    test = runPocsCmd('ee')
    test.cmdloop()
