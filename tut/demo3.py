#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
from gwiriwr import gwirio_llinell, request, input, agor_geiriadur, cadw_geiriadur
from xml.etree import cElementTree as ET
from difflib import SequenceMatcher as SM
import re

WIKI_API_URL = "https://cy.wikipedia.org/w/api.php?format=xml&action=query&pageids={}&prop=revisions&rvprop=content"
WIKI_MARKUP_DELIMS = (u'[', u"'", u'<', u'~', u'{', u'#',
                    # link  bold   ref   sig   cite  redirect
                      u'=', u'*', u'#', u':', u']')
                    # head, bullet, list, indent
                    
wikipedia.set_lang('cy')

class COLOUR:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def get_match(needle, haystack):
    wiki_markup_re = u"(\s?(?:{})*.*?)".format(u"|".join(m if m not in ('[', '{', '*') else "\%s" % m for m in WIKI_MARKUP_DELIMS))
    m = re.search("({}){}".format(needle[0], u"".join("(?:(\[\[)?({})|(\]\])?({}))".format(g, g) if g != " " else wiki_markup_re for g in needle[1:])), haystack)
    return m

def gwirio_yn_markup(llinell, llinell_wedi_gwirio, gwiriadau, markup_lines):
    if llinell in markup_lines:
        ind = markup_lines.index(llinell)
        markup_lines[ind] = llinell_wedi_gwirio
        return

    ratios = sorted((t for t in [(i, l, SM(None, l, llinell).ratio()) for i, l in enumerate(markup_lines)] if t[2] > 0.2), key=lambda x:-x[2])

    if not len(ratios):
        print(u"Dim wedi darganfod llinell i'w gwirio. ABORT!")
        return
    
    for i, markup_line, ratio in ratios:
        match = (ratio > 0.72)
        if not match:
            print(u"""
========================================================
Wedi methu darganfod y llinell cod cyfateb yn awtomatig.
========================================================

{}
--------------------
{}

========================================""".format(markup_line, llinell))
            ans = input("Ydi'r ddau llinell uchod yn gyfateb Y/n? ").lower()
            if ans == u'y':
                match = True
        if match:
            for hen, newydd in gwiriadau:
                if hen in markup_line:
                    markup_line = markup_line.replace(hen, newydd)
                else:
                    markup_match = get_match(hen, markup_line)
                    # spans = [re.search(g, markup_match).span() for g in markup_match.groups()]
                    hen_geiriau = hen.split(u' ')
                    geiriau_newydd = newydd.split(u' ')
                        # Fix markup for links
                    k = 0
                    last = 0
                    parts = []
                    for gr in [gr for gr in markup_match.groups() if gr]:
                        if k == len(hen)-1:
                            parts.append(hen[last:])
                        elif gr != hen[k]:
                            parts.append(hen[last:k])
                            parts.append(gr)
                            last = k
                        else:
                            k += 1
                    chunk_newydd = newydd
                    new_parts = []
                    for part in parts[::-1]:
                        if part in newydd:
                            new_parts.insert(0, part)
                            chunk_newydd = chunk_newydd[:-len(part)]
                        elif any(l in WIKI_MARKUP_DELIMS for l in part):
                            new_parts.insert(0, part)
                        else:
                            new_parts.insert(0, chunk_newydd.split(" ")[-1])
                    print(new_parts, parts)
                    markup_line = markup_line.replace(u"".join(parts), u"".join(new_parts))
                markup_lines[i] = markup_line

def lawrlwytho_tudalen(enw):
    tudalen = wikipedia.page(enw)
    xml = ET.parse(request.urlopen(WIKI_API_URL.format(tudalen.pageid)))
    markup = xml.findtext("query/pages/page/revisions/rev")
    return tudalen, markup

def main():
    geiriadur_personol = agor_geiriadur()

    enw = ""
    while not enw:
        enw = input(u"Rhowch enw'r tudalen: ")
    
    tudalen, markup = lawrlwytho_tudalen(enw)
    # markup_lines = markup.split("\n")
    markup_lines = ["yn [[Bangor]]"]
    print((u"\n\nGWIRIO {}\n".format(tudalen.title) + u"-"*(len(tudalen.url)+7) + u"\n\n"))

    # cadw pob llinell testun mewn list
    # llinellau = filter(len, (t.strip() for t in tudalen.content.split(u"\n")))
    llinellau = ["yn Bangor"]

    llinellau_wedi_gwirio = [] #tuple (gwreiddiol, newydd)

    for llinell in llinellau:
        llinell_wedi_gwirio = None
        gwiriadau_llinell = []
        while True:
            # Rhaid ail-gwirio brawddegau tad nad oes unrhywbeth wedi newid o fewn y brawddeg
            llinell_wedi_gwirio, gwiriadau = gwirio_llinell(llinell_wedi_gwirio or llinell, geiriadur_personol)

            if len(gwiriadau) == 0:
                break
            else:
                gwiriadau_llinell.extend(gwiriadau)

        if llinell != llinell_wedi_gwirio:
            gwirio_yn_markup(llinell, llinell_wedi_gwirio, gwiriadau_llinell, markup_lines)
        llinellau_wedi_gwirio.append((llinell, llinell_wedi_gwirio))
    
    
    
    print(u"\n\nWEDI GORFFEN GWIRIO {}\n".format(tudalen.url))
    
    markup_newydd = u"\n".join(markup_lines)
    if markup_newydd != markup:
        enw_ffeil = u"{}.txt".format(tudalen.title.replace(u" ", u"_"))
        print(u"Compïwch y testun ô'r ffeil {} yn ôl i Wicipedia".format(enw_ffeil))
    
        with open(enw_ffeil, 'wb') as f:
            f.write(markup_newydd.encode('utf-8'))
    else:
        print(u"Dim byd yn bod!")
    
    cadw_geiriadur(geiriadur_personol)

if __name__ == "__main__":
    main()