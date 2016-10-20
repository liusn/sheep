#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
from thread import error as threadError
from lib.core.data import th, logger
from lib.core.exception import SheepThreadException, SheepValueException, SheepConnectionException
from lib.core.settings import PYVERSION




def runThreads(numThreads, threadFunction, forwardException=True, startThreadMsg=True):
    threads = []

    th.multiThreadMode = True
    th.threadContinue = True
    th.threadException = False

    try:
        if numThreads > 1:
            if startThreadMsg:
                infoMsg = "starting %d threads" % numThreads
                logger.info(infoMsg)
        else:
            threadFunction()
            return

        for numThread in xrange(numThreads):
            thread = threading.Thread(target=exceptionHandledFunction, name=str(numThread), args=[threadFunction])
            setDaemon(thread)
            try:
                thread.start()
            except threadError, errMsg:
                errMsg = "error occurred while starting new thread ('%s')" % errMsg
                logger.error(errMsg)
                break
            threads.append(thread)

        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print
        th.threadContinue = False
        th.threadException = True

        if numThreads > 1:
            logger.info('waiting for threads to finish (Ctrl+C was pressed)')
        try:
            while (threading.activeCount() > 1):
                pass

        except KeyboardInterrupt:
            raise SheepThreadException("user aborted (Ctrl+C was pressed multiple times)")

        if forwardException:
            raise

    except (SheepValueException, SheepConnectionException), errMsg:
        print
        th.threadException = True
        logger.error('thread %s: %s' % (threading.currentThread().getName(), errMsg))

    except Exception, errMsg:
        th.threadException = True
        logger.error("thread %s: %s" % (threading.currentThread().getName(), errMsg))
#        traceback.print_exc()

    finally:
        th.multiThreadMode = False
        th.bruteMode = False
        th.threadContinue = True
        th.threadException = False

def setDaemon(thread):
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def exceptionHandledFunction(threadFunction):
    try:
        threadFunction()
    except KeyboardInterrupt:
        th.threadContinue = False
        th.threadException = True
    except Exception, errMsg:
        # thread is just going to be silently killed
        logger.error("thread %s: %s" % (threading.currentThread().getName(), errMsg))