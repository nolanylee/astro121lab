import ugradio
from ugradio.leo import *
import numpy as np
import pandas as pd
import csv
from astropy.time import Time
from astropy.coordinates import Angle, SkyCoord, EarthLocation, AltAz

def bubble_coords():
    coords = {}
    b = np.arange(-70, -8, 2)
    for i in b:
        l = np.arange(160, 220.001, 2 / np.cos(i*np.pi/180))
        coords[i] = l
    with open('bubble_coords.csv', 'w') as f:
        for key in coords.keys():
            f.write("%s,%s\n"%(key, coords[key]))

def gal2altaz(l,b): 
    gal_coord = SkyCoord(l=l, b=b, frame='galactic', unit='deg')
    time = Time.now()
    #campbell = EarthLocation(lat=37.873199 * u.deg, lon=-122.27573 * u.deg, height=20 * u.meter)
    leuschner = EarthLocation(lat = lat, lon = lon, height = alt)
    altaz_frame = AltAz(obstime = time, location = leuschner)
    altaz_coord = gal_coord.transform_to(altaz_frame)
    return altaz_coord.alt, altaz_coord.az

def test_obs(l,b):
    alt, az = gal2altaz(l,b)
    ugradio.LeuschTelescop.point(alt, az)
    spec = gradio.leusch.Spectrometer()
    spec.Spectrometer.read_spec('test.fits,', 1000, (l,b), 'ga')
    sd = ugradio.agilent.SynthDirect()
    sd.SynthClient.set_frequency(1e6)
    spec.Spectrometer.read_spec('test_LO.fits', 1000, (l,b), 'ga')
    LeuschTelescope.stow()



