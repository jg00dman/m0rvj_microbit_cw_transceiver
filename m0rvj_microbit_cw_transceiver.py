##########################
#   This is a working CW Radio. 'B' is key. 'A' shows message received in text.
#   A shake opens a menu and you make selections by sending a character. Settings are retained.
#   Connect Speaker or Headphones to Pin 0 and Ground
#   Or connect Piezo Buzzer or Haptic Motor for Silent operation to pin1 and ground
#   pin2 is capacitive touch keying.
#   Copyright (C) 2019 Revd. John Goodman M0RVJ,
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
###########################nu
from microbit import *
import radio, music

radio.on()
radio.reset()
conf = ['A','H','N','U'] #"ABCDEF" give speeds. GHIJKLM give tones NOPQRS give channels T tutor mode UV power high/low WXYZ"
di = 80
dah = 240
space = 560
tx = True
tone = 550
morse = [115, 97, 42, 50, 63, 47, 39, 35, 33, 32, 48, 56, 60, 62, 120, 120, 109, 49, 109, 76, 90, 5, 24, 26, 12, 2, 18, 14, 16, 4, 23, 13, 20, 7, 6, 15, 22, 29, 10, 8, 3, 9, 17, 11, 25, 27, 28]
music.play(music.POWER_UP)
#encodes morse by replacing ascii char with morse binary from the morse array
def enc(message):
    z = []
    for i in message:
        if i != ' ':
            y = ord(i.upper())# get int for char
            if y < 44 or y > 90: y = 63 #replace message with 63 makes it a ?
            z.append(morse[y-44])#returns the char from morse
        else: z.append(1)
    return z


# decodes morse binary to text.
def decoder(*message):
    y=''
    for i in message:
        try:
            if i == 1: y += ' '
            else:
                x = chr(morse.index(i)+44)#bump char by 44 to match ASCII
                y += x #if found add it to the return variable
        except: y+= '?' #if it isn't found
    return y


# playMorse cw
def playMorse(*binarycw):
    for x in binarycw:
        for i in x:
            if i == 1: sleep(space)
            pattern = bin(i)[3:]
            for c in pattern:
                if c == "0":
                    display.set_pixel(2,2,9)
                    pin1.write_digital(1)
                    music.pitch(tone, di)
                elif c == "1":
                    display.show("-")
                    pin1.write_digital(1)
                    music.pitch(tone, dah)
                display.clear()
                pin1.write_digital(0)
                sleep(di)
            sleep(dah)

#"ABCDEF" give speeds. GHIJKLM give tones NOPQRS give channels T tutor mode UV power high/low WXYZ"
def menu(*command):
    global tx
    global tone
    global di
    global dah
    global space
    global conf
    power = 'QRO'
    WPM = 15
    try:
        with open('f.txt') as cwf:
            config = cwf.read()
        for i in range(0,3): conf[i] = config[i]
        config = ''
        display.scroll('.')
    except:
        display.scroll('-')
    if command:
        if command[0] is 'Z':
            conf = ['A', 'H', 'N', 'U']
        for i in command: conf.append(i)
    for i in conf:
        x = ord(i) - 64
        if x < 1 or x > 23 and not 26: #out of range / unknown command
            playMorse(enc('?'))
            return
        elif x < 7: #"ABCDEF" give speeds.
            WPM = 12 + x * 3 #range 15-30
            di = int( 60000 / ( WPM * 50 ) )
            dah = di * 3
            space = di * 7
            conf[0] = i
        elif x < 14: #GHIJKLM tone pitch
            tone = (x + 3) * 50 #range 500hz-800hz
            conf[1] = i
        elif x < 20:
            chn = x -13 #channels 1-6
            radio.config(channel=chn)
            conf[2] = i
#        elif x is 20: pass #tutor mode needs creating
        elif x is 21: #power hi U
            radio.config(power=7)
            conf[3] = i
            power = 'QRO'
        elif x is 22: #power lo V
            radio.config(power=2)
            conf[3] = i
            power = 'QRP'
        else: pass #wxyz unknown command
    if command:
        conf = conf[:4]
        if command[0] is 'T':
            playMorse(enc('M0RVJ suggests cwops.org'))
        else:
            playMorse(enc('S' + str(WPM) + "T" + str(tone) + "C" + str(chn) + power))
        try:
            with open('f.txt', 'w') as f:
                f.write(conf[0] + conf[1] + conf[2] + conf[3])
        except: display.scroll('-')
    tx = 1 #exit command mode.


def receiver():
    global tx
    message = ''
    if tx: display.show(Image("90909:09990:00900:00900:00900"))
    else: display.show('?')
    t0 = running_time()
    while True:
        t1 = running_time() - t0
        received = radio.receive()
        if received:
            playMorse(enc(received))
            message += received
            display.show(Image("90909:09990:00900:00900:00900"))
        if button_b.is_pressed(): return # breakin
        if pin2.is_touched(): return # breakin
        if button_a.was_pressed():
            display.scroll(message) # nb blocks receive
            message = ''
            return
        if len(message) > 15: message = message[1:16] #keep message buffer short
        if accelerometer.was_gesture("shake"):
            tx = not tx
            if tx: return
            else: display.show('?')


def keyer():
    buffer = '' #for di or dah sent
    started = running_time() #timer
    while True:
            waited = running_time() - started
            key_down_time = None
            while button_b.is_pressed() or pin2.is_touched():#button B keying or capacitive touch (tip: lick 2 fingers one on gnd one on pin 2)
                if not key_down_time: key_down_time = running_time()
                music.pitch(tone, -1, pin0, False)
                pin1.write_digital(1)
                while True:
                    if not button_b.is_pressed() and not pin2.is_touched():
                        break
            music.stop()
            pin1.write_digital(0)
            key_up_time = running_time()
            if key_down_time:
                duration = key_up_time - key_down_time
                if duration < dah:
                    buffer += '0'
                    display.clear()
                    display.set_pixel(2,2,9)
                elif duration:
                    buffer += '1'
                    display.show('-')
                started = running_time()
            elif len(buffer) > 0 and waited > dah: #or DASH_THRESHOLD = di * 5
                character = decoder(int("0b1" + buffer, 2))
                buffer = ''
                display.show(character)
                if tx: radio.send(character)
                else: menu(character)
            if waited > space * 2: return


menu()
while True:
    keyer()
    receiver()