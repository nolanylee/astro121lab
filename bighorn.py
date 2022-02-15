import ugradio
import numpy as np

def gather_data(local_o=1419.4e6, nsamples=2048, sample_rate=2.2e6):
    data = ugradio.sdr.capture_data_mixer(local_o, 
        nsamples,
        sample_rate)
    fourier = np.fft.fft(data)
    fourier_freq = np.fft.fftfreq(nsamples, 1/sample_rate)
    fourier_shift = np.fft.fftshift(fourier)
    fourier_freq_shift = np.fft.fftshift(fourier_freq)
    return fourier_freq_shift, np.abs(fourier_shift)**2 

def gather_blocks(nblocks, local_o=1419.4e6, nsamples=2048, sample_rate=2.2e6):
    data_blocks = np.empty((nblocks, nsamples))
    for i in range(nblocks):
        data = gather_data(local_o, nsamples, sample_rate)
        data_blocks[i] = data[1]
    return data[0], data_blocks
        
