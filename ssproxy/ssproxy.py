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



PAC_FILE = os.path.join("~", ".Shadowsocks", "gfwlist.js")


class PACFileParser(class):
    def __init__(self, pacPath, userDefinedHOSTFilePath=None):
        pass


    def add(self, pattern):
        pass


    def rm(self, pattern):
        pass


    def show(self):
        pass


    def restore(self):
        pass


    def _backup(self):
        pass


    def _async(self):
        pass



class hostParamParser(argparse.Action):
    '''
    host类型参数处理器
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        pass


def main():
    parser = argparse.ArgumentParser(description=u"Mail账户验证/爆破")
    parser.add("-l", "--list", action="store_true", help=u"列举所有自定义HOST")
    parser.add("-a", "--add", action=hostParamParser, help=u"增加自定义HOST")
    parser.add("-d", "--delete", action=hostParamParser, help=u"删除自定义HOST")
    parser.add("-r", "--restore", help=u"恢复原始PAC文件")
    args = parser.parse_args()


    print "============================SS pac file manage===============================\n"
    ssm = PACFileParser()
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
        if ssm.rm(args.add):
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


