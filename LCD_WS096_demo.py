# ---------------------------------------------------------------------
# LCD_WS096_demo.py
# =================
#
# Samostatna ukazka pouziti tridy LCD_WS096lite z modulu "LCD_WS096.py"
# Staci ulozit do Rapberry Pi Pico jako "main.py". Modul "LCD_WS096.py"
# okopirujte samozrejme do Rapberry Pi Pico take. NEMENTE!! prosim jeho
# jmeno!!! Pokud tak ucinite upravte prislusne tomu nazev modulu u pri-
# kazu IMPORT na zacatku tohoto kodu.
# Spoustet lze samostatne jednotlive ukazky nebo tzv. "SlideShow" kdy
# jsou s 5 vterinovymi prodlevami porad ddokola spousteny automaticky
# vsechny ukazky obsazene v kodu. Ridi promenne:
#
#    SlideShow      zapina/vypina rezim "SlideShow"
#    SampleNumber   cislo ukazky z nabidky v kodu pro individualni spou
#                   steni (SlideShow = False)
#
# *bylo zaroven pouzito v ramci procesu ladeni a testovani me verze tri
# dy LCD_WS096lite z modulu "LCD_WS096.py"
#
#  1 Puvodni ukazka z DEMO kodu od vyrobce desky "Hello pico!"
#  2 Puvodni ukazka z DEMO kodu od vyrobce desky "bila mrizka"
#  3 Ukazka typu TEXTOVA/ZNAKOVA matice (20 x 8 znaku)
#  4 Na vsech 8 radku (od 1 pozice) vypise cisla radku pro pozicovani
#  5 Postupne zobrazi plnou "textovou" matici (20 x 8 znaku)
#  6 Na vsech 8 radku (od 1 pozice) vypise cisla sloupcu pro pozicovani
#  7 Ukazka zmen(y) barvy pozadi B&W + RGB
#  8 Ukazka zmen(y) barvy pozadi B + CMY
#  9 Ukazka pouziti nove metody "Text2Row" - "Ahoj RP2040-LCD-0.96!"
# 10 Ukazka pouziti nove metody "Text2Row" - "Ahoj RP2040-LCD-0.96!"
#    *s vyuzitim svetleho pozadi
#
# vytvoreno:       13.05.2022 (RKu70cz)
# verze:           1.00
# posledni uprava: 20.05.2022 (RKu70cz)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------

import LCD_WS096
import time

if __name__=='__main__':

    SlideShow = True    # False = spusti pouze ukazku definovanou v SampleNumber
                        # True  = spousti automaticky beh se vsemi ukazkami 
    SampleNumber = 10   # cislo ukazky (1-10) pro rezim kdy SlideShow = False

    lcd = LCD_WS096.LCD_WS096lite()

    while True:

        # [1.] Puvodni ukazka z DEMO kodu od vyrobce desky "Hello pico!".
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.text"
        #
        if SlideShow or SampleNumber == 1:

            lcd.fill(LCD_WS096.LCD_WS096_BLACK)
            lcd.text("Hello pico!",35,15,LCD_WS096.LCD_WS096_GREEN)
            lcd.text("This is:",50,35,LCD_WS096.LCD_WS096_GREEN)
            lcd.text("Pico-LCD-0.96",30,55,LCD_WS096.LCD_WS096_WHITE)
            lcd.Show()
            
        if ( SlideShow ):
            time.sleep(5)

        # [2.] Puvodni ukazka z DEMO kodu od vyrobce desky "bila mrizka".
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.hline"
        #                "FrameBuffer.vline"
        #
        if SlideShow or SampleNumber == 2:

            lcd.fill(LCD_WS096.LCD_WS096_WHITE)
            
            i = 0
            while ( i <= 80 ):
                lcd.hline(0,i,160,LCD_WS096.LCD_WS096_BLACK)
                i = i + 10
            
            i = 0
            while ( i<= 160 ):
                lcd.vline(i,0,80,LCD_WS096.LCD_WS096_BLACK)
                i = i + 10
            
            lcd.Show()

        if ( SlideShow ):
            time.sleep(5)

        # [3.] Ukazka typu TEXTOVA/ZNAKOVA matice klasicky za pouziti metod tridy
        # "FrameBuffer". Displej plnen po celych radcich a jeho obsah zobrazen az
        # na samem konci. Zacatek kazdeho radku je uvozen znakem ">". Konec radku
        # pro zmenu oznacen znakem "<".
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.text"
        #
        if SlideShow or SampleNumber == 3:
            
            lcd.fill(LCD_WS096.LCD_WS096_BLACK)
            rowLine = 1
            i = 1
            while ( i <= 8 ):
                lcd.text(">XXXXXXXXXXXXXXXXXX<",0,rowLine,LCD_WS096.LCD_WS096_WHITE)
                i = i + 1
                rowLine = rowLine + 10
            lcd.Show()

        if ( SlideShow ):
            time.sleep(5)

        # [4.] Na vsech 8 radku (od 1 pozice) vypise cisla radku pro pozicovani
        # v "textovem" rezimu ...
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.text"
        #
        if SlideShow or SampleNumber == 4:
            lcd.fill(LCD_WS096.LCD_WS096_BLACK)
            lcd.Show()
    
            rowLine = 1
            i = 1
            while ( i <= 8 ):
                lcd.text(str(rowLine),0,rowLine,LCD_WS096.LCD_WS096_WHITE)
                lcd.Show()
                i = i + 1
                rowLine = rowLine + 10

        if ( SlideShow ):
            time.sleep(5)
        
        # [5.] Postupne zobrazi plnou "textovou" matici (20 x 8 znaku). Zacatek kazdeho
        # radku je uvozen znakem ">". Konec radku pro zmenu oznacen znakem "<". Vykres-
        # lovana je postupne kazda jedna zmena - udela neco jako "hada".
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.text"
        #
        if SlideShow or SampleNumber == 5:
            lcd.fill(LCD_WS096.LCD_WS096_BLACK)
            lcd.Show()
            
            columnLine = 0
            rowLine = 1
            x = 1
            y = 1
            
            while ( y <= 8 ):
                while ( x <= 20 ):
                    if x == 1: lcd.text(">",columnLine,rowLine,LCD_WS096.LCD_WS096_WHITE)
                    if x == 20: lcd.text("<",columnLine,rowLine,LCD_WS096.LCD_WS096_WHITE)
                    if x > 1 and x < 20: lcd.text("X",columnLine,rowLine,LCD_WS096.LCD_WS096_WHITE)
                    lcd.Show()
                    columnLine = columnLine + 8
                    x = x + 1
                columnLine = 0
                x = 1
                rowLine = rowLine + 10
                y = y + 1
                
        if ( SlideShow ):
            time.sleep(5)

        # [6.] Na vsech 8 radku (od 1 pozice) vypise cisla sloupcu pro pozicovani
        # v "textovem" rezimu. V tomto pripade samozrejme pouze prvnich osm ...
        #
        # vyuziva metody "FrameBuffer.fill"
        #                "FrameBuffer.text"
        #
        if SlideShow or SampleNumber == 6:
            lcd.fill(LCD_WS096.LCD_WS096_BLACK)
            lcd.Show()
    
            columnLine = 0
            rowLine = 1
            i = 1
            while ( i <= 8 ):
                lcd.text(str(columnLine),0,rowLine,LCD_WS096.LCD_WS096_WHITE)
                lcd.Show()
                i = i + 1
                rowLine = rowLine + 10
                columnLine = columnLine + 8

        if ( SlideShow ):
            time.sleep(5)

        # [7.] Ukazka zmen(y) barvy pozadi, ktere je postupne prebarvovano.
        # Opakovano 3x za sebou. Prodleva mezi zmenami 0,5s. Zkouska puvod-
        # nich resp. zakladnich definic barev B&W + RGB.
        #
        # vyuziva nove metody "ClearDisplay"
        #                     "FillDisplay"
        #
        if SlideShow or SampleNumber == 7:
            lcd.ClearDisplay()
            time.sleep(0.5)

            i = 1
            while i<= 3:
                lcd.FillDisplay(LCD_WS096.LCD_WS096_RED)
                time.sleep(0.5)
                lcd.FillDisplay(LCD_WS096.LCD_WS096_GREEN)
                time.sleep(0.5)
                lcd.FillDisplay(LCD_WS096.LCD_WS096_BLUE)
                time.sleep(0.5)
                lcd.FillDisplay(LCD_WS096.LCD_WS096_WHITE)
                time.sleep(0.5)
                lcd.FillDisplay()
                time.sleep(0.5)

                i = i + 1
        
        if ( SlideShow ):
            time.sleep(4.5)

        # [8.] Ukazka zmen(y) barvy pozadi, ktere je postupne prebarvovano.
        # Opakovano 3x za sebou. Prodleva mezi zmenami 1,5s. Zkouska nove
        # pridanych definic barev CMY.
        #
        # vyuziva nove metody "ClearDisplay"
        #                     "FillDisplay"
        #
        if SlideShow or SampleNumber == 8:
            lcd.ClearDisplay()
            time.sleep(0.5)

            i = 1
            while i<= 3:
                lcd.FillDisplay(LCD_WS096.LCD_WS096_CYAN)
                time.sleep(1.5)
                lcd.FillDisplay(LCD_WS096.LCD_WS096_MAGENTA)
                time.sleep(1.5)
                lcd.FillDisplay(LCD_WS096.LCD_WS096_YELLOW)
                time.sleep(1.5)
                lcd.FillDisplay()
                time.sleep(1.5)

                i = i + 1
        
        if ( SlideShow ):
            time.sleep(3.5)

        # [9.] Ukazka pouziti nove metody "Text2Row" - "Ahoj RP2040-LCD-0.96!"
        # Pouziva snad vsechny mozne i nemozne kombinace parametru teto rutiny.
        # Lze snadno odvodit vsechny zpusoby jejiho pouziti. Od nejjedodussiho
        # az po ty slozitejsi.
        #
        # vyuziva nove metody "Text2Row"
        #
        if SlideShow or SampleNumber == 9:

            lcd.Text2Row("Waveshare LCD 0.96''", 1)
            lcd.Text2Row("--------------------", 2)
            lcd.Text2Row("Ahoj RP2040-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_GREEN)
            lcd.Text2Row("DEMO tridy:", 5, Color=LCD_WS096.LCD_WS096_GREEN)
            lcd.Text2Row("'LCD_WS096lite'", 6, 6)
            lcd.Text2Row("RKu70cz", 8, 14, LCD_WS096.LCD_WS096_BLUE)
            
        if ( SlideShow ):
            time.sleep(5)

        # [10.] Ukazka pouziti nove metody "Text2Row" - "Ahoj RP2040-LCD-0.96!"
        # Pouziva snad vsechny mozne i nemozne kombinace parametru teto rutiny.
        # Lze snadno odvodit vsechny zpusoby jejiho pouziti. Od nejjedodussiho
        # az po ty slozitejsi. O proti predchozi ukazce je stejny text zobrazen
        # na svetlem pozadi.
        #
        # vyuziva nove metody "Text2Row"
        #                     "ClearDisplay"
        #
        if SlideShow or SampleNumber == 10:
            
            lcd.ClearDisplay(LCD_WS096.LCD_WS096_CYAN)
            
            lcd.Text2Row("Waveshare LCD 0.96''", 1, Color=LCD_WS096.LCD_WS096_BLACK)
            lcd.Text2Row("--------------------", 2, Color=LCD_WS096.LCD_WS096_BLACK)
            lcd.Text2Row("Ahoj RP2040-LCD-0.96!", 4, Color=LCD_WS096.LCD_WS096_RED)
            lcd.Text2Row("DEMO tridy:", 5, Color=LCD_WS096.LCD_WS096_RED)
            lcd.Text2Row("'LCD_WS096lite'", 6, 6, Color=LCD_WS096.LCD_WS096_BLACK)
            lcd.Text2Row("RKu70cz", 8, 14, LCD_WS096.LCD_WS096_BLUE)
            
        if ( SlideShow ):
            time.sleep(5)
            
        if ( SlideShow != True ):
            break
