#!/usr/bin/env python
# -*- coding: utf-8 -*-

readme = {
    "target" : u"attack target",
    "thread" : u"Threading ",
    "user" : u"username",
    "pass" : u"password"
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

