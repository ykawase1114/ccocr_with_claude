#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cred.py     250205  cy
#   updated: 260319.153926 by cy
#   updated: 260321 rename keyring keys to ccocr_cv_key/ccocr_cv_ep
#   updated: 260321 add cred_di() for Document Intelligence
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import subprocess
import urllib.parse
import keyring

from m.prnt         import prnt
from jobs.env       import DD
from jobs.util.msg  import cred_unset

#def setenv(key,ep,pas):
def setenv(key,ep):
    user    = os.environ.get('USERNAME')
    DD.url_up = f'{ep}vision/v3.2/read/analyze?readingOrder=natural'
    DD.hdr_up = {
        'Ocp-Apim-Subscription-Key' : key                           ,
        'Content-Type'              : 'application/octet-stream'    , }
    DD.hdr_dn = { 'Ocp-Apim-Subscription-Key' : key, }
#    DD.proxy = {
#        'http'  : f'http://{user}:{pas}@proxy.ttc.toyotsu.co.jp:3128/' ,
#        'https' : f'http://{user}:{pas}@proxy.ttc.toyotsu.co.jp:3128/' , }
    prnt(f'using CV cred for {ep}')
    return

def setenv_di(key,ep):
    DD.di_key = key
    DD.di_ep  = ep
    prnt(f'using DI cred for {ep}')
    return

def cred():
    key_now = keyring.get_password('ccocr_cv_key', 'me')
    ep_now  = keyring.get_password('ccocr_cv_ep', 'me')
#    pas_now = keyring.get_password('tkz_mypas2', 'me')
#    if key_now != None and ep_now != None and pas_now != None:
    if key_now != None and ep_now != None:
        prnt('using saved cred')
#        setenv(key_now,ep_now,pas_now)
        setenv(key_now,ep_now)
        return
    prnt('asking new cred')
    while True:
        jsn = subprocess.run(
            ['python', os.path.join(os.path.dirname(__file__),'askcred.py')],
            capture_output=True, text=True).stdout
        prnt(f'json stdout "{type(jsn)}"')
        jsn = json.loads(jsn)
        jsn['key'] = jsn['key'].strip()
        jsn['ep'] = jsn['ep'].strip()
#        jsn['pass'] = jsn['pass'].strip()
#        jsn['pass'] = urllib.parse.quote(jsn['pass'])
        prnt(f'json stripped dict {type(jsn)}')
#        if jsn['key'] != '' and jsn['ep'] != '' and jsn['pass'] != '':
        if jsn['key'] != '' and jsn['ep'] != '':
            break
        cred_unset()        # -> possibly quit()
    keyring.set_password('ccocr_cv_key', 'me', jsn['key'])
    keyring.set_password('ccocr_cv_ep', 'me', jsn['ep'])
#    keyring.set_password('tkz_mypas2','me',jsn['pass'])
    key_new = keyring.get_password('ccocr_cv_key', 'me')
    ep_new = keyring.get_password('ccocr_cv_ep','me')
#    pas_new = keyring.get_password('tkz_mypas2', 'me')
#    setenv(key_new,ep_new,pas_new)
    setenv(key_new,ep_new)
    prnt(f'credential set/updated')

def cred_di():
    key_now = keyring.get_password('ccocr_di_key', 'me')
    ep_now  = keyring.get_password('ccocr_di_ep', 'me')
    if key_now != None and ep_now != None:
        prnt('using saved DI cred')
        setenv_di(key_now, ep_now)
        return
    prnt('asking new DI cred')
    while True:
        jsn = subprocess.run(
            ['python', os.path.join(os.path.dirname(__file__),'askcred.py')],
            capture_output=True, text=True).stdout
        jsn = json.loads(jsn)
        jsn['di_key'] = jsn['di_key'].strip()
        jsn['di_ep']  = jsn['di_ep'].strip()
        if jsn['di_key'] != '' and jsn['di_ep'] != '':
            break
        cred_unset()
    keyring.set_password('ccocr_di_key', 'me', jsn['di_key'])
    keyring.set_password('ccocr_di_ep',  'me', jsn['di_ep'])
    key_new = keyring.get_password('ccocr_di_key', 'me')
    ep_new  = keyring.get_password('ccocr_di_ep',  'me')
    setenv_di(key_new, ep_new)
    prnt(f'DI credential set/updated')
