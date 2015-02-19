#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from gwiriwr import gwirio_llinell, request

class COLOUR:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def lawrlwytho_tudalen_arhap():
    data = request.urlopen(u"http://cy.wikipedia.org/wiki/.pr")
    r = ""
    url = None
    try:
        r = data.read()
        url = data.geturl()
    finally:
        data.close()
    return r, url

if __name__ == "__main__":
    with open('geiriadur.txt', 'r') as g:
        geiriadur_personol = set(l.strip() for l in g.read().decode('utf-8').split(u'\n'))


    data, url = lawrlwytho_tudalen_arhap()

    print((u"\n\nGWIRIO {}\n".format(url) + u"-"*(len(url)+7) + u"\n\n").encode('utf-8'))

    html_tudalen_arhap = BeautifulSoup(data)

    # tynnu'r <div> testun allan o'r tudalen wicipedia
    testun = html_tudalen_arhap.find(id="mw-content-text")

    # echdynnu a dileu'r div 'NavFrame1'
    nav_frame = testun.find(class_="NavFrame")
    if nav_frame:
        nav_frame.extract()

    # tacluso'r testun a'i newid yn text
    testun = testun.text.replace(u"[golygu]", u"")

    # cadw pob llinell testun mewn list
    llinellau = filter(len, (t.strip() for t in testun.split(u"\n")))

    llinellau_wedi_gwirio = []
    
    for llinell in llinellau:
        llinell_wedi_gwirio = None
        while True:
            # Rhaid ail-gwirio brawddegau tad nad oes unrhywbeth wedi newid o fewn y brawddeg
            llinell_wedi_gwirio, nifer_gwiriadau = gwirio_llinell(llinell_wedi_gwirio or llinell, geiriadur_personol)

            if nifer_gwiriadau == 0:
                break
        llinellau_wedi_gwirio.append(llinell_wedi_gwirio)
    
        
    print(u'Testun wedi gwirio:\n\n{}'.format(u'\n'.join(llinellau_wedi_gwirio)).encode('utf-8'))
    print(u"\n\nWEDI GORFFEN GWIRIO {}\n".format(url).encode('utf-8'))

    with open('geiriadur.txt', 'w') as g:
        g.write(u'\n'.join(sorted(geiriadur_personol)).encode('utf-8'))
