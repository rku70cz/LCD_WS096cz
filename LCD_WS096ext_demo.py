# ---------------------------------------------------------------------
# LCD_WS096ext_demo.py
# ====================
#
# Samostatna ukazka pouziti tridy LCD_WS096 z modulu "LCD_WS096ext.py".
# V tomto okamziku ( k 25.05.2022 ) ukazuje moznosti rizeni podsviceni
# displeju 0.96'' na deskach spolecnosti Waveshare.
#
# Staci ulozit do Rapberry Pi Pico jako modul "main.py". Modul(y) s naz
# vy "LCD_WS096.py" a "LCD_WS096ext.py" okopirujte samozrejme do RPi Pi
# Pico take. Pokud zmenite jejich nazvy upravte prislusne tomu nazev(y)
# modulu u prikazu IMPORT na zacatku tohoto kodu.
#
# Spoustet lze samostatne jednotlive ukazky nebo tzv. "SlideShow" kdy
# jsou s 2 vterinovymi prodlevami porad dokola spousteny automaticky
# vsechny ukazky obsazene v kodu. Ridi promenne:
#
#    SlideShow      zapina/vypina rezim "SlideShow"
#    SampleNumber   cislo ukazky z nabidky v kodu pro individualni spou
#                   steni (SlideShow = False); v tomto okamziku 1-2
#    BoardID        oznaceni desky predavane do konstruktoru tridy; pod
#                   porovana oznaceni:
#                   "RP2040-LCD-0.96"
#                   "Pico-LCD-0.96" nebo i treba "PICO-LCD-0.96" atd.
#                   *je CASE INSENSITIVE a MEZERY na zacatku a konci re
#                   tezce jsou ODMAZAVANY
#
# *bylo zaroven pouzito v ramci procesu ladeni a testovani me verze tri
# dy "LCD_WS096" z modulu "LCD_WS096ext.py"
#
# vytvoreno:       23.05.2022 (RKu70cz)
# verze:           1.00
# posledni uprava: 25.05.2022 (RKu70cz)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------

import LCD_WS096
import LCD_WS096ext
import time

#
# metoda "DisplayContent1"
#         ===============
#
# Z duvodu potreby opakovani vysazeno do samostatne procedury (metody). Pro
# ukazku 1. z tohoto modulu zajistuje zobrazeni testovaciho textu.
#
# Pouziva snad vsechny mozne i nemozne kombinace parametru metody "Text2Row"
# stejne jako predchozi ukazka(y). Lze snadno odvodit vsechny zpusoby jejiho
# pouziti. Od nejjedodussiho az po ty slozitejsi ...
#
# vyuziva nove metody "Text2Row"
#                     "ClearDisplay"
#
# (c) 2022, RKu70cz
#
def DisplayContent1( intensityBacklight=1000 ):

    iBacklightS = str( intensityBacklight )
    
    lcd.ClearDisplay()
    
    lcd.Text2Row("Waveshare LCD 0.96''", 1, NoShow=True)
    lcd.Text2Row("--------------------", 2, NoShow=True)

    if ( lcd.board == "RP2040-LCD-0.96" ):
        lcd.Text2Row("Ahoj RP2040-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_GREEN, NoShow=True)

    if ( lcd.board == "PICO-LCD-0.96" ):
        lcd.Text2Row("Ahoj Pico-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_GREEN, NoShow=True)

    lcd.Text2Row("DEMO tridy:", 5, Color=LCD_WS096.LCD_WS096_GREEN, NoShow=True)
    lcd.Text2Row("'LCD_WS096'", 6, 10, NoShow=True)
    lcd.Text2Row("RKu70cz", 8, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

    if ( len(iBacklightS) == 3 ):
        lcd.Text2Row( iBacklightS, 8, 18, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)    
    if ( len(iBacklightS) == 4 ):
        lcd.Text2Row( iBacklightS, 8, 17, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

    lcd.Show()

#
# metoda "DisplayContent2"
#         ===============
#
# Z duvodu potreby opakovani vysazeno do samostatne procedury (metody). Pro
# ukazku 2. z tohoto modulu zajistuje zobrazeni testovaciho textu.
#
# Pouziva snad vsechny mozne i nemozne kombinace parametru metody "Text2Row"
# stejne jako predchozi ukazka(y). Lze snadno odvodit vsechny zpusoby jejiho
# pouziti. Od nejjedodussiho az po ty slozitejsi ...
#
# vyuziva nove metody "Text2Row"
#                     "ClearDisplay"
#
# (c) 2022, RKu70cz
#
def DisplayContent2( intensityBacklight=1000 ):

    iBacklightS = str( intensityBacklight )
    
    lcd.ClearDisplay(LCD_WS096.LCD_WS096_CYAN)
    
    lcd.Text2Row("Waveshare LCD 0.96''", 1, Color=LCD_WS096.LCD_WS096_BLACK, NoShow=True)
    lcd.Text2Row("--------------------", 2, Color=LCD_WS096.LCD_WS096_BLACK, NoShow=True)
    
    if ( lcd.board == "RP2040-LCD-0.96" ):
        lcd.Text2Row("Ahoj RP2040-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_RED, NoShow=True)
        
    if ( lcd.board == "PICO-LCD-0.96" ):
        lcd.Text2Row("Ahoj Pico-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_RED, NoShow=True)

    lcd.Text2Row("DEMO tridy:", 5, Color=LCD_WS096.LCD_WS096_RED, NoShow=True)
    lcd.Text2Row("'LCD_WS096'", 6, 10, Color=LCD_WS096.LCD_WS096_BLACK, NoShow=True)
    lcd.Text2Row("RKu70cz", 8, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

    if ( len(iBacklightS) == 3 ):
        lcd.Text2Row( iBacklightS, 8, 18, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)    
    if ( len(iBacklightS) == 4 ):
        lcd.Text2Row( iBacklightS, 8, 17, Color=LCD_WS096.LCD_WS096_BLUE, NoShow=True)

    lcd.Show()

#
# ===
#

if __name__=='__main__':

    SlideShow = True               # False = spusti pouze ukazku definovanou v SampleNumber
                                   # True  = spousti automaticky beh se vsemi ukazkami 
    
    SampleNumber = 2               # cislo ukazky (1-2) pro rezim kdy SlideShow = False

    BoardID = "RP2040-LCD-0.96"   # pro desku MCU RP2040 s LCD displejem 0.96''
    #BoardID = "Pico-LCD-0.96"      # pro desku LCD displeje 0.96'' s tlacitky 
                                   # interne osetreno tak, ze je CASE INSENSITIVE

    lcd = LCD_WS096ext.LCD_WS096( BoardID )

    while True:

        # [1.] Ukazka pouziti nove metody "Backlight" - "Ahoj ... neco ...!"
        # Pouzit zakladni text z DEMO aplikace v modulu "LCD_WS096_demo.py".
        # Na chvili snizi podsviceni na polovinu. Nasledne vrati zpet resp.
        # deaktivuje PWM na prislusnem PINu desky.
        #
        # vyuziva novou metodu "Backlight"
        #
        if SlideShow or SampleNumber == 1:
            
            lcd.Backlight( 1000 )          
            DisplayContent1( 1000 )
            time.sleep(2)
            
            lcd.Backlight( 500 )
            DisplayContent1( 500 )
            time.sleep(2)

            lcd.Backlight( -1 )
            DisplayContent1( 1000 )
            
        if ( SlideShow ):
            time.sleep(2)

        # [2.] Ukazka pouziti nove metody "Backlight" - "Ahoj ... neco ...!"
        # Pouzit zakladni text z DEMO aplikace v modulu "LCD_WS096_demo.py".
        # V cyklu po 1 vterine snizuje intenzitu podsviceni az do uplneho vy-
        # pnuti a po stejnych krocich zpet.
        # Nasledne vrati vse do puvodniho stavu resp. deaktivuje PWM na pri-
        # slusnem PINu desky.
        #
        # vyuziva novou metodu "Backlight"
        #
        if SlideShow or SampleNumber == 2:
            
            lcd.Backlight( 1000 )
            DisplayContent2( 1000 )
            
            i = 1000
            while ( i > 0 ):
                time.sleep(1)
                i = i - 100
                lcd.Backlight( i )
                DisplayContent2( i )
                
            while ( i <= 1000 ):
                lcd.Backlight( i )
                DisplayContent2( i )
                time.sleep(1)
                i = i + 100
            
            lcd.Backlight( -1 )

        if ( SlideShow ):
            time.sleep(2)
            
        if ( SlideShow != True ):
            break
