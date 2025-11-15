import pytest
import numpy as np
import builtins

import cross_correlation as cc

def test_calc_cross_correlation_known_phase():
    fs = 100000
    f = 1000
    t = np.arange(0, 1, 1/fs)
    phase_shift = np.pi / 2 +1 # 90 degrees

    sig1 = np.sin(2*np.pi*f*t)
    sig2 = np.sin(2*np.pi*f*t + phase_shift)

    phase_diff = cc.calc_cross_correlation((sig1, sig2), fs, f)
    print(phase_diff)
    # Should roughly equal the true phase shift (mod 2π)
    assert np.isclose(phase_diff, phase_shift * 360/(2*np.pi), atol=1.8)
"""
def test_phase_sign_reversal():
    fs = 10000
    f = 1000
    t = np.arange(0, 1, 1/fs)
    shift = np.pi / 3
    sig1 = np.sin(2*np.pi*f*t)
    sig2 = np.sin(2*np.pi*f*t + shift)

    pd1 = cc.calc_cross_correlation((sig1, sig2))
    pd2 = cc.calc_cross_correlation((sig2, sig1))

    assert np.isclose(pd1, pd2, atol=0.1)

def test_identical_signals_zero_phase():
    fs = 10000
    f = 1000
    t = np.arange(0, 1, 1/fs)
    sig = np.sin(2*np.pi*f*t)

    phase_diff = cc.calc_cross_correlation((sig, sig))
    assert abs(phase_diff) < 1e-5
"""