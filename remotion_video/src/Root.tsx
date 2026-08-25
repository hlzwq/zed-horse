import React from 'react';
import {Composition} from 'remotion';
import {AiJudge} from './AiJudge';
import {SCENES, TOTAL_FRAMES} from './AiJudge/constants';

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="AiJudge"
        component={AiJudge}
        durationInFrames={TOTAL_FRAMES}
        width={1920}
        height={1080}
        fps={30}
      />
    </>
  );
};
