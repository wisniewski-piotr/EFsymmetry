import numpy as np
from piotr import symmetry as sym

w = 2*np.pi*299792458/800.0e-9 * 2.41889e-17
sym.set_omega(w); T = sym.cycle_period
sym.reset_wave()
sym.add_wave(1, 1, np.pi/2, 1, 1, 0)
sym.add_wave(1, -2, np.pi/2, 1, -2, 0)
sym.set_extrema_locs([0.0]); sym.set_zero_crossings_locs([T/6])

assert sym.test(sym.rotate(2*np.pi/3, sym.translate(T/3, sym.syminput())))
assert not sym.test(sym.rotate(2*np.pi/4, sym.translate(T/4, sym.syminput())))
assert sym.test(sym.time_refl(
    [sym.field_refl(m*np.pi/3, sym.syminput([m*T/6])) for m in range(6)],
    sym.syminput()))
print("(w,2w) OK")

sym.reset_wave()
sym.add_wave(1, 1, np.pi/2, 1, 1, 0)
sym.add_wave(1, -3, np.pi/2, 1, -3, 0)
assert not sym.test(sym.time_refl([sym.field_refl(m*np.pi/3, sym.syminput([m*T/6])) for m in range(6)], sym.syminput()))
assert     sym.test(sym.time_refl([sym.field_refl(m*np.pi/4, sym.syminput([m*T/8])) for m in range(8)], sym.syminput()))
print("(w,3w) OK")

sym.reset_wave()
sym.add_wave(1, 1, np.pi/2, 1, 1, 0)
sym.add_wave(1, -4, np.pi/2, 1, -4, 0)
assert not sym.test(sym.time_refl([sym.field_refl(m*np.pi/4, sym.syminput([m*T/8])) for m in range(8)], sym.syminput()))
assert     sym.test(sym.time_refl([sym.field_refl(m*np.pi/5, sym.syminput([m*T/10])) for m in range(10)], sym.syminput()))
print("(w,4w) OK")

sym.reset_wave()
sym.add_wave(1, 1, np.pi/2, 1, 1, 0)
for bad in (-np.pi, -1.5, 1.5):
    try:
        sym.add_wave(1, bad, 0, 1, bad, 0)
        raise SystemExit(f"FAIL: s={bad} was accepted")
    except AssertionError:
        pass
print("integer-harmonic guard OK")
