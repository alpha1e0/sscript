#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Python 代码注释规范
Copyright (c) 2016 alpha1e0
========================================================
该模块用于说明Python代码的注释风格(模块的简单描述信息)
'''

__author__ = "alpha1e0"
__version__ = "1.0"


def someFunc(param1,param2,*args,**kwargs):
    '''
    函数功能的简单描述
        函数功能的详细描述
    @params:
        param1: 类型, 参数param1的说明
        param2: 类型, 参数params2的说明
    @returns:
        类型, 函数返回值的说明
            函数返回中某些部分的详细说明
    @remarks:
        该函数其他的备注信息
    @examples:
        该函数的使用示例
    '''
    param = params.strip() # 单行的注释

    # 多行功能模块的注释
    strCookie = strCookie.strip()
    if strCookie.find("Cookie:") == 0:
        strCookie = strCookie[7:].lstrip()


    return {'a':'aa','b':'bb'}


class Result(dict):
    '''
    类的简单描述
        类的详细描述
    @remarks:
        类的其他重要信息
    @examples:
        该类的使用示例
    '''
    
    NOTVUL = 0  # 静态变量的注释

    def __init__(self, expObject=None):
        '''
        函数功能的简单描述
            函数功能的详细描述
        @params:
            param1: 类型, 参数param1的说明
            param2: 类型, 参数params2的说明
        @returns:
            类型, 函数返回值的说明
                函数返回中某些部分的详细说明
        @remarks:
            该函数其他的备注信息
        @examples:
            该函数的使用示例
        '''
        pass