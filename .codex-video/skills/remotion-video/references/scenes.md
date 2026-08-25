# Scene-driven architecture patterns

Tutorial / explainer videos are split into **scenes**. This file covers the patterns
that make them work: progress bar, captions, scene transitions, scene-starting hook.

## Progress bar

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { SCENES } from "./audioConfig";

export const ProgressBar: React.FC<{ index: number }> = ({ index }) => {
  const pct = ((index + 1) / SCENES.length) * 100;
  return (
    <div style={{
      position: "absolute", bottom: 30, left: 60, right: 60, height: 4,
      backgroundColor: "rgba(255,255,255,0.2)",
    }}>
      <div style={{
        width: `${pct}%`, height: "100%", backgroundColor: "#3498DB",
      }} />
    </div>
  );
};
```

## Scene title overlay

```tsx
import { useCurrentSceneIndex } from "./useCurrentSceneIndex";
import { SCENES } from "./audioConfig";

export const SceneTitle: React.FC = () => {
  const i = useCurrentSceneIndex();
  const s = SCENES[i];
  return (
    <div style={{
      position: "absolute", top: 40, left: 0, right: 0, textAlign: "center",
      color: "white", fontSize: 42,
    }}>
      {s?.title}
    </div>
  );
};
```

## Smooth scene transitions

Hard cuts feel cheap. Add a fade between scenes:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SCENES, getSceneStart } from "./audioConfig";

export const SceneFade: React.FC<{ sceneIndex: number }> = ({ sceneIndex }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const start = getSceneStart(sceneIndex);
  const localFrame = frame - start;
  const duration = Math.min(15, SCENES[sceneIndex].durationInFrames / 2);

  const opacity = interpolate(localFrame, [0, duration], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "black", opacity: 1 - opacity }} />
  );
};
```

## Captions overlay (subtitles from Whisper)

After running `transcribe()` (see `references/remotion-api.md`), iterate the
transcription to render caption Sequences:

```tsx
import { Sequence, AbsoluteFill } from "remotion";
import { useCurrentFrame, useVideoConfig } from "remotion";

type Caption = { text: string; startMs: number; endMs: number };

export const Captions: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 120 }}>
      {captions.map((c, i) => {
        const startFrame = (c.startMs / 1000) * fps;
        const endFrame = (c.endMs / 1000) * fps;
        return (
          <Sequence key={i} from={startFrame} durationInFrames={endFrame - startFrame}>
            <div style={{
              backgroundColor: "rgba(0,0,0,0.6)", color: "white",
              padding: "8px 20px", borderRadius: 8, fontSize: 48, maxWidth: "80%",
              textAlign: "center",
            }}>
              {c.text}
            </div>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Scene-starting hook (relative frame)

Each scene component should animate from frame 0, not from the global video frame:

```tsx
// In a scene wrapped by <Sequence from={...} durationInFrames={...}>:
const localFrame = useCurrentFrame();   // always 0-based within the Sequence
```

If the scene is rendered conditionally (e.g. `{sceneIndex === 0 && <Scene01 />}`),
the `useCurrentFrame()` still returns the global frame. Convert manually:

```tsx
const globalFrame = useCurrentFrame();
const localFrame = globalFrame - getSceneStart(sceneIndex);
```

## One-concept-per-scene checklist

Before shipping a scene, ask:
- Is the visual showing **one** idea, or two glued together?
- Does the audio explain the same thing the visual shows?
- Could a viewer understand the scene with no audio? (Visual should be self-contained.)
- Is the scene long enough for a 3-second cognitive load pause, but short enough to stay focused? (~5-15s typical)
