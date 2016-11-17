"""Define the base Matrix class."""
from __future__ import division, print_function
import numpy


class Matrix(object):
    """Base matrix class.

    This class is used for global Jacobians.

    Attributes
    ----------
    _comm : MPI.Comm or FakeComm
        communicator of the top-level system that owns the Jacobian.
    _matrix : object
        implementation-specific representation of the actual matrix.
    _op_submats : dict
        dictionary of sub-jacobian data keyed by (op_ind, ip_ind).
    _ip_submats : dict
        dictionary of sub-jacobian data keyed by (op_ind, ip_ind).
    _op_metadata : dict
        implementation-specific data for the sub-jacobians.
    _ip_metadata : dict
        implementation-specific data for the sub-jacobians.
    """

    def __init__(self, comm):
        """Initialize all attributes.

        Args
        ----
        comm : MPI.Comm or FakeComm
            communicator of the top-level system that owns the Jacobian.
        """
        self._comm = comm
        self._matrix = None
        self._op_submats = {}
        self._ip_submats = {}
        self._op_metadata = {}
        self._ip_metadata = {}

    def prod_fwd(self, in_vec, row_range=None):
        """Perform a forward product.

        Args
        ----
        in_vec : ndarray[:]
            incoming vector to multiply.
        row_range : [int, int] or None
            the row index range for which to compute the product.

        Returns
        -------
        out_vec : ndarray[:]
            vector resulting from the product.
        """
        out_vec = self._prod(in_vec, 'fwd')
        if row_range is None:
            return out_vec
        else:
            return out_vec[row_range[0]:row_range[1]]

    def prod_rev(self, in_vec, row_range=None):
        """Perform a reverse product.

        Args
        ----
        in_vec : ndarray[:]
            incoming vector to multiply.
        row_range : [int, int] or None
            the row index range with which to compute the product.

        Returns
        -------
        out_vec : ndarray[:]
            vector resulting from the product.
        """
        if row_range is not None:
            in_vec = numpy.array(in_vec)
            in_vec[:row_range[0]] = 0.
            in_vec[row_range[1]:] = 0.

        out_vec = self._prod(in_vec, 'rev')
        return out_vec

    def _op_add_submat(self, key, jac, irow=0, icol=0):
        """Declare a sub-jacobian.

        Args
        ----
        key : (int, int)
            the global output and input variable indices.
        jac : ndarray or scipy.sparse or tuple
            the sub-jacobian.
        irow : int
            the starting row index (offset) for this sub-jacobian.
        icol : int
            the starting col index (offset) for this sub-jacobian.
        """
        self._op_submats[key] = (jac, irow, icol)

    def _ip_add_submat(self, key, jac, irow=0, icol=0):
        """Declare a sub-jacobian.

        Args
        ----
        key : (int, int)
            the global output and input variable indices.
        jac : ndarray or scipy.sparse or tuple
            the sub-jacobian.
        irow : int
            the starting row index (offset) for this sub-jacobian.
        icol : int
            the starting col index (offset) for this sub-jacobian.
        """
        self._ip_submats[key] = (jac, irow, icol)

    def _op_update_submat(self, key, jac):
        """Update the values of a sub-jacobian.

        Args
        ----
        key : (int, int)
            the global output and input variable indices.
        jac : ndarray or scipy.sparse or tuple
            the sub-jacobian, the same format with which it was declared.
        """
        self._update_submat(self._op_submats, self._op_metadata, key, jac)

    def _ip_update_submat(self, key, jac):
        """Update the values of a sub-jacobian.

        Args
        ----
        key : (int, int)
            the global output and input variable indices.
        jac : ndarray or scipy.sparse or tuple
            the sub-jacobian, the same format with which it was declared.
        """
        self._update_submat(self._ip_submats, self._ip_metadata, key, jac)

    def _update_submat(self, submats, metadata, key, jac):
        """Update the values of a sub-jacobian.

        Args
        ----
        submats : dict
            dictionary of sub-jacobian data keyed by (op_ind, ip_ind).
        metadata : dict
            implementation-specific data for the sub-jacobians.
        key : (int, int)
            the global output and input variable indices.
        jac : ndarray or scipy.sparse or tuple
            the sub-jacobian, the same format with which it was declared.
        """
        pass

    def _build(self, num_rows, num_cols):
        """Allocate the matrix.

        Args
        ----
        num_rows : int
            number of rows in the matrix.
        num_cols : int
            number of cols in the matrix.
        """
        pass

    def _prod(self, vec, mode):
        """Perform a matrix vector product.

        Args
        ----
        vec : ndarray[:]
            incoming vector to multiply.
        mode : str
            'fwd' or 'rev'.

        Returns
        -------
        ndarray[:]
            vector resulting from the product.
        """
        pass
