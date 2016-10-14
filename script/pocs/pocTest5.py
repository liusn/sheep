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
    print "poctest Running..."
    print
    print "End!"
    return True

def poc(target = "1.1.1.1"):
    return True

