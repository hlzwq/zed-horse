import React from 'react';
import {AbsoluteFill} from 'remotion';
import {TransitionSeries, linearTiming, crossZoom} from '@remotion/transitions';
import {SCENES, TRANSITION_DURATION, COLORS} from './constants';
import {AudioLayer} from './components/AudioLayer';
import {Scene1Hook} from './scenes/Scene1Hook';
import {Scene2Doubt} from './scenes/Scene2Doubt';
import {Scene3WhatToEval} from './scenes/Scene3WhatToEval';
import {Scene4SevenDims} from './scenes/Scene4SevenDims';
import {Scene5FourDims} from './scenes/Scene5FourDims';
import {Scene6ThreeModels} from './scenes/Scene6ThreeModels';
import {Scene7Median} from './scenes/Scene7Median';
import {Scene8Conclusion} from './scenes/Scene8Conclusion';

const SCENE_COMPONENTS = [
  Scene1Hook,
  Scene2Doubt,
  Scene3WhatToEval,
  Scene4SevenDims,
  Scene5FourDims,
  Scene6ThreeModels,
  Scene7Median,
  Scene8Conclusion,
];

export const AiJudge: React.FC = () => {
  return (
    <AbsoluteFill style={{background: COLORS.background.dark}}>
      {/* Persistent global background */}
      <AbsoluteFill style={{
        background: `linear-gradient(135deg, ${COLORS.background.dark} 0%, ${COLORS.background.medium} 100%)`,
      }} />

      <TransitionSeries>
        {SCENES.map((scene, i) => {
          const SceneComp = SCENE_COMPONENTS[i];
          const elements: React.ReactNode[] = [];

          elements.push(
            <TransitionSeries.Sequence
              durationInFrames={scene.duration}
              key={`scene-${i}`}
            >
              <SceneComp />
            </TransitionSeries.Sequence>,
          );

          if (i < SCENES.length - 1) {
            elements.push(
              <TransitionSeries.Transition
                key={`trans-${i}`}
                presentation={crossZoom({})}
                timing={linearTiming({durationInFrames: TRANSITION_DURATION})}
              />,
            );
          }

          return <React.Fragment key={`group-${i}`}>{elements}</React.Fragment>;
        })}
      </TransitionSeries>

      {/* Audio layer — sibling of TransitionSeries, NOT inside it */}
      <AudioLayer />
    </AbsoluteFill>
  );
};
