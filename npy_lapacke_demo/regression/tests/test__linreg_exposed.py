__doc__ = """Tests for internal _linreg functions.

The internal C extension functions in _linreg are exposed using their
respective Python-accessible wrappers in _linreg_exposed.

.. codeauthor:: Derek Huang <djh458@stern.nyu.edu>
"""

import numpy as np
import pytest

from .. import _linreg_exposed


def test_npy_vector_matrix_mean(default_rng):
    """Test the internal npy_vector_matrix_mean function on model inputs.

    Parameters
    ----------
    default_rng : int
        pytest fixture. See top-level package conftest.py.
    """
    # 1D ndarray to compute the mean for
    ar_1d = default_rng.integers(0, 10, size=50)
    # 2D ndarray to compute the mean for
    ar_2d = default_rng.integers(0, 10, size=(10, 20))
    # check that 1D result is same when using ndarray.mean
    np.testing.assert_allclose(
        _linreg_exposed.npy_vector_matrix_mean(ar_1d), ar_1d.mean()
    )
    # check that the 2D result is the same when using ndarray.mean
    np.testing.assert_allclose(
        _linreg_exposed.npy_vector_matrix_mean(ar_2d), ar_2d.mean(axis=0)
    )
    # check that ValueError is raised when passed higher-dimension ndarray
    with pytest.raises(ValueError, match="ar must be 1D or 2D only"):
        _linreg_exposed.npy_vector_matrix_mean(
            default_rng.random(size=(3, 2, 5))
        )


def test_compute_intercept_single(lr_single):
    """Test the internal compute_intercept function on single-response data.

    Parameters
    ----------
    lr_single : tuple
        pytest fixture. See local conftest.py.
    """
    # get X, y, coefficients, intercept
    X, y, coef_, intercept_, _, _ = lr_single
    # compute row-wise (axis=0) means for X, y
    X_mean = X.mean(axis=0)
    y_mean = y.mean()
    # compute the intercept and check that it is close to the true intercept
    np.testing.assert_allclose(
        _linreg_exposed.compute_intercept(coef_, X_mean, y_mean),
        intercept_, rtol=1e-2
    )


def test_compute_intercept_multi(lr_multi):
    """Test the internal compute_intercept function on multi-response data.

    Parameters
    ----------
    lr_multi : tuple
        pytest fixture. See local conftest.py.
    """
    # get X, y, coefficients, intercept
    X, y, coef_, intercept_, _, _ = lr_multi
    # compute row-wise means for X< y
    X_mean = X.mean(axis=0)
    y_mean = y.mean(axis=0)
    # compute the intercept and check that it is close to the true intercept
    np.testing.assert_allclose(
        _linreg_exposed.compute_intercept(coef_, X_mean, y_mean),
        intercept_, rtol=1e-2
    )