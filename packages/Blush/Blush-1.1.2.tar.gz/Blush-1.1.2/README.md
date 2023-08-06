# Blush

A simple parallel wrapper for embarrassingly parallel method calls.

This package simplifies the process of instantiating a pool and sending computations to it.

## Quickstart

```python
from blush import parallelise, unpack_results

# Define your function.
def myfunc(arg1, arg2):
    return arg1 * arg2

# Set up some configuration
num_threads = 4
method = 'imap_unordered'
arg1 = 2 # Scalar arguments will be duplicated between processes
arg2 = [1,2,3,4,5] # All iterable arguments must be of the same length, each process will get one.

# Parallelise the function call, results are an iterator.
iresults = parallelise(
    myfunc,
    num_threads=num_cores,
    method=method,
    arg1=arg1, arg2=arg2
)

# Results will be unpacked as they finish computation.
# Now you can do something with them.
results = unpack_results(uresults)
```

## Why?

I've lost count at the number of times I've built this functionality, so here is a package so that I never need to do it again.

## Why would you use Blush instead of something like Dask?

Good question:

1. The thing you are trying to do doesn't fit into the "dask way" of doing things.
2. You don't want the overhead of a bigger library.
3. You want a quick-and-dirty parallel wrapper to parallelise your code.
4. You enjoy a python package with good word-play that doesn't take itself too seriously.