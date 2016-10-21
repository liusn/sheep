#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
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
        self.shellPrompt = "\033[01;35msheep>script>runPocs>\033[0m"
        self.allPocs = pocs
        self.targets = Queue.Queue()
        self.mixTargets = Queue.Queue()
        self.ip = None
        self.file = None
        self.url = None
        self.threadsun = 1
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
            output = (pocName, tar, "success" if result else "failed")
            self.results.add(output)


    def create_output_dir(self):
        """Create the output directory!"""
        pocsPath = os.path.join(paths.OUTPUT_PATH, 'pocs')
        if not os.path.isdir(pocsPath):
            try:
                os.makedirs(pocsPath)
                logger.info("Using '%s' as the pocs output directory" % pocsPath)
            except Exception, e:
                logger.warning("Create pocs output directory '%s' failed! %s" % (pocsPath, e))

        #Create a directory by current time
        today = time.strftime("%Y-%m-%d")
        todayPath = os.path.join(pocsPath, today)
        if not os.path.isdir(todayPath):
            try:
                os.makedirs(todayPath)
                logger.info("Using '%s' as the pocs today output directory" % todayPath)
            except Exception, e:
                logger.warning("Create pocs today output directory '%s' failed! %s" % (todayPath, e))

        return todayPath


    def set_record_files(self):
        """Create the output file!"""
        todayPath = self.create_output_dir()
        second = time.strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
        outputPath = os.path.join(todayPath, second)
        msg_format = " {:>25}  {:^50}  {:<10} \n"
        if not os.path.isfile(outputPath):
            try:
                with open(outputPath, "w") as f:
                    f.write(msg_format.format("pocName", "target", "result"))
                    f.write(msg_format.format("=======", "======", "======"))
                    f.close()
            except Exception, e:
                logger.warning("Create %s file failed! %s" % (outputPath, e))

        try:
            with open(outputPath, "a+") as f:
                for (pocName, target, result) in self.results:
                    f.write(msg_format.format(pocName, target, result))
                f.close()
        except Exception, e:
            logger.warning("Write this results error! %s" % e)
        logger.info("Save the result in %s!" % outputPath)


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
            self.set_record_files()
            self.results.clear()


    def do_set(self, line):
        """Set pocs target options. usage:set ip=1.1.1.1"""
        if line == "" or line.find('=') == -1:
            logger.warning("Invalid, usage:set ip=1.1.1.1")
            return
        _ = line.split('=', 1)
        k = _[0].strip()
        v = _[1].strip()
        if k == 'ip':
            self.ip = v
        elif k == 'file':
            self.file = v
        elif k == 'url':
            self.url = v
        elif k == 'threads':
            self.threadsun = int(v)
        else:
            logger.warning('Not this options, only ip, file, url, threads!')


    def show_options(self):
        """Show option by table"""
        ipDec = "target ip/mask, usage: set = 127.0.0.1/24"
        fileDec = "target file, Please put the DATA directory.  ussge: set file = target.txt"
        urlDec = "target url. usage: set url = www.baidu.com"
        threadDec = "Default thread id 1, usage: set threads = 10"
        table = PrettyTable()
        print "\033[01;33m          ---------------------------------------------\033[0m"
        print "\033[01;32m          *******target(Choose one of the three)*******\033[0m"
        print "\033[01;33m          ---------------------------------------------\033[0m"
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
