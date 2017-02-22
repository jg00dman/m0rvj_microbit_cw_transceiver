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

# reverse dict.
#decodemorse = {v: k for k, v in morse.items()}
# in our final program we don't want to waste the overhead by having this dict.

#Turn a string of raw CW in the form 001100 into an ASCII character byte
def rawCWtoASCII(dotdashstring):
    #code input as raw morse to int
    cwcharint = int("0b1" + dotdashstring,2) + 34
    #int to char
    return chr(cwcharint)
    
#make a codestring which contains all cw characters in the same order as the ascii range 44-91
codestring = ''
for i in range(44,91):codestring+=rawCWtoASCII(morse.get(chr(i)))
#codestring now contains the whole morse code 
#we don't need to run all of this code on the microbit
#we can just use the string as our data source for the code.
#now run the program with python3 NAME>cw.txt
print(codestring)

#so in future programs all of the above can be simplified into
codestring = "LTaQIECBRZ^`Sn|':<.$402&9/6)(18?,*%+3-;=>"
#now turn a character into cw
#encodes morse as ascii char morsechar from the codestring
def encoder(message):
    return codestring[ord(message.upper())-44]
    
# decodes from morsechar to text character.
def decoder(morsechar):
    return chr(codestring.find(morsechar)+44)
    
#display a morse character in the form of dots and dashes like "..--.."
def toText(message):
    return bin(message)-34[3:].translate(" "*47+"/.-"+" "*206)
    
#prove coding workds
def proofTEST():
    for i in range(44,91):
        j = chr(i)
        print(j + " codes to: " + encoder(j) + " & decodes to: " + decoder(encoder(j)))

#proofTEST()

# Decode ascii cw char to binary morse like 001100
def asciitoCWBIN(message):
    return bin(ord(message)-34)[3:]

#print(asciitoCWBIN(encoder('?')))


# convert string to cw
def EncodeMorse(message):
    m = message.upper()
    enc = ""
    for c in m:
        if c !=" ":
            enc = enc + encoder(c) + " "
        else:
            enc = enc + " "
    return enc

print(EncodeMorse("John"))

print(chr(codestring.find('?')+44))
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

'''
    requiring further thought might be...
Ä 	di-dah-di-dah
Á 	di-dah-dah-di-dah
Å 	di-dah-dah-di-dah
Ch 	dah-dah-dah-dah
É 	di-di-dah-di-dit
Ñ 	dah-dah-di-dah-dah
Ö 	dah-dah-dah-dit
Ü 	di-di-dah-dah
AA, New line 	di-dah-di-dah
AR, End of message 	di-dah-di-dah-dit
AS, Wait 	di-dah-di-di-dit
BK, Break 	dah-di-di-di-dah-di-dah
BT , New paragraph 	dah-di-di-di-dah
CL, Going off the air ("clear") 	dah-di-dah-di-di-dah-di-dit
CT, Start copying 	dah-di-dah-di-dah
DO, Change to wabun code 	dah-di-di-dah-dah-dah
KN, Invite a specific station to transmit 	dah-di-dah-dah-dit
SK, End of transmission 	di-di-di-dah-di-dah
SN, Understood (also VE) 	di-di-di-dah-dit
SOS, Distress message 	di-di-di-dah-dah-dah-di-di-dit
'''


