#!/usr/bin/env python3
"""Build a dry+wet impulse response: delta + energy-normalised room * W.
usage: mkir.py room.wav W out.wav
"""
import sys, wave
import numpy as np

room, W, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
w = wave.open(room, 'rb')
sr = w.getframerate()
r = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
w.close()
r = r / np.sqrt(np.sum(r * r)) if np.sum(r * r) > 0 else r
mix = np.zeros(max(len(r) + 1, 1))
mix[0] = 1.0
mix[1:1 + len(r)] += r * W
mix = np.clip(mix, -1.0, 1.0)
w = wave.open(out, 'wb')
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(sr)
w.writeframes((mix * 32767).astype('<i2').tobytes())
w.close()
