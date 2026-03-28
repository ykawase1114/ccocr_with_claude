#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   dump2db.py      260328  cy
#
#   Write jsn4db results to {jobid}.dump.db (SQLite).
#   Called from svjsn() after all jsn4db() calls complete.
#
#   Input:  results dict  { dst_path: out_dict }
#           out_dict keys: pdf, engine, apisrc, pages
#
#   Tables:
#     page(pdf, page, ptop, plft, pryt, engine, apisrc)
#     elm (seq, pdf, page, node, typ, top..ryt, txt, otop..oryt,
#          note1..3, pg_top, pg_btm, conf, engine, apisrc)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3

from m.prnt         import prnt
from m.env          import D
from jobs.env       import DD
from .dump2db_xl    import dump2db_xl


def dump2db(results):
    """
    results : { dst_path: out_dict }
    Writes page + elm tables, then generates dump Excel.
    """
    dbf    = os.path.join(D.logd, f'{D.jobid}.dump.db')
    DD.dbf = dbf
    prnt('writing dump db')

    con = sqlite3.connect(dbf)
    cur = con.cursor()
    _create_tables(cur)

    for out in results.values():
        _write_out(cur, out)

    con.commit()
    con.close()
    dump2db_xl()


def _create_tables(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS page (
            pdf     TEXT,
            page    INTEGER,
            ptop    INTEGER,
            plft    INTEGER,
            pryt    INTEGER,
            engine  TEXT,
            apisrc  TEXT,
            UNIQUE(pdf, page, engine, apisrc)
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS elm (
            seq     INTEGER PRIMARY KEY,
            pdf     TEXT,
            page    INTEGER,
            node    TEXT,
            typ     TEXT,
            top     INTEGER,
            btm     INTEGER,
            lft     INTEGER,
            ryt     INTEGER,
            txt     TEXT,
            otop    INTEGER,
            obtm    INTEGER,
            olft    INTEGER,
            oryt    INTEGER,
            note1   TEXT,
            note2   TEXT,
            note3   TEXT,
            pg_top  INTEGER,
            pg_btm  INTEGER,
            conf    REAL,
            engine  TEXT,
            apisrc  TEXT
        )''')


def _write_out(cur, out):
    pdf    = out['pdf']
    engine = out['engine']
    apisrc = out['apisrc']
    tb_exp = 100000

    for pg in out['pages']:
        page_num = pg['page']
        cur.execute('''
            INSERT OR IGNORE INTO page(pdf, page, ptop, plft, pryt, engine, apisrc)
            VALUES(?,?,?,?,?,?,?)''',
            (pdf, page_num, pg['ptop'], pg['plft'], pg['pryt'], engine, apisrc))

        for line in pg['lines']:
            _ins_elm(cur, pdf, page_num, engine, apisrc, line, 'line', tb_exp)
            for word in line.get('words', []):
                _ins_elm(cur, pdf, page_num, engine, apisrc, word, 'word', tb_exp)

        for word in pg.get('orphan_words', []):
            _ins_elm(cur, pdf, page_num, engine, apisrc, word, 'orphan', tb_exp)


def _ins_elm(cur, pdf, page_num, engine, apisrc, elem, typ, tb_exp):
    top = elem['top']
    btm = elem['btm']
    cur.execute('''
        INSERT INTO elm(
            pdf, page, node, typ,
            top, btm, lft, ryt,
            txt,
            otop, obtm, olft, oryt,
            pg_top, pg_btm,
            conf, engine, apisrc
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
        pdf, page_num, elem['node'], typ,
        top, btm, elem['lft'], elem['ryt'],
        elem['text'],
        elem['otop'], elem['obtm'], elem['olft'], elem['oryt'],
        page_num * tb_exp + top,
        page_num * tb_exp + btm,
        elem['conf'], engine, apisrc,
    ))
