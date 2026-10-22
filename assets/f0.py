#!/usr/bin/env python3
"""Median F0 of the loudest 2s, numpy autocorrelation, 24k mono s16 wav."""
import sys, wave
import numpy as np


def main(path):
    w = wave.open(path, 'rb')
    sr = w.getframerate()
    nch = w.getnchannels()
    n = w.getnframes()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    w.close()
    if nch > 1:
        d = d.reshape(-1, nch).mean(axis=1)
    if d.size < sr // 10:
        print("0")
        return
    win = int(2.0 * sr)
    if d.size > win:
        hop = max(1, int(0.1 * sr))
        best, bi = -1.0, 0
        for i in range(0, d.size - win, hop):
            r = float(np.sqrt(np.mean(d[i:i + win] ** 2)))
            if r > best:
                best, bi = r, i
        d = d[bi:bi + win]
    X = np.fft.rfft(d)
    f = np.fft.rfftfreq(d.size, 1.0 / sr)
    X[(f < 55) | (f > 450)] = 0
    d = np.fft.irfft(X, d.size)
    L, H = int(0.04 * sr), int(0.02 * sr)
    lo, hi = int(sr / 450), int(sr / 55)
    vals = []
    for i in range(0, d.size - L, H):
        x = d[i:i + L].astype(np.float64)
        x = x - x.mean()
        if np.sqrt(np.mean(x * x)) < 0.004:
            continue
        ac = np.correlate(x, x, 'full')[L - 1:]
        ac /= ac[0] if ac[0] != 0 else 1
        hi2 = min(hi, L - 1)
        if hi2 <= lo:
            continue
        seg = ac[lo:hi2]
        k = int(np.argmax(seg)) + lo
        if ac[k] < 0.35:
            continue
        while k // 2 >= lo and ac[k // 2] > 0.85 * ac[k]:
            k //= 2
        if 0 < k < ac.size - 1:
            a, b, c = ac[k - 1], ac[k], ac[k + 1]
            den = a - 2 * b + c
            if den != 0:
                k = k - (c - a) / (2 * den)
        if k > 0:
            vals.append(sr / k)
    print(f"{float(np.median(vals)):.1f}" if vals else "0")


main(sys.argv[1])
