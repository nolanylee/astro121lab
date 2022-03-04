import ugradio
import numpy as np
import astropy
import scipy
import pandas as pd

#figure out proper coord convsersion b/n ra,dec and az,alt
#apply these conversions for the moon's pos in the night sky
#write script to track movement
    #determine coords for every step of time
    #for every step save data
#record data
#stop recording
#stow telescopes when done

### Determining Position
# ugradio.coord.moonpos(jd,lat,lon,alt) returns ra,dec of moon
# ugradio.coord.precess(ra,dec,jd,equinox) compensates for precession
# ugradio.coord.get_altaz(ra,dec,jd,lat,alt) returns alt,az of moon
# ifm.point(alt,az) points telescopes at specified alt,az

def moon_point():
    time = ugradio.timing.julian_date()
    lat, lon, alt = ugradio.nch
    equinox = 'J2000'
    moon_ra, moon_dec = ugradio.coord.moonpos(time,lat,lon,alt)
    precess_ra, precess_dec = ugradio.coord.precess(moon_ra,
                                                    moon_dec,
                                                    time,
                                                    equinox)     
    moon_alt, moon_az = ugradio.coord.get_altaz(precess_ra,
                                                precess_dec,
                                                time,
                                                equinox)
    return moon_alt, moon_az

#to do:
#make sure time.now() is in units of jd
#define the lat, lon, alt, and equinox of observing from Campbell

### Tracking the MOON
# commence the acquisition of data
# write a for loop of some kind using moon_point, per christian
# determine how frequently we should reposition the interfs (time steps)
# determine how frequently we should save the h2h data
# stop collecting data when finished (when?)
# stow telescopes

def observe(title):
    ifm = ugradio.interf.Interferometer()
    hpm = ugradio.hp_multi.HP_Multimeter()
    moon_alt, moon_az = moon_point()
    ifm.point(moon_alt, moon_az)
    hpm.start_recording(10)
    all_voltages = []
    all_times = []
    for i in range(5):
        moon_alt, moon_az = moon_point()
        ifm.point(moon_alt, moon_az)
        east_moving = True  # telescope is moving
        west_moving = True
        while east_moving or west_moving:
            west_moving = (ifm.get_pointing()['ant_w'] != moon_alt, moon_az)
            east_moving = (ifm.get_pointing()['ant_e'] != moon_alt, moon_az)
            time.sleep(1.)
        time.sleep(12.)
        voltages, times = hpm.get_recording_data()
        all_voltages.append(voltages)
        all_times.append(times)
    hpm.end_recording()
    ifm.stow()
    df = pd.DataFrame({'all_voltages': all_voltages, 'all_times': all_times})
    df.to_csv('/home/pi/astro121lab/'+title+'.csv')
