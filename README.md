# Voicebox TUI

A terminal voice studio for local voice cloning, built on [chatterbox.cpp](https://github.com/gianni-cor/chatterbox.cpp). Generate speech in cloned voices, audition alternate seeds, and master takes with pitch/EQ/compression/reverb — all from a keyboard-driven TUI.

---

## Features

- **Interactive TUI** — gum-powered menus for generating, cloning, tuning, and managing voices.
- **Local voice cloning** — record from the mic or import a clip, then build a reusable voice profile.
- **Emotion styles** — Calm, Confident, Excited, Serious, Neutral presets over the engine's sampling params.
- **A/B auditioning** — generate alternate seeds and keep the best take.
- **Tuning studio** — pitch, tempo, warmth, body, presence, de-harsh, reverb, compression, and loudness targeting, plus fixed presets (Cinematic, Dramatic, Smooth, Warm, Intense, Space, Reset).
- **Loudness and F0 measurement** — EBU R128 integrated loudness, true peak, and median F0 of every take.
- **Denoise** — rnnoise when a model is present, afftdn otherwise.
- **Non-destructive** — source takes and reference clips are never modified; every render is a new file.

---

## Requirements

- Linux with PulseAudio/PipeWire (`pw-play` or `ffplay` for playback)
- [gum](https://github.com/charmbracelet/gum)
- `ffmpeg` (with `rubberband` and `arnndn` filters for tuning/denoise)
- `python3` + `numpy` (F0 measurement)
- [chatterbox.cpp](https://github.com/gianni-cor/chatterbox.cpp) built with the turbo models:

```
~/voice-clone/chatterbox.cpp/
├── build/chatterbox
├── models/chatterbox-t3-turbo.gguf
├── models/chatterbox-s3gen.gguf
└── voices/                    # cloned voice profiles land here
```

Optional: an rnnoise model at `~/.local/share/rnnoise/bd.rnnn` for better denoise.

---

## Install

```bash
git clone https://github.com/shoaibmahmud244-lang/voicebox-tui.git ~/voice-clone/voicebox-tui
ln -s ~/voice-clone/voicebox-tui/voicebox ~/.local/bin/voicebox
voicebox --check
```

`voicebox --check` reports which dependencies and engine files are missing.

---

## Usage

```bash
voicebox                      # interactive TUI
voicebox --check              # dependency + profile check
voicebox --presets            # list tuning presets
voicebox --f0 FILE            # measured F0 (Hz)
voicebox --say TEXT --profile NAME [--seed N] [--temp T] [--emotion STYLE] [--out FILE]
voicebox --denoise FILE [--out FILE] [--mix 0-1]
voicebox --clone FILE NAME    # build a profile from an audio file
voicebox --tune FILE [--preset NAME] [--out FILE] [--pitch st --tempo X --warm dB --body dB --pres dB --harsh dB --rev % --comp % --lufs LUFS]
```

### Tuning presets

`Cinematic`, `Dramatic`, `Smooth`, `Warm`, `Intense`, `Space`, and `Reset`. Parameters: `pitch` (semitones), `tempo` (multiplier), `warmth` (dB @ 120 Hz), `body` (dB @ 250 Hz), `presence` (dB @ 6 kHz), `de-harsh` (dB @ 3.2 kHz), `reverb` (%), `compress` (%), `loudness` (LUFS).

---

## AI Agents & Automation (with Earshot)

Voicebox is fully scriptable for autonomous coding agents (Claude Code, Antigravity, OpenCode, Codex, Cursor). Because LLMs cannot physically hear audio, this repository bundles **[Earshot](skills/earshot/SKILL.md)** to serve as the agent's acoustic perception:

- **Audition takes across seeds**: Agents generate alternate takes (`--seed N`) and rank them using `earshot rank` or `earshot ab`.
- **Acoustic vetting**: Reference audio is vetted for clean speech and absence of background music with `earshot find` and `earshot describe` before running `voicebox --clone`.
- **Mastering verification**: Output LUFS and peak dynamics are verified with `earshot measure`.

See **[AGENTS.md](AGENTS.md)** and **[skills/voicebox/SKILL.md](skills/voicebox/SKILL.md)** for complete agent workflows and non-interactive recipes.

---

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `VOICEBOX_ROOT` | `~/voice-clone/chatterbox.cpp` | Engine, models, and voices root |
| `RNNOISE_DIR` | `~/.local/share/rnnoise` | Directory holding `bd.rnnn` |
| `RNNOISE_MODEL` | `$RNNOISE_DIR/bd.rnnn` | Explicit rnnoise model path |
| `DN_MIX` | `0.95` | rnnoise wet/dry mix |

Generated takes go to `~/voice-clone/out`; temporary state lives in `~/.local/state/voicebox`.

---

## Ethics

Clone only voices you have permission to use. Voice cloning can be misused; you are responsible for how the output is used.

---

## License

MIT — see [LICENSE](LICENSE).
