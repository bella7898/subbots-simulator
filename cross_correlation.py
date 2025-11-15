import global_vars
import numpy as np
from scipy.signal import correlate, resample_poly

#INPUTS
#signal: list (size n) of np arrays: represents hydrophone data

#OUTPUTS
#phase_differences: list (size n-1) of floats: representing phase differences between the hydrophone signals

def cross_correlation_stage(signals):
    # number of components
    num_components = len(global_vars.hydrophone_positions) - 1

    phase_analysis_inputs = [
            (signals[0], signals[i+1])
            for i in range(num_components)
    ]

    phase_differences = [
        calc_cross_correlation(pair)
        for pair in phase_analysis_inputs
    ]

    return phase_differences

#INPUTS: 
#signal_pair: list of two np arrays: represents two hydrophone signals

#OUTPUTS: 
#phase_difference: float: represents the phase difference between two hydrophone signals

def calc_cross_correlation(signal_pair, sampling_frequency, signal_frequency):
    # compute cross correlation
    h0_sig, h_sig = signal_pair

    # find discrete signal frequency
    f = signal_frequency / sampling_frequency
    
    # find number of samples per signal period
    N = int(np.ceil(1/f))

    # find and compare center index from signals
    center_index1 = int(len(h0_sig)/2)
    center_index2 = int(len(h_sig)/2)

    if(center_index1 != center_index2):
        raise Exception("Error: Signals are not the same size!")
    
    #we can define a window size for doign our cross correlation sweep, our only requirment is that the 
    #first array be one period larger than the second to allow for a full period of angle sweep
    #window can be made larger if signal sizes allow for better averaging
    window = 100*N

    # extract a section of the signals - one of them should be longer for cross
    # correlation to work to avoid edge effects
    long_signal = h0_sig[center_index1 - int(window/2) : center_index1 + int(window/2+N)]
    short_signal = h_sig[center_index1 - int(window/2) : center_index1 + int(window/2)]

    # valid mode doesn't pad out edges
    cross_correlation = correlate(long_signal, short_signal, mode='valid')

    maxima_idx = np.argmax(cross_correlation)

    phase_shift = maxima_idx * 360 * f
    print(phase_shift)

    return phase_shift;