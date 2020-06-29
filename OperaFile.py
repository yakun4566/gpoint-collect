# -*- coding:utf-8 -*-
def write_txt(filename, str):
    txt = open(filename, mode="w", encoding="utf-8")
    txt.write(str)
    txt.close()


def write_line(filename, str):
    txt = open(filename, mode="a", encoding="utf-8")
    txt.write(str)
    txt.close()


def read_txt(filename):
    txt = open(filename, mode="r", encoding="utf-8")
    t = txt.read()
    txt.close()
    return t
