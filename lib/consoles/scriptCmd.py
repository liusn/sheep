#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.consoles.baseCmd import baseCmd
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as colorInit

class scriptCmd(baseCmd):
    def __init__(self):
        if IS_WIN:
            colorInit()
        baseCmd.__init__(self)
        self.shellPrompt = "sheep>script>"

