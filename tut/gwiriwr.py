#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

try:
    from urllib import request
    from urllib.parse import urlencode
except ImportError:
    import urllib2 as request
    from urllib import urlencode

try:
    # python2
    input = raw_input
except NameError:
    # python3
    input = input

import json

# ==============================
# = GOSODIADAU / USER SETTINGS =
# ==============================
# Eich allwedd API - o https://api.techiaith.org
# Your API Key - from https://api.techiaith.org
# Cewch hefyd gadael hyn yn wag, a cadw'ch allwedd API mewn ffeil 'API_KEY'
# You can also leave this empty and keep your API key in a file called 'API_KEY'
API_KEY = ""

# Gellir defnyddio 'cy' neu 'en' ar gyfer iaith yr API
# Api lang parameter can be either 'cy' or 'en'
API_LANG = 'cy'

API_URL = "https://api.techiaith.org/cysill/v1/?"

# ==============
# = Cod / Code =
# ==============

if not API_KEY:
    # ceisio darllen yr API key o ffeil
    import os
    if os.path.exists("API_KEY"):
        with open("API_KEY", 'rb') as a:
            API_KEY = a.read().decode('utf-8').strip()

if API_KEY == "":
    print("""
=================
***GWALL/ERROR***
=================

RHAID gosod eich allwedd API in gwiriwr.py yn gyntaf. Gwelwch https://api.techiaith.org
You MUST set your API Key in gwiriwr.py first. See https://api.techiaith.org
""")
    import sys
    sys.exit(1)


class Colour:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'


def get_errors(llinell):
    """
    Galw'r API ar gyfer gwirio'r sillafu un llinell
    Call the API to check the spelling for one line
    """
    params = {
        'api_key': API_KEY.encode('utf-8'),
        'lang': API_LANG.encode('utf-8'),
        'text': llinell.encode('utf-8')
    }
    url = API_URL + urlencode(params)
    
    response = request.urlopen(url)
    response = json.loads(response.read().decode('utf-8'))
    if not response['success']:
        # Gwall gyda'r galwad API
        # something went wrong with the API call
        error_messages = u'\n'.join(response['errors'])
        raise ValueError(error_messages)
    
    return response['result']

GEIRIADU_WEDI_ANWYBYDDU = []

def gwirio_llinell(llinell, geiriadur_personol):
    """
    Gwirio un llinell ar y tro
    Corrects one line at a time
    """

    errors = get_errors(llinell)

    if not len(errors):
        return llinell, []
    
    gwiriadau = []
    
    for error in errors:
        gair_camsillafu = llinell[error['start']:error['start'] + error['length']]
        if gair_camsillafu in GEIRIADU_WEDI_ANWYBYDDU or gair_camsillafu.lower() in GEIRIADU_WEDI_ANWYBYDDU:
            continue

        if (gair_camsillafu in geiriadur_personol) or (gair_camsillafu.lower() in geiriadur_personol):
            continue

        print(u"\nGWALL {}:  {}".format(u"SILLAFU" if error['isSpelling'] else u'GRAMADEG',
                                        u"".join((llinell[0:error['start']], Colour.RED, gair_camsillafu,
                                                  Colour.END, llinell[error['start']+error['length']:]))
                                        ))

        nifer_awgrymiadau = len(error['suggestions'])
        awgrym = None

        print(u"{}.\n\nDewisiwch opsiwn canlynol:\n--------------------------".format(error['message']))

        opsiynau = ((u'a', u'Anwybyddu'), (u'y', u"Ychwanegu '{}{}{}' i'r geiriadur".format(Colour.RED, gair_camsillafu, Colour.END)), (u'm', 'Mewnbynnu cywiriad eich hun'), (u'g', "Gorffen gwirio'r llinell"))

        if nifer_awgrymiadau:
            opsiynau += tuple([(str(i+1), u"Cywiro i '{}{}{}'".format(Colour.GREEN, sugg, Colour.END)) for i, sugg in enumerate(error['suggestions'])])
        
        opsiynau_dict = OrderedDict(opsiynau)
        
        print(u'\n'.join(u"[{}] {}".format(k,v) for k,v in opsiynau_dict.items()))
        
        ans = -1
        while (not opsiynau_dict.get(ans)):
            ans = input(u"Dewisiwch opsiwn ({}): ".format(u', '.join(opsiynau_dict.keys()))).lower()
        
        if ans == u'a':
            # anwybyddu
            GEIRIADU_WEDI_ANWYBYDDU.append(gair_camsillafu)
            continue
        elif ans == u'y':
            # ychwanegu i'r geiriadur
            geiriadur_personol.add(gair_camsillafu)
        elif ans == 'm':
            # mewnbynnu testun eich hun
            awgrym = input(u"Ysgrifennwch testun i cywiro '{}{}{}': ".format(Colour.RED, gair_camsillafu, Colour.END)).strip()
        elif ans == 'g':
            return llinell, []
        else:
            try:
                awgrym = error['suggestions'][int(ans)-1]
            except ValueError:
                continue

        if awgrym is not None:
            gwiriadau.append((gair_camsillafu, awgrym))
            llinell = llinell[0:error['start']] + awgrym + llinell[error['start']+error['length']:]
            # diweddaru start positions pob 'error' arral
            for pob_err in errors[errors.index(error)+1:]:
                pob_err['start'] += len(awgrym) - len(gair_camsillafu)
    return llinell, gwiriadau

def agor_geiriadur(enw="geiriadur.txt"):
    """Agor geiriadur a dychwelyd set o'r eiriau"""

    with open(enw, 'rb') as g:
        geiriadur_personol = set(l.strip() for l in g.read().decode('utf-8').split(u'\n'))
    return geiriadur_personol

def cadw_geiriadur(geiriadur_personol, enw="geiriadur.txt"):
    """Cadw'r geiriadur personol"""
    
    with open(enw, 'wb') as g:
        g.write(u'\n'.join(sorted(geiriadur_personol)).encode('utf-8'))
