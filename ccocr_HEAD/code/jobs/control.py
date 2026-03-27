#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   control.py      251225  cy
#   updated: 260320.093743 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt                 import prnt
from .env                   import DD
from .loadxl.loadxl         import loadxl
from .mv2input.mv2input     import mv2input
from .setup_flds.setup_flds import setup_flds
from .docopy.docopy         import docopy
from .pdf2png.pdf2png       import pdf2png
from .util.svjsn.svjsn      import svjsn
#from .jsn2db.jsn2db         import jsn2db
from .aby.aby               import aby

from .txtmode.jsn2txt       import jsn2txt


def control():
    loadxl()                        # parse global setting only
    if DD.jobtyp == 'frm':
        msconf = mv2input()         # parse _dd and such
        setup_flds()
        if docopy() is False:       # use lod png* or not
            pdf2png()
            svjsn()
            #
            #   CHECKPOINT (B)
            #
            #   jsnRAW  ready   hoge.ext.NN.CV.json
            #                   hoge.ext.NN.DI.json
            #
            #   pngPRE  ready   hoge.ext.NN.png             (canvas only)
            #   pngUP   ready   hoge.ext.NN.png / hoge.ext.STRAIGHT.ext
            #
            #   NOT YET         pngROT pngMK pngRMK
            #
            prnt('''

    CHECK (B): svjsn() finished
    1) jsnRAW : API responses ready (hoge.ext.NN.CV.json / .DI.json)
    2) pngROT pngMK pngRMK : NOT YET CREATED

    BACKUP log folder

    hit a key to quit now ...
            ''')
            input('ok? ')
            quit()

            ## chkjson moved
#            jsn2db()                ## json -> db, mark png

        aby(msconf)
    elif DD.jobtyp == 'txt':
        setup_flds()
        mv2input()
        pdf2png()                   # -> twoup -> updn
        svjsn()
        jsn2txt()
    else:
        raise Exception('PG bug')
#    finish()
    return
