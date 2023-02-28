# ---------------------------------------------------------------------
# KEYs_WS096_demo01.py
# ====================
#
# Ukazka pouziti tridy "KEYs_WS096timer" z modulu "KEYs_WS096.py".  Pro
# interakci s uzivatelem pouziva pouze jednoduchy vystup do konzole. Je
# proto urceno pouze pro spousteni v ramci vyvojoveho prostredi Thonny. 
#
# https://www.waveshare.com/wiki/Pico-LCD-0.96
#
# *bylo zaroven pouzito v ramci procesu ladeni a prvotniho testovani vy
# se uvedene tridy ...
#
# vytvoreno:       24.02.2023 (RKu70cz)
# verze:           1.00
# posledni uprava: 28.02.2023 (RKu70cz)
#
# (c) 2023, RKu70cz
# ---------------------------------------------------------------------

import sys, os
import time

sys.path.insert(0, './classes')            # doplnuje alternativni cestu pro hledani modulu trid; v tomto pripade
import KEYs_WS096                          # podadresar './classes' vuci ROOTu v ulozisti Raspberry Pi Pico

#
# ===
#

keys = KEYs_WS096.KEYs_WS096timer( 100 )   # paramer konstruktoru urcuje cyklus timeru; v tomto pripade 100ms
                                           # tj. cteni stavu microspinacu 10x za vterinu
while True:

    keyCode = keys.getStatusKeys()
    print(keyCode)
    time.sleep(0.5)
