# Berlekamp-Massey decoding algorithm demo program 
This program is a Berlekamp-Massey decoding algorithm demo program.

## Preparation
Install [sage](https://www.sagemath.org). This program is written in [sage](https://www.sagemath.org). [Sage](https://www.sagemath.org) is a programming language for mathematicians. [Sage](https://www.sagemath.org) is python-based language and has many extensive features for algebra, algebraic geometry and number theory.


## Downdloading the demo program
Clone demo program's repository.

```sh
git clone https://github.com/xenocaliver/BMDecoder.git ./
```

## Run the demo program
Run demo program as follows.  Regarding BCH code's demo program, run `BCHDecoder.py`.

```sh
sage BCHDecoder.py
```

Regarding Reed-Solomon code's demo program, run `RSDecoder.py`.

```sh
sage RSDecoder.py
```

## Implimentation details
### Cyclic codes
Before discussing Berlekamp-Massey algorithm, we must discuss cyclic codes. We begin crush course for cyclic codes. For persons who want to learn cyclic codes deeply, I recommend coding theory text book e.g. [Error Correction Coding: Mathematical Methods and Algorithms](https://onlinelibrary.wiley.com/doi/book/10.1002/0471739219). I assume that readers know basic algebra.

Let $`\mathbb{F}_{q}`$ be a finite field with characteristic $`q`$. In coding theory, $`q=2^{M}`$ and $`M`$ is a natural number. Let $`k`$ is a natural number called "dimension". $`m_{i}\in\mathbb{F}_{q}(i=0,\ldots,k-1)`$ and we call $`\boldsymbol{m} = (m_{0},\ldots,m_{k-1})`$ a message vector. We express the message as a polynomial

$$
m(x)=m_{0}+m_{1}x+\cdots+m_{k-1}x^{k-1}
$$

and we call $m(x)$ a message polynomial. Let $n$ be a integer "code length" such as $n>k$. We multiply $m(x)$ by $x^{n-k}$ and divide it by generator polynomial $g(x)$ and we have

$$
x^{n-k}m(x)=q(x)g(x)+r(x).
$$

$q(x)$ is a quotient polynomial and $r(x)$ is a remainder polynomial. And $c(x)$ be a code polynomial and it is defined as follows:

$$
c(x)=x^{n-k}m(x)-r(x).
$$

A transmitter sends $c(x)$ and a receiver receives $y(x)$. One can check whether $y(x)$ has errors or not by means of dividing $y(x)$ by $g(x)$. If remainder $r(x)$ equals to $0$, $y(x) = c(x)$ in other words, $y(x)$ has no errors. On the other hand, if $r(x)\neq 0$, $y(x)$ has some errors.