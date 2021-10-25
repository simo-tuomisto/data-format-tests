% Nordic-RSE : I/O profiling and optimization
% Simo Tuomisto
% 26.10.2021

## Contents of this talk

- What kinds of IO problems occur in HPC environments?
- How do we spot them?
- How can they be solved?

## Disclaimer

- I have worked a lot with I/O problems, but don't take me for an authority on solving them.
  I suggest looking at what big players are doing.
- I/O frameworks move constantly, I might have missed some good frameworks.
  Let me know if you have good suggestions.

## What is common for I/O problems?

- Shared filesystems have to deal with increased load, which can result in various problems
- Jobs execution slows down as CPU/RAM waits for I/O
- They slow down interactive usage

## What kinds of problems are there?

- Most common problems in my opinion (in no particular order):

. . .

1. "ab != ba"-problems

. . .

2. "Jenga"-problems

. . .

3. "I hope I didn't forget anything"-problems

. . .

4. "She'll have the steak"-problems


## "ab != ba"-problem

In many fields of mathematics, all operations do not have the commutative property.

For matrices usually: $$ AB \neq BA $$

. . .

How is this related to I/O?

## "ab != ba"-problem

- From coding perspective, both of these can produce the same results:

```python
for parameter in parameters:
    for datafile in datafiles:
        data = load_data(datafile)
        calculate_model(data, parameter)
```
vs.
```python
for datafile in datafiles:
    for parameter in parameters:
        data = load_data(datafile)
        calculate_model(data, parameter)
```

## "ab != ba"-problem

- From I/O perspective, the code is not commutative:

```python
for parameter in parameters:
    for datafile in datafiles: # <- I/O is multiplied
        data = load_data(datafile)
        calculate_model(data, parameter)
```

## "ab != ba"-problem

- The problem might look trivial, but it is surprisingly hard to spot!
- Usually requires unraveling the whole workflow.
- When working with small data, this might not cause any problems.

## "ab != ba"-problem

- One way of spotting this is with `strace`:
  ```sh
  strace -c -e trace=file ./command
  ```
- If the number of IO operations scales with the number of parameters, something might be amiss.

## "Jenga"-problem

- Closely related to the "ab != ba"-problem.
- First steps do not cause problems, but as time goes on the situation becomes more problematic due to constant I/O.

![Jenga[^1]](https://upload.wikimedia.org/wikipedia/commons/6/6b/Jenga_distorted.jpg?download){ width=150px }

[^1]: [Source: Wikipedia](https://commons.wikimedia.org/w/index.php?curid=17999924)

## "Jenga"-problem

- I/O in machine learning is especially suspect to this problem as data will be iterated over multiple times
- Having a bad I/O pattern doesn't matter for one epoch, but as training can consist of thousands of epochs, the overall result is bad

## "Jenga"-problem

Quick demo:

https://github.com/simo-tuomisto/data-format-tests

## "ab != ba"-problem

- The problem might look trivial, but it is surprisingly hard to spot!
- Usually requires unraveling the whole workflow.
- When working with small data, this might not cause any problems.