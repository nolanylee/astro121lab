import ugradio
import numpy as np
import pandas as pd
import time

ifm = ugradio.interf.Interferometer()
hpm = ugradio.hp_multi.HP_Multimeter()

def altaz_point(ra, dec):

    precess_ra, precess_dec = ugradio.coord.precess(ra, dec)
    alt, az = ugradio.coord.get_altaz(precess_ra, precess_dec)

    return alt, az

def initialize(ra, dec, dt):

    alt, az = altaz_point(ra, dec)
    ifm.point(alt, az)
    hpm.start_recording(dt)

def terminate(title):
    
    hpm.end_recording()
    voltages, times = hpm.get_recording_data()
    df = pd.DataFrame({'Voltages': voltages, 'Times': times})
    df.to_csv('./'+title+'.csv')
    ifm.stow()
    
def observe(ra, dec, steps, dt, title):

    print('Initializing observation...')
    initialize(ra, dec, dt)

    for i in range(steps):
        alt, az = altaz_point(ra, dec)
        print(f'Repositioning to coordinates {alt, az}')
        try:
            ifm.point(alt, az)
        except AssertionError as e:
            print(e)
            print('YOU FOOL: script errored out at {i=}')
            break
        time.sleep(dt)

    print('Terminating observation')
    terminate(title)
  
def f_transform(data):
    
    fourier = np.fft.fft(data)
    fourier_freq = np.fft.fftfreq(len(data), 1/(10.7))
    fourier_shift = np.fft.fftshift(fourier)
    fourier_freq_shift = np.fft.fftshift(fourier_freq)
    power_spectrum = np.abs(fourier_shift)**2
    
    return fourier_freq_shift, power_spectrum

