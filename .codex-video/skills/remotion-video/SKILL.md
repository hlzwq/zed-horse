---
name: remotion-video
description: |
  Create MP4 videos programmatically with the Remotion framework (React components to video).
  Triggers: "Remotion", "remotion", "用代码做视频", "编程视频", "React 视频", "/remotion-video",
  "make a video with code", "programmatic video", "code-driven video", "code-generated video".
  Use for: tutorial/explainer videos with TTS narration, data-visualization videos,
  music visualizations, 3D product showcases, batch video generation (e.g. year-in-review).
  Do NOT use for: screen recording, manual video editing, live streaming, OBS-style work.
---

# Remotion Video

Create MP4 videos by writing React components. A Composition runs frame-by-frame, so any
deterministic animation, transition, or data-driven layout is straightforward.

## When to use this skill

| Use it for | Don`t use it for |
|---|---|
| Tutorial / explainer videos with TTS voiceover | Screen recordings |
| Data visualization, year-in-review videos | Manual editing of existing footage |
| Music-reactive visualizations | Live streaming |
| 3D product showcases, logo animations | One-off static images |
| Batch generation (e.g. personalized reports) | Quick phone clips |

## Workflow

1. **Gather requirements** — ask up front:
   - Topic & audience
   - Length (drives TTS cost and render time)
   - Style: tutorial / data-viz / music-viz / 3D
   - TTS provider: **StepFun** `stepaudio-2.5-tts` (paid, contextual with emotion/pause control, voice clone), **MiniMax** T2A v2 (paid, voice clone), or **Edge TTS** (free, preset voices)
   - Aspect ratio: 16:9 (1920x1080), 9:16 (1080x1920 short-form), 1:1

2. **Scaffold a Remotion project**
   ```bash
   npx create-video@latest my-video
   cd my-video && npm install
   ```
   Use the blank template unless the user wants 3D (then `--template three`).

3. **Write the script -> scenes.** For tutorial / explainer videos, follow
   **scene-driven architecture** below. Each scene = one chunk of narration = one audio
   file = one scene component. **One concept per scene.**

4. **Generate TTS audio** (foreground, see `references/tts.md`):
   ```bash
   export MINIMAX_API_KEY=... MINIMAX_VOICE_ID=...
   python scripts/generate_audio_minimax.py    # or generate_audio_edge.py
   ```
   The script writes MP3s to `public/audio/` and auto-updates `src/audioConfig.ts`
   with real durations. **Do not hand-edit durations** -- let the script set them.

5. **Wire up audio + progress UI** in the composition (see Scene-driven architecture).

6. **Preview & render**
   ```bash
   npm run dev                                  # Remotion Studio, hot-reload
   npx remotion render MyComposition out/video.mp4
   ```
   **Always run in the foreground** so the user sees progress. Don`t background it.

---

## Core Remotion API (the minimum)

### Composition definition

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";
import { TOTAL_FRAMES, FPS } from "./audioConfig";

export const RemotionRoot = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
```

### Driving animation from frames

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

export const MyVideo = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Linear: 0->30 frames, opacity 0->1
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

  // Spring (physics) entry
  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });

  return (
    <AbsoluteFill style={{ backgroundColor: "white", justifyContent: "center" }}>
      <div style={{ opacity, transform: `scale(${scale})`, fontSize: 100 }}>Hello</div>
    </AbsoluteFill>
  );
};
```

### Sequencing scenes

```tsx
import { Sequence, Audio, staticFile } from "remotion";

<Sequence from={0} durationInFrames={60}><Intro /></Sequence>
<Sequence from={60} durationInFrames={90}><Main /></Sequence>
<Sequence from={150}><Outro /></Sequence>   // no duration = play to end
```

`useCurrentFrame()` inside a `<Sequence>` returns frames **relative to that Sequence`s
start**, not global. Pass props if you need absolute time.

### Media

```tsx
<Audio src={staticFile("audio/01-intro.mp3")} volume={0.5} />
<Video src={staticFile("bg.mp4")} />
<Img src={staticFile("logo.png")} style={{ width: 200 }} />
```

Files in `public/` are referenced with `staticFile()` (no leading `/` or `public/`).

---

## Scene-driven architecture (for tutorial / explainer videos)

The single most important pattern in this skill. **Audio duration drives scene length**,
and `audioConfig.ts` is the single source of truth.

```
script.txt -> TTS script -> public/audio/*.mp3 + src/audioConfig.ts -> scene components
```

### `src/audioConfig.ts` (template: `templates/audioConfig.ts`)

```ts
export interface SceneConfig {
  id: string;
  title: string;
  durationInFrames: number;   // auto-filled by the TTS script
  audioFile: string;
}

export const SCENES: SceneConfig[] = [
  { id: "01-intro", title: "开场", durationInFrames: 300, audioFile: "01-intro.mp3" },
  // ...
];

export const getSceneStart = (i: number) =>
  SCENES.slice(0, i).reduce((sum, s) => sum + s.durationInFrames, 0);

export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;
export const FPS = 30;
```

### Scene-switching hook

```tsx
import { useCurrentFrame } from "remotion";
import { SCENES } from "./audioConfig";

export const useCurrentSceneIndex = () => {
  const frame = useCurrentFrame();
  let acc = 0;
  for (let i = 0; i < SCENES.length; i++) {
    acc += SCENES[i].durationInFrames;
    if (frame < acc) return i;
  }
  return SCENES.length - 1;
};
```

### Main composition pattern

```tsx
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { SCENES, getSceneStart } from "./audioConfig";
import { useCurrentSceneIndex } from "./useCurrentSceneIndex";

export const TutorialVideo: React.FC = () => {
  const { width, height } = useVideoConfig();
  const sceneIndex = useCurrentSceneIndex();

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
      {sceneIndex === 0 && <Scene01 />}
      {sceneIndex === 1 && <Scene02 />}

      {SCENES.map((s, i) => (
        <Sequence key={s.id} from={getSceneStart(i)} durationInFrames={s.durationInFrames}>
          <Audio src={staticFile(`audio/${s.audioFile}`)} />
        </Sequence>
      ))}

      <ProgressBar index={sceneIndex} total={SCENES.length} />
    </AbsoluteFill>
  );
};
```

**One concept per scene.** If a scene is trying to explain two things, split it.

---

## Common pitfalls (top 3 -- see `references/pitfalls.md` for more)

1. **Literal `\n` in TypeScript generated by Python** -- never use `",\\n".join()` inside
   an f-string. Build the joined string outside the f-string, or iterate and write lines.
2. **Camera shake in 3D** -- `position += (target - position) * 0.05` per frame never
   converges. Use `spring()`, set `camera.position.set(...)` directly, or clamp when
   within a threshold (e.g. `< 0.001`).
3. **Image rotated 90 deg** -- in image grids, `row` -> y (and **flipped**: image row 0
   is at the top), `col` -> x. Mixing them up rotates the image 90 deg.

---

## TTS scripts (quick reference)

| Script | Provider | Cost | Voice clone | Key capability | Setup |
|---|---|---|---|---|---|
| `scripts/generate_audio_stepfun.py` | StepFun stepaudio-2.5-tts | 5.8 CNY / 10k chars | Yes | Inline `()` emotion / pause / breath + global `instruction` | `STEP_API_KEY`, optional `STEP_VOICE_ID` |
| `scripts/generate_audio_minimax.py` | MiniMax T2A v2 | ~0.1 CNY / 1k chars | Yes | Fast, high quality | `MINIMAX_API_KEY`, `MINIMAX_VOICE_ID` |
| `scripts/generate_audio_edge.py` | Microsoft Edge | Free | No | Zero-config, preset voices | `pip install edge-tts` |

Both scripts: skip existing files (resume), show foreground progress, auto-update
`src/audioConfig.ts` after generation. Set voice_id in the SCENES list (or env var)
before running. See `references/tts.md`.

---

## When to read the references

| Reference | Read it when... |
|---|---|
| `references/remotion-api.md` | You need a specific API (player, captions, AWS Lambda, props schema, ...) |
| `references/tts.md` | Setting up MiniMax keys, choosing voices, troubleshooting API errors |
| `references/scenes.md` | Building a tutorial, want progress-bar / caption overlays, scene transitions |
| `references/3d-video.md` | Using `@remotion/three`, GLTF models, 3D characters, WebGL config |
| `references/tutorial-style.md` | 3Blue1Brown-style visual explanations, process animation (step-by-step, value fly-in) |
| `references/pitfalls.md` | A render / animation looks wrong, frames out of sync, errors you don`t recognize |
