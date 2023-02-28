# ---------------------------------------------------------------------
# KEYs_WS096_test.py
# ==================
#
# Zakladni test funkcnosti tlacitek a jejich obsluhy na desce Waveshare
# "Pico-LCD-0.96". Je urceno pro spousteni v ramci vyvojoveho prostredi
# Thonny. Vyuziva totiz pro interakci pouze jednoduchy vystup do konzo-
# le ...
#
# https://www.waveshare.com/wiki/Pico-LCD-0.96
#
# POZOR!!! Nezapomente GPIO, na ktera jsou tlacitka a joystick pripojen
# definovat jako VSTUPNI s "PULL UP" rezistorem. Tlacitka totiz fyzicky
# spinaji prislusny pin chipu natvrdo proti zemi.
#
# Joystick UP       GPIO 02 (pin 04)
# Joystick DOWN     GPIO 18 (pin 24)
# Joystick LEFT     GPIO 16 (pin 21)
# Joystick RIGHT    GPIO 20 (pin 26)
# Joystick ENTER    GPIO 03 (pin 05)
#
# User Key A        GPIO 15 (pin 20)
# User Key B        GPIO 17 (pin 22)
#
# vytvoreno:       24.02.2023 (RKu70cz)
# verze:           1.00
# posledni uprava: 24.02.2023 (RKu70cz)
#
# (c) 2023, RKu70cz
# ---------------------------------------------------------------------
from machine import Pin
import time

jupPIN2 = Pin(2, Pin.IN, Pin.PULL_UP)
jdownPIN18 = Pin(18, Pin.IN, Pin.PULL_UP)
jleftPIN16 = Pin(16, Pin.IN, Pin.PULL_UP)
jrightPIN20 = Pin(20, Pin.IN, Pin.PULL_UP)
jenterPIN3 = Pin(3, Pin.IN, Pin.PULL_UP)
        
ukaPIN15 = Pin(15, Pin.IN, Pin.PULL_UP)
ukbPIN17 = Pin(17, Pin.IN, Pin.PULL_UP)

i = 1

while True:
    
    jup = jupPIN2.value()
    jdown = jdownPIN18.value()
    jleft = jleftPIN16.value()
    jright = jrightPIN20.value()
    jenter = jenterPIN3.value()

    uka = ukaPIN15.value()
    ukb = ukbPIN17.value()

    if jup == 0:
        print ("{count} Joystick UP: {value}".format(count=i,value=jup))    

    if jdown == 0:
        print ("{count} Joystick DOWN: {value}".format(count=i,value=jdown))
        
    if jleft == 0:
        print ("{count} Joystick LEFT: {value}".format(count=i,value=jleft))
        
    if jright == 0:
        print ("{count} Joystick RIGHT: {value}".format(count=i,value=jright))
        
    if jenter == 0:
        print ("{count} Joystick ENTER: {value}".format(count=i,value=jenter))

    if uka == 0:
        print ("{count} User Key A: {value}".format(count=i,value=uka))
        
    if ukb == 0:
        print ("{count} User Key B: {value}".format(count=i,value=ukb))
    
    i = i + 1   
    time.sleep(0.25)
