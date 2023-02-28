# ---------------------------------------------------------------------
# KEYs_WS096.py
# =============
#
# Modul trid pro obsluhu uzivatelskych tlacitek a joysticku na desce vy
# robce Waveshare 'Pico-LCD-0.96'. 
#
# trida(y): KEYs_WS096timer
#
# https://www.waveshare.com/wiki/Pico-LCD-0.96
# https://rpishop.cz/pico-karty/4021-waveshare-096-lcd-displej-pro-raspberry-pi-pico-16080-spi.html
#
# vytvoreno:       24.02.2023 (RKu70cz)
# verze:           1.00
# posledni uprava: 28.02.2023 (RKu70cz)
#
# (c) 2023, RKu70cz
# ---------------------------------------------------------------------

from machine import Pin
from machine import Timer

# konstanty s kody "klaves" (jako u PC/NTB)

JOY_UP = 38      # sipka nahoru
JOY_DOWN = 40    # sipka dolu
JOY_LEFT = 37    # sipka doleva
JOY_RIGHT = 39   # sipka nahoru
JOY_ENTER = 13   # enter

BUTTON_A = 65    # klavesa A
BUTTON_B = 66    # klasesa B

# ---------------------------------------------------------------------
# trida KEYs_WS096timer
#       ===============
#
# Nejjednodussi varianta, ktera mne "na prvni dobrou" napadla.Urcite pu
# jde jeste vylepsovat a zdokonalovat.  V teto variante pomoci casovace
# v pravidelnych intervalech sejme stavy GPIO, na ktere  jsou pripojeny
# microspinace desky 'Pico-LCD-0.96'.Stav ulozi a z "nadrizeneho" exter
# niho kodu si jej pomoci metody 'getStatusKeys' vyzvednete.  Novy stav
# neni do pomyslneho "bufferu" ulozen pokud jeste nedoslo k precteni to
# ho predchazejiciho.
#
# - vytvoreny nove ukazky "DEMO "KEYs_WS096_demo01.py" a
#                         "DEMO "KEYs_WS096_demo02.py"
#                         vyuzivajici tento modul "KEYs_WS096.py"
#                         a tridu "KEYs_WS096timer" v nem ...
#
# - doplneny komentare (prozatim ceska mutace)
#
# (c) 2023, RKu70cz
# ---------------------------------------------------------------------
class KEYs_WS096timer():   

    def __init__(self,checkInterval=250):
        
        # GPIO snimaneho joysticku
        self.jupPIN2 = Pin(2, Pin.IN, Pin.PULL_UP)
        self.jdownPIN18 = Pin(18, Pin.IN, Pin.PULL_UP)
        self.jleftPIN16 = Pin(16, Pin.IN, Pin.PULL_UP)
        self.jrightPIN20 = Pin(20, Pin.IN, Pin.PULL_UP)
        self.jenterPIN3 = Pin(3, Pin.IN, Pin.PULL_UP)
        
        # GPIO snimanych tlacitek
        self.ukaPIN15 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.ukbPIN17 = Pin(17, Pin.IN, Pin.PULL_UP)
        
        # PROPERTy urcujici zda bylo provedeno nacteni stavu microspinacu a vpusteni do dalsiho zpracovani
        # TRUE = provedeno "sliznuti" stavu externim kodem
        # FALSE = doposud nenacteno externim kodem
        self.readStatus = True
        
        # PROPERTIES stavu jednotlivych microspinacu
        # 1 = NEstisknut/NEaktivni
        # 0 = Stisknut/Aktivni
        self.jup = 1
        self.jdown = 1
        self.jleft = 1
        self.jright = 1
        self.jenter = 1
        
        self.uka = 1
        self.ukb = 1

        # PROPERTy s ulozenym poslednim KODEM stisknuteho microspinace/klavesy/tlacitka
        self.lastKeyCode = 0
        
        # aktivuje TIMER s periodou predanou konstruktoru teto tridy
        # v pozadovane periode/intervalu vola metodu "checkStatusKeys", ktera fyzicky nacte stavy
        # jednotlivych GPIO (deje se tak nezavisle na behu zbytku hlavniho kodu)
        self.tmr = Timer(mode=Timer.PERIODIC, period=checkInterval, callback=self.checkStatusKeys)

    #
    # metoda "checkStatusKeys"
    #         ===============
    # Fyzicky precte, ulozi stavy GPIO, na ktere jsou pripojeny microspinace modulu.
    # Provede se pouze tehdy pokud hodnota z predchoziho nacitani byla jiz zpracova-
    # na. Takova pojistka aby se zadny ze zaznamenanych stavu "neztratil" a vzdy do-
    # stal az k hlavnimu kodu ...
    #
    # (c) 2023, RKu70cz
    #
    def checkStatusKeys(self,timer):

        # pouze pokud predchozi stav tlacitek (microspinacu) byl precten a vpusten do dalsiho zpracovani
        if self.readStatus:
            
            # provede fyzicke sejmuti stavu mikrospinacu joysticku
            self.jup = self.jupPIN2.value()
            self.jdown = self.jdownPIN18.value()
            self.jleft = self.jleftPIN16.value()
            self.jright = self.jrightPIN20.value()
            self.jenter = self.jenterPIN3.value()

            # provede fyzicke sejmuti stavu uzivatelskych tlacitek [A],[B]
            self.uka = self.ukaPIN15.value()
            self.ukb = self.ukbPIN17.value()
            
            # secte drze jejich 1 a 0 (stavy) pro dalsi vyhodnoceni
            # 7 = NEaktivni zadny z microspinacu
            # 6 = Aktivni PRAVE JEDEN (korektni stav)
            # 6 > chyba; Aktivni JE VICE JAK JEDEN
            sum = self.jup + self.jdown + self.jleft + self.jright + self.jenter
            sum = sum + self.uka + self.ukb
            
            if sum < 6:
                
                # detekovano soucasne sepnuti vice mikrospinacu (tlacitek)
                # vse se uvede do vychoziho stavu jako by se nic nestalo ...
                self.jup = 1
                self.jdown = 1
                self.jleft = 1
                self.jright = 1
                self.jenter = 1
            
                self.uka = 1
                self.ukb = 1
                
                self.readStatus = True
            
            elif sum == 6:
                
                # stisknuto prave jedno tlacitko (microspinac)
                # stav se zafixuje do jeho nacteni a vpusteni do dalsiho zpracovani
                self.readStatus = False

    #
    # metoda "getStatusKeys"
    #         =============
    # Vycte posledne zaznamenany stav a vrati kod. Tim je "buffer" uvolnen pro dalsi
    # nacitani... Dokud nedojde k odberu kodu a dalsimu zpracovani v nadrizenem kodu
    # neni dalsi stisk microspinace zaznamenavan.
    #
    # navratovy kod stejny jako u klaves standardu PC:
    #
    # 38   sipka nahoru
    # 40   sipka dolu
    # 37   sipka doleva
    # 39   sipka nahoru
    # 13   enter
    # 65   klavesa A
    # 66   klasesa B
    #
    # (c) 2023, RKu70cz
    #
    def getStatusKeys(self):
        
        retValue = 0
        if self.readStatus:
            return retValue
        else:
            
            if self.jup == 0:
                retValue = JOY_UP

            if self.jdown == 0:
                retValue = JOY_DOWN
            
            if self.jleft == 0:
                retValue = JOY_LEFT
            
            if self.jright == 0:
                retValue = JOY_RIGHT
                
            if self.jenter == 0:
                retValue = JOY_ENTER
                
            if self.uka == 0:
                retValue = BUTTON_A
                
            if self.ukb == 0:
                retValue = BUTTON_B

        if self.lastKeyCode != retValue:
            self.lastKeyCode = retValue
        else:
            self.lastKeyCode = 0
            retValue = 0

        self.readStatus = True
        return retValue
