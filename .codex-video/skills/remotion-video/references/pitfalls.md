# Common Pitfalls

Encountered-and-fixed problems when building Remotion videos. If something looks wrong,
scan this list first.

## TTS script generation

### Literal `\n` in TypeScript

**Symptom:** `src/audioConfig.ts` has `SyntaxError: "n"` or string content like
`[{...},\n{...}]` rendered literally (no newlines).

**Cause:** Python f-string with `",\\n".join()` -- inside an f-string, the backslash is
escaped to a literal `\n` text instead of a newline character.

```python
# BAD: literal "\n" in output
content = f`export const SCENES = [{",\\n".join(items)}];`

# GOOD: build the joined string outside the f-string
scenes_content = ",\n".join(items)
content = f"""export const SCENES = [
{scenes_content}
];"""

# ALSO GOOD: just iterate
lines = ["export const SCENES = ["]
for item in items:
    lines.append(f"  {item!r},")
lines.append("];")
content = "\n".join(lines)
```

### MiniMax `invalid api key`

**Symptom:** API returns `{"error": "invalid api key"}`.

**Cause:** Wrong API domain. `api.minimax.chat` is a **bogus** domain (probably an LLM
hallucination or stale docs). Use `api.minimax.io` (international) or
`api.minimaxi.com` (mainland China).

### TTS job hangs with no output

**Symptom:** `python scripts/generate_audio_*.py` runs forever, nothing prints.

**Cause:** Run in background (`&` / `Start-Process`) -- output is buffered or hidden.

**Fix:** Run in the foreground, or pipe to a log file with `tee`:
```bash
python scripts/generate_audio_minimax.py 2>&1 | tee /tmp/audio.log
```

## 3D rendering

### Camera shake (jitter that never settles)

**Symptom:** Subtle continuous zoom-in / zoom-out, especially when the camera is
"approaching" a target.

**Cause:** `position += (target - position) * factor` per frame. For `factor < 1`, the
camera asymptotically approaches but never reaches the target -- so the value never
stops changing.

**Fix (any of):**
```tsx
// A. Snap directly
camera.position.set(target.x, target.y, target.z);
camera.lookAt(0, 0, 0);

// B. Spring transition
const z = spring({ frame: frame - transitionFrame, fps, from: prevZ, to: targetZ, ... });
camera.position.z = z;

// C. Lerp + threshold
useEffect(() => {
  const d = target - camera.position.z;
  if (Math.abs(d) < 0.001) camera.position.z = target;
  else camera.position.z += d * 0.1;
}, [frame]);
```

### Image rotated 90 deg

**Symptom:** A digit (like "7") or any image appears sideways.

**Cause:** Image coordinates are `image[row][col]` with `row` from top to bottom and
`col` from left to right. Mapped naively to 3D, that means `row -> -y` (top is +y), `col -> x`.
Mixing `row -> x` and `col -> y` rotates the image 90 deg.

```tsx
// BAD
const x = (row - size/2) * cellSize;
const y = (col - size/2) * cellSize;

// GOOD
const x = (col - size/2 + 0.5) * cellSize;
const y = ((size - 1 - row) - size/2 + 0.5) * cellSize;  // y flipped
```

### WebGL context overflow

**Symptom:** `Error creating WebGL context` (or renders blank).

**Cause:** Multiple `<ThreeCanvas>` instances in a Composition exceed the browser`s
context limit (8-16).

**Fix:** Conditional render only the active scene, or render with `--gl=angle`, or use
the `LazyScene` buffer pattern (see `references/3d-video.md`).

### `useCurrentFrame()` inside `<Sequence>` returns local frame

**Symptom:** Animation seems to start over when a Sequence starts.

**Cause:** Inside `<Sequence from={N}>`, `useCurrentFrame()` returns `N`-relative frames
(0 at the Sequence`s start), not the global frame.

**Fix:** If you need the global frame, compute it manually:
```tsx
const globalFrame = useCurrentFrame() + sequenceFrom;
```
Or pass `frame` as a prop from outside the Sequence.

## Animation

### Progress variable exceeds 100%

**Symptom:** Things blow up to absurd scales (camera at z=4000, alpha=5000).

**Cause:** Linear progress `(frame - start) / duration` is not clamped -- if the scene
runs long, it overshoots.

**Fix:**
```tsx
// BAD
const p = (frame - start) / duration;

// GOOD
const p = Math.min(1, (frame - start) / duration);
```

For an interpolating target, clamp the output:
```tsx
const t = interpolate(frame, [start, end], [0, 1], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
```

## Audio

### Audio plays once but doesn`t loop

**Fix:** `<Audio src={...} loop />`.

### Audio drift / out of sync

**Cause:** Audio duration != `<Sequence durationInFrames>`.

**Fix:** Set `durationInFrames` from measured audio duration (the TTS script does this
automatically; never hand-edit).

### Audio is silent in render but plays in Studio

**Cause:** MP3 sample-rate / channel mismatch, or audio file is in `public/` but path
is wrong.

**Fix:** Verify path with `staticFile("audio/foo.mp3")` (no leading `/`); check Studio
console for file resolution errors.

## Rendering

### Render hangs at frame 0

**Cause:** `delayRender()` was called but `continueRender()` was never called.

**Fix:** Search for `delayRender` in the codebase; ensure every call is matched. Wrap
in `useEffect` with cleanup.

### Font not rendering

**Cause:** Font file not loaded, or the TTF path is wrong.

**Fix:** Use `@remotion/google-fonts` (call `loadFont()` once), or place TTF in
`public/fonts/` and use `staticFile("fonts/Foo.ttf")`.

### Out-of-memory on long videos

**Fix:** Lower `--concurrency`, or render on AWS Lambda (see `references/remotion-api.md`).

### WebM/VP9 looks blocky

**Fix:** Use H.264 (MP4) unless web delivery specifically requires WebM.
