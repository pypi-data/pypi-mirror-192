"""Functions for parallel execution."""
import multiprocessing as mp
import pandas as pd
from tqdm import tqdm
from importlib_metadata import version as _version

# Constants
MAX_CORES = mp.cpu_count()


__version__ = _version('blush')


def _parallel_wrap(mp_args):
    """Wrapper around the function.
    
    Args: 
        mp_args (list) : Arguments of the form [func, dict]
    
    Returns:
        mixed : The return value of func(**dict)
    """
    return mp_args[0](**mp_args[1])


def convert_kwargs(**kwargs):
    """Convert a series of kwargs into arguments suitable for multiprocessing.

    Returns:
        list: List of dictionaries of arguments.
    """
    return pd.DataFrame(kwargs).to_dict('records')


def parallelise(func, num_threads=MAX_CORES, method='imap_unordered', progress=True, **kwargs):
    """Parallelise computation of `func`, supplied with `kwargs`.
    
    Args:
        func (callable) : Function
        num_threads (int) : Number of processes (Default=MAX_CORES)
        method (str) : Pool method to use (Default='imap_unordered')
        **kwargs : Keyword arguments to be passed `func`
    
    Returns:
        multiprocessing.pool.IMapUnorderedIterator : Results
    """
    # Convert the kwargs to argument list of dicts
    mp_args = convert_kwargs(**kwargs)

    # Attach the function pointer as the first argument
    mp_args = [[func, mp_arg] for mp_arg in mp_args]

    # Build a pool, get the function
    pool = mp.Pool(processes=num_threads)
    mp_func = getattr(pool, method)

    iterable = enumerate(mp_func(_parallel_wrap, mp_args))

    # Attach progressbar if requested
    if progress:
        iterable = tqdm(iterable, total=len(mp_args))

    # Start processing
    results = []
    for _, result in iterable:
        results.append(result)

    pool.close()
    pool.join()

    return results


def unpack_results(results):
    """Unpack results from the parallel computation.
    
    Args:
        results (multiprocessing.pool.IMapUnorderedIterator) : Results from `parallelise`
    
    Returns:
        list : List of result objects
    """
    return [result for result in results]


# For our American friends...
parallelize = parallelise