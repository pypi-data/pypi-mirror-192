from .sops import Sops
from .checkutils import check_axis

from typing import Union

import scipy as sp
import numpy as np

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def append_row(
    mat: sp.sparse.spmatrix, row: Union[sp.sparse.spmatrix, np.ndarray]
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices

    Args:
        mat (scipy.sparse.spmatrix): sparse matrix
        row (Union[sp.sparse.spmatrix, np.ndarray]): rows to append

    Raises:
        TypeError: if axis is neither 0 nor 1

    Returns:
        scipy.sparse.spmatrix: new matrix
    """
    return sparse_append(mat=mat, rowOrCols=row, axis=0)


def append_col(
    mat: sp.sparse.spmatrix, col: Union[sp.sparse.spmatrix, np.ndarray]
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices

    Args:
        mat (scipy.sparse.spmatrix): sparse matrix
        col (Union[sp.sparse.spmatrix, np.ndarray]): columns to append

    Raises:
        TypeError: if axis is neither 0 nor 1

    Returns:
        scipy.sparse.spmatrix: new matrix
    """
    return sparse_append(mat=mat, rowOrCols=col, axis=1)


def sparse_append(
    mat: sp.sparse.spmatrix,
    rowOrCols: Union[sp.sparse.spmatrix, np.ndarray],
    axis: Union[int, bool],
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices

    Args:
        mat (scipy.sparse.spmatrix): sparse matrix
        rowOrCols (Union[sp.sparse.spmatrix, np.ndarray]): rows to append
        axis (Union[int, bool]): 0 for rows, 1 for columns.

    Raises:
        TypeError: if axis is neither 0 nor 1

    Returns:
        scipy.sparse.spmatrix: new matrix
    """

    if not isinstance(mat, sp.sparse.spmatrix):
        raise TypeError(f"mat is not a sparse matrix. provided {type(mat)}")

    check_axis(axis)

    original_sparse_type = Sops.identify_sparse_type(mat)

    new_mat = None
    if axis == 0:
        if mat.shape[0] != rowOrCols.shape[0]:
            raise TypeError(
                f"matrix and new row do not have the same length. matrix: {mat.shape[0]}, row: {row.shape[0]}"
            )

        new_mat = sp.sparse.vstack([mat, rowOrCols])
    else:
        if mat.shape[1] != rowOrCols.shape[0]:
            raise TypeError(
                f"matrix and new row do not have the same length. matrix: {mat.shape[1]}, row: {row.shape[1]}"
            )

        new_mat = sp.sparse.hstack([mat, rowOrCols])

    if new_mat is None:
        raise Exception("This should never happen")

    cmat = Sops.convert_sparse_type(new_mat, original_sparse_type)
    return cmat
