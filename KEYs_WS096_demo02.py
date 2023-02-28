# ---------------------------------------------------------------------
# KEYs_WS096_demo02.py
# ====================
#
# Ukazka pouziti tridy "KEYs_WS096timer" z modulu "KEYs_WS096.py".  Pro
# interakci s uzivatelem pouziva LCD displej 0.96'' teze desky. Zobrazo
# vani je tudiz obslouzeno jiz drive  naprogramovanymi tridami pro jeho
# obsluhu "LCD_WS096lite" a "LCD_WS096" (efektnejsi verze).
#
# *bylo zaroven pouzito v ramci procesu ladeni a prvotniho testovani vy
# se uvedene tridy
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
import LCD_WS096                           # podadresar './classes' vuci ROOTu v ulozisti Raspberry Pi Pico
import LCD_WS096ext
import KEYs_WS096

#
# ===
#

#
# metoda "DisplayContent"
#         ==============
# Za pomoci metod tridy LCD_WS096ext.LCD_WS096 naplni displej vychozim obsahem.
# 
def DisplayContent():
    
    lcd.ClearDisplay()
    
    lcd.Text2Row("Pico-LCD-0.96", 1, NoShow=True)
    lcd.Text2Row("-------------", 2, NoShow=True)

    lcd.Text2Row("A", 2, 18, NoShow=True)
    lcd.Text2Row("B", 7, 18, NoShow=True)
    
    lcd.Text2Row("joystick:", 5, NoShow=True)
    lcd.Text2Row("-", 5, 11, NoShow=True)
    
    lcd.Text2Row("RKu70cz", 8, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

    lcd.Show()

#
# metoda "DisplayContentKEYs"
#         ==================
# Prekresleni displeje se zohlednenim predaneho kodu klavesy resp. microspinace.
# *za pomoci metod tridy LCD_WS096ext.LCD_WS096
#
def DisplayContentKEYs(keyCode):

    if keyCode != 0:

        lcd.ClearDisplay()
            
        lcd.Text2Row("Pico-LCD-0.96", 1, NoShow=True)
        lcd.Text2Row("-------------", 2, NoShow=True)

        if keyCode == KEYs_WS096.BUTTON_A:
            lcd.Text2Row("[A]", 2, 17, Color=LCD_WS096.LCD_WS096_YELLOW, NoShow=True)
        else:
            lcd.Text2Row("A", 2, 18, NoShow=True)
        
        if keyCode == KEYs_WS096.BUTTON_B:
            lcd.Text2Row("[B]", 7, 17, Color=LCD_WS096.LCD_WS096_YELLOW, NoShow=True)
        else:
            lcd.Text2Row("B", 7, 18, NoShow=True)
        
        lcd.Text2Row("joystick:", 5, NoShow=True)
        
        if keyCode == KEYs_WS096.JOY_UP:
            lcd.Text2Row("UP", 5, 11, Color=LCD_WS096.LCD_WS096_YELLOW,NoShow=True)
        elif keyCode == KEYs_WS096.JOY_DOWN:
            lcd.Text2Row("DOWN", 5, 11, Color=LCD_WS096.LCD_WS096_YELLOW,NoShow=True)
        elif keyCode == KEYs_WS096.JOY_LEFT:
            lcd.Text2Row("LEFT", 5, 11, Color=LCD_WS096.LCD_WS096_YELLOW,NoShow=True)
        elif keyCode == KEYs_WS096.JOY_RIGHT:
            lcd.Text2Row("RIGHT", 5, 11, Color=LCD_WS096.LCD_WS096_YELLOW,NoShow=True)
        elif keyCode == KEYs_WS096.JOY_ENTER:
            lcd.Text2Row("ENTER", 5, 11, Color=LCD_WS096.LCD_WS096_YELLOW,NoShow=True)
        else:
            lcd.Text2Row("-", 5, 11, NoShow=True)
        
        lcd.Text2Row("RKu70cz", 8, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

        lcd.Show()

#
# ===
#
                                                                                                                                                                   
if __name__=='__main__':
    
    BoardID = "Pico-LCD-0.96"                 # pro desku LCD displeje 0.96'' (Pico-LCD-0.96) s tlacitky
    lcd = LCD_WS096ext.LCD_WS096( BoardID )
    lcd.Backlight( 1000 )                     # maximalni jas (uroven podsvetleni) disleje
    DisplayContent()                          # vychozi obsah displeje
    
    keys = KEYs_WS096.KEYs_WS096timer( 100 )  # paramer konstruktoru urcuje cyklus timeru; v tomto pripade 100ms
    lastKeyCode = 0                           # tj. cteni stavu microspinacu 10x za vterinu

    # ***
    # NEKONECNA HLAVNI SMYCKA
    # ***
    while True:
        
        # sejmu posledni stisk microspinace
        keyCode = keys.getStatusKeys()

        # pokud bylo neco stisknuto prekreslim obsah disleje
        DisplayContentKEYs(keyCode)

        time.sleep(0.25)

        if keyCode == 0 and lastKeyCode != 0:
            DisplayContent()
        
        if lastKeyCode != keyCode:
            lastKeyCode = keyCode
