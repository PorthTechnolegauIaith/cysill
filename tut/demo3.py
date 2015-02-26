#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
from gwiriwr import gwirio_llinell, request, input
from xml.etree import cElementTree as ET
import Levenshtein

WIKI_API_URL = "https://cy.wikipedia.org/w/api.php?format=xml&action=query&pageids={}&prop=revisions&rvprop=content"

wikipedia.set_lang('cy')

class COLOUR:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def gwirio_yn_markup(llinell, llinell_wedi_gwirio, markup_lines):
    if llinell in markup_lines:
        markup_lines.replace(llinell, llinell_wedi_gwirio)
        return 
        

    ratios = sorted((t for t in [(i, l, Levenshtein.ratio(l, llinell)) for i, l in enumerate(markup_lines)] if t[2] > 0.5), key=lambda x:-x[2])

    if not len(ratios):
        import pdb
        pdb.set_trace()
        print(u"Dim wedi darganfod llinell i'w gwirio. ABORT!")
        return
    
    for ratio in ratios:
        match = (ratio[2] > 0.9)
        if not match:
            ans = input(u"""
==========================================
Wedi methu darganfod y llinell cod cyfateb.
==========================================

{}
--------------------
{}

========================================
Ydi'r ddau llinell uchod yn gyfateb Y/n? """.format(ratio[1], llinell).encode('utf-8')).lower()
            if ans == u'y':
                match = True
        if match:
            geiriau_wedi_newid = [(i, hen, newydd) for i, (hen, newydd) in enumerate(zip(llinell.split(u" "), llinell_wedi_gwirio.split(u" "))) if hen != newydd]
            markup_ind = dict(enumerate(ratio[1].split(u" ")))
            def replace(ind, hen, newydd):
                if not markup_ind.get(ind):
                    return False
                    
                if markup_ind[ind] == hen:
                    markup_ind[ind] = newydd
                    return True
                elif hen in markup_ind[ind]:
                    markup_ind[ind] = markup_ind[ind].replace(hen, newydd)
                return False

            for i, hen, newydd in geiriau_wedi_newid:

                for f in (0, 1, -1, 2, -2, 3, -3, 4, -4):
                    if replace(i+f, hen, newydd):
                        break
            import pdb
            pdb.set_trace()
            markup_lines[ratio[0]] = u" ".join(w for _, w in sorted(markup_ind.items()))
            return

def lawrlwytho_tudalen(enw):
    tudalen = wikipedia.page(enw)
    xml = ET.parse(request.urlopen(WIKI_API_URL.format(tudalen.pageid)))
    markup = xml.findtext("query/pages/page/revisions/rev")
    return tudalen, markup

def main():
    with open('geiriadur.txt', 'r') as g:
        geiriadur_personol = set(l.strip() for l in g.read().decode('utf-8').split(u'\n'))
    
    enw = ""
    while not enw:
        enw = input(u"Rhowch enw'r tudalen: ")
    
    tudalen, markup = lawrlwytho_tudalen(enw)
    markup_lines = markup.split("\n")
    print((u"\n\nGWIRIO {}\n".format(tudalen.title) + u"-"*(len(tudalen.url)+7) + u"\n\n").encode('utf-8'))

    # cadw pob llinell testun mewn list
    llinellau = filter(len, (t.strip() for t in tudalen.content.split(u"\n")))

    llinellau_wedi_gwirio = [] #tuple (gwreiddiol, newydd)

    for llinell in llinellau:
        llinell_wedi_gwirio = None
        while True:
            # Rhaid ail-gwirio brawddegau tad nad oes unrhywbeth wedi newid o fewn y brawddeg
            llinell_wedi_gwirio, nifer_gwiriadau = gwirio_llinell(llinell_wedi_gwirio or llinell, geiriadur_personol)

            if nifer_gwiriadau == 0:
                break

        if llinell != llinell_wedi_gwirio:
            gwirio_yn_markup(llinell, llinell_wedi_gwirio, markup_lines)
        llinellau_wedi_gwirio.append((llinell, llinell_wedi_gwirio))
    
    
    
    print(u"\n\nWEDI GORFFEN GWIRIO {}\n".format(tudalen.url).encode('utf-8'))
    
    markup_newydd = u"\n".join(markup_lines)
    if markup_newydd != markup:
        enw_ffeil = u"{}.txt".format(tudalen.title.replace(u" ", u"_"))
        print(u"Compïwch y testun ô'r ffeil {} yn ôl i Wicipedia".format(enw_ffeil).encode('utf-8'))
    
        with open(enw_ffeil, 'w') as f:
            f.write(markup_newydd.encode('utf-8'))
    else:
        print(u"Dim byd yn bod!".encode('utf-8'))
    
    with open('geiriadur.txt', 'w') as g:
        g.write(u'\n'.join(sorted(geiriadur_personol)).encode('utf-8'))

if __name__ == "__main__":
    main()