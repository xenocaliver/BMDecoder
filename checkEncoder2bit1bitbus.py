#!/usr/bin/python
# coding: utf-8

import sys #for argv function

DIMENSION = 7               #データビット数
DEGREEOFGENERATOR = 8     #生成多項式の次数
INPUTFILE   = './input.dat'
CODEWORD01  = './codeword01.dat'
CODEWORD08  = './codeword08.dat'
CODEWORD16  = './codeword16.dat'
CHECKBITS01 = './checkbits01.dat'
CHECKBITS08 = './checkbits08.dat'
CHECKBITS16 = './checkbits16.dat'

def BCHEncoder(BusWidth = 1):
    # x, y, z stands for Linear Feedback Shift Register
    x = []

    input = []

    #initialize x, y, z
    for i in range(0, DEGREEOFGENERATOR):
        x.append(0)
    
    #initialize input list
    for i in range(0, DIMENSION):
        input.append(0)
    # open file
    try:
        fp = open(INPUTFILE, 'r')
        for i in range(0, DIMENSION):
            input[i] = int(fp.read(1), 2) #2進数として読み込み
        
        fp.close()
    except IOError:
        print u"%sを開けませんでした"%INPUTFILE
        sys.exit()
    

    # branch BusWidth
    if BusWidth == 1:
        for i in range(0, DIMENSION):
            x = lfsr01(x, input[i])
        #write to the file output01.dat
        try:
            fp = open(CODEWORD01, 'w')
            for i in range(0, DIMENSION):
                fp.write(str(input[i]))
            for i in range(DEGREEOFGENERATOR - 1, -1, -1):
                fp.write(str(x[i]))
        except IOError:
            print u"%sを開けませんでした"%CODEWORD01
            sys.exit()
    else:
        print "Invalid BusWidth = {0}".format(BusWidth)
        print "You should set BusWidth to 1"
        sys.exit()
#end of function

def lfsr01(x, bz):
    y = []
    for i in range(0, DEGREEOFGENERATOR):
        y.append(0)

    y[  7] = x[  7]^bz^x[  6]
    y[  6] = x[  7]^bz^x[  5]
    y[  5] = x[  4]
    y[  4] = x[  7]^bz^x[  3]
    y[  3] = x[  2]
    y[  2] = x[  1]
    y[  1] = x[  0]
    y[  0] = x[  7]^bz
    
    return y
#end of function

def BCHDecoder(BusWidth):
    x = []
    for i in range(0, DEGREEOFGENERATOR):
        x.append(0)
    input = []
    for i in range(0, DIMENSION + DEGREEOFGENERATOR):
        input.append(0)
            
    if BusWidth == 1:
        try:
            fp = open(CODEWORD01, 'r')
            for i in range(DIMENSION + DEGREEOFGENERATOR - 1, -1, -1):
                input[i] = int(fp.read(1), 2) #2進数として読み込み
            fp.close()
        except IOError:
            print u"ファイルを開けませんでした{0}".format(CODEWORD01)
            sys.exit()

        for i in range(DIMENSION + DEGREEOFGENERATOR - 1, -1, -1):
#        for i in range(0, DIMENSION):
            x = lfsr01(x, input[i])

        try:
            fp = open(CHECKBITS01, 'w')
            for i in range(0, DEGREEOFGENERATOR):
                fp.write(str(x[i]))
            fp.close()
        except IOError:
            print "ファイルを開けませんでした:{0}".format(CHECKBITS01)
            sys.exit()
    else:
        print "Invalid BusWidth = {0}".format(BusWidth)
        print "You should set BusWidth to 1"
        sys.exit()

def generateTestData():
    a = 1
    try:
        fp = open(INPUTFILE, 'w')
        for i in range(0, DIMENSION):
            fp.write(str(a))
            if(a == 1):
                a = 0
            else:
                a = 1
    except IOError:
        print u"ファイルを開けませんでした"
        sys.exit()
    fp.close()
    return
#end of function
if __name__ == '__main__':
    #translate command line argument
    argvs = sys.argv           #argvs is a list of commandline argument
    if len(argvs) != 2:
        print "Usage ./checkEncoder <BusWidth>"
        sys.exit()

    BusWidth = int(argvs[1])   #argvs[0] is this script file name
    # generate Test Data
    generateTestData()
    BCHEncoder(BusWidth)
    BCHDecoder(BusWidth)
