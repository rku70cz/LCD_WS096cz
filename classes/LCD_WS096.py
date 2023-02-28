# ---------------------------------------------------------------------
# LCD_WS096.py
# ============
#
# Modul trid pro obsluhu LCD displeje 0.96'' na deskach Waveshare s ra-
# dicem (kontrolerem) ST7735S. 
#
# trida(y): LCD_WS096lite
#
# *sestaveno dle ukazkoveho kodu od vyrobce desek spolecnosti Waveshare
# *otestovano na modulech/deskach "RP2040-LCD-0.96" a "Pico-LCD-0.96"
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip
#
# vytvoreno:       12.05.2022 (RKu70cz)
# verze:           1.00
# posledni uprava: 20.05.2022 (RKu70cz)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------

from machine import Pin,SPI,PWM
import framebuf
import time

# konstanty s kody barev ( cerna, bila + RGB + CMY ); RGB 5-6-5

                             #  15 14 13 12 11 10 09 08 - 07 06 05 04 03 02 01 00 (16-bit)
                             #  D7 D6 D5 D4 D3 D2 D1 D0 - D7 D6 D5 D4 D3 D2 D1 D0
                             #  -------------------------------------------------
                             #  g2 g1 g0 b4 b3 b2 b1 b0 - r4 r3 r2 r1 r0 g5 g4 g3
                             #  -------------------------------------------------

LCD_WS096_RED = 0x00F8       #  0  0  0  0  0  0  0  0    1  1  1  1  1  0  0  0
LCD_WS096_GREEN = 0xE007     #  1  1  1  0  0  0  0  0    0  0  0  0  0  1  1  1
LCD_WS096_BLUE = 0x1F00      #  0  0  0  1  1  1  1  1    0  0  0  0  0  0  0  0

LCD_WS096_WHITE = 0xFFFF     #  1  1  1  1  1  1  1  1    1  1  1  1  1  1  1  1
LCD_WS096_BLACK = 0x0000     #  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0

LCD_WS096_CYAN = 0xFF07      #  1  1  1  1  1  1  1  1    0  0  0  0  0  1  1  1
LCD_WS096_MAGENTA = 0x1FF8   #  0  0  0  1  1  1  1  1    1  1  1  1  1  0  0  0
LCD_WS096_YELLOW = 0xE0FF    #  1  1  1  0  0  0  0  0    1  1  1  1  1  1  1  1

# ---------------------------------------------------------------------
# trida LCD_WS096lite
#       =============
#
# Odlehcena "lite" verze tridy "LCD_0inch96" z ukazkoveho kodu ze stra-
# nek spolecnosti Waveshare ( vyrobce modulu/desek "RP2040-LCD-0.96" a
# "Pico-LCD-0.96" ).
# https://www.waveshare.com/w/upload/9/9c/Pico_LCD_code.zip
#
# O proti originalu provedeny zmeny:
# - prejmenovany konstanty s definici zakladnich barev (B&W + RGB)
# - doplneny kody barev CMY
# - zjednodusena pocatecni inicializace (nove v metode "initialization"
#   aby se nepletlo novackum v Pythonu, jako jsem i ja, s konstruktorem
#   tridy ___init___)
# - vynechano prozatim rizeni podsviceni displeje
# - prejmenovana medota "SetWindows" na "set_window"; jde prece jenom
#   pouze o interni metodu, kterou neni vne potreba pouzivat
# - doplneny nove metody (prepracovany stavajici) pro bezne pouziti:
#      Show
#      ClearDisplay
#      FillDisplay
#      Text2Row
#
# - vytvoreno nove DEMO "LCD_WS096_demo.py" vyuzivajici tento modul 
# - doplneny komentare (prozatim ceska mutace)
#
# (c) 2022, RKu70cz
# ---------------------------------------------------------------------
class LCD_WS096lite(framebuf.FrameBuffer):
    def __init__(self):

        # natvrdo rozmer displeje a moznosti radice; organizace pameti radice 132(H) x RGB x 162(V) bits
        self.width = 160     # rozliseni displeje ( 160 bodu na sirku )
        self.height = 80     # rozliseni displeje ( 80 bodu na vysku )
        self.lines = 132     # max. pocet radku ( dle dokumentace radice; viz. organizace pameti radice vyse )
        self.columns = 162   # max. pocet sloupcu ( dle dokumentace radice; viz. organizace pameti radice vyse )
        
        self.offset_top = ( self.lines - self.height ) // 2
        self.offset_left = ( self.columns - self.width ) // 2
        
        # videoRAM, buffer
        self.buffer = bytearray( self.height * self.width * 2 )
        
        # objekty jednotlivych PINu rozhrani displeje
        self.csPIN9 = Pin(9, Pin.OUT)      # PIN9, "Chip Select"
        self.rstPIN12 = Pin(12, Pin.OUT)   # PIN12, "Reset"
        
        self.csPIN9(1)                     # nastavi PIN "Chip Select" na "NEaktivni"

        # objekt SPI rozhrani ( machine.SPI - Hardware SPI bus )
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)        # PIN10 = SPI clock; PIN11 = SPI data
        self.spi = SPI(1, 10000_000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)

        # POZOR!!! objekt PINu 8 "Data/Command" je potreba inicializovat opravdu az v tomto okamziku!!!
        self.dcPIN8 = Pin(8,Pin.OUT)       # PIN8, "Data/Command"
        self.dcPIN8(1)                     # nastavi PIN "Data/Command" na "DATA"

        # zavola puvodni konstruktor tridy "FrameBuffer"
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        
        # pocatecni inicializace (konfigurace) radice/kontroleru displeje
        self.initialization()
        self.set_window(0, 0, self.width-1, self.height-1)

    #
    # metoda "reset"
    # Provede HARDWAROVY RESET zobrazovace resp. jeho radice
    #
    def reset(self):
        self.rstPIN12(1)   # nastavi PIN "Reset" na "NEaktivni" ( *podle mne preventivne, musi byt ve vychozim stavu na 1 ) 
        time.sleep(0.2)
        self.rstPIN12(0)   # nastavi PIN "Reset" na "AKTIVNI" ( vyvola HW RESET radice/kontroleru displeje )
        time.sleep(0.2)
        self.rstPIN12(1)   # nastavi PIN "Reset" zpet na "NEaktivni"
        time.sleep(0.2)

    #
    # metoda "write_command"
    # Prepne kontroler/radic displeje do rezimu prenosu prikazu a pres SPI jej zapise
    #
    # V ukazkovem kodu od vyrobce desek Waveshare jde o puvodni metodu "write_cmd".
    # Pouze doplneny komentare, metoda prejmenovana a opravena chybka viz. komentar
    # nize
    #
    # *v puvodni verzi metody "write_cmd" chybel na konci prikaz pro prepnuti pinu 9
    # "Chip Select" zpet na hodnotu 1 tj. "NEaktivni"
    #
    # (c) 2022, RKu70cz
    #
    def write_command(self, command):
        self.dcPIN8(0)                         # nastavi PIN "Data/Command" na "COMMAND"
        self.csPIN9(0)                         # nastavi PIN "Chip Select" na "AKTIVNI"
        self.spi.write(bytearray([command]))   # prenese kod prikazu predaneho parametrem
        self.csPIN9(1)                         # nastavi PIN "Chip Select" na "NEaktivni"

    #
    # metoda "write_data"
    # Prepne kontroler/radic displeje do rezimu prenosu dat a pres SPI jej zapise
    #
    def write_data(self, buff):
        self.dcPIN8(1)                      # nastavi PIN "Data/Command" na "DATA"
        self.csPIN9(0)                      # nastavi PIN "Chip Select" na "AKTIVNI"
        self.spi.write(bytearray([buff]))   # prenese sekvenci dat predanou parametrem
        self.csPIN9(1)                      # nastavi PIN "Chip Select" na "NEaktivni"

    #
    # metoda "initialization"
    # Zkracena, zjednodusena verze pocatecni incializace displeje resp. jeho radice.
    #
    # (c) 2022, RKu70cz
    #
    def initialization(self):
        self.reset()

        self.write_command(0x11)   # SLPOUT (11h) sleep mode off
        time.sleep(0.12)

        self.write_command(0x21)   # INVON (21h) Display Inversion On

        self.write_command(0x3A)   # COLMOD (3Ah) Interface Pixel Format
        self.write_data(0x05)      # 101 = 16-bit/pixel ( MCU Interface Color Format )

        self.write_command(0x36)   # MADCTL (36h) Memory Data Access Control
        self.write_data(0xA8)      # 101010 00
                                   # MY-MX-MV (101) 3bits control MCU to memory write/read direction 
                                   # MY       (1) Row Address Order
                                   # MX       (0) Column Address Order
                                   # MV       (1) Row/Column Exchange
                                   #
                                   # ML       (0) vertical refresh TOP to BOTTOM
                                   # RGB      (1) RGB-BGR order ( 0 = RGB; 1 = BGR ) 
                                   # MH       (0) horizontal refresh LEFT to RIGHT

        self.write_command(0x29)   # DISPON (29h) Display On

    #
    # metoda "set_window"
    #         ===========
    # Nastavuje "pruhled" resp. okno, do ktereho se bude v realu zobrazovat. Souvisi s tim, ze
    # zobrazovac disponuje jinym rozlisenim (160x80 bodu) o proti deklarovane organizaci pameti
    # radice/controleru ST7735S, ktera je 162(V) x RGB x 132(H). Nastavuje se v ramci konstruk-
    # toru tridy. Jde o properties (promenne)
    #    self.width = 160     rozliseni displeje ( 160 bodu na sirku )
    #    self.height = 80     rozliseni displeje ( 80 bodu na vysku )
    #    self.lines = 132     max. pocet radku ( dle dokumentace radice; viz. organizace pameti radice vyse )
    #    self.columns = 162   max. pocet sloupcu ( dle dokumentace radice; viz. organizace pameti radice vyse )
    #
    # V ukazkovem kodu od vyrobce desek Waveshare jde o puvodni metodu "SetWindows". Pouze do-
    # plneny komentare, metoda prejmenovana a centrovani ramce/okna zajisteno dynamicky pomoci
    # spoctenych hodnot v promennych "self.offset_left", "self.offset_top"
    #
    # Parametry: Xstart - sloupec leveho horniho rohu okna
    #            Ystart - radek leveho horniho rohu okna
    #            Xend   - sloupec praveho dolniho rohu okna
    #            Yend   - radek praveho dolniho rohu okna
    #
    # (c) 2022, RKu70cz
    #
    def set_window(self, Xstart, Ystart, Xend, Yend):
        Xstart = Xstart + self.offset_left
        Xend = Xend + self.offset_left
        Ystart = Ystart + self.offset_top
        Yend = Yend + self.offset_top

        self.write_command(0x2A)   # CASET (2Ah) Column Address Set
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend)

        self.write_command(0x2B)   # RASET (2Bh) Row Address Set
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)

        self.write_command(0x2C)   # RAMWR (2Ch) Memory Write

    #
    # metoda "Show"
    #         ====
    # Zapise resp. prenese do displeje (a tim vlastne zobrazi) aktualni obsah interniho bufferu.
    # V ukazkovem kodu od vyrobce desek Waveshare jde o puvodni metodu "display". Pouze doplneny
    # komentare a metoda prejmenovana.
    #
    # Parametry: zadne
    # (c) 2022, RKu70cz
    #
    def Show(self):

        self.set_window(0,0,self.width-1,self.height-1)
        self.dcPIN8(1)                # nastavi "Data/Command" na "DATA"
        self.csPIN9(0)                # nastavi "Chip Select" na "AKTIVNI" 
        self.spi.write(self.buffer)   # prenese data pro zobrazeni
        self.csPIN9(1)                # nastavi "Chip Select" na "NEaktivni"

    #
    # metoda "ClearDisplay"
    #         ============
    # Nastavi vsechny body zobrazovace na shodnou barvu a zaroven vymaze kompletne stavajici obsah.
    # Obsah displeje je jednoduse prepisovan mezerami po jednotlivych radcich 1-8 ...
    #
    # Parametry: FillColor - nepovinny; povolene hodnoty jsou ty z definic konstant
    #                        LCD_WS096_RED, LCD_WS096_GREEN, LCD_WS096_BLUE,
    #                        LCD_WS096_WHITE a LCD_WS096_BLACK,
    #                        LCD_WS096_CYAN, LCD_WS096_MAGENTA, LCD_WS096_YELLOW
    #                        pokud neni urceno plati vychozi barva CERNA (LCD_WS096_BLACK)
    #
    # *vyuziva standardni metody "FrameBuffer.fill" a nove metody "Text2Row" s parametrem NoShow=True
    # *na uplny zaver provede automaticky aktualizaci na zobrazovaci (metoda "Show") - proto se pouzi
    # va Text2Row s parametrem NoShow=True - aby doslo k prekresleni pouze jednou
    #
    # (c) 2022, RKu70cz
    #
    def ClearDisplay(self, FillColor=LCD_WS096_BLACK):

        if FillColor != LCD_WS096_RED and FillColor != LCD_WS096_GREEN and FillColor != LCD_WS096_BLUE:
            if FillColor != LCD_WS096_WHITE and FillColor != LCD_WS096_BLACK:
                if FillColor != LCD_WS096_CYAN and FillColor != LCD_WS096_MAGENTA and FillColor != LCD_WS096_YELLOW:
                    FillColor = LCD_WS096_BLACK

        self.fill(FillColor)
        
        i = 1
        while i <= 8:
            self.Text2Row("                    ", i, Color=FillColor,NoShow=True)
            i = i + 1

        self.Show()

    #
    # metoda "FillDisplay"
    #         ===========
    # Nastavi vsechny body zobrazovace na shodnou barvu. POZOR, nelze brat za fyzicke smazani. Obsah
    # displeje zustane zachovan. Pouze diky teto operaci nebude videt. Hodi se napr. pri potrebe zme
    # nit barvu pozadi. Pro smazani obsahu displeje je treba pouzit predchozi metodu "ClearDisplay".
    #
    # Parametry: FillColor - nepovinny; povolene hodnoty jsou ty z definic konstant
    #                        LCD_WS096_RED, LCD_WS096_GREEN, LCD_WS096_BLUE,
    #                        LCD_WS096_WHITE a LCD_WS096_BLACK,
    #                        LCD_WS096_CYAN, LCD_WS096_MAGENTA, LCD_WS096_YELLOW
    #                        pokud neni urceno plati vychozi barva CERNA (LCD_WS096_BLACK)
    #
    # *vyuziva standardni metody "FrameBuffer.fill"
    # *automaticky provede aktualizaci na zobrazovaci (metoda "Show")
    #
    # (c) 2022, RKu70cz
    #
    def FillDisplay(self, FillColor=LCD_WS096_BLACK):

        if FillColor != LCD_WS096_RED and FillColor != LCD_WS096_GREEN and FillColor != LCD_WS096_BLUE:
            if FillColor != LCD_WS096_WHITE and FillColor != LCD_WS096_BLACK:
                if FillColor != LCD_WS096_CYAN and FillColor != LCD_WS096_MAGENTA and FillColor != LCD_WS096_YELLOW:
                    FillColor = LCD_WS096_BLACK

        self.fill(FillColor)
        self.Show()

    #
    # metoda "Text2Row"
    #         ========
    # Ma za cil zjednoduseni pouziti displeje v klasickem textovem rezimu. V tomto rezimu pri kodovani
    # znaku do matice 8x8 bodu (jak dovoluje "FrameBuffer.text") lze vyzivat plochu na zobrazeni max.
    # 20 znaku na jeden z 8 radku. Metoda si radky 1-8 a pripadne sloupce 1-20 sama prepocita na abso-
    # lutni cisla. Delka zobrazovaneho textu a jeho pripadne preteceni neni kontrolovano ani osetreno.
    # V zakladu staci metode predat string s pozadovanym textem a cislo radku (viz. demo).
    #
    # Parametry: TextString - text (string) pro zobrazeni
    #            RowNum     - cislo radku, na kterem ma byt text zobrazen (v rozsahu 1-8)
    #            ColNum     - nepovinny; cislo sloupce, od ktereho se ma zacit zobrazovat (v rozsahu 1-20)
    #                         pokud neni uveden je automaticky zvolen sloupec 1
    #            Color      - nepovinny; barva zobrazovaneho textu; povolene hodnoty jsou ty z definic
    #                         konstant LCD_WS096_RED, LCD_WS096_GREEN, LCD_WS096_BLUE
    #                                  LCD_WS096_WHITE, LCD_WS096_BLACK
    #                                  LCD_WS096_CYAN, LCD_WS096_MAGENTA, LCD_WS096_YELLOW
    #                         pokud neni urcena plati vychozi barva pisma BILA (LCD_WS096_WHITE)
    #            NoShow     - nepovinny; FALSE = provede automatickou aktualizaci displeje
    #                                    TRUE  = aktualizace obsahu displeje je VYNECHANA (zavolani me-
    #                                            tody "Show" neni na zaver provedeno)
    #
    # *vyuziva standardni metody "FrameBuffer.text"
    #
    # (c) 2022, RKu70cz
    #
    def Text2Row(self, TextString, RowNum, ColNum=-1, Color=LCD_WS096_WHITE, NoShow=False):

      if isinstance( TextString, str ):
          if len(TextString) > 0:
            if isinstance( RowNum, int ):

                if Color != LCD_WS096_RED and Color != LCD_WS096_GREEN and Color != LCD_WS096_BLUE:
                    if Color != LCD_WS096_WHITE and Color != LCD_WS096_BLACK:
                        if Color != LCD_WS096_CYAN and Color != LCD_WS096_MAGENTA and Color != LCD_WS096_YELLOW:
                            Color = LCD_WS096_WHITE

                MinRowNum = 1
                MaxRowNum = 8
                MinColNum = 1
                MaxColNum = 20

                if RowNum < MinRowNum or RowNum > MaxRowNum:
                    RownNum = 1
                    
                if ColNum != -1:
                    if ColNum < MinColNum or ColNum > MaxColNum:
                        ColNum = 1
                else:
                    ColNum = 1
                
                # prepocet znakovych pozic na ty absolutni
                RowLine = ( ( RowNum - 1 ) * 10 ) + 1 
                ColLine = ( ( ColNum - 1 ) * 8 )
                
                self.text(TextString,ColLine,RowLine,Color)
                
                if NoShow == False:
                    self.Show()
