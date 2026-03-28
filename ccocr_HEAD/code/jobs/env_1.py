#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   env.py      250129  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

class DD:
    ## set at loadxl
    config  = None
    jobtyp  = None  # txt, frm, cnf
    pdf2up  = None
    horiz   = None
    ## set at extraitms (values are for old "global" sheet)
    engines     = ['vision']
    pdf2api     = False
    png2api     = True
    use_web     = False
    use_macro   = True
    use_spic    = True
    ## set at cred
    url_up  = None
    hdr_up  = None
    hdr_dn  = None
    proxy   = None
    di_ep   = None        # Document Intelligence endpoint
    di_key  = None        # Document Intelligence key
    ## set at setup_flds
    usrd        = None
    inputd      = None
    img         = None
    pdfpg       = None
    pdfpgPng    = None
    pngPRE          = None
    pngUP           = None
    jsn         = None
    jsn_raw     = None        # API responses (CV + DI, hoge.ext.NN.CV/DI.json)
    ## set at encChk
    skipPdf     = []    # list of pdf which needs preprocess
    skipPdfEnc  = {}    # { 'hoge.pdf': {'90ms-RKSJ-H', ...}, ... }
    ## set at savetxt
    txtd    = None
    ## used at chkdrctn
    angls = [-180, -90, 0 , 90, 180 ]
    ## set at updn
    cred_ok = False
    ## used at towup
    twoupdic    = {}

    ## set at markpng or cpydb
    pngROT  = None
    pngMK   = None
    pngRMK  = None

    ## set at writedb or cpydb
    dbf     = None

    ## set at writexl or cpydb
    dumpf   = None

    ## set at ldsorter
    mscnf   = None

    # used at wtitedb, m_loadsorter.m_loadxl.vl0chk
    tb_exp  = 100000

    # used at loadxl, ...
    frmopt  = {}

    # used at mv2input
    # supprted image extentions
    imgext  = ['pdf','png','gif','jpg','jpeg','bmp']

    # used at mv2input
    imgs    = []

    # used at cancopy
    cpysrc  = None

    # set at optins


    outd        = None

##
## ocr json key-value
##
class jkvs:
    class CV:
#       ##  LV1 check : lv1() ##
#       $.status                            exists/not
#       $.createdDateTime                   exists/not
#       $.lastUpdatedDateTime               exists/not
#       $.analyzeResult.version             '3.2.0'
#       $.analyzeResult.modelVersion        '2022-04-30'
#       $.analyzeResult.readResults         []  -> LV2
        top     = [ 'status', 'createdDateTime', 'lastUpdatedDateTime',
                        'analyzeResult']
        apiv    = '3.2.0'       # $.analyzeResult.version '3.2.0'
        mdlv    = '2022-04-30'  # $.analyzeResult.modelVersion '2022-04-30'
#       ## LV2 check : lv2() ##
#       $.analyzeResult.readResults[N]
#       .page                           exists/not
#       .angle                          exists/not
#       .width                          exists/not
#       .height                         exists/not
#       .unit                           exists/not
#       .lines                          if blank add dummy item -> LV3
        page        = [ 'page', 'angle', 'width', 'height', 'unit', 'lines']
#       ## LV3 check : lv3() ##
#       $.analyzeResult.readResults[N].lines[N]
#       .boundingBox
#       .text
#       .appearance.style.name
#       .appearance.style.confidence
#       .words
        line        = [ 'boundingBox', 'text', 'appearance', 'words']
        appearance  = [ 'style']
        app_val     = [ 'other', 'handwriting' ]
#       ## LV4 check : lv3() ##
#       $.analyzeResult.readResults[N].lines[N].words[N]
#       .boundingBox
#       .text
#       .confidence
        word        = [ 'boundingBox', 'text', 'confidence']
