"""Test core functionality."""
from blush import convert_kwargs, unpack_results


def test_convert_kwargs():
    """Test the conversion of kwargs to mp_args."""
    result = convert_kwargs(arg1=True, arg2=['v1', 'v2'])

    assert result[0]['arg1'] == True
    assert result[0]['arg2'] == 'v1'
    assert result[1]['arg1'] == True
    assert result[1]['arg2'] == 'v2'


def test_unpack_results():
    """Test the results iterator."""
    results = [1,2,3,4]
    assert results == unpack_results(results)