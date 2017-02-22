#python app designed to encode and decode cw in minimum chars
#codestring = "•ƒwTaQIECBRZ^`šŒ#S#n|':<.$402&9/6)(18?,*%+3-;=>"

# note that the ascii charset conveniently orders the characters we want to encode
#for i in range(44,91):print(str(i) + ": " + chr(i))
#from this we make a string which is 44-91 in order.
encodestring=",-,./0123456789\":;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#this means that a string of 40 chars can be matched to the respective cw
#how do we encode these chars? First we manually write in the cw 1 is dah 0 is dit
morse = {
    ",":"110011",
    "-":"100001",
    ".":"01010",
    "/":"10010",
    "0":"11111",
    "1":"01111",
    "2":"00111",
    "3":"00011",
    "4":"00001",
    "5":"00000",
    "6":"10000",
    "7":"11000",
    "8":"11100",
    "9":"11110",
    ":":"111000",
    ";":"111000",
    "<":"101101",
    "=":"10001",
    ">":"101101",
    "?":"001100",
    "@":"011010",
    "A":"01",
    "B":"1000",
    "C":"1010",
    "D":"100",
    "E":"0",
    "F":"0010",
    "G":"110",
    "H":"0000",
    "I":"00",
    "J":"0111",
    "K":"101",
    "L":"0100",
    "M":"11",
    "N":"10",
    "O":"111",
    "P":"0110",
    "Q":"1101",
    "R":"010",
    "S":"000",
    "T":"1",
    "U":"001",
    "V":"0001",
    "W":"011",
    "X":"1001",
    "Y":"1011",
    "Z":"1100"
}

morse2 = [ 0b1110011, 0b1100001, 0b101010, 0b110010, 0b111111, 0b101111, 0b100111, 0b100011, 0b100001, 0b100000, 0b110000, 0b111000, 0b111100, 0b111110, 0b1111000, 0b1111000, 0b1101101, 0b110001, 0b1101101, 0b1001100, 0b1011010, 0b101, 0b11000, 0b11010, 0b1100, 0b10, 0b10010, 0b1110, 0b10000, 0b100, 0b10111, 0b1101, 0b10100, 0b111, 0b110, 0b1111, 0b10110, 0b11101, 0b1010, 0b1000, 0b11, 0b1001, 0b10001, 0b1011, 0b11001, 0b11011, 0b11100 ]


# reverse dict.
#decodemorse = {v: k for k, v in morse.items()}
# in our final program we don't want to waste the overhead by having this dict.

#Turn a string of raw CW in the form 001100 into an ASCII character byte
#def rawCWtoASCII(dotdashstring):
    #code input as raw morse to int
 #   cwcharint = int("0b1" + dotdashstring,2) + 34
    #int to char
  #  return chr(cwcharint)
    
#make a codestring which contains all cw characters in the same order as the ascii range 44-91
codestring = ''
#for i in range(44,91):codestring+=rawCWtoASCII(morse.get(chr(i)))
#codestring now contains the whole morse code 
#we don't need to run all of this code on the microbit
#we can just use the string as our data source for the code.
#now run the program with python3 NAME>cw.txt
print(codestring)

#so in future programs all of the above can be simplified into
#codestring = "LTaQIECBRZ^`Sn|':<.$402&9/6)(18?,*%+3-;=>"
#now turn a character into cw

#Turn a string of raw CW in Binary form like 001100 into ASCII morse chars
def rawCWtoASCII(dotdashstring):
    y = ''
    for i in dotdashstring.split():
        try:#code input as raw morse to int
            cwcharint = int("0b1" + i,2) + 34
            #int to char
            y += chr(cwcharint)
        except:
            y += chr(18) # return a question mark if the cw can't be encoded.
    return y

#for i in morse:codestring+=rawCWtoASCII(i)
codestring = morse2

def rawCWtoBinary(dotdashstring):
    y = ''
    for i in dotdashstring.split():
        try:#code input as raw morse to int
            y += "0b1" + i
            #int to char
        except:
            y += Bin(18) # return a question mark if the cw can't be encoded.
    return y

# Decode ascii cw char to binary morse like 001100 which can then be easily played etc.
def asciitoCWBIN(message):
    y = ''
    try:
        for i in message:
            if i > 0:
                y += ' '
            y += bin(ord(i)-34)[3:]
    except:
        y += "001100"
    return y


#encodes morse by replacing ascii char with morsechar from the codestring
def encoder(message):
    z = ''#buffer to build the message
    for i in message:
        if i != ' ':#check for spaces
            y = ord(i.upper())# get int for char
            if y < 44 or y > 90:
                y = 63 #replace message with 63 makes it a ?
            z += codestring[y-44]#returns the char from codestring with the binary of the cw stored in it.
        else:
            z += " "
    return z


# decodes from string of morsechars to string of text characters.
def decoder(morsechar):
    y=''
    for i in morsechar:
        try:
            x = chr(codestring.find(i)+44)#find the character in the codestring and bump it by 44 to find the ASCII char
            y += x #if found add it to the return variable
        except: 
            y+= ' ' #if it isn't found then return a question mark
    return y


#prove coding workds
def proofTEST():
    for i in range(44,91):
        j = chr(i)
        print(j + " codes to: " + encoder(j) + " & decodes to: " + decoder(encoder(j)))

proofTEST()

#prove coding workds try to give errors
def proofTEST2():
    for i in range(0,100):
        j = chr(i)
        print(j + " codes to: " + encoder(j) + " & decodes to: " + decoder(encoder(j)))

#proofTEST2()


#print(asciitoCWBIN(encoder('?')))
print(encoder("John"))
print(rawCWtoASCII("0111 111 0000 10"))
print(decoder(rawCWtoASCII("0111 111 0000 10")))
print(asciitoCWBIN(encoder("Jo+n")))

for i in morse2:
    print("0b1" + i)


#(Create alternative codestring)
#y = '['
#for i in range(44,91):y+= " \"" + asciitoCWBIN(encoder(chr(i))) + "\", "
#y += "]"
#print(y)
#Morse Keyer with accurate timings


#Radio Receiver

#Tutor


#amazing short code example encodes morse as ".--." this won't be needed in the final program but was interesting...
#def encode(message):
#    y = ''
#    for c in message.upper():
#        y+=c<","and"/"or bin(ord(codestring[ord(c)-44])-34)[3:].translate(" "*47+"/.-"+" "*206)
#    return y
    

#y = ''
#for x in ",-,./0123456789\":;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ": y+=encoder(x)
#print(y)

    


#def DecodeMorse(message):
    #int('11111111', 2) opposite of bin
    #ord() opposite of chr()
#    int(chr("•ƒwTaQIECBRZ^`šŒ#S#n|':<.$402&9/6)(18?,*%+3-;=>"[chr(message)+44])+34,2)[-3:]#.translate(" "*47+"/.-"+" "*206)
    
#print(EncodeMorse("1234567890 John Goodman M0RVJ/p?"))

#print("..--.. / john 12345".translate(" "*47+"/.-"+" "*206))
#print(DecodeMorse("•"))


#y = ''
#for x in ",-,./0123456789\":;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ": y+=encoder(x)
#print(y)
#print(codestring)




