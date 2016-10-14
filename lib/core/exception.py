#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SheepBaseException(Exception):
    pass


class SheepConnectionException(Exception):
    pass


class SheepThreadException(SheepBaseException):
    pass


class SheepDataException(SheepBaseException):
    pass


class SheepMissingPrivileges(SheepBaseException):
    pass


class SheepUserQuitException(SheepBaseException):
    pass


class SheepSystemException(SheepBaseException):
    pass


class SheepValueException(SheepBaseException):
    pass


class SheepPluginException(SheepBaseException):
    pass
