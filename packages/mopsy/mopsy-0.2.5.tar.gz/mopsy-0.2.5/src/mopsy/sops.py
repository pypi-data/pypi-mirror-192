from .mops import Mops
from .nops import Nops

from scipy import sparse as sp
import numpy as np
from statistics import mean

from typing import Callable, Any, Iterator, Tuple, Sequence, Optional

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Sops(Mops):
    """Sops, Sparse Matrix Operation Class"""

    def __init__(self, mat: sp.spmatrix, non_zero: bool = False) -> None:
        """Initialize the class from a scipy sparse matrix.

        Args:
            mat (scipy.sparse.spmatrix): a scipy sparse matrix
            non_zero (bool): filter zero values ?
        """
        super().__init__(mat, non_zero=non_zero)

    def iter(self, group: list = None, axis: int = 0) -> Iterator[Tuple]:
        """Iterator over groups and an axis

        Args:
            group (list, optional): group variable. Defaults to None.
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Yields:
            tuple (str, matrix): of group and the submatrix
        """
        mat = self.matrix.tocsr() if axis == 0 else self.matrix.tocsc()
        if group is None:
            yield (group, self)
        else:
            idx_groups = self.groupby_indices(group)
            for k, v in idx_groups.items():
                if axis == 0:
                    yield (
                        k,
                        Sops(mat[v,], self.non_zero,),
                    )
                else:
                    yield (k, Sops(mat[:, v], self.non_zero))

    def _apply(self, func: Callable[[list], Any], axis: int = 0) -> np.ndarray:
        """Apply a function over the matrix

        Args:
            func (Callable): function to apply over row or col wise vectors
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Returns:
            numpy.ndarray: a dense vector
        """
        mat = self.matrix.tocsc() if axis == 0 else self.matrix.tocsr()
        if self.non_zero:
            # reduction along an axis
            fmat = np.zeros(mat.shape[1] if axis == 0 else mat.shape[0])
            for i in range(len(mat.indptr) - 1):
                start_idx = mat.indptr[i]
                end_idx = mat.indptr[i + 1]
                if start_idx == end_idx:
                    fmat[i] = 0
                else:
                    mslice = mat.data[slice(start_idx, end_idx)]
                    fmat[i] = 0 if len(mslice) == 0 else func(mslice)

            return fmat if axis == 0 else fmat.T
        else:
            if func in [sum, mean, min, max]:
                if func == sum:
                    mat = mat.sum(axis=axis)
                elif func == mean:
                    mat = mat.mean(axis=axis)
                elif func == min:
                    mat = mat.min(axis=axis).todense()
                elif func == max:
                    mat = mat.max(axis=axis).todense()

                # flatten
                tmat = mat.getA1()
                return tmat if axis == 0 else tmat.T
            else:
                dense_mat = Nops(self.matrix.toarray(), self.non_zero)
                return dense_mat._apply(func, axis)

    def apply(
        self,
        func: Callable[[list], Any],
        group: Sequence = None,
        axis: int = 0,
    ) -> Tuple[np.ndarray, Optional[Sequence]]:
        """Apply a function to groups along an axis

        Args:
            func (Callable): a function to apply
            group (list, optional): group variable. Defaults to None.
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Raises:
            Exception: ApplyFuncError, when a function cannot be applied

        Returns:
            Tuple[np.ndarray, Optional[Sequence]]: a tuple of matrix and its labels
        """
        original_sparse_type = self.identify_sparse_type()
        mat, groups = super().apply(func, group, axis)

        cmat = self.convert_sparse_type(mat, original_sparse_type)

        return cmat, groups

    def multi_apply(
        self,
        funcs: Sequence[Callable[[list], Any]],
        group: list = None,
        axis: int = 0,
    ) -> Tuple[np.ndarray, Optional[Sequence]]:
        """Apply multiple functions, the first axis
        of the ndarray specifies the results of the inputs functions in
        the same order

        Args:
            funcs (List[Callable[[list], Any]]): functions to be called.
            group (list, optional): group variable. Defaults to None.
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Raises:
            Exception: ApplyFuncError, when a function cannot be applied

        Returns:
            Tuple[np.ndarray, Optional[Sequence]]: a tuple of matrix and its labels
        """
        original_sparse_type = self.identify_sparse_type()
        mats, groups = super().multi_apply(funcs, group, axis)
        cmats = [
            self.convert_sparse_type(m, original_sparse_type) for m in mats
        ]

        return cmats, groups

    def identify_sparse_type(self):
        """Identify the sparse matrix format

        Raises:
            TypeError: matrix is not sparse

        Returns:
            an internal matrix representation object
        """
        if not isinstance(self.matrix, sp.spmatrix):
            raise TypeError(
                f"mat is not a sparse representation, it is {type(self.matrix)}"
            )

        if sp.isspmatrix_csc(self.matrix):
            return "csc"
        elif sp.isspmatrix_csr(self.matrix):
            return "csr"
        elif sp.isspmatrix_bsr(self.matrix):
            return "bsr"
        elif sp.isspmatrix_coo(self.matrix):
            return "coo"
        elif sp.isspmatrix_dia(self.matrix):
            return "dia"
        elif sp.isspmatrix_dok(self.matrix):
            return "dok"
        elif sp.isspmatrix_lil(self.matrix):
            return "lil"

    def convert_sparse_type(self, mat: sp.spmatrix, format: str):
        """Convert to a sparse matrix format

        Args:
            mat (scipy.sparse.spmatrix): a numpy or scipy matrix
            format (str): sparse matrix format, one of `identify_sparse_type()`

        Raises:
            TypeError: matrix is not sparse

        Returns:
            an internal matrix representation object
        """
        if not isinstance(mat, np.ndarray):
            raise TypeError(
                f"mat is not a sparse representation, it is {type(mat)}"
            )

        if format == "csc":
            return sp.csc_matrix(mat)
        elif format == "csr":
            return sp.csr_matrix(mat)
        elif format == "bsr":
            return sp.bsr_matrix(mat)
        elif format == "coo":
            return sp.coo_matrix(mat)
        elif format == "dia":
            return sp.dia_matrix(mat)
        elif format == "dok":
            return sp.dok_matrix(mat)
        elif format == "lil":
            return sp.lil_matrix(mat)
