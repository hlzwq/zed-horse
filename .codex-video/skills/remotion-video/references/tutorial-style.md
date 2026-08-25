# Tutorial / Explainer Visual Style

Patterns for making tutorial videos that feel like 3Blue1Brown: let the viewer
**discover** the answer rather than be told. The script drives the visual -- if the
narration says "step 1", the visual must show step 1, with breathing room.

## 3B1B core principles

1. **Why -> What.** Start with a question the viewer can relate to, then show what
   solves it. Never just announce a concept.
2. **Stepwise build-up.** Elements appear one at a time, not all at once.
3. **Color has meaning.** Don`t use red/blue/green as decoration. Pick a palette where
   colors signal **positive / negative / highlight / result** (see below).
4. **Show numbers.** Floating point values like `0.7` or `0.92` make abstract things
   concrete. Render them in `<Text>` with a monospace font.
5. **2D first.** Use 3D only when the content is inherently 3D. A 2D orthographic camera
   + flat planes is often clearer than a perspective render.

## 3B1B palette (semantic)

```ts
export const COLORS = {
  background: "#000000",
  positive:  "#58C4DD",   // blue   -- positive weight / value
  negative:  "#FF6B6B",   // red    -- negative weight / value
  highlight: "#FFFF00",   // yellow -- current focus
  result:    "#83C167",   // green  -- final / correct
  text:      "#FFFFFF",
  neutral:   "#888888",   // grey   -- inactive
  accent:    "#FF8C00",   // orange -- emphasis
};
```

## 2D / 3D decision

| Content | Dimensionality | Why |
|---|---|---|
| Neural-net diagrams | 2D | Layers align, labels read clearly |
| Data flow / arrows | 2D + animated arrows | Sequence and causality matter |
| Convolution kernels | 2D top-down | Grids align, numbers read |
| Feature-map stacks | 2.5D (perspective) | Show depth / channel count |
| Product / object | 3D | The content is 3D |
| Logo animations | 3D | Brand impact |

For "2D inside 3D", use `OrthographicCamera`:

```tsx
import { OrthographicCamera } from "@react-three/drei";

<OrthographicCamera makeDefault position={[0, 0, 10]} zoom={100} />
<mesh><planeGeometry args={[1, 1]} /><meshBasicMaterial color={...} /></mesh>
```

## Staggered entry

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import React from "react";

export const StaggeredGroup: React.FC<{
  children: React.ReactNode[];
  delayPerItem?: number;
}> = ({ children, delayPerItem = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <>
      {React.Children.map(children, (child, i) => {
        const delay = i * delayPerItem;
        if (frame < delay) return null;
        const progress = spring({
          frame: frame - delay, fps,
          config: { damping: 12, stiffness: 100 },
        });
        return <group scale={Math.max(0, progress)} opacity={progress}>{child}</group>;
      })}
    </>
  );
};

// usage:
// <StaggeredGroup delayPerItem={10}>
//   <Neuron position={[0, 0, 0]} />
//   <Neuron position={[1, 0, 0]} />
//   <Neuron position={[2, 0, 0]} />
// </StaggeredGroup>
```

## Value labels (with semantic color)

```tsx
import { Text } from "@react-three/drei";
import { COLORS } from "./colors";

export const ValueLabel: React.FC<{
  value: number;
  position: [number, number, number];
}> = ({ value, position }) => (
  <Text
    position={position} fontSize={0.15} anchorX="center" anchorY="middle"
    color={value > 0.5 ? COLORS.positive : value < -0.5 ? COLORS.negative : COLORS.neutral}
    font={undefined}   // or path to a monospace TTF in /public/fonts
  >
    {value.toFixed(2)}
  </Text>
);
```

## Focus box (highlight current step)

```tsx
import { Text } from "@react-three/drei";
import { useCurrentFrame } from "remotion";
import { COLORS } from "./colors";

export const FocusBox: React.FC<{
  position: [number, number, number];
  size: [number, number];
  label?: string;
}> = ({ position, size, label }) => {
  const frame = useCurrentFrame();
  const pulse = 1 + Math.sin(frame * 0.15) * 0.08;
  return (
    <group position={position}>
      <mesh scale={[pulse, pulse, 1]}>
        <planeGeometry args={size} />
        <meshBasicMaterial color={COLORS.highlight} transparent opacity={0.2} />
      </mesh>
      {label && (
        <Text position={[0, size[1] / 2 + 0.2, 0]} fontSize={0.12} color={COLORS.highlight}>
          {label}
        </Text>
      )}
    </group>
  );
};
```

## Process animation (showing "how", not just "what")

For algorithms, math derivations, data pipelines. The visual walks through each
operation; the script pauses for each one.

### Step-by-step text reveal

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const StepByStep: React.FC<{
  steps: string[]; startFrame: number; framesPerStep?: number;
}> = ({ steps, startFrame, framesPerStep = 20 }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ fontFamily: "monospace", fontSize: 28, color: "white" }}>
      {steps.map((step, i) => {
        const s = startFrame + i * framesPerStep;
        const opacity = interpolate(frame, [s, s + 10], [0, 1], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        const isResult = i === steps.length - 1;
        return (
          <span key={i} style={{ opacity, fontWeight: isResult ? "bold" : "normal" }}>
            {step}{" "}
          </span>
        );
      })}
    </div>
  );
};
```

### Value fly-in (calculation result "lands" at target position)

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import { Text } from "@react-three/drei";

export const ValueFlyIn: React.FC<{
  value: number; from: [number, number, number]; to: [number, number, number]; startFrame: number;
}> = ({ value, from, to, startFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const p = spring({ frame: frame - startFrame, fps, config: { damping: 15, stiffness: 80 } });
  const position: [number, number, number] = [
    from[0] + (to[0] - from[0]) * p,
    from[1] + (to[1] - from[1]) * p,
    from[2] + (to[2] - from[2]) * p,
  ];
  const scale = 1.5 - 0.5 * p;
  return (
    <Text position={position} fontSize={0.12 * scale} color="#83C167"
          anchorX="center" anchorY="middle">
      {value.toFixed(1)}
    </Text>
  );
};
```

## Script writing for visual pacing

**Bad** (info-dump):
> "The convolution kernel slides over the image, and at each position performs a
> dot product, producing one value."

**Good** (pause-friendly):
> "Let`s see how convolution works.
> (pause)
> The kernel covers these 9 pixels.
> (pause)
> We multiply each pixel by its corresponding weight...
> (pause)
> ...and sum them all.
> (pause)
> That result is written to the feature map at this position.
> (pause)
> First position done. Now the window slides one step..."

### Time budget

| Detail | First showing | Repeated |
|---|---|---|
| High | 3-4 sec / step | 0.5 sec / step |
| Medium | 2 sec / step | 0.3 sec / step |
| Low (already explained) | 1 sec / step | flash |

## Anti-patterns

- 3D for 3D`s sake -- perspective is distracting when the content is 2D
- Colors as decoration -- pick a semantic palette and stick to it
- All elements appear at once -- stagger them
- Script that says only "what" -- always pair it with a "why" question first
- One big scene with everything in it -- one concept per scene
