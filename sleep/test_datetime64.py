import numpy as np

t1 = np.arange('2022-03-05', '2022-03-09', dtype='datetime64[m]')
t2 = np.arange('2022-03-06', '2022-03-10', dtype='datetime64[m]')
t0 = np.datetime64('2022-03-06T18')
print(type(t1-t0))