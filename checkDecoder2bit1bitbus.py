#!/usr/bin/python
# coding: utf-8

import sys #for argv function

DIMENSION = 7                      #データビット数
DEGREEOFGENERATOR = 8            #生成多項式の次数
DEGREEOFMINIMUMPOLYNOMIAL = 4     #最小多項式の次数
NUMBEROFMINIMUMPOLYNOMIAL = 2     #最小多項式の個数
INPUTFILE   = './input.dat'
CODEWORD01  = './codeword01.dat'
CODEWORD08  = './codeword08.dat'
CODEWORD16  = './codeword16.dat'
CHECKBITS01 = './checkbits01.dat'
CHECKBITS08 = './checkbits08.dat'
CHECKBITS16 = './checkbits16.dat'
      
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

def BCHDecoder(filename, BusWidth):
    #declare as lists
    x01 = []
    x03 = []
    syn01 = []
    syn03 = []
    
    #initialize lists
    for i in range(0, DEGREEOFMINIMUMPOLYNOMIAL):
        x01.append(0)
        x03.append(0)
        syn01.append(0)
        syn03.append(0)

    input = []
    for i in range(0, DIMENSION + DEGREEOFGENERATOR):
        input.append(0)
            
    if BusWidth == 1:
        try:
            fp = open(filename, 'r')
            for i in range(DIMENSION + DEGREEOFGENERATOR - 1, -1, -1):
                input[i] = int(fp.read(1), 2) #2進数として読み込み
            fp.close()
        except IOError:
            print u"ファイルを開けませんでした{0}".format(filename)
            sys.exit()

# input date into LFSR
        for i in range(DIMENSION + DEGREEOFGENERATOR - 1, -1, -1):
            x01 = lfsr0101(x01, input[i])
            x03 = lfsr0103(x03, input[i])
	syn01 = BCHSyndrome01(x01)
        syn03 = BCHSyndrome03(x03)

        print "Minimum Polynomials"
        print "x01 = [{0}, {1}, {2}, {3}]".format(x01[3], x01[2], x01[1], x01[0])
        print "x03 = [{0}, {1}, {2}, {3}]".format(x03[3], x03[2], x03[1], x03[0])
        print "Syndromes"
        print "syndrome01 = [{0}, {1}, {2}, {3}]".format(syn01[3], syn01[2], syn01[1], syn01[0])
        print "syndrome03 = [{0}, {1}, {2}, {3}]".format(syn03[3], syn03[2], syn03[1], syn03[0])
    else: 
        print "Invalid BusWidth = {0}".format(BusWidth)
        print "You should set BusWidth = 1"
        sys.exit()
#end of function

def lfsr0101(x, bz):
    y = []
    for i in range(0, DEGREEOFMINIMUMPOLYNOMIAL):
	y.append(0)

    y[  3] = x[  2]
    y[  2] = x[  1]
    y[  1] = x[  0]^bz^x[  3]
    y[  0] = bz^x[  3]

    return y
#end of function

def lfsr0103(x, bz):
    y = []
    for i in range(0, DEGREEOFMINIMUMPOLYNOMIAL):
	y.append(0)

    y[  3] = x[  2]^bz^x[  3]
    y[  2] = bz^x[  3]^x[  1]
    y[  1] = x[  0]^bz^x[  3]
    y[  0] = bz^x[  3]

    return y
#end of function

def BCHSyndrome01(x):
    y = []
    for i in range(0, DEGREEOFMINIMUMPOLYNOMIAL):
	   y.append(0)

    y[3] = x[3]
    y[2] = x[2]
    y[1] = x[1]
    y[0] = x[0]
    return y
#end of function

def BCHSyndrome03(x):
    y = []
    for i in range(0, DEGREEOFMINIMUMPOLYNOMIAL):
        y.append(0)

    y[3] = x[1]^x[2]^x[3]
    y[2] = x[2]
    y[1] = x[3]
    y[0] = x[0]
    return y
#end of function

if __name__ == '__main__':
    #translate command line argument
    argvs = sys.argv           #argvs is a list of commandline argument
    if len(argvs) != 3:
        print "Usage: ./checkDncoder <filename> <BusWidth>"
        sys.exit()
    filename = str(argvs[1])
    BusWidth = int(argvs[2])   #argvs[0] is this script file name
    # Decode bitstream in the file 
    BCHDecoder(filename, BusWidth)
