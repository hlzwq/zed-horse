import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import {SCENES, AUDIO_SEGMENTS} from '../constants';

// Play narration audio for each scene
const SceneNarration: React.FC<{sceneKey: string; sceneStart: number}> = ({
  sceneKey,
  sceneStart,
}) => {
  const segments = AUDIO_SEGMENTS[sceneKey as keyof typeof AUDIO_SEGMENTS];
  if (!segments) return null;

  return (
    <>
      {segments.map((seg, i) => (
        <Sequence
          key={`${sceneKey}-${i}`}
          from={sceneStart + seg.startFrame}
          durationInFrames={seg.endFrame - seg.startFrame + 30} // extra buffer
        >
          <Audio src={staticFile(`audio/narration/${seg.file}`)} volume={1} />
        </Sequence>
      ))}
    </>
  );
};

export const AudioLayer: React.FC = () => {
  const sceneKeys = ['hook', 'doubt', 'whatToEval', 'sevenDims', 'fourDims', 'threeModels', 'median', 'conclusion'];

  return (
    <>
      {sceneKeys.map((key, i) => (
        <SceneNarration
          key={key}
          sceneKey={key}
          sceneStart={SCENES[i].start}
        />
      ))}
    </>
  );
};
