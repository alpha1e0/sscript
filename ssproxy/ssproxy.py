#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
ssproxy.
===================================================================
shadowsocks 客户端pac文件管理，增加/删除/查询自定义过代理HOST
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
        self._pacContent = self._pacContent.replace(self.RULE_START, "".join([self.RULE_START, "\n  ", pattern, ","]))
        self.save()


    def delete(self, pattern):
        self._pacContent = self._pacContent.replace("".join(["  \"", pattern, "\",\n"]), "")
        self.save()


    def show(self):
        print "\n".join(self._currUserEntries)


    def restore(self):
        with open(self.SSPAC_BACKUP_FILE) as _file:
            rawContent = _file.read()

        with open(self.pacFilePath, 'w') as _file:
            _file.write(rawContent)


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
        pass


def main():
    parser = argparse.ArgumentParser(description=u"Mail账户验证/爆破")
    parser.add_argument("-l", "--list", action="store_true", help=u"列举所有自定义HOST")
    parser.add_argument("-a", "--add", action=hostParamParser, help=u"增加自定义HOST")
    parser.add_argument("-d", "--delete", action=hostParamParser, help=u"删除自定义HOST")
    parser.add_argument("-r", "--restore", help=u"恢复原始PAC文件")
    args = parser.parse_args()


    print "============================SS pac file manage===============================\n"
    ssm = PACFileParser(PAC_FILE)

    if args.list:
        print u"[+]: 有以下自定义HOST:"
        print ssm.show()
        return

    if args.add:
        if ssm.add(args.add):
            print u"[+]: 增加自定义HOST {0} 成功".format(args.add)
        else:
            print u"[!]: 增加自定义HOST {0} 失败".format(args.add)
        return

    if args.delete:
        if ssm.delete(args.delete):
            print u"[+]: 删除自定义HOST {0} 成功".format(args.add)
        else:
            print u"[!]: 删除自定义HOST {0} 失败".format(args.add)
        return

    if args.restore:
        if ssm.restore():
            print u"[+]: 恢复原始PAC文件成功"
        else:
            print u"[!]: 恢复原始PAC文件失败".format(args.add)
        return


if __name__ == '__main__':
    main()


