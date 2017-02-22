#python app designed to encode and decode cw in minimum chars

# note that the ascii charset conveniently orders the characters we want to encode
#for i in range(44,91):print(str(i) + ": " + chr(i))
#from this we make a string which is 44-91 in order.
encodestring=",-,./0123456789\":;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#this means that a string of 40 chars can be matched to the respective cw
#how do we encode these chars? First we manually write in the cw 1 is dah 0 is dit and store them in a byte.

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
def decoder(message):
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


print(decoder([0b101, 0b11000, 0b11010]))

#prove coding workds try to give errors
def proofTEST2():
    for i in range(44,91):
        j = chr(i)
        x = decoder(encoder(j))
        print(j + " encodes and decodes to: " + x)
        
proofTEST2()
encoder("This is a crazy test?")
print("can encode")
print(encoder("This is a crazy test?"))
print(decoder(encoder("This is a crazy test?")))
buffer = "010"
print(decoder(bin(int("0b1" + buffer, 2))))
print(decoder(10))
#Morse Keyer with accurate timings
#Radio Receiver
#Tutor





