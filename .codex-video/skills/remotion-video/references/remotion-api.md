# Remotion API Reference

Use this when the core API in `SKILL.md` is not enough. Each section is a quick
copy-paste recipe.

## Parametrized compositions (dynamic data)

Define a `zod` schema and pass `defaultProps`. Useful for batch generation where each
video gets different data.

```tsx
import { z } from "zod";

const mySchema = z.object({
  title: z.string(),
  bgColor: z.string(),
  rows: z.array(z.object({ label: z.string(), value: z.number() })),
});

export const MyVideo: React.FC<z.infer<typeof mySchema>> = ({ title, bgColor, rows }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, color: "white", padding: 80 }}>
      <h1>{title}</h1>
      {rows.map((r, i) => <div key={i}>{r.label}: {r.value}</div>)}
    </AbsoluteFill>
  );
};

// Root.tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={mySchema}
  defaultProps={{ title: "Hello", bgColor: "#222", rows: [] }}
  durationInFrames={300} fps={30} width={1920} height={1080}
/>
```

Render with custom props from CLI:
```bash
npx remotion render MyVideo out.mp4 --props=$(cat props.json)
# or
npx remotion render MyVideo out.mp4 --props=title=Hi,bgColor=red
```

## Rendering options

```bash
# MP4 (default)
npx remotion render MyVideo out/video.mp4

# Codec
npx remotion render --codec=h264 MyVideo out.mp4
npx remotion render --codec=h265 MyVideo out.mp4
npx remotion render --codec=vp9 MyVideo out.webm
npx remotion render --codec=gif  MyVideo out.gif
npx remotion render --codec=mp3  MyVideo out/audio.mp3   # audio only
npx remotion render --codec=wav  MyVideo out/audio.wav

# Image sequence
npx remotion render --sequence MyVideo out/frames

# Single frame (thumbnail)
npx remotion still MyVideo --frame=30 out/thumbnail.png

# Quality (0-51, lower = better, default 18)
npx remotion render --crf=15 MyVideo out.mp4

# Parallel rendering
npx remotion render --concurrency=4 MyVideo out.mp4

# Lower res for fast iteration
npx remotion render --scale=0.5 MyVideo out.mp4
```

## Captions (auto-generated subtitles)

```bash
npm i @remotion/captions @remotion/install-whisper-cpp
npx remotion-install-whisper-cpp   # one-time, installs whisper.cpp binary
```

```ts
import { transcribe } from "@remotion/install-whisper-cpp";
import { whisperCppPath } from "@remotion/install-whisper-cpp";

const { transcription } = await transcribe({
  inputPath: "audio.mp3",
  whisperPath: whisperCppPath,
  model: "medium",   // tiny / base / small / medium / large
});
```

Then iterate `transcription` to render captions with `<Sequence from={start} durationInFrames={end-start}>`.

## Web player (embed in apps)

```bash
npm i @remotion/player
```

```tsx
import { Player } from "@remotion/player";
import { MyVideo } from "./MyVideo";

<Player
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  compositionWidth={1920}
  compositionHeight={1080}
  controls
  inputProps={{ title: "Dynamic" }}
  style={{ width: "100%" }}
/>
```

## AWS Lambda (distributed render at scale)

```bash
npm i @remotion/lambda
npx remotion lambda policies role    # one-time IAM setup
npx remotion lambda sites create     # deploy the bundle to S3 + CloudFront
npx remotion lambda render <site-url> MyVideo --props=props.json
```

## Google Fonts (no manual font file)

```bash
npm i @remotion/google-fonts
```

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
loadFont();   // call once, then "Inter" is available as a system font
```

## Useful hooks

```tsx
import { useCurrentFrame, useVideoConfig, staticFile, delayRender, continueRender } from "remotion";

const frame = useCurrentFrame();
const { fps, durationInFrames, width, height } = useVideoConfig();

// Async data: block render until ready
const [handle] = useState(() => delayRender());
useEffect(() => {
  fetchData().then(data => {
    setData(data);
    continueRender(handle);
  });
}, []);
```

## Debugging checklist

| Symptom | Fix |
|---|---|
| Font not rendering | `loadFont()` first, or place TTF in `public/fonts/` |
| Audio plays once, no loop | `<Audio loop />` |
| Video freezes on a frame | Use `<OffthreadVideo>` instead of `<Video>` for H.264 |
| Frame is blank | Check that `useCurrentFrame()` actually ticks -- add `console.log(frame)` |
| Studio hot-reload broken | `rm -rf node_modules/.cache && npm run dev` |
| Render hangs at frame 0 | Probably a `delayRender` that never `continueRender`s |
