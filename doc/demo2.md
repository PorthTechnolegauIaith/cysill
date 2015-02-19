# Tiwtorial 2

Gwirio tudalen Wicipedia gyda'r API Cysill Ar-lein.

## Pethau i'w osod er mwyn rhedeg y tiwtorial

Mae'r twitorial yma angen modiwl python `beautifulsoup`. Dilynwch y camau isod er mwyn gosod y modiwl ar eich Pi:

* `cd tut`
* `pip install -r requirements_demo2.txt`

Efallai bydd eich peiriant yn gofyn am caniatad `sudo` er mwyn gosod `beautifulsoup`

## Ychwanegu eich allwedd API

Cyn cychwyn, mae'n rhaid gosod eich allwedd API yn `gwiriwr.py`. Agorwch `gwiriwr.py` yn eich golygydd testun, a newidiwch y llinell:   

```
API_KEY = ""
```
   
i   
```
API_KEY = "eich allwedd api o https://api.techiaith.org"
```

Mae'n rhaid defnyddio'r allwedd API rydych chi wedi derbyn o ein Ganolfan APIs

## Rhedeg y tiwtorial

Mae'r tiwtorial yma yn ddangos sut gellir defnyddio'r API Cysill i gwirio testun ar lein fel tudalen o Wicipedia. Mae'n ymestyniad o tiwtorial 1, felly bydd yn syniad edrych dros tiwtorial 1 cyn rhedeg y tiwtorial yma.

Er mwyn rhedeg y tiwtorial, dilynwch y camau isod:

* `cd tut`
* `python demo2.py`
* Dilynwch y negeseuon ar y sgrin

Mae'r sgript yn lawrlwytho tudalen o Wicipedia ar-hap, ac yn gofyn i chi mewnbynnu eich dewisiadau
