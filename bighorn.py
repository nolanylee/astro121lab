import ugradio
import numpy as np
import pandas as pd

def gather_data(local_o=1420e6, nsamples=2048, nblocks=1000, sample_rate=2.2e6, gain=1.0):
    
    """
    takes a digitally sampled signal via software defined radio (SDR) and
    returns the components needed to plot a power spectrum
    
    Arguments:
    -----------
    local_o : float
        frequency of our local oscillator
    nsamples : int
        number of samples in a given set of data
    nblocks : int
        number of blocks of data to be taken
    sample_rate : float
        sampling rate of the SDR
    gain : float
        applied gain to the sampled signal
    
    Returns: 
    ---------
    fourier_freq_shift : array
        power spectrum frequencies of units Hz (x-axis)
    power_spectrum : array
        power spectrum amplitudes of arbitrary units (y-axis)
        averaged over the total number of blocks taken
    """
    
    data = ugradio.sdr.capture_data(direct=False,
        center_freq=local_o, 
        nsamples=nsamples,
        nblocks=nblocks,
        sample_rate=sample_rate,
        gain=gain)
    fourier = np.fft.fft(data)
    fourier_freq = np.fft.fftfreq(nsamples, 1/sample_rate)
    fourier_shift = np.fft.fftshift(fourier)
    fourier_freq_shift = np.fft.fftshift(fourier_freq)
    power_spectrum = np.mean(np.abs(fourier_shift)**2, axis=0)
    return fourier_freq_shift, power_spectrum



def data2csv(title, data):
    
    """
    generates a data frame from the captured SDR data and saves it as a csv
    
    Arguments:
    -----------
    title : string
        title of the saved csv
    data : tuple
        captured SDR data, the indices of which will serve as columns
    
    Returns: 
    ---------
    title.csv : 
        saved data frame of the captured data in csv format (see astro121lab file)
    """
    
    df = pd.DataFrame({'f': data[0], 'a': data[1]})
    return df.to_csv('/home/pi/astro121lab/'+title+'.csv')


def S_line(s_cal, s_cold):
    
    """
    removes the instrumental bandpass by taking the ratio b/n s_cal and s_cold
    
    Arguments:
    -----------
    s_cal : array
        calibrated data taken in the presence of an ideal blackbody (cole)
    s_cold : array
        data taken when pointed at the cold sky
    
    Returns: 
    ---------
    s_line : array
        the shape of our spectral line (not the intensity)
    """
    
    s_line = s_cold / s_cal
    return s_line



def gain(T_cal=300, s_cal, s_cold):
    
    """
    generates a data frame from the captured SDR data and saves it as a csv
    
    Arguments:
    -----------
    T_cal : float
        calibration temperature ie the thermal power injected into the telescope
        by an ideal blackbody
    s_cal : array
        calibrated data taken in the presence of an ideal blackbody
    s_cold : array
        data taken when pointed at the cold sky
    
    Returns: 
    ---------
    g : float
        the gain of our spectrum
    """
    
    sum_cold = sum(s_cold)
    sum_diff = sum(s_cal-s_cold)
    g = T_cal/sum_diff*sum_cold
    return g



def T_line(T_cal, s_cold, s_cold):
    
    """
    calculates the intensity calibrated spectrum T_line
    
    Arguments:
    -----------
    T_cal : float
        calibration temperature ie the thermal power injected into the telescope
        by an ideal blackbody
    s_cal : array
        calibrated data taken in the presence of an ideal blackbody
    s_cold : array
        data taken when pointed at the cold sky
    
    Returns: 
    ---------
    t_line : array
        the final intensity calibrated spectrum
    """
    
    s_line = bighorn.S_line(s_cal, s_cold)
    gain = bighorn.gain(T_cal, s_cal, s_cold)
    t_line = s_line*gain
    return t_line