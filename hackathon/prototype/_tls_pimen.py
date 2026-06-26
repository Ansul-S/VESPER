"""One-off: TLS recovery of Pi Mensae c (full-search arm demo)."""
import numpy as np
from transitleastsquares import transitleastsquares

d = np.load('hackathon/prototype/cache/261136679.npz')
t = d['time'].astype(float); flux = 1.0 + d['resid'].astype(float)
m = np.isfinite(t) & np.isfinite(flux)
t, flux = t[m], flux[m]
res = transitleastsquares(t, flux).power(
    period_min=2.0, period_max=12.0, use_threads=1,
    oversampling_factor=2, duration_grid_step=1.15)
print(f"RESULT period={res.period:.4f} d depth={(1-res.depth)*1e6:.0f} ppm "
      f"T0={res.T0:.4f} SDE={res.SDE:.1f} dur_h={res.duration*24:.2f}")
np.savez('hackathon/prototype/cache/_pimen_tls.npz',
         period=res.period, T0=res.T0, depth=float(res.depth),
         dur=res.duration, sde=res.SDE)
print("saved")
