#!/usr/local/sage/default/sage -python
# coding: utf-8

import sys # for argv function

from sage.all import *


def generateRandomData(BaseElement, MultiplicativeOrder, CorrectableBits):
    q = BaseElement
    m = MultiplicativeOrder
    Fq = GF(q**m, name = 'alpha')
    Dimension = q**m - 1 - 2*CorrectableBits
    u = random_vector(Fq, Dimension)
    return u

def makeCodeword(data, BaseElement, MultiplicativeOrder, CorrectableBits):
    q = BaseElement
    m = MultiplicativeOrder
    Fq = GF(q**m, name='alpha')
    x = PolynomialRing(Fq, 'x').gen()
   
    Dimension = q**m - 1 - 2*CorrectableBits 
    v = 0 + 0*x
    for i in range(0, Dimension):
        v += data[i]*x**i
    v = v*x**(2*CorrectableBits)
    #calculate generator polynomial
    generator = getRSCodeGeneratingPolynomials(BaseElement, MultiplicativeOrder, CorrectableBits)
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
    print position
    tmp = 1*0 + 0*x
    for p in position:
        tmp += x**p
    print tmp
    return tmp 
#    return position
# end of function

def verify(pos1, pos2, BaseElement, MultiplicativeOrder):
    Fq = GF(BaseElement**MultiplicativeOrder, name = 'alpha')
    x = PolynomialRing(Fq, 'x').gen()
    result = 0 + 0*x
    for i in pos2:
        result += x**i

    if pos1 == result:
        return True
    else:
        return False
#################################################    
def RSDecoder(BaseElement, MultiplicativeOrder, CodeLength, CorrectableBits):
    Fq = GF(BaseElement**MultiplicativeOrder, name = 'alpha')
    x = PolynomialRing(Fq, 'x').gen()
    
    # generate random data
    u = generateRandomData(BaseElement, MultiplicativeOrder, CorrectableBits)
    # make codeword polynomial
    c = makeCodeword(u, BaseElement, MultiplicativeOrder, CorrectableBits)
    # determin error position
    errors = injectErrors(c, CorrectableBits, CodeLength, BaseElement, MultiplicativeOrder)
    # inject errors
    y = 1*0 + 0*x
    y = c + errors
    # make syndrome
    syndromes = RSSyndrome(y, BaseElement, MultiplicativeOrder, CorrectableBits)
    # create error locator polynomial
    errorlocator = BMDecoder(syndromes, BaseElement, MultiplicativeOrder, CorrectableBits)
    # chien search
    pointout = chien(errorlocator, BaseElement, MultiplicativeOrder)
    #verify
    result = verify(errors, pointout, BaseElement, MultiplicativeOrder)
    if result == True:
        print "Correction is successfully completed."
    else:
        print "Oh my God! Correction is failed."
        print "error position = {0}".format(errors)
        print "result = {0}".format(pointout)
        print "error locator = {0}".format(errorlocator)
        print "syndromes = {0}".format(syndromes)
        sys.exit()
    return result
#end of function

########################### Syndrome Calculation ##########################
def RSSyndrome(input, BaseElement, MultiplicativeOrder, CorrectableBits):
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
    generator = getRSCodeGeneratingPolynomials(BaseElement, MultiplicativeOrder, CorrectableBits)
    
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
    Fq = GF(q**m, name='alpha')
    # Declare polynomial variables
    x = PolynomialRing(Fq, 'x').gen()
    # Define Galois Field GF(q**m) and its primitive element is alpha
    # generate instance of alpha
    alpha = Fq.gen()
    
#    print "<DEBUG> syndromepolynomial = {0}".format(syndromepolynomial)
    #initialize functions and variables
    D = 0                         #branch decision parameter
    delta = 1                     #coefficient for error locator sigma
    sigma = 1 + 0*x               #error locator polynomial
    tau = 1 + 0*x                 #auxiliary polynomial for sigma


    #Initially, DELTA = syndromes[0]
    DELTA =  syndromes[0]
    print "syndromes = {0}".format(syndromes)
    # iterative computation for sigma and tau
    for i in range(0, 2*CorrectableBits):
        tautmp = tau
        deltatmp = delta
        if DELTA == 0 or 2*D >= i + 1:
            tau = x*tau
        else:
            D = i + 1 - D
            delta = DELTA
            tau = sigma
        print "{0:>2} D = {1} delta = {2} tau = {3} DELTA = {4}".format(i, D, delta, tau, DELTA)

        #calculation sigma
        sigma = deltatmp*sigma+DELTA*x*tautmp
        sigmacoefficients = sigma.coefficients()
        print "{0:>2} sigma = {1}".format(i, sigma)
        #calculation DELTA
        #DELTA(i+1)=S_{i+1}*sigma_{0}^{(i)}+S_{i}*sigma_{1}^{(i)}+...+S_{i+1-nu_{i}}*sigma_{nu_{i}}^{(i)}
        #nu_{i} = sigma^{(i)}.degree()
        if i == 2*CorrectableBits - 1:
            zeta = sigma.coefficients()
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

############################### get generator polynomial for BCH Code ##################################
def getRSCodeGeneratingPolynomials(BaseElement, MultiplicativeOrder, CorrectableBits):
    q = BaseElement
    m = MultiplicativeOrder
    F = GF(q**m, name = "alpha")
    alpha = F.gen()
    x = PolynomialRing(F, "x").gen()
    generator = 1 + 0*x
    for i in range(1, 2*CorrectableBits + 1):
        generator *= (x - alpha**i)
    return generator

######################################## End of Function ###############################################

if __name__ == '__main__':
    #translate command line argument
    argvs = sys.argv           #argvs is a list of commandline argument
    # generate Test Data
    BaseElement = 2
    MultiplicativeOrder = 4
    CorrectableBits = 2
    CodeLength = BaseElement**MultiplicativeOrder - 1
    for i in range(0, 10000):
        result = RSDecoder(BaseElement, MultiplicativeOrder, CodeLength, CorrectableBits)
