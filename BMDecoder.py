#!/usr/local/sage/default/sage -python
# coding: utf-8

import sys # for argv function

from sage.all import *


def generateRandomData(Dimension):
    u = random_vector(Dimension, 0, 2)
    return u

def makeCodeword(data, q, m, CorrectableBits, BaseElement, NarrowFlag):
    q = BaseElement
    m = MultiplicativeOrder
    x = PolynomialRing(GF(q), 'x').gen()
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='alpha', modulus=f)
    else:
        K = GF(q**m, name='alpha')
   
    Dimension = q**m - 1 - m*CorrectableBits 
    v = 0
    for i in range(0, Dimension):
       v += data[i]*x**i
    v = v*x**(m*CorrectableBits)
    #calculate generator polynomial
    generator = getBCHCodeGeneratingPolynomials(q**m - 1, 2*CorrectableBits + 1, BaseElement, NarrowFlag = 0)
    # divide data bits by generator
    quorem = v.quo_rem(generator)
    # c = v + remainder
    c = v + quorem[1]
    return c

def injectErrors(codeword, CorrectableBits, CodeLength, BaseElement, MultiplicativeOrder):
    q = BaseElement
    m = MultiplicativeOrder
    x = PolynomialRing(GF(q), 'x').gen()
    if m == 14:
        f=x**14+x**10+x**6+x+1
        K = GF(q**m, name='alpha', modulus=f)
    else:
        K = GF(q**m, name='alpha')

    position = []
    while(len(position) != CorrectableBits):
        r = ZZ.random_element(CodeLength, distribution = "uniform")
        if r not in position:
            position.append(r)
    position.sort()
#    print position
#    tmp = 1*0 + 0*x
#    for p in position:
#        tmp += x**p
#    y = codeword + tmp
#    return y
    return position
# end of function

def verify(pos1, pos2):
    if pos1 == pos2:
        return True
    else:
        return False
#################################################    
def BCHDecoder(BaseElement, CorrectableBits, MultiplicativeOrder, CodeLength):
    q = BaseElement
    m = MultiplicativeOrder
    x = PolynomialRing(GF(q), 'x').gen()
    
    # generate random data
    u = generateRandomData(CodeLength - CorrectableBits*MultiplicativeOrder)
    # make codeword polynomial
    c = makeCodeword(u, BaseElement, MultiplicativeOrder, CorrectableBits, BaseElement, NarrowFlag)
    # determin error position
    errorposition = injectErrors(c, CorrectableBits, CodeLength, BaseElement, MultiplicativeOrder)
    # inject errors
    y = 1*0 + 0*x
    tmp = 1*0 + 0*x
    for pos in errorposition:
        tmp += x**pos
    y = c + tmp
    # make syndrome
    syndromes = BCHSyndrome(y, BaseElement, MultiplicativeOrder, CorrectableBits)
    # create error locator polynomial
    errorlocator = BMDecoder(syndromes, BaseElement, MultiplicativeOrder, CorrectableBits)
    # chien search
    pointout = chien(errorlocator, BaseElement, MultiplicativeOrder)
    #verify
    result = verify(errorposition, pointout)
    if result == True:
        print "Correction is successfully completed."
    else:
        print "Oh my God! Correction is failed."
        print "error position = {0}".format(errorposition)
        print "result = {0}".format(pointout)
        print "error locator = {0}".format(errorlocator)
        print "syndromes = {0}".format(syndromes)
        sys.exit()
    return result
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


#    print "<syndrome> codeword = {0}".format(codeword)
    #calculate generator polynomial
    generator = getBCHCodeGeneratingPolynomials(q**m - 1, 2*CorrectableBits + 1, BaseElement, NarrowFlag = 0)
    
    #check errors
    quorem = input.quo_rem(generator)
    if quorem[1] == 0:
        print "<BCHSyndrome> No Error"
        sys.exit(1)

    remainder = quorem[1]
    #declare syndromes as a list   
    syndromes = []
    
    #add syndromes
    for i in range(1, 2*CorrectableBits + 1):
        syndromes.append(remainder(alpha**i))
            
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
        sigmacoefficients = sigma.coefficients(sparse = False)
        print "{0:>2} sigma = {1}".format(i, sigma)
        #calculation DELTA
        #DELTA(i+1)=S_{i+1}*sigma_{0}^{(i)}+S_{i}*sigma_{1}^{(i)}+...+S_{i+1-nu_{i}}*sigma_{nu_{i}}^{(i)}
        #nu_{i} = sigma^{(i)}.degree()
        if i == 2*CorrectableBits - 1:
            zeta = sigma.coefficients(sparse = False)
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
                DELTA += syndromes[i + 1 - j]*sigmacoefficients[j]
#                print "{0:>2} j = {1} x = {2}".format(i, j, syndromes[i + 1 - j]*sigmacoefficients[j])
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
    # generate Test Data
    BaseElement = 2
    MinimumDistance = 5 
    CorrectableBits = (MinimumDistance - 1)/2
    MultiplicativeOrder = 4
    NarrowFlag = 0
    CodeLength = BaseElement**MultiplicativeOrder - 1
#    u = generateRandomData(7)
#    c = makeCodeword(u, BaseElement, MultiplicativeOrder, CorrectableBits, BaseElement, NarrowFlag)
#    y = injectErrors(c, CorrectableBits, CodeLength, BaseElement, MultiplicativeOrder)
#    syndromes = BCHSyndrome(y, BaseElement, MultiplicativeOrder, CorrectableBits)
#    errorlocator = BMDecoder(syndromes, BaseElement, MultiplicativeOrder, CorrectableBits)
#    errorposition = chien(errorlocator, BaseElement, MultiplicativeOrder)
    for i in range(0, 10000):
        result = BCHDecoder(BaseElement, CorrectableBits, MultiplicativeOrder, CodeLength)
