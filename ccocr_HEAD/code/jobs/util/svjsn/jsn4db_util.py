#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn4db_util.py  260328  cy
#
#   Shared geometry helpers for jsn4db converters.
#
#--------1---------2---------3---------4---------5---------6---------7--------#


def raw4(bb):
    # bb: [TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y]
    top = min(bb[1], bb[3])
    btm = max(bb[5], bb[7])
    lft = min(bb[0], bb[6])
    ryt = max(bb[2], bb[4])
    return top, btm, lft, ryt


def page_bounds(elems):
    ptop = min(e[0] for e in elems)
    plft = min(e[2] for e in elems)
    pryt = max(e[3] for e in elems)
    return ptop, plft, pryt


def zoom(plft, pryt):
    width = pryt - plft
    return 1200 / width if width > 0 else 1.0


def elem(node, raw, ptop, plft, zm, text, conf):
    top, btm, lft, ryt = raw
    return {
        'node' : node,
        'top'  : round((top - ptop) * zm),
        'btm'  : round((btm - ptop) * zm),
        'lft'  : round((lft - plft) * zm),
        'ryt'  : round((ryt - plft) * zm),
        'otop' : top,
        'obtm' : btm,
        'olft' : lft,
        'oryt' : ryt,
        'text' : text,
        'conf' : conf,
    }
