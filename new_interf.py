import ugradio
import numpy as np
import pandas as pd
import time

def time2deg(hour, minute, second):

    deg_h = hour*360/24
    deg_m = minute*360/24/60
    deg_s = second*360/24/3600

    return deg_h + deg_m + deg_s

def altaz_point(ra, dec):

    precess_ra, precess_dec = ugradio.coord.precess(ra, dec)
    alt, az = ugradio.coord.get_altaz(precess_ra, precess_dec)

    return alt, az

def initialize(ra, dec, dt, ifm, hpm):

    alt, az = altaz_point(ra, dec)
    ifm.point(alt, az)
    hpm.start_recording(dt/2)

def terminate(title, ifm, hpm):
    
    hpm.end_recording()
    voltages, times = hpm.get_recording_data()
    df = pd.DataFrame({'Voltages': voltages, 'Times': times})
    df.to_csv('./'+title+'.csv', mode = 'w')
    ifm.stow()
    
def observe(ra, dec, steps, dt, title):

    ifm = ugradio.interf.Interferometer()
    hpm = ugradio.hp_multi.HP_Multimeter()

    print('Initializing observation...')
    initialize(ra, dec, dt, ifm, hpm)

    for i in range(steps):
        alt, az = altaz_point(ra, dec)
        print(f'Repositioning to coordinates {alt, az}...')
        try:
            ifm.point(alt, az)
        except (AssertionError, TimeoutError):
            print(f'YOU FOOL: script errored out at {i=}')
            break
        finally:
            voltages, times = hpm.get_recording_data()
            df = pd.DataFrame({'Voltages': voltages, 'Times': times})
            df.to_csv('/home/crforrester/astro121lab/'+title+'.csv', mode='w')
        time.sleep(dt)

    print('Terminating observation')
    terminate(title, ifm, hpm)
  
def f_transform(data):
    
    fourier = np.fft.fft(data)
    fourier_freq = np.fft.fftfreq(len(data), 1/(10.7))
    fourier_shift = np.fft.fftshift(fourier)
    fourier_freq_shift = np.fft.fftshift(fourier_freq)
    power_spectrum = np.abs(fourier_shift)**2
    
    return fourier_freq_shift, power_spectrum

