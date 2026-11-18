---
name: voicebox
description: Automated local voice cloning, speech synthesis, take auditioning, and audio mastering using Voicebox and Earshot. Use when an agent needs to clone a voice profile from audio, generate takes across seeds, audition and rank takes without human ears, and apply mastering presets headlessly.
---

# voicebox: automated voice cloning & studio for agents

Voicebox is a terminal voice studio built on `chatterbox.cpp` turbo models. Because coding agents cannot hear sound, **Earshot serves as the agent's ears** to vet source audio, audition alternate takes, detect artifacts, and verify mastering.

## Cardinal Rules for Agents

1. **Never launch interactive menus:** Bare `voicebox` or menu prompts invoke `gum` (TUI), which blocks automated turns. Always use the non-interactive CLI flags documented below.
2. **Never judge audio blindly:** Never declare that a voice clone "sounds natural" or "matches the tone" without citing an Earshot reading (`match`, `rank`, `realness`, or `measure`).
3. **Always explore alternate seeds:** Neural TTS engines vary by seed. Always generate 3-4 alternate seeds (`--seed N`) and let Earshot select the cleanest take.

---

## Prerequisites & Environment

```bash
# Verify environment and dependencies
voicebox --check
voicebox --presets

# Default paths (can be overridden via environment variables):
export VOICEBOX_ROOT="${VOICEBOX_ROOT:-$HOME/voice-clone/chatterbox.cpp}"
export RNNOISE_DIR="${RNNOISE_DIR:-$HOME/.local/share/rnnoise}"
export OUT="${OUT:-$HOME/voice-clone/out}"
```

Profiles live in `$VOICEBOX_ROOT/voices/<profile_name>/embedding.npy`.

---

## The 4-Stage Agent Production Pipeline

### Stage 1: Source Audio Vetting & Cloning

Before building a voice profile, vet the source clip to ensure it contains clean, isolated human speech without background music, reverb, or clicks.

1. **Find the cleanest speech window:**
   ```bash
   earshot find raw_audio.wav "a single clean speaking voice without background music" --top 3
   ```
   Inspect the timestamps, kind (`stroke`/`event`/`window`), and head/tail cuts.

2. **Verify speech content and naturalness:**
   ```bash
   # Check AudioSet labels (must be Speech, not Music or Noise)
   earshot describe raw_audio.wav --start 1.2 --end 8.5

   # Check authentic recording vs artifacted audio
   earshot realness raw_audio.wav --start 1.2 --end 8.5
   ```

3. **Optional Denoise:**
   If background hiss or room noise is present:
   ```bash
   voicebox --denoise raw_audio.wav --mix 0.95 --out /tmp/clean_ref.wav
   ```

4. **Clone the Voice Profile:**
   ```bash
   # Generates $VOICEBOX_ROOT/voices/narrator/embedding.npy and runs a smoke test
   voicebox --clone /tmp/clean_ref.wav narrator
   ```

---

### Stage 2: Batch Take Generation

Generate multiple takes across varying seeds and emotion styles:

```bash
TEXT="The universe is under no obligation to make sense to you."
PROFILE="narrator"

voicebox --say --text "$TEXT" --profile "$PROFILE" --seed 42  --emotion Confident --out takes/take_s42.wav
voicebox --say --text "$TEXT" --profile "$PROFILE" --seed 108 --emotion Confident --out takes/take_s108.wav
voicebox --say --text "$TEXT" --profile "$PROFILE" --seed 777 --emotion Confident --out takes/take_s777.wav
```

Available emotion presets:
- `Neutral` (default)
- `Calm` (lower temperature, steadier cadence)
- `Confident` (firm pacing, strong presence)
- `Excited` (faster tempo, higher pitch variance)
- `Serious` (deliberate timing, lower pitch bias)

---

### Stage 3: Auditioning & Selection with Earshot

Select the best take using Earshot's acoustic analysis:

1. **Rank takes against target style:**
   ```bash
   earshot rank "clear confident conversational narrator without glitches" takes/ --top 3
   ```
   Look for the candidate with the highest alignment z-score.

2. **A/B compare the top two finalists:**
   ```bash
   earshot ab takes/take_s42.wav takes/take_s108.wav --query "steady professional voiceover"
   ```

3. **Verify against generative distortion:**
   ```bash
   earshot realness takes/take_s42.wav
   ```
   Ensure the take does not trigger heavy synthetic distortion or high-frequency buzzing.

4. **Check pitch (F0):**
   ```bash
   voicebox --f0 takes/take_s42.wav
   ```

---

### Stage 4: Mastering & Tuning

Apply equalization, dynamic control, and loudness normalization:

1. **Apply tuning preset or custom parameters:**
   ```bash
   # Using preset
   voicebox --tune takes/take_s42.wav --preset Cinematic --lufs -18.5 --out final_master.wav

   # Or manual parametric tuning
   voicebox --tune takes/take_s42.wav \
     --pitch 0 \
     --warm 2.0 \
     --body 1.5 \
     --pres 1.0 \
     --harsh -2.0 \
     --comp 25 \
     --lufs -18.5 \
     --out final_master.wav
   ```

   **Presets available:** `Cinematic`, `Dramatic`, `Smooth`, `Warm`, `Intense`, `Space`, `Reset`.

2. **Objective Master Verification:**
   ```bash
   earshot measure final_master.wav
   ```
   Verify that:
   - Integrated loudness matches the target (e.g. `-18.5 LUFS` ± 0.5 for mobile/vertical video, `-14.0 LUFS` for standard web video).
   - True peak is safe (`≤ -1.0 dBTP`).
   - Dynamic range and spectral roll-off are balanced.
