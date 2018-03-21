import numpy as np

# Generate 'quasirandom' points. These appear random to the eye, but cover the desired area well.
def quasirandom(n):
    w = len(bin(n))

    x = np.arange(n, dtype=float)
    y = np.zeros_like(x)

    for i, a in enumerate(x):
        b = bin(i)
        c = int(b[:1:-1] + (w - len(b)) * '0', 2)
        y[i] = c

    return x, y
