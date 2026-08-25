# 3D Video with @remotion/three

For product showcases, cartoon characters, spatial data, logo animations. Uses
React Three Fiber inside a Remotion Composition.

## Setup

```bash
# Use the official 3D template
npx create-video@latest --template three

# Or add to an existing project
npm i three @react-three/fiber @remotion/three @types/three
npm i @react-three/drei    # optional helpers (OrbitControls, Text, useGLTF, ...)
```

## Minimal 3D composition

```tsx
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { useThree } from "@react-three/fiber";

const My3DScene = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const camera = useThree((s) => s.camera);

  // Set camera once
  useEffect(() => { camera.position.set(0, 0, 5); camera.lookAt(0, 0, 0); }, [camera]);

  const rotation = interpolate(frame, [0, durationInFrames], [0, Math.PI * 2]);
  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });

  return (
    <mesh rotation={[0, rotation, 0]} scale={scale}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  );
};

export const My3DVideo: React.FC = () => {
  const { width, height } = useVideoConfig();
  return (
    <ThreeCanvas width={width} height={height}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <My3DScene />
    </ThreeCanvas>
  );
};
```

## Loading GLTF / GLB models

```tsx
import { useGLTF } from "@react-three/drei";
import { useCurrentFrame, interpolate } from "remotion";

const Model: React.FC<{ url: string }> = ({ url }) => {
  const frame = useCurrentFrame();
  const { scene } = useGLTF(url);
  const rotation = interpolate(frame, [0, 150], [0, Math.PI * 2]);
  return <primitive object={scene} rotation={[0, rotation, 0]} scale={0.5} />;
};

// usage: <Model url={staticFile("models/character.glb")} />
```

## Video as a 3D texture

```tsx
import { useVideoTexture } from "@remotion/three";
import { staticFile } from "remotion";

const VideoCube = () => {
  const tex = useVideoTexture(staticFile("/clip.mp4"));
  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshBasicMaterial map={tex} />
    </mesh>
  );
};
```

For frame-accurate rendering, use `useOffthreadVideoTexture()`.

## Camera controller (no shake!)

```tsx
// Pattern A: snap (no transition) -- simplest
const CameraController: React.FC<{ sceneIndex: number }> = ({ sceneIndex }) => {
  const { camera } = useThree();
  const cameraSettings: Record<number, [number, number, number]> = {
    0: [0, 0, 4],
    1: [0, 0, 3],
    2: [-0.5, 0, 3.5],
  };
  const target = cameraSettings[sceneIndex] ?? [0, 0, 4];
  camera.position.set(...target);
  camera.lookAt(0, 0, 0);
  return null;
};

// Pattern B: spring transition
const CameraController: React.FC<{ sceneIndex: number; transitionFrame: number }> = ({
  sceneIndex, transitionFrame,
}) => {
  const { camera } = useThree();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const targetZ = { 0: 4, 1: 3, 2: 3.5 }[sceneIndex] ?? 4;

  const z = spring({
    frame: frame - transitionFrame, fps,
    from: camera.position.z, to: targetZ,
    config: { damping: 20, stiffness: 100 },
  });
  camera.position.z = z;
  return null;
};
```

**Never** do `position += (target - position) * 0.05` per frame -- it never converges.

## WebGL configuration

Multiple `<ThreeCanvas>` instances in a Composition will exceed the browser`s WebGL
context limit (typically 8-16). Two options:

1. **Use `--gl=angle`** when rendering:
   ```bash
   npx remotion render --gl=angle MyVideo out.mp4
   ```
   Or in `remotion.config.ts`:
   ```ts
   export default { chromiumOptions: { gl: "angle" } };
   ```

2. **Conditional rendering** -- only mount the active 3D scene:
   ```tsx
   {sceneIndex === 0 && <ThreeCanvas><Scene01 /></ThreeCanvas>}
   {sceneIndex === 1 && <ThreeCanvas><Scene02 /></ThreeCanvas>}
   ```

3. **Lazy mount with buffer**:
   ```tsx
   const LazyScene = ({ sceneStart, sceneDuration, children }) => {
     const frame = useCurrentFrame();
     const buffer = 30;
     if (frame < sceneStart - buffer) return null;
     if (frame > sceneStart + sceneDuration + buffer) return null;
     return <>{children}</>;
   };
   ```

## Server-side rendering

When using `renderMedia()` / `renderFrames()` / `getCompositions()` programmatically,
`gl: "angle"` is required:

```ts
import { renderMedia } from "@remotion/renderer";

await renderMedia({
  composition, serveUrl, outputLocation: "out.mp4",
  chromiumOptions: { gl: "angle" },
});
```

## 3D character kit (composite primitives)

No need for a modeler -- build characters from primitives:

```tsx
const Cartoon = () => {
  const frame = useCurrentFrame();
  const legSwing = Math.sin(frame * 0.2) * 0.3;
  return (
    <group>
      <mesh position={[0, 1.5, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="#FFE4C4" />
      </mesh>
      <mesh position={[0, 0.5, 0]}>
        <capsuleGeometry args={[0.3, 0.8, 16, 32]} />
        <meshStandardMaterial color="#4169E1" />
      </mesh>
      <mesh position={[-0.15, -0.3, 0]} rotation={[legSwing, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.08, 0.6]} />
        <meshStandardMaterial color="#333" />
      </mesh>
      <mesh position={[0.15, -0.3, 0]} rotation={[-legSwing, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.08, 0.6]} />
        <meshStandardMaterial color="#333" />
      </mesh>
    </group>
  );
};
```

## Resources

| Resource | Use | URL |
|---|---|---|
| Mixamo | Free rigged character animations | https://www.mixamo.com |
| Sketchfab | Free / paid 3D models | https://sketchfab.com |
| Ready Player Me | Avatar generator | https://readyplayer.me |
| Spline | Browser 3D design tool | https://spline.design |
| gltfjsx | GLTF -> React component | `npx gltfjsx model.glb` |
