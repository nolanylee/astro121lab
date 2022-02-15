import ugradio
import numpy as np

def gather_data(local_o=1419.4e6, nsamples=2048, sample_rate=2.2e6, gain=1.0):
    data = ugradio.sdr.capture_data_mixer(local_o, 
        nsamples,
        sample_rate,
        gain)
    fourier = np.fft.fft(data)
    fourier_freq = np.fft.fftfreq(nsamples, 1/sample_rate)
    fourier_shift = np.fft.fftshift(fourier)
    fourier_freq_shift = np.fft.fftshift(fourier_freq)
    return fourier_freq_shift, np.abs(fourier_shift)**2

    """
    takes a digitally sampled signal via software defined radio (SDR) and
    returns the components needed to plot a power spectrum
    
    Arguments:
    -----------
    local_o : float
        frequency of our local oscillator
    nsamples : int
        number of samples in a given set of data
    sample_rate : float
        sampling rate of the SDR
    gain : float
        applied gain to the sampled signal
    
    Returns: 
    ---------
    fourier_freq_shift : array
        power spectrum frequencies of units Hz (x-axis)
    np.abs(fourier_shift)**2 : array
        power spectrum amplitudes of arbitrary units (y-axis)
    """

def gather_blocks(nblocks, local_o=1419.4e6, nsamples=2048, sample_rate=2.2e6):
    data_blocks = np.empty((nblocks, nsamples))
    for i in range(nblocks):
        data = gather_data(local_o, nsamples, sample_rate)
        data_blocks[i] = data[1]
    return data[0], np.mean(data_blocks)

    """
    repeats the process in gather_data() in order to take the averaged power spectrum 
    over multiple blocks of data
    
    Arguments:
    -----------
    nblocks : int
        number of blocks to be taken
    local_o : float
        frequency of our local oscillator
    nsamples : int
        number of samples in a given set of data
    sample_rate : float
        sampling rate of the SDR
    gain : float
        applied gain to the sampled signal
    
    Returns: 
    ---------
    data[0] : array
        power spectrum frequencies of units Hz (x-axis)
    np.mean(data_blocks) : float
        averaged power spectrum amplitudes of arbitrary units (y-axis)
    """
        
