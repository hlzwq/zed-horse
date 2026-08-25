# TTS Integration Deep Dive

Three scripts in `scripts/` cover the TTS use cases. All of them:
- skip audio files that already exist (resume support)
- show progress in the foreground
- write a fresh `src/audioConfig.ts` with measured durations

| Script | Provider | Cost | Voice clone | Special |
|---|---|---|---|---|
| `generate_audio_stepfun.py` | StepFun `stepaudio-2.5-tts` | 5.8 CNY / 10k chars | Yes | Inline `()` direction + global `instruction` |
| `generate_audio_minimax.py` | MiniMax T2A v2 | ~0.1 CNY / 1k chars | Yes | Fast, high quality |
| `generate_audio_edge.py` | Microsoft Edge | Free | No | Zero-config |


## MiniMax TTS (`scripts/generate_audio_minimax.py`)

Cloud API, paid, supports voice cloning. Recommended when the user wants a specific
voice or needs Chinese voice quality.

### Setup

```bash
# 1. Get an API key
#    International: https://www.minimax.io
#    Mainland China: https://platform.minimaxi.com

# 2. Pick a voice (built-in or clone your own on the platform)

# 3. Set env vars (add to ~/.bashrc / ~/.zshrc / $PROFILE)
export MINIMAX_API_KEY="your-api-key"
export MINIMAX_VOICE_ID="your-voice-id"
```

### Edit the script

The script has a `SCENES` list at the top. **Edit this list** to define your scenes:

```python
SCENES = [
    {"id": "01-intro",    "title": "开场",   "text": "欢迎观看本期视频..."},
    {"id": "02-concept",  "title": "概念",   "text": "今天我们来讲..."},
    {"id": "03-demo",     "title": "演示",   "text": "让我们看一个例子..."},
    {"id": "04-summary",  "title": "总结",   "text": "感谢观看，下期见！"},
]
```

Each scene -> one `public/audio/<id>.mp3` + one entry in `src/audioConfig.ts`.

### Run

```bash
python scripts/generate_audio_minimax.py
```

### Common errors

| Error | Cause | Fix |
|---|---|---|
| `invalid api key` | Wrong domain | International: `api.minimax.io`, China: `api.minimaxi.com`. **Never** use `api.minimax.chat`. |
| `audioConfig.ts` has literal `\n` | Python f-string + `",\\n".join()` | Patch the script to iterate and write lines, or build the joined string outside the f-string |
| Long wait with no output | Script run in background | Run in foreground; redirect to a log file with `tee` if needed |
| 429 / quota | Out of credits | Top up at platform.minimax.io / platform.minimaxi.com |

### Pricing (check current rates)

- `speech-02-hd`    ~0.1 CNY / 1k chars  (high quality)
- `speech-02-turbo` ~0.05 CNY / 1k chars (fast)

## Edge TTS (`scripts/generate_audio_edge.py`)

Free, preset voices, no setup beyond `pip install edge-tts`. Good default when the user
doesn`t need voice cloning.

### Setup

```bash
pip install edge-tts
```

### Recommended voices

| Voice ID | Style | Best for |
|---|---|---|
| `zh-CN-YunyangNeural`   | Professional broadcaster | Most Chinese content (default) |
| `zh-CN-XiaoxiaoNeural`  | Warm, natural | Friendly explainers |
| `zh-CN-YunxiNeural`     | Youthful, energetic | Energetic topics |
| `en-US-GuyNeural`       | Warm male | English narration |
| `en-US-JennyNeural`     | Clear female | English narration |

Set the voice at the top of the script, or pass it as an env var if the script supports it.

## Choosing between MiniMax and Edge

```
Need voice cloning / specific brand voice -> MiniMax
Otherwise (free, fast, decent)            -> Edge TTS
Have API key already + budget             -> MiniMax for higher quality
```

## Tips

- **Run in foreground.** Long audio jobs are confusing without progress.
- **Don`t hand-edit durations in `audioConfig.ts`.** Re-run the script; it overwrites
  with measured values.
- **Resume is automatic.** Re-running skips already-generated files.
- **Validate before rendering.** Listen to a couple of scenes first; the cost of
  re-generating is much lower than the cost of re-rendering an entire video.


## StepFun TTS (`scripts/generate_audio_stepfun.py`)

Cloud API, paid, supports contextual TTS with inline emotion/pause control and voice
cloning. Recommended when the narration has emotional beats you want the model to deliver
realistically (e.g. suspense, anger, breathy asides) or when you need a cloned voice.

### Setup

```bash
# 1. Create a key at https://platform.stepfun.com
# 2. Set env vars (add to ~/.bashrc / ~/.zshrc / $PROFILE so they persist)
export STEP_API_KEY="your-api-key"
export STEP_VOICE_ID="cixingnansheng"   # optional, defaults to the demo voice
export STEP_MODEL="stepaudio-2.5-tts"    # optional, default
```

### Unique capabilities

1. **Global `instruction`** (max 200 chars) -- sets the overall tone of the entire
   audio. Use it for the project's voice identity ("语气专业、节奏平稳").
2. **Inline `()` direction** -- in each scene's `text`, anything inside `()` is treated
   as a per-phrase directing note (emotion, pause, breath) and is **not** spoken.
   Example:
   ```
   "（压低声音）嗨，你好。（短息）是不是我眼花了？"
   ```
   The model will whisper the first sentence, then pause, then speak the second.
3. **Voice cloning** -- upload a reference audio at platform.stepfun.com to get a
   cloned `voice_id`, then `export STEP_VOICE_ID=<that-id>`.

### Edit `SCENES`

```python
SCENES = [
    {
        "id": "01-intro",
        "title": "开场",
        "text": "（沉稳的声音）欢迎来到阶跃星辰。",
        # optional, overrides DEFAULT_INSTRUCTION for this scene only
        "instruction": "沉稳专业、带一点神秘感",
    },
    {"id": "02-concept", "title": "核心概念", "text": "今天我们来讲..."},
    # ...
]
```

### Run

```bash
python scripts/generate_audio_stepfun.py
```

Output: `model=stepaudio-2.5-tts voice=cixingnansheng`, then per-scene `[gen ]` /
`[skip]` lines, then a `wrote src/audioConfig.ts` line. Idempotent: re-running skips
already-generated files.

### Common errors

| Error | Cause | Fix |
|---|---|---|
| `HTTP 401` / `invalid api key` | Key wrong or expired | Re-copy from platform.stepfun.com, or rotate |
| `HTTP 429` | Rate-limited | Script auto-retries 3x with backoff; otherwise slow down |
| `input` truncated to 1000 | Scene text is too long | Split the scene -- one concept per scene anyway |
| `instruction` ignored | Wrong model (e.g. `step-tts-mini`) | Use `stepaudio-2.5-tts` (default) or unset `STEP_MODEL` |
| `voice_label` error | `stepaudio-2.5-tts` does not support `voice_label` | Use `instruction` + `()` instead |
| Inline `()` is read aloud | User put parens that should be spoken | Replace with `（全角）` (full-width) or remove |

### Pricing (check current rates)

- 5.8 CNY / 10,000 characters for `stepaudio-2.5-tts`
- 9.9 CNY / voice for voice clone (preview endpoint is free except for the synthesis cost)

### Streaming variant

For long videos where you want progress as the audio is generated, use the WebSocket
endpoint `wss://api.stepfun.com/v1/realtime/audio?model=stepaudio-2.5-tts`. Send
`tts.create` (with `session_id`, `voice_id`, `response_format`, `sample_rate`,
`instruction`) then stream `tts.text.delta` chunks. Most scenes are <1000 chars and
non-streaming is fine; reach for streaming only if a single scene exceeds a few
seconds of generation.
