# Voicebox TUI — Agent Guidelines

This repository provides a local voice cloning studio built on `chatterbox.cpp` turbo models. It includes both an interactive `gum`-powered TUI for humans and non-interactive CLI flags for autonomous LLM agents.

---

## 1. Headless Rule for Agents

**Never run bare `voicebox` or menu commands in automated workflows.**
Interactive prompts require a TTY and user keystrokes, which will block an agent session. Always use explicit command-line flags:

```bash
voicebox --check
voicebox --presets
voicebox --f0 <file.wav>
voicebox --clone <ref.wav> <profile_name>
voicebox --say --text "<text>" --profile <name> [--seed <N>] [--emotion <style>] [--out <file.wav>]
voicebox --tune <file.wav> [--preset <name>] [--lufs <LUFS>] [--out <file.wav>]
voicebox --denoise <file.wav> [--mix <0-1>] [--out <file.wav>]
```

---

## 2. Earshot as Sensory Grounding

Because AI agents cannot physically listen to audio, **Earshot serves as your ears**.
Two agent skills are bundled in this repository under `skills/`:
- `skills/earshot/SKILL.md` — Core acoustic listening, similarity search, realness vetting, and loudness measurement.
- `skills/voicebox/SKILL.md` — End-to-end voice cloning, alternate-seed auditioning, and mastering pipeline.

### Rules of Engagement
- **Vet before cloning:** Never pass unvetted audio to `voicebox --clone`. Run `earshot find` and `earshot describe` to ensure the sample is clean speech free of background music, reverb, or noise.
- **Generate alternate seeds:** Neural voice synthesis varies between seeds. Always generate 3–4 takes (`--seed 42`, `--seed 108`, etc.) for any important line.
- **Select with evidence:** Use `earshot rank` or `earshot ab` to audition and select the winning take. Quote the z-score, `p_real`, and LUFS in your report.
- **Verify mastering:** After `voicebox --tune`, confirm the final file with `earshot measure` to verify LUFS target and true peak.

---

## 3. Environment & Paths

| Variable | Default | Purpose |
|---|---|---|
| `VOICEBOX_ROOT` | `~/voice-clone/chatterbox.cpp` | Root containing `build/chatterbox`, `models/`, and `voices/` |
| `RNNOISE_DIR` | `~/.local/share/rnnoise` | Location of optional `bd.rnnn` denoise model |
| `OUT` | `~/voice-clone/out` | Destination for generated speech and tuned takes |

Cloned voice profiles are saved as `$VOICEBOX_ROOT/voices/<name>/embedding.npy`.

---

## 4. Quick Verification Recipe

```bash
# 1. Check system setup
voicebox --check

# 2. Generate a test take with seed exploration
voicebox --say --text "Agent testing voicebox pipeline." --profile saveo_dn --seed 42 --out test_take.wav

# 3. Audit take quality with Earshot
earshot realness test_take.wav
earshot measure test_take.wav
```
