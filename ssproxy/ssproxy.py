#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
ssproxy.
===================================================================
shadowsocks 客户端pac文件管理，增加/删除/查询自定义过代理
'''


import os
import sys
import json
import argparse



#PAC_FILE = os.path.join("~", ".Shadowsocks", "gfwlist.js")
PAC_FILE = os.path.join(sys.path[0], "pac.txt")


class pacerror(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "pacerror: " + str(self.msg)


def isAscii(pattern):
    if not isinstance(pattern, str):
        return False
    else:
        try:
            pattern.decode("utf-8")
            pattern.decode("gbk")
        except UnicodeDecodeError:
            return False
        else:
            return True


class Output(object):
    '''
    终端输出功能
        该类用于输出信息到控制台和文件
    '''
    _RED = '\033[31m'
    _BLUE = '\033[34m'
    _YELLOW = '\033[33m'
    _GREEN = '\033[32m'
    _EOF = '\033[0m'

    _WIDTH = 80
    _CHAR = "-"

    def __init__(self, title=None, tofile=None):
        pass

    @classmethod
    def safeEncode(cls, msg, method=None):
        '''
        安全编码
            如果msg中有不能编码的字节，自动处理为16进制
        '''
        if isinstance(msg, str):
            return msg
        elif isinstance(msg, unicode):
            method = method.lower() if method else sys.stdout.encoding
            return msg.encode(method)


    @classmethod
    def R(cls, msg):
        '''
        字符串着色为红色
        '''
        return cls._RED + msg + cls._EOF

    @classmethod
    def Y(cls, msg):
        '''
        字符串着色为橙色
        '''
        return cls._YELLOW + msg + cls._EOF

    @classmethod
    def B(cls, msg):
        '''
        字符串着色为蓝色
        '''
        return cls._BLUE + msg + cls._EOF

    @classmethod
    def G(cls, msg):
        '''
        字符串着色为绿色
        '''
        return cls._GREEN + msg + cls._EOF


    @classmethod
    def raw(cls, msg):
        '''
        无颜色输出
        '''
        print cls.safeEncode(msg)
    

    @classmethod
    def red(cls, msg):
        '''
        打印红色信息
        '''
        cls.raw(cls.R(msg))

    @classmethod
    def yellow(cls, msg):
        '''
        打印橙色信息
        '''
        cls.raw(cls.Y(msg))

    @classmethod
    def blue(cls, msg):
        '''
        打印蓝色信息
        '''
        cls.raw(cls.B(msg))

    @classmethod
    def green(cls, msg):
        '''
        打印绿色信息
        '''
        cls.raw(cls.G(msg))



class PACFileParser(object):
    SSPAC_BACKUP_FILE = os.path.join(sys.path[0], ".sspacbackup")
    RULE_START = "var rules = ["
    SPLIT_LINE = "\".user-defined-entries-split.line\""

    def __init__(self, pacFilePath):
        self._pacFilePath = pacFilePath

        if not os.path.exists(self._pacFilePath):
            raise pacerror("pac file not found at {0}".format(self._pacFilePath))

        self._pacContent = ""

        self._loadPacFile()
        self._firstParse()

        self._currUserEntries = self._loadUserEntries()


    def add(self, pattern):
        if pattern in self._pacContent:
            return False

        self._pacContent = self._pacContent.replace(self.RULE_START, "".join([self.RULE_START, "\n  ", "\"", pattern, "\","]))
        self.save()

        return True


    def delete(self, pattern):
        if pattern not in self._pacContent:
            return False

        self._pacContent = self._pacContent.replace("".join(["  \"", pattern, "\",\n"]), "")
        self.save()

        return True


    def list(self):
        return "\n".join(self._currUserEntries)


    def restore(self):
        with open(self.SSPAC_BACKUP_FILE) as _file:
            rawContent = _file.read()

        with open(self._pacFilePath, 'w') as _file:
            _file.write(rawContent)

        return True


    def _flushProxyConfig(self):
        pass


    def _saveChanges(self):
        with open(self._pacFilePath, "w") as _file:
            _file.write(self._pacContent)


    def save(self):
        self._saveChanges()

        self._flushProxyConfig()


    def _loadPacFile(self):
        with open(self._pacFilePath) as _file:
            self._pacContent = _file.read()


    def _loadUserEntries(self):
        startPos = self._pacContent.find(self.RULE_START) + len(self.RULE_START)
        endPos = self._pacContent.find(self.SPLIT_LINE)

        userEntriesStr = self._pacContent[startPos:endPos]

        userEntries = [x.strip().strip("\"") for x in userEntriesStr.split(",")]

        return userEntries


    def _backup(self):
        if not os.path.exists(self.SSPAC_BACKUP_FILE):
            with open(self.SSPAC_BACKUP_FILE,'w') as _file:
                _file.write(self._pacContent)


    def _firstParse(self):
        if self.SPLIT_LINE not in self._pacContent:
            self._backup()
            self._pacContent = self._pacContent.replace(self.RULE_START, "".join([self.RULE_START, "\n  ", self.SPLIT_LINE, ","]))
            self._saveChanges()



class hostParamParser(argparse.Action):
    '''
    host类型参数处理器
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        values = values.strip()
        if not isAscii(values):
            raise pacerror("url should be ascii")
        if values.startswith("|") or values.startswith("@") or values.startswith("."):
            setattr(namespace, self.dest, values)
        else:
            setattr(namespace, self.dest, "||"+values)


def main():
    parser = argparse.ArgumentParser(description=u"Shadowsocks PAC 操作")
    parser.add_argument("-l", "--list", action="store_true", help=u"列举所有自定义项")
    parser.add_argument("-a", "--add", action=hostParamParser, help=u"增加自定义项")
    parser.add_argument("-d", "--delete", action=hostParamParser, help=u"删除自定义项")
    parser.add_argument("-r", "--restore", action="store_true", help=u"恢复原始PAC文件")
    args = parser.parse_args()


    out = Output()
    out.yellow(u">>>>>>>>>>>>>>>  Shadowsocks PAC 操作  <<<<<<<<<<<<<<<<<<\n")

    ssm = PACFileParser(PAC_FILE)

    if args.list:
        out.yellow(u"[+]: 有以下自定义项:\n")
        out.raw(ssm.list())
        return

    if args.add:
        if ssm.add(args.add):
            out.green("[+]: 增加 \"{0}\" 成功".format(args.add))
        else:
            out.red(u"[!]: 增加 \"{0}\" 失败".format(args.add))
        return

    if args.delete:
        if ssm.delete(args.delete):
            out.green(u"[+]: 删除 \"{0}\" 成功".format(args.delete))
        else:
            out.red(u"[!]: 删除 \"{0}\" 失败".format(args.delete))
        return

    if args.restore:
        if ssm.restore():
            out.green(u"[+]: 恢复原始PAC文件成功")
        else:
            out.red(u"[!]: 恢复原始PAC文件失败".format(args.add))
        return


if __name__ == '__main__':
    try:
        main()
    except pacerror as error:
        print str(error)


