import ugradio
import new_interf

M17_ra = new_interf.time2deg(18, 20, 26)
M17_dec = -16 - 10.6/60

sun_ra, sun_dec = ugradio.coord.sunpos()

new_interf.observe(M17_ra, M17_dec, 2700, 10, 'long_obs_data')
