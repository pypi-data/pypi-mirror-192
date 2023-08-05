from numba import njit
import numpy as np
import pandas as pd
from . import bootstrap
try:
    import statsmodels.stats.api as sms
except:
    pass

def t_interval(x, alpha=0.05, alternative="two-sided"):
    return sms.DescrStatsW(x).tconfint_mean(alpha=alpha, alternative=alternative)

@njit
def compute_coverage(CI, data, stat, N, seed=0, num_iters=1000):
    low, high = CI
    estimates = bootstrap.resample_nb(data, stat, R=num_iters, N=N, seed=seed)[:, 0]
    low_fails = (estimates < low).mean()
    high_fails = (estimates > high).mean()
    coverage = 1 - (low_fails + high_fails)
    return np.array([low_fails, high_fails, coverage])

def coverage(*args, num_N=20, **kwargs):
    Ns = np.unique(np.linspace(2, args[1].shape[0], num_N, dtype=int))
    covg_data = np.vstack([compute_coverage(*args, N=N, **kwargs) for N in Ns]).T # shape: (3, num_N).  3: low_fails, high_fails, coverage
    return Ns, covg_data

def CI_specs(CIs, data, stat, coverage_iters=int(1e4), seed=42, avg_len=3):
    CI_arr = CIs.values
    coverages = np.stack([coverage(CI, data, stat, num_iters=coverage_iters, seed=seed)[1] for CI in CI_arr], axis=1) # shape: (3, #CI, num_N)
    low_fails_last, high_fails_last, coverages_last = coverages[:, :, -1]
    low_fails_avg, high_fails_avg, coverages_avg = coverages[:, :, -avg_len:].mean(axis=-1)
    spread = np.hstack([np.diff(CI) for CI in CI_arr])
    CIs2 = CIs.copy()
    CIs2['width'] = spread
    env = locals()
    for k in ['low_fails', 'high_fails', 'coverages']:
        for end in ['avg', 'last']:
            key = f"{k}_{end}"
            CIs2[key.replace("_", "-")] = env[key]
    return CIs2

def find_best(CIs, data=None, stat=None, alpha=0.05, alpha_margin_last=0.01, alpha_margin_avg=0.02):
    alpha_expanded_last = alpha + alpha_margin_last
    alpha_expanded_avg = alpha + alpha_margin_avg
    if 'coverage-last' in CIs.columns:
        coverages_last, coverages_avg, spread = CIs[['coverage-last', 'coverage-3-avg', 'width']].values.T
    else:
        CI_arr = CIs.values
        coverages = np.vstack([coverage(CI, data, stat)[1] for CI in CI_arr]).T
        coverages_avg = coverages[:-3].mean(axis=0)
        coverages_last = coverages[-1]
        spread = np.hstack([np.diff(CI) for CI in CI_arr])
    valid = np.unique(np.hstack([np.where(coverages_last >= (1-alpha_expanded_last))[0],
                                 np.where(coverages_avg >= (1-alpha_expanded_avg))[0],
                                 np.abs(coverages_last - (1-alpha)).argmin()]))
    min_spread = spread[valid].argmin()
    return CIs.iloc[valid].iloc[min_spread]
