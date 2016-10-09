#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
from lib.core.data import paths, logger, conf
from lib.core.exception import SheepMissingPrivileges


def setPaths():
    """
    Sets absolute paths for project directories and files
    :return:
    """
    root_path = paths.SHEEP_ROOT_PATH
    paths.DATA_PATH = os.path.join(root_path, "data")
    paths.SCRIPT_PATH = os.path.join(root_path, "script")
    paths.OUTPUT_PATH = os.path.join(root_path, "output")
    paths.CONFIG_PATH = os.path.join(root_path, "sheep.conf")
    if not os.path.exists(paths.SCRIPT_PATH):
        os.mkdir(paths.SCRIPT_PATH)
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)

    paths.WEAK_PASS = os.path.join(paths.DATA_PATH, "pass100.txt")
    paths.LAGRE_WEAK_PASS = os.path.join(paths.DATA_PATH, "pass1000.txt")
    paths.UA_LIST_PATH = os.path.join(paths.DATA_PATH, "user-agents.txt")

    if os.path.isfile(paths.CONFIG_PATH) and os.path.isfile(paths.WEAK_PASS) and os.path.isfile(paths.LAGRE_WEAK_PASS) and os.path.isfile(paths.UA_LIST_PATH):
        pass
    else:
        msg = 'Some files missing, it may cause an issue.\n'
        raise SheepMissingPrivileges(msg)

def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return u'NULL'

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances