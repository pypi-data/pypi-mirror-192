import oasis
import oasis_nan
import numpy as np
import matplotlib.pyplot as plt

# generate example trace
y, c, s = np.squeeze(oasis.functions.gen_data(g=[0.95], N=1))

# deconvolve example trace
c_hat, s_hat = oasis.oasis_methods.oasisAR1(y, .95, s_min=.5)
c_nan, s_nan = oasis_nan.oasisAR1(y, .95, s_min=.5)
print(np.allclose(c_hat, c_nan))  # same results for data w/o nans?

# introduce nans
y_nan = y.copy()
t_nan = np.random.rand(len(y)) > .5
y_nan[t_nan] = np.nan
c_nan, s_nan = oasis_nan.oasisAR1(y_nan, .95, s_min=.5)
plt.figure(figsize=(15, 3))
plt.subplot(211)
plt.plot(y_nan, label='data y')
plt.plot(c, label='true c')
plt.plot(c_nan, label='oasis $\hat{c}$')
plt.xlim(0, len(y))
plt.legend()
plt.subplot(212)
plt.plot(s, c='C1', label='true s')
plt.plot(s_nan, c='C2', label='oasis $\hat{s}$')
plt.xlim(0, len(y))
plt.legend()
plt.tight_layout(0)
plt.savefig('nan_example.pdf')

