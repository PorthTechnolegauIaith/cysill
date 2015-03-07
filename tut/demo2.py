#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from gwiriwr import gwirio_llinell, request, agor_geiriadur, cadw_geiriadur

class COLOUR:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def lawrlwytho_tudalen_arhap():
    data = request.urlopen(u"https://cy.wikipedia.org/wiki/Arbennig:Random")
    r = ""
    url = None
    try:
        r = data.read()
        url = data.geturl()
    finally:
        data.close()
    return r, url

if __name__ == "__main__":
    geiriadur_personol = agor_geiriadur()
    data, url = lawrlwytho_tudalen_arhap()

    print((u"\n\nGWIRIO {}\n".format(url) + u"-"*(len(url)+7) + u"\n\n"))

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
            llinell_wedi_gwirio, gwiriadau = gwirio_llinell(llinell_wedi_gwirio or llinell, geiriadur_personol)

            if len(gwiriadau) == 0:
                break
        llinellau_wedi_gwirio.append(llinell_wedi_gwirio)
    
        
    print(u'Testun wedi gwirio:\n\n{}'.format(u'\n'.join(llinellau_wedi_gwirio)))
    print(u"\n\nWEDI GORFFEN GWIRIO {}\n".format(url))
    
    cadw_geiriadur(geiriadur_personol)
