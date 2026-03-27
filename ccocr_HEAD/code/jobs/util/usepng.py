#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   usepng.py   260318  cy
#   updated: 260321 strip_label handles CV/DI suffixes
#
#   Utility functions for DD.usepng value checking.
#   DD.usepng can be True / False / 'BOTH'.
#   Centralizing these checks prevents bugs from 'BOTH' being truthy.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from ..env import DD

def use_png_conversion():
    # True when PNG conversion is performed before sending to API
    return DD.usepng in (True, 'BOTH')

def use_straight():
    # True when files are sent to API as-is (without PNG conversion)
    return DD.usepng in (False, 'BOTH')

def use_noup_png():
    # True when NOUP.png (marking copy) should be used instead of plain .png
    return DD.usepng in (False, 'BOTH')

def strip_label(name):
    # Remove BOTH-mode and engine suffixes added to elmlst[0] for Excel column A labeling
    return (name
            .replace(' STRAIGHT', '')
            .replace(' from PNG', '')
            .replace(' CV', '')
            .replace(' DI', ''))

def straight_name(bn):
    # hoge.pdf -> hoge.pdf.STRAIGHT.pdf
    # hoge.jpg -> hoge.jpg.STRAIGHT.jpg
    # hoge.png -> hoge.png.STRAIGHT.png
    ext = os.path.splitext(bn)[1]   # e.g. '.pdf'
    return f'{bn}.STRAIGHT{ext}'
