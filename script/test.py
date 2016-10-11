#!/usr/bin/env python
# -*- coding: utf-8 -*-

readme = {
    "target" : u"目标ip，或网址",
    "theard" : u"线程数，默认为1",
    "user" : u"用户名",
    "pass" : u"密码"
}

def run(arg = None):
    if arg == None or type(arg) != dict:
        print "Missing Parameters or parameter is not a dict!"
        return
    for k, v in arg.items():
        print "k = %s, v = %s" % (k, v)
    print "Running..."
    print
    print "End!"

def defaultRun(target = "1.1.1.1", thread = '1', user = "admin", password = "qwe等等" ):
    print "Running default..."
    print "target = %s, thread = %s, user = %s, password = %s" % (target, thread, user, password)
    print
    print "End!"

