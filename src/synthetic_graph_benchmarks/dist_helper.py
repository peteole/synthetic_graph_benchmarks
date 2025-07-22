###############################################################################
#
# Adapted from https://github.com/lrjconan/GRAN/ which in turn is adapted from https://github.com/JiaxuanYou/graph-generation
#
###############################################################################
import numpy as np
import concurrent.futures
from functools import partial
from scipy.linalg import toeplitz
from scipy.stats import wasserstein_distance
from scipy.optimize import linprog


def _compute_emd_with_distance_matrix(x, y, distance_mat):
    """
    Compute EMD using linear programming when a custom distance matrix is provided.
    This is equivalent to pyemd.emd but implemented using scipy.
    """
    x = x.astype(float)
    y = y.astype(float)

    # Ensure distributions are normalized
    if np.sum(x) > 0:
        x = x / np.sum(x)
    if np.sum(y) > 0:
        y = y / np.sum(y)

    n = len(x)
    m = len(y)

    # Create the cost vector (flattened distance matrix)
    c = distance_mat[:n, :m].flatten()

    # Create equality constraints for supply (sum over columns = x[i])
    A_eq_supply = np.zeros((n, n * m))
    for i in range(n):
        for j in range(m):
            A_eq_supply[i, i * m + j] = 1
    b_eq_supply = x

    # Create equality constraints for demand (sum over rows = y[j])
    A_eq_demand = np.zeros((m, n * m))
    for j in range(m):
        for i in range(n):
            A_eq_demand[j, i * m + j] = 1
    b_eq_demand = y

    # Combine constraints
    A_eq = np.vstack([A_eq_supply, A_eq_demand])
    b_eq = np.hstack([b_eq_supply, b_eq_demand])

    # Bounds: all variables >= 0
    bounds = [(0, None) for _ in range(n * m)]

    # Solve the linear program
    try:
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if result.success:
            return result.fun
        else:
            # Fallback to simpler Wasserstein distance
            return wasserstein_distance(np.arange(n), np.arange(m), x, y)
    except Exception:
        # Fallback to simpler Wasserstein distance
        return wasserstein_distance(np.arange(n), np.arange(m), x, y)


def emd(x, y, distance_scaling=1.0):
    support_size = max(len(x), len(y))
    d_mat = toeplitz(range(support_size)).astype(float)
    distance_mat = d_mat / distance_scaling

    # convert histogram values x and y to float, and make them equal len
    x = x.astype(float)
    y = y.astype(float)
    if len(x) < len(y):
        x = np.hstack((x, [0.0] * (support_size - len(x))))
    elif len(y) < len(x):
        y = np.hstack((y, [0.0] * (support_size - len(y))))

    emd_result = _compute_emd_with_distance_matrix(x, y, distance_mat)
    return emd_result


def l2(x, y):
    dist = np.linalg.norm(x - y, 2)
    return dist


def emd_with_sigma(x, y, sigma=1.0, distance_scaling=1.0):
    """EMD
    Args:
        x, y: 1D pmf of two distributions with the same support
        sigma: standard deviation
    """
    support_size = max(len(x), len(y))
    d_mat = toeplitz(range(support_size)).astype(float)
    distance_mat = d_mat / distance_scaling

    # convert histogram values x and y to float, and make them equal len
    x = x.astype(float)
    y = y.astype(float)
    if len(x) < len(y):
        x = np.hstack((x, [0.0] * (support_size - len(x))))
    elif len(y) < len(x):
        y = np.hstack((y, [0.0] * (support_size - len(y))))

    return np.abs(_compute_emd_with_distance_matrix(x, y, distance_mat))


def gaussian_emd(x, y, sigma=1.0, distance_scaling=1.0):
    """Gaussian kernel with squared distance in exponential term replaced by EMD
    Args:
        x, y: 1D pmf of two distributions with the same support
        sigma: standard deviation
    """
    support_size = max(len(x), len(y))
    d_mat = toeplitz(range(support_size)).astype(float)
    distance_mat = d_mat / distance_scaling

    # convert histogram values x and y to float, and make them equal len
    x = x.astype(float)
    y = y.astype(float)
    if len(x) < len(y):
        x = np.hstack((x, [0.0] * (support_size - len(x))))
    elif len(y) < len(x):
        y = np.hstack((y, [0.0] * (support_size - len(y))))

    emd_result = _compute_emd_with_distance_matrix(x, y, distance_mat)
    return np.exp(-emd_result * emd_result / (2 * sigma * sigma))


def gaussian(x, y, sigma=1.0):
    support_size = max(len(x), len(y))
    # convert histogram values x and y to float, and make them equal len
    x = x.astype(float)
    y = y.astype(float)
    if len(x) < len(y):
        x = np.hstack((x, [0.0] * (support_size - len(x))))
    elif len(y) < len(x):
        y = np.hstack((y, [0.0] * (support_size - len(y))))

    dist = np.linalg.norm(x - y, 2)
    return np.exp(-dist * dist / (2 * sigma * sigma))


def gaussian_tv(x, y, sigma=1.0):
    support_size = max(len(x), len(y))
    # convert histogram values x and y to float, and make them equal len
    x = x.astype(float)
    y = y.astype(float)
    if len(x) < len(y):
        x = np.hstack((x, [0.0] * (support_size - len(x))))
    elif len(y) < len(x):
        y = np.hstack((y, [0.0] * (support_size - len(y))))

    dist = np.abs(x - y).sum() / 2.0
    return np.exp(-dist * dist / (2 * sigma * sigma))


def kernel_parallel_unpacked(x, samples2, kernel):
    d = 0
    for s2 in samples2:
        d += kernel(x, s2)
    return d


def kernel_parallel_worker(t):
    return kernel_parallel_unpacked(*t)


def disc(samples1, samples2, kernel, is_parallel=True, *args, **kwargs):
    """Discrepancy between 2 samples"""
    d = 0

    if not is_parallel:
        for s1 in samples1:
            for s2 in samples2:
                d += kernel(s1, s2, *args, **kwargs)
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for dist in executor.map(
                kernel_parallel_worker,
                [(s1, samples2, partial(kernel, *args, **kwargs)) for s1 in samples1],
            ):
                d += dist
    if len(samples1) * len(samples2) > 0:
        d /= len(samples1) * len(samples2)
    else:
        d = 1e6
    return d


def compute_mmd(samples1, samples2, kernel, is_hist=True, *args, **kwargs):
    """MMD between two samples"""
    # normalize histograms into pmf
    if is_hist:
        samples1 = [s1 / (np.sum(s1) + 1e-6) for s1 in samples1]
        samples2 = [s2 / (np.sum(s2) + 1e-6) for s2 in samples2]
    mmd = (
        disc(samples1, samples1, kernel, *args, **kwargs)
        + disc(samples2, samples2, kernel, *args, **kwargs)
        - 2 * disc(samples1, samples2, kernel, *args, **kwargs)
    )

    mmd = np.abs(mmd)

    if mmd < 0:
        import pdb

        pdb.set_trace()

    return mmd


def compute_emd(samples1, samples2, kernel, is_hist=True, *args, **kwargs):
    """EMD between average of two samples"""
    # normalize histograms into pmf
    if is_hist:
        samples1 = [np.mean(samples1)]
        samples2 = [np.mean(samples2)]
    return disc(samples1, samples2, kernel, *args, **kwargs), [samples1[0], samples2[0]]
