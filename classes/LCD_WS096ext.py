# ---------------------------------------------------------------------
# LCD_WS096ext.py
# ===============
#
# Modul trid pro obsluhu LCD displeje 0.96'' na deskach Waveshare s ra-
# dicem (kontrolerem) ST7735S. 
#
# trida(y): LCD_WS096
#
# *sestaveno dle ukazkoveho kodu od vyrobce desek spolecnosti Waveshare
# *otestovano na modulech/deskach "RP2040-LCD-0.96" a "Pico-LCD-0.96"
#
# https://www.waveshare.com/w/upload/2/28/Pico_code.7z
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip
#
# vytvoreno:       23.05.2022 (RKu70cz)
# verze:           1.00
# posledni uprava: 25.05.2022 (RKu70cz)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------

import LCD_WS096
from machine import Pin,PWM

# ---------------------------------------------------------------------
# trida LCD_WS096
#       =========
#
# Ukazka dedeni trid v Pythonu. Slouzi k rozsirovani, modifikaci chova-
# ni zakladni tridy "LCD_WS096lite".
#
# Puvodni tridu doplnuje o:
#   board - string (text) s oznacenim desky
#           podporovane hodnoty "RP2040-LCD-0.96" nebo "PICO-LCD-0.96"
#   blPIN - objekt PINu, pres ktery se na desce ridi podsvetleni
#           na RP2040-LCD-0.96 jde o PIN 25
#           na Pico-LCD-0.96 jde o PIN 13
#   pwm   - objekt generatoru PWM, ktery se aktivuje na prislusnem PINu
#
# - doplněna nová metoda "Backlight"
# - vytvoreno nove DEMO "LCD_WS096ext_demo.py" vyuzivajici tento modul
# - doplneny komentare (prozatim ceska mutace)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------
class LCD_WS096(LCD_WS096.LCD_WS096lite):
    def __init__(self, BoardType="unknown"):

        self.board = "unknown"               # vychozi hodnota property 'board'
        
        BoardType = BoardType.lstrip()       # upravi vstupni parametr, oreze mezery zleva
        BoardType = BoardType.rstrip()       # oreze pripadne mezery zprava
        BoardType = BoardType.upper()        # prevede na VELKA PISMENA

        if isinstance( BoardType, str ):
            if ( len(BoardType) > 0 ):
                if ( BoardType == "RP2040-LCD-0.96" or BoardType == "PICO-LCD-0.96" ):
                    self.board = BoardType   # pokud jde o korektni hodnotu zapise ji do nove property 'board'

        # zavola puvodni konstruktor tridy "LCD_WS096lite"
        super().__init__()

    #
    # metoda "Backlight"
    #         =========
    # Podle ID (typu resp. oznaceni) desky predaneho konstruktoru tridy v parametru
    # inicializuje na prislusnem PINu generator PWN pro rizeni podsviceni. Ridi int.
    # property 'board'. Pokud neni korektne nastaveno nebude se volani metody nijak
    # projevovat (bude bez efektu).
    #
    # Parametry: value - hodnota 0 az 1000 ( 0 minimum, 1000 maximum )
    #                    hodnota -1 PWM deaktivuje
    #
    # V ukazkovem kodu od vyrobce desek Waveshare jde o puvodni metodu "backlight".
    # Pouze doplneny komentare, metoda prejmenovana a zohledneno rozdilne zapojeni
    # vyse uvedenych desek spolecnosti Waveshare. Navic rozsireno o moznost PWN na
    # danem PINu uplne deaktivovat (viz. popis parametru vyse)
    #
    # (c) 2022, RKu70cz
    #
    def Backlight(self,value):

        if ( isinstance( value, int ) ):
            if ( value >= -1 and value <= 1000 ):

                if value == -1:
                    
                    try:
                        if pwm in self:
                            if isinstance( self.pwm, PWN ):
                                self.pwm.deinit()           # vypne (deaktivuje) PWM
                    except:
                        value = -1                          # vlasne NIC; nema zadny efekt; slouzi k potlaceni vyjimky
                        
                    finally:                            
                        if ( self.board == "RP2040-LCD-0.96" ):
                            self.blPIN = Pin(25, Pin.OUT)   # nastavi PIN zpet jako bezny se smerem ven ( OUT, vystupni )
                            self.blPIN(1)                   # natvrdo nastavi PIN na logickou "1"
                        
                        if ( self.board == "PICO-LCD-0.96" ):
                            self.blPIN = Pin(13, Pin.OUT)   # nastavi PIN zpet jako bezny se smerem ven ( OUT, vystupni )
                            self.blPIN(1)                   # natvrdo nastavi PIN na logickou "1"
                        
                else:

                    if ( self.board == "RP2040-LCD-0.96" or self.board == "PICO-LCD-0.96" ):
                        
                        if ( self.board == "RP2040-LCD-0.96" ):
                            self.blPIN = Pin(25, Pin.OUT)
                            self.pwm = PWM(self.blPIN)

                        if ( self.board == "PICO-LCD-0.96" ):
                            self.blPIN = Pin(13, Pin.OUT)
                            self.pwm = PWM(self.blPIN)

                        self.pwm.freq(1000)
                        if ( value >= 1000 ):
                            value = 1000
                        
                        data = int( value * 65536 / 1000 )       
                        self.pwm.duty_u16(data)
