#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023-02-15 15:55
# @Site    :
# @File    : sycmDecrypt.py
# @Software: PyCharm

"""生意参谋解密调用此文件，不要调用SYCMCryptUtil"""
from XZGUtil.SYCMCryptUtil import decrypt, transitId

def get_transitId():
    return transitId()


def data_decrypt(msg):
    return decrypt(msg)

