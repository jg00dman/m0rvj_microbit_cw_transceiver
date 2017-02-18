##########################
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
# V2 Reduces memory footprint by switching to binary representation of Morse in prep for adding more features.
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
interletter = dotlength * 2
interword = dotlength * 7

ANT = Image("30303:03330:00300:00300:00300")

morse = [ 0b1110011, 0b1100001, 0b101010, 0b110010, 0b111111, 0b101111, 0b100111, 0b100011, 0b100001, 0b100000, 0b110000, 0b111000, 0b111100, 0b111110, 0b1111000, 0b1111000, 0b1101101, 0b110001, 0b1101101, 0b1001100, 0b1011010, 0b101, 0b11000, 0b11010, 0b1100, 0b10, 0b10010, 0b1110, 0b10000, 0b100, 0b10111, 0b1101, 0b10100, 0b111, 0b110, 0b1111, 0b10110, 0b11101, 0b1010, 0b1000, 0b11, 0b1001, 0b10001, 0b1011, 0b11001, 0b11011, 0b11100 ]

#encodes morse by replacing ascii char with morse binary from the morse array
def encoder(message):
    z = []#buffer to build the message
    for i in message:
        if i != ' ':#check for spaces
            y = ord(i.upper())# get int for char
            if y < 44 or y > 90:
                y = 63 #replace message with 63 makes it a ?
            z.append(morse[y-44])#returns the char from codestring with the binary of the cw stored in it.
        else:
            z.append(0b1)
    return z


# decodes morse binary to text.
def decoder(*message):
    y=''
    for i in message:
        try:
            if i == 0b1:
                y += ' '
            else:
                x = chr(morse.index(i)+44)#find the character in the codestring and bump it by 44 to find the ASCII char
                y += x #if found add it to the return variable
        except: 
            y+= '?' #if it isn't found then return a space
    return y


# function to flash and play cw
def playMorse(binarycw):
    for i in binarycw:
        if i == 0b1:
            sleep(interword)
        pattern = bin(i)[3:]
        for c in pattern:
            if c == "0":
                display.set_pixel(2,2,9)
                pin1.write_digital(1)
                music.pitch(sidetone, dotlength)
                display.clear()
                pin1.write_digital(0)
                sleep(dotlength)
            elif c == "1":
                display.show("-")
                pin1.write_digital(1)
                music.pitch(sidetone, dashlength)
                display.clear()
                pin1.write_digital(0)
                sleep(dotlength)
            else:
                sleep(interletter)


def receiver():
    display.show(ANT)
    message = ''
    started = running_time()
    while True:
        waiting = running_time() - started
        received = radio.receive()
        if received:
            playMorse(encoder(received))
            message += received
        if button_b.is_pressed():
            return # breakin to immediate keying
        if pin2.is_touched():
            return # breakin to immediate keying
        if button_a.was_pressed():
            display.scroll(message) # nb blocks receive while showing
            message = ''
        if waiting > interword * 2:
            display.show(ANT)
        if len(message) > 15: #keep message buffer short
            message = message[1:16]
        if accelerometer.was_gesture("shake"):
            display.scroll("CW TRX by M0RVJ")


def keyer():
    buffer = ''
    started = running_time()
    while True:        
            waited = running_time() - started
            key_down_time = None
            while button_b.is_pressed():#button B keying
                if not key_down_time:
                    key_down_time = running_time()
                music.pitch(sidetone, -1, pin0, False)
                pin1.write_digital(1)
                while True:
                    if not button_b.is_pressed():
                        music.stop()
                        pin1.write_digital(0)
                        break
            while pin2.is_touched():#touch keying
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
                if duration < interletter:
                    buffer += '0'
                    display.clear() # might not be needed
                    display.set_pixel(2,2,9)
                elif duration:
                    buffer += '1'
                    display.show('-')
                started = running_time()
            elif len(buffer) > 0 and waited > interword: #or DASH_THRESHOLD = dotlength * 5
                display.clear() # might not be needed
                character = decoder(int("0b1" + buffer, 2))
                buffer = ''
                display.show(character)
                if txenabled:
                    radio.send(character)
            if waited > interword * 2:
                return


while True:
    keyer()
    receiver()
