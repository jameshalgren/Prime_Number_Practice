# Visualizing Primes Using Variable Sieves of Eratosthenes

## Motivation and Background
I wanted to get better at programming and to explore how prime numbers behave, using a tool that shows the periodic nature of the "strike-out" patterns in the sieve of Eratosthenes.
We noticed some fun things as the width of the sieve and the number of primes whose multiples are struck out change.

Open the sieve ([`index.html`](index.html)), move the sliders, and see what you learn!

Post problems, or cool things you figure out, as issues here on GitHub.

Earlier versions of the sieve (and the original README) are kept in [`archive/`](archive/).

## Definitions to Fill In
- Totatives
- Semiprimes
- Big Omega, Ω(n), and k-almost primes
- Primorial (be sure to talk about why it matters here: the repetition of any pattern depends on this value.)
- Next-prime square
- Next-prime cube

## Things We Have Noticed
- The 30-wide sieve has a remarkable property: every number in the first row that can sit above a prime (that is, every number less than 30 with no factor in common with 30) is itself prime, apart from 1. So every prime lines up below another prime (or below 1). 30 is the largest width with this property. 30 is the primorial 2 × 3 × 5, and once the width is bigger than 30, the square of the smallest prime that doesn't divide the width (such as 7 × 7 = 49) fits into the first row. For instance, in the 60-wide sieve almost all of the column heads that can hold primes are prime, but 7 × 7 = 49 is also one of them.
- **Question:** What is the sequence of open columns, and can we predict the gaps between them from the multiples of the small primes? (These open columns are the totatives of the width; the gaps between them repeat with a period equal to the primorial.)
- Every sieve is symmetric in where the prime-holding columns (the "swim lanes") are: column c can hold primes exactly when column W − c can, where W is the width. This is easiest to see in the even widths. (Need to include a screenshot of several showing the swim lanes.)
- The first composite number with three prime factors (Ω = 3) that a partial sieve misses is the cube of the next prime.
- This is a useful tool for teaching about prime numbers. Possibly none of this is groundbreaking mathematically, but it is probably a new way to show it (and a useful one, we think).
- **Idea:** Could we plot the distribution of the primes down the columns? Could we compare the distributions of the primes in symmetric columns (mirrored or translated)?
- **Idea:** What if we started the sieve at 0? Or 2? Or 5? Or any other number? (0 seems most useful.)
- Other grid widths produce interesting stripes among the non-primes. Watching those gaps is fun. Width 15 has a fun checkerboard pattern. When we zoom way out on those patterns, some of what we see is aliasing caused by how the numbers' text is rendered, rather than real aliasing of the cross-out patterns. We want to try different ways of rendering to see if we can capture the real aliasing (moiré) effects, which might be interesting.
- **Question:** The primorial grows very quickly: the product of the primes up to p is roughly e^p. How does that compare with the next-prime square, which grows only like p², and with the prime-counting function π(x), which grows like x / ln x? Can the tool show these different rates? For example, how much of one primorial-wide repeat of the pattern lies below the next-prime square, where every unstruck number is guaranteed to be prime?
- **Question:** Can the Mersenne primes, or other special kinds of primes, be shown in any special way on these plots?

## A Nod to Legacy
This was the first message we got when we pushed code into this repository. Enjoy it, because I have no idea whatsoever why it would print this!!

‣牐浩彥畎扭牥偟慲瑣捩੥

\- "The vast and boundless universe"

(Mystery solved later: it is the README's original first line, `# Prime_Number_Practice`, read as UTF-16 text instead of plain ASCII.)
