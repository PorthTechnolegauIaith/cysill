#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
from gwiriwr import gwirio_llinell, agor_geiriadur, cadw_geiriadur

if __name__ == '__main__':
        
    geiriadur_personol = agor_geiriadur()

    if len(sys.argv) > 1:
        ffeil = sys.argv[1]
        with open(ffeil, 'r') as f:
            testun = f.read().decode('utf-8')
    else:
        testun = ""
        while not testun.strip():
            testun = raw_input(u"Ysgrifennwch testun i'w gwirio:\n".encode('utf-8'))
        testun = testun.decode('utf-8')

    # cadw pob llinell testun mewn list
    llinellau = testun.split(u"\n")

    llinellau_wedi_gwirio = []

    for llinell in llinellau:
        llinell_wedi_gwirio = None
        while True:
            # Rhaid ail-gwirio brawddegau tad nad oes unrhywbeth wedi newid o fewn y brawddeg
            llinell_wedi_gwirio, gwiriadau = gwirio_llinell(llinell_wedi_gwirio or llinell, geiriadur_personol)
            if len(gwiriadau) == 0:
                break
        llinellau_wedi_gwirio.append(llinell_wedi_gwirio)

    print(u'\n===================\nTestun wedi gwirio:\n===================\n\n{}'.format(u'\n'.join(llinellau_wedi_gwirio)).encode('utf-8'))
    
    # Cadw unrhyw newidiadau i'r 'geiriadur personol'
    cadw_geiriadur(geiriadur_personol)
    