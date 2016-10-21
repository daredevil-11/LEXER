import sys
import getopt
import re
from tabulate import tabulate

imp = ""
try :
    opts, args = getopt.getopt(sys.argv[1:], "hi:")
except getopt.GetoptError :
    print "USAGE: python lexer.py -i <sourcecodefile>"
    sys.exit(2)

for opt, arg in opts :
    if opt == '-h':
        print "USAGE: python lexer.py -i <sourcecodefile>"
        sys.exit()
    elif opt == '-i':
        imp = arg

try :
    source = open(imp, "r")
    #print "SourceCode is in: ", source.name
except IOError :
    print "Unable to open the file"
    sys.exit(3)

typeOf = r"^(int|char)$"
identifiers = r"^[a-zA-Z_][a-zA-Z0-9]*$"
reserved = r"^(true|false|and|or|not|skip|if|while|else|:=|==|<|<=|>|>=|\(|\)|\{|\}|;)$"
value = r"^-?[0-9][0-9]*$"
character = r"'.'"
checkExp = typeOf + r"|" + identifiers + r"|" + reserved + r"|" + value + r"|" + character

identifier = re.compile(identifiers)
reserve = re.compile(reserved + "|" + typeOf)
regex = re.compile(checkExp)

lineCount = 0
symbolDict = {}

code = source.read().splitlines()
for line in code :
    lineCount += 1
    wordArr = line.split()
    
    for wordNumber, word in enumerate(wordArr) :
        if regex.match(word) == None :
            print "Syntax Error in Line %d at (%d):%s" % (lineCount, wordNumber+1, word)
            sys.exit(-1)
    
    for wordNumber, word in enumerate(wordArr) :
        if word == "char" :
            if wordNumber+1 >= len(wordArr) :
                print "Error at line %d: Invalid identifier declaration at (%d:)%s" %(lineCount, wordNumber, word)
                sys.exit(4)

            identify = wordArr[wordNumber+1]
            if symbolDict.has_key(identify) :
                print "Error: Identifier redefinded at line %d (%d:)%s" % (lineCount, wordNumber+1, identify)
                sys.exit(-2)

            elif identifier.match(identify) == None or reserve.match(identify) != None :
                print "Error: Identifier can not be definied at line %d (%d:)%s" % (lineCount, wordNumber+1, identify)
                sys.exit(-3)

            else :
                symbolDict[wordArr[wordNumber+1]] = "char"
        
        elif word == "int" :
            if wordNumber+1 >= len(wordArr) :
                print "Error at line %d: Invalid identifier declaration at (%d:)%s" %(lineCount, wordNumber, word)
                sys.exit(4)

            identify = wordArr[wordNumber+1]    
            if symbolDict.has_key(identify) :
                print "Error: Identifier redefinded at line %d (%d:)%s" % (lineCount, wordNumber+1, identify)
                sys.exit(-2)
            elif identifier.match(identify) == None or reserve.match(identify) != None :
                print "Error: Identifier can not be definied at line %d (%d:)%s" % (lineCount, wordNumber+1, identify)
                sys.exit(-3)
            else :
                symbolDict[wordArr[wordNumber+1]] = "int"
        
            
print "SYMBOL TABLE:"
header = ["Identifier", "Type", "Size in Bytes"]
symbolTable= []
for key, value in symbolDict.iteritems() :
    if value == "int" :
        symbolTable.append([key, value, 2])
    if value == "char" :
        symbolTable.append([key, value, 1])

print tabulate(symbolTable, header, tablefmt="grid")
source.close()

