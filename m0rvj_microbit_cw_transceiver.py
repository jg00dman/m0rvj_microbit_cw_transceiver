##########################
#   v 1.0 Initial Public Release
#   This is a working CW Radio. 'B' is key. 'A' shows message received in text.
#   Connect Speaker or Headphones to Pin 0 and Ground
#   Or connect Piezo Buzzer or Haptic Motor for Silent operation to pin1 and ground
#   pin2 is capacitive touch keying.
#   Copyright (C) 2017 Revd. John Goodman M0RVJ, 
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>L
#   
#   This uses some public domain code by Giles Booth.
#   See here http://www.suppertime.co.uk/blogmywiki/2016/05/microbit-morse-code-transmitter/
###########################
from microbit import *
import radio
import music

radio.on()
radio.reset()

#Customise these settings for tx, pwr, channel and speed.
radio.config(power=7)
radio.config(channel=98)
WPM = 15
txenabled = True #in case you want to practice without sending
sidetone = 550

dotlength = int( 60000 / ( WPM * 50 ) )
dashlength = dotlength * 3
interelement = dotlength
interletter = dotlength * 2
interword = dotlength * 7
DOT_THRESHOLD = dotlength * 2
DASH_THRESHOLD = dotlength * 5
WORD_THRESHOLD = dotlength * 7

DOT = Image("00000:00000:00900:00000:00000")
DASH = Image("00000:00000:09990:00000:00000")             
ANT = Image("90909:09990:00900:00900:00900")        

morse = {
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
    "0":"-----",
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    ".":".-.-.",
    ",":"--..--",
    "/":"-..-.",
    "?":"..--.."
    }
# reverse dict.
decodemorse = {v: k for k, v in morse.items()}

# convert string to cw
def EncodeMorse(message):
    m = message.upper()
    enc = ""
    for c in m:
        enc = enc + morse.get(c," ")
        if morse.get(c," ") != " ":
            enc = enc + " "
    return enc
    
# function to flash and play cw
def FlashMorse(pattern):
   for c in pattern:
       if c == ".":
           display.show(DOT)
           pin1.write_digital(1)
           music.pitch(sidetone, dotlength)
           display.clear()
           pin1.write_digital(0)
           sleep(interelement)
       elif c == "-":
           display.show(DASH)
           pin1.write_digital(1)
           music.pitch(sidetone, dashlength)
           display.clear()
           pin1.write_digital(0)
           sleep(interelement)
       elif c == " ":
           sleep(interletter)
   return


def ReceiveCW():     
    display.show(ANT)
    message = ''
    started = running_time()
    while True:
        waiting = running_time() - started
        received = radio.receive()
        if received:
            FlashMorse(EncodeMorse(received))
            message += received
        if button_b.is_pressed():
            return # breakin to immediate keying
        if pin2.is_touched():
            return # breakin to immediate keying
        if button_a.was_pressed():
            display.scroll(message) # nb blocks receive while showing...
            message = ''
        if waiting > WORD_THRESHOLD * 2:
            display.show(ANT)
        if len(message) > 15: #keep message buffer short...
            message = message[1:16]
        if accelerometer.was_gesture("shake"):
            display.scroll("CW TRX by M0RVJ")
            
def Keyer():
    buffer = ''
    message = ''
    started = running_time()
    while True:        
            waited = running_time() - started
            key_down_time = None
            while button_b.is_pressed(): ## button B keying
                if not key_down_time:
                    key_down_time = running_time()
                music.pitch(sidetone, -1, pin0, False)
                pin1.write_digital(1)
                while True:
                    if not button_b.is_pressed():
                        music.stop()
                        pin1.write_digital(0)
                        break
            while pin2.is_touched(): ## touch keying
                if not key_down_time:
                    key_down_time = running_time()
                music.pitch(sidetone, -1, pin0, False)
                pin1.write_digital(1)
                while True:
                    if not pin2.is_touched():
                        music.stop()
                        pin1.write_digital(0)
                        break
            key_up_time = running_time()
            if key_down_time:
                duration = key_up_time - key_down_time
                if duration < DOT_THRESHOLD:
                    buffer += '.'
                    display.show(DOT)
                elif duration:
                    buffer += '-'
                    display.show(DASH)
                started = running_time()
            elif len(buffer) > 0 and waited > DASH_THRESHOLD:
                display.clear()
                character = decodemorse.get(buffer, '?')
                buffer = ''
                display.show(character)
                if txenabled:
                    radio.send(character)
                message += character
            if waited > WORD_THRESHOLD * 2:
                return
                
while True:
    Keyer()
    ReceiveCW()
