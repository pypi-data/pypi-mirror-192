import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
ds = xr.tutorial.load_dataset("air_temperature")

# in: 3D, out: 2D

def func(x):
    shifted = x.shift(time=-1)
    sign = x.where(x - shifted < 0, 1)
    sign = sign.where(x - shifted != 0, 0)
    sign = sign.where(x - shifted > 0, -1)
    return sign

sign = func(ds.air)
sign.isel(time=slice(1,10)).plot(col="time",col_wrap=4)
plt.show()

mean = sign.mean('time')
variance = sign.var('time')

z_mk = mean.where(mean < 0 , (mean - 1)/np.sqrt(variance) )
z_mk = z_mk.where(mean != 0 , 0 )
z_mk = z_mk.where(mean > 0 , (mean + 1)/np.sqrt(variance) )

z_mk

import scipy.stats

alpha = 0.05
z_score = scipy.stats.norm.ppf(1 - alpha)

(z_mk >= z_score).plot()