#!/usr/local/sage/sage -python
# coding: utf-8

import sys # for argv function
from sage.all import *

DIMENSION = 7                      # データビット数
DEGREEOFGENERATOR = 8              # 生成多項式の次数
DEGREEOFMINIMUMPOLYNOMIAL = 4      # 最小多項式の次数
NUMBEROFMINIMUMPOLYNOMIAL = 2      # 最小多項式の個数
# primitive polynomial = x^4 + x + 1
INPUTFILE   = '/home/mnemodyne/workspace/Verilog/BCH16_2/input.dat'
CODEWORD01  = '/home/mnemodyne/workspace/Verilog/BCH16_2/codeword01.dat'
CODEWORD08  = '/home/mnemodyne/workspace/Verilog/BCH16_2/codeword08.dat'
CODEWORD16  = '/home/mnemodyne/workspace/Verilog/BCH16_2/codeword16.dat'
CHECKBITS01 = '/home/mnemodyne/workspace/Verilog/BCH16_2/checkbits01.dat'
CHECKBITS08 = '/home/mnemodyne/workspace/Verilog/BCH16_2/checkbits08.dat'
CHECKBITS16 = '/home/mnemodyne/workspace/Verilog/BCH16_2/checkbits16.dat'

CORRECTEDDATA = './corrected.dat'
      
def generateTestData(BaseElement, MultiplicativeOrder):
    CodeWordLength = BaseElement**MultiplicativeOrder - 1
    try:
        fp = open(INPUTFILE, 'w')
        for i in range(0, CodeWordLength - 1):
            fp.write(str(0))
#            if(a == 1):
#                a = 0
#            else:
#                a = 1
        fp.write(str(1))
    except IOError:
        print u"ファイルを開けませんでした"
        sys.exit()
    fp.close()
    return

def BCHDecoder(BaseElement, CorrectableBits, MultiplicativeOrder, Filename):

    # open file and read bit stream
    try:
        fp = open(Filename, 'r')
        input = []
        for i in range(0, BaseElement**MultiplicativeOrder - 1):
            input.append(0)
        for i in range(0, BaseElement**MultiplicativeOrder - 1):
            input[i] = int(fp.read(1), 2)       #2進数として読み込み
        fp.close()
    except IOError:
        print u"ファイルを開けませんでした:{0}".format(Filename)
        sys.exit()

    #get syndromes     
    syndromes = BCHSyndrome(input, BaseElement, MultiplicativeOrder, CorrectableBits)
    
    # calculate error locator
    sigma = BMDecoder(syndromes, BaseElement, MultiplicativeOrder, CorrectableBits)
    
    # return error position
    errorposition = chien(sigma, BaseElement, MultiplicativeOrder)
    
    # write corrected input[] to a file "corrected.dat"
    correctData(errorposition, input)

#end of function

########################### Correct Data ##################################
def correctData(errorposition, input):
   
    # reverse input[]
    input.reverse()
    
    for i in errorposition:
        input[i] = bitflip(input[i])
    
    # reverse agaom input[] avoiding conflict other functions
    input.reverse()

    # open file and save corrected data
    try:
        #open file
        fp = open(CORRECTEDDATA, 'w')

        for i in range(0, BaseElement**MultiplicativeOrder - 1):
            fp.write(str(input[i]))       #write as a 0 or 1 character
        fp.close()
    except IOError:
        print u"ファイルを開けませんでした:{0}".format(Filename)
        sys.exit()

   
#end of function

############################# bit flip function ##########################
def bitflip(x):
    y = 0
    if x == 0:
        y = 1
    else:
        y = 0
    
    return y

#end of function

########################### Syndrome Calculation ##########################
def BCHSyndrome(input, BaseElement, MultiplicativeOrder, CorrectableBits):
    q = BaseElement
    m = MultiplicativeOrder
    x = PolynomialRing(GF(q), 'x').gen()
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='alpha', modulus=f)
    else:
        K = GF(q**m, name='alpha')

    # generate primitive element alpha        
    alpha = K.gen()   

    #initial condition   
    codeword = 0
    for i in range(0, q**m - 1):
        codeword += input[i]*x**(q**m - 2 - i)

#    print "<syndrome> codeword = {0}".format(codeword)
    #calculate generator polynomial
    generator = getBCHCodeGeneratingPolynomials(q**m - 1, 2*CorrectableBits + 1, BaseElement, NarrowFlag = 0)
    
    #check errors
    residue = codeword%generator 
    if residue == 0:
        print "<BCHSyndrome> No Error"
        sys.exit(1)

    #declare syndromes as a list   
    syndromes = []
    
    #add syndromes
    for i in range(1, 2*CorrectableBits + 1):
        syndromes.append(residue(alpha**i))
            
    return syndromes

# Chien Search function
def chien(errorlocator, BaseElement, MultiplicativeOrder):
    q = BaseElement
    m = MultiplicativeOrder
    x = PolynomialRing(GF(q), 'x').gen()
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='alpha', modulus=f)
    else:
        K = GF(q**m, name='alpha')

    alpha = K.gen() 
    
    print "<chien> errorlocator = {0}".format(errorlocator)
    if errorlocator == 1:
        print "No Error"
        sys.exit(1)
        
    errorflag = 0
    errorposition = []
    for i in range(0, q**m - 1):
        Ex = errorlocator(1/alpha**i)
        if Ex == 0:
            print "bit {0} error detected".format(i)
            errorposition.append(i)                 #save error position for correction
            errorflag += 1
    
    if errorflag == 0 or errorflag != errorlocator.degree():
        print "Logical Conflict Detected"
        print "errorlocator = {0}".format(errorlocator)
        print "But this program can not identify error bit"
        sys.exit(1)
    
    return errorposition

# end of function
def BMDecoder(syndromes, BaseElement, MultiplicativeOrder, CorrectableBits):
    q = BaseElement
    m = MultiplicativeOrder
    # Declare polynomial variables
    x = PolynomialRing(GF(q), 'x').gen()
    z = PolynomialRing(GF(q), 'z').gen()
    # Define Galois Field GF(q**m) and its primitive element is alpha
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='alpha', modulus=f)
    else:
        K = GF(q**m, name='alpha')
    # generate instance of alpha
    alpha = K.gen()
    
#    print "<DEBUG> syndromepolynomial = {0}".format(syndromepolynomial)
    #initialize functions and variables
    D = 0                         #branch decision parameter
    delta = 1                     #coefficient for error locator sigma
    sigma = 1 + 0*z               #error locator polynomial
    tau = 1 + 0*z                 #auxiliary polynomial for sigma


    #Initially, DELTA = syndromes[0]
    DELTA =  syndromes[0]
    print "syndromes = {0}".format(syndromes)
    # iterative computation for sigma and tau
    for i in range(0, 2*CorrectableBits):
        tautmp = tau
        deltatmp = delta
        if DELTA == 0 or 2*D >= i + 1:
            tau = z*tau
        else:
            D = i + 1 - D
            delta = DELTA
            tau = sigma
        print "{0:>2} D = {1} delta = {2} tau = {3} DELTA = {4}".format(i, D, delta, tau, DELTA)

        #calculation sigma
        sigma = deltatmp*sigma+DELTA*z*tautmp
        sigmacoeffs = sigma.coeffs()
        print "{0:>2} sigma = {1}".format(i, sigma)
        #calculation DELTA
        #DELTA(i+1)=S_{i+1}*sigma_{0}^{(i)}+S_{i}*sigma_{1}^{(i)}+...+S_{i+1-nu_{i}}*sigma_{nu_{i}}^{(i)}
        #nu_{i} = sigma^{(i)}.degree()
        if i == 2*CorrectableBits - 1:
            zeta = sigma.coeffs()
            sigma = sigma/zeta[0]
            return sigma
        else:
            # calculate Degree of sigma
            nu = sigma.degree()
            print "{0:>2} nu = {1}".format(i, nu)
            # calculate DELTA
            DELTA = 0
            for j in range(0, nu + 1):
                print "{0:>2} i + 1 -j = {1} j = {2}".format(i, i + 1 - j, j)
                DELTA += syndromes[i + 1 - j]*sigmacoeffs[j]
#                print "{0:>2} j = {1} x = {2}".format(i, j, syndromes[i + 1 - j]*sigmacoeffs[j])
#            DELTA = DELTA%2
            print "{0:>2} DELTA = {1}".format(i, DELTA)
#end of function

################################ get Minimum Polynomials for BCH Code #################################
def getBCHCodeMinimumPolynomials(CodeWordLength, MinimumDistance, BaseElement, NarrowFlag = 0):
    q = BaseElement
    R = IntegerModRing(CodeWordLength)
    m = R(q).multiplicative_order()
    x = PolynomialRing(GF(q), "x").gen()
    # if m == 14 then choose Mizushima's primitive polynomial
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='a', modulus=f)
    else:
        K = GF(q**m, name='a')
        
    a = K.gen()
    L0 = [a**i for i in range(NarrowFlag, NarrowFlag + MinimumDistance)]
    L1 = [b.minpoly() for b in L0]
    L1.pop(0) # L1[0] is trivial polynomial "x+1".

# return List of Minimum Polynomials
    return L1
######################################## End of Function ###############################################

############################### get generator polynomial for BCH Code ##################################
def getBCHCodeGeneratingPolynomials(CodeWordLength, MinimumDistance, BaseElement, NarrowFlag = 0):
    q = BaseElement
    R = IntegerModRing(CodeWordLength)
    m = R(q).multiplicative_order()
    x = PolynomialRing(GF(q), "x").gen()

    L1 = getBCHCodeMinimumPolynomials(CodeWordLength, MinimumDistance, BaseElement, NarrowFlag = 0)

    generator = LCM(L1)
    if not (generator.divides(x**CodeWordLength-1)):
        ValueError, "BCH Codes do not exist with the given input"
    else:
#        print "Generating Polynomial"
        return generator
######################################## End of Function ###############################################

if __name__ == '__main__':
    #translate command line argument
    argvs = sys.argv           #argvs is a list of commandline argument
    if len(argvs) != 2:
        print "Usage ./BMdecoder <file name>"
        sys.exit()

    Filename = argvs[1]
    # generate Test Data
    BaseElement = 2
    MinimumDistance = 81
    CorrectableBits = (MinimumDistance - 1)/2
    MultiplicativeOrder = 14
    NarrowFlag = 0
#    generateTestData(BaseElement, MultiplicativeOrder)
    BCHDecoder(BaseElement, CorrectableBits, MultiplicativeOrder, Filename)