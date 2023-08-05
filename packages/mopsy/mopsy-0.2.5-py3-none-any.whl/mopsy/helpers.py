from statistics import mean, median
from .utils import get_matrix_type

from typing import Sequence, Union, Callable, Any
import numpy
import scipy

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def colsum(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply colsum

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(sum, mat, group=group, axis=1, non_zero=non_zero)


def rowsum(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply rowsum

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(sum, mat, group=group, axis=0, non_zero=non_zero)


def colmean(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply colmean

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(mean, mat, group=group, axis=1, non_zero=non_zero)


def rowmean(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply rowmean

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(mean, mat, group=group, axis=0, non_zero=non_zero)


def colmedian(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply colmedian

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(median, mat, group=group, axis=1, non_zero=non_zero)


def rowmedian(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply rowmedian

    Args:
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    return apply(median, mat, group=group, axis=0, non_zero=non_zero)


def apply(
    func: Callable[[list], Any],
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    axis: int,
    group: Sequence = None,
    non_zero: bool = False,
):
    """A generic apply function

    Args:
        func (Callable): function to be called.
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        axis (int): 0 for rows, 1 for columns.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    tmat = get_matrix_type(mat, non_zero=non_zero)
    return tmat.apply(func, group=group, axis=axis)


def multi_apply(
    funcs: Sequence[Callable[[list], Any]],
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    axis: int,
    group: Sequence = None,
    non_zero: bool = False,
):
    """Apply multiple functions, the first axis
        of the ndarray specifies the results of the inputs functions in
        the same order

    Args:
        funcs (Sequence[Callable[[list], Any]]): functions to be called.
        mat (Union[numpy.ndarray, scipy.sparse.spmatrix]): matrix
        group (Sequence, optional): group variable. Defaults to None.
        axis (int): 0 for rows, 1 for columns.
        non_zero (bool): filter zero values ?

    Returns:
        numpy.ndarray: matrix
    """
    tmat = get_matrix_type(mat, non_zero=non_zero)
    return tmat.multi_apply(funcs, group=group, axis=axis)
