# Berlekamp-Massey decoding algorithm demo program 
This program is a Berlekamp-Massey decoding algorithm demo program.

## Preparation
Install [sage](https://www.sagemath.org). This program is written in [sage](https://www.sagemath.org). [Sage](https://www.sagemath.org) is a programming language for mathematicians. [Sage](https://www.sagemath.org) is python-based language and has many extensive features for algebra, algebraic geometry and number theory.


## Downloading the demo program
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

Let $ \mathbb{F}_{q} $ be a finite field with characteristic $ q $. In coding theory, $ q=2^{M} $ and $ M $ is a natural number. Let $ k $ be a natural number called "dimension". $ m_{i}\in\mathbb{F}_{q}(i=0,\ldots,k-1) $ and we call $ \boldsymbol{m} = (m_{0},\ldots,m_{k-1}) $ a message vector. We express the message as a polynomial

$$
m(x)=m_{0}+m_{1}x+\cdots+m_{k-1}x^{k-1}
$$

and we call $m(x)$ a message polynomial. Let $n$ be a integer "code length" such as $n>k$. We multiply $m(x)$ by $x^{n-k}$ and divide it by generator polynomial $g(x)$ and we have

$$
x^{n-k}m(x)=q(x)g(x)+r(x).
$$

$q(x)$ is a quotient polynomial and $r(x)$ is a remainder polynomial. And $c(x)$ be a code polynomial and it is defined as follows:

$$
c(x)=x^{n-k}m(x)-r(x).\tag{1}
$$

A transmitter sends $c(x)$ and a receiver receives $y(x)$. One can check whether $y(x)$ has errors or not by means of dividing $y(x)$ by $g(x)$. If remainder $r(x)$ equals to $0$, $y(x) = c(x)$ in other words, $y(x)$ has no errors. On the other hand, if $r(x)\neq 0$, $y(x)$ has some errors.

### BCH Codes
Let $p$ be a prime number and $m$ be a natural number. And let $q=p^{m}$ and $\mathbb{F}_{q}$ be a finite field over $q=p^{m}$. Let $\alpha$ be a primitive $n$-th root of unity. A BCH code whose length equals to $n$ and which can correct at least $t$ errors is defined as follows:

- Find $\mathbb{F}_{p^{m}}$ which as $n$ primitive $n$ - root of unity $\alpha$.
- Select Non-negative integer $b$.
- Write down $2t$ **consecutive** powers of $\alpha$:

$$
\alpha^{b},\alpha^{b+1},\ldots,\alpha^{b+2t-1}.
$$

- Determine minimal polynomial with respect to $\mathbb{F}_{p}$ of each of powers of $\alpha$.
- generator polynomial $g(x)$ is Least Common Multiplier of above minimal polynomials.

If $b=1$ on construction procedure, the BCH code is said to be **narrow**. If $ n=p^{m}-1 $, the BCH code is called **primitive**.

### Reed-Solomon Codes
Reed-Solomon codes is $ q $-ary BCH codes whose length equals to $ p^{m} - 1 $.

In $\mathbb{F}_{q}$, the minimal polynomials for any root $ \alpha $ is simply $ (x-\alpha) $. Therefore, generator polynomial of Reed-Solomon codes is 

$$
g(x) = (x-\alpha^{b})(x-\alpha^{b+1})\cdots(x-\alpha^{b+2t-1}).
$$

## Decoding of BCH codes and Reed-Solomon codes
In (1), if $r(x)\neq 0$ then received word $y(x)$ has some errors. As per construction of generator polynomials of BCH codes and Reed-Solomon codes, 

$$
g(\alpha)=g(\alpha^{2})=\cdots=g(\alpha^{2t})=0. \tag{2}
$$

Let $e(x)$ be a error polynomial i.e.

$$
e(x)=\sum_{i=0}^{n-1}e_{i}x^{i}
$$

where $e_{i}$ is a coefficient which represents error value and $i$ represents error posistion in the code word. For example, $e_{i}$ is $\{0,1\}$ in binary codes. $e_{i}$ is $\mathbb{F}_{q}$ value in non-binary codes. Thus, received word polynomial is written as follows:

$$
y(x)=c(x)+e(x).
$$

Because $c(x)=q(x)g(x)$ and $(2)$,

$$
y(\alpha^{i})=e(\alpha^{i})\,\,\,(i=0,\ldots,2t).
$$

Then, we define **syndromes** as follows:

$$
S_{i} = e(\alpha^{i})=\sum_{j=0}^{n-1}e_{j}(\alpha^{i})^{j}.
$$

Let $\nu$ be total number of errors and $k_{1},\ldots,k_{\nu}$ be error positions. Then, we have

$$
S_{i}=\sum_{j=1}^{\nu}e_{k_{j}}(\alpha^{i})^{k_{j}}=\sum_{j=1}^{\nu}e_{k_{j}}(\alpha^{k_{j}})^{i}.
$$

Let $X_{j}=\alpha^{k_{j}}$, then we can re-write the syndromes as follows:

$$
S_{i}=\sum_{j=1}^{\nu}e_{k_{j}}(X_{j})^{i}. \tag{3}
$$

Consecutive $2t$ syndromes are shown as follows:

$$
\begin{aligned}
S_{1}&=e_{k_{1}}X_{1}+e_{k_{2}}X_{2}+\cdots+e_{k_{\nu}}X_{\nu}\\
S_{2}&=e_{k_{1}}X_{1}^{2}+e_{k_{2}}X_{2}^{2}+\cdots+e_{k_{\nu}}X_{\nu}^{2}\\
&\vdots \\
S_{2t}&=e_{k_{1}}X_{1}^{2t}+e_{k_{2}}X_{2}^{2t}+\cdots e_{k_{\nu}}X_{\nu}^{2t}.
\end{aligned}
$$

We construct a polynomial whose roots are inverse of $X_{j}$. The polynomial is
shown as follows:

$$
\sigma(x)=\prod_{j=1}^{\nu}(1-X_{j}x)=\sigma_{\nu}x^{\nu}+\sigma_{\nu-1}x^{\nu-1}+\cdots+\sigma_{1}x+\sigma_{0}. \tag{4}
$$

The polynomial is called **error locator polynomial**. By contruction, $\sigma_{0}=0$. Calculating $(4)$ directly, we get

$$
\begin{aligned}
\sigma_{0}&=1\\
-\sigma_{1}&= X_{1}+\cdots+X_{\nu} = \sum_{k=1}^{\nu}X_{k}\\
\sigma_{2}&=X_{1}X_{2}+X_{1}X_{3}+\cdots+X_{1}X_{\nu}+\cdots+X_{\nu-1}X_{\nu}=\sum_{i<j}X_{i}X_{j}\\
-\sigma_{3}&=X_{1}X_{2}X_{3}+\cdots+X_{\nu-2}X_{\nu-1}X_{\nu}=\sum_{i<j<k}X_{i}X{j}X_{k}\\
&\vdots\\
(-1)^{\nu}\sigma_{\nu}&=X_{1}X_{2}\cdots X_{\nu}.
\end{aligned}
$$

As per [Newton's identities](https://en.wikipedia.org/wiki/Newton%27s_identities), $k$-th syndrome $S_{k}$ is given by

$$
-S_{k}=\sigma_{k-\nu}S_{k-\nu}+\sigma_{k-1}S_{k-\nu+1}+\cdots+\sigma_{1}S_{k-1}.
$$

