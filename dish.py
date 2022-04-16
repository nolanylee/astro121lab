import ugradio
from ugradio.leo import *
import numpy as np
import pandas as pd
import astropy
from astropy.time import Time
from astropy.coordinates import Angle, SkyCoord, EarthLocation, AltAz

def bubble_coords():
    coords = []
    bs = np.arange(-70, -8, 2)
    for b in bs:
        ls = np.arange(160, 220.1, 2/np.cos(b*np.pi/180))
        for l in ls:
            coords.append((l,b))
    return coords

def gal2altaz(l, b): 
    gal_coord = SkyCoord(l=l, b=b, frame='galactic', unit='deg')
    #time = Time.now()
    #campbell = EarthLocation(lat=37.873199 * u.deg, lon=-122.27573 * u.deg, height=20 * u.meter)
    leuschner = EarthLocation(lat = lat, lon = lon, height = alt)
    altaz_frame = AltAz(obstime = Time.now(), location = leuschner)
    altaz_coord = gal_coord.transform_to(altaz_frame)
    return altaz_coord.alt, altaz_coord.az

def bubble_obs(l, b, nspec):

    telescope = ugradio.leusch.LeuschTelescope()
    spectrometer = ugradio.leusch.Spectrometer()
    noise = ugradio.leusch.LeuschNoise()

    coords = bubble_coords()

    for i in len(coords):

        l, b = coords[i]
        alt, az = gal2altaz(l,b)

        print(f'Pointing to coordinates {alt, az...}')
        try:
            telescope.point(alt, az)
            print('Activating noise diode...')
            noise.on()
            print('Gathering spectra (diode on)')
            spectrometer.read_spec(f'{jd}_nd1.fits', nspec, (l,b), 'ga')
            print('Deactivating noise diode')
            noise.off()
            print('Gathering Spectra (diode off)')
            spectrometer.read_spec(f'{jd}_nd0.fits', nspec, (l,b), 'ga')
        except AssertionError:
            print('YOU FOOL: You failed to point the telescope')
            break
    
    print('Stowing telescope')
    telescope.stow()


    
