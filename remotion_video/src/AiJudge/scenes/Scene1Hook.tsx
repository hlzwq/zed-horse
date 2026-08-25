import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {
  SceneBg,
  AmbientParticles,
  AnimatedEntrance,
  AIRobot,
  QuestionBubble,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

export const Scene1Hook: React.FC = () => {
  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={1} />

      {/* AI Robot */}
      <div style={{position: 'absolute', left: 760, top: 200, zIndex: 10}}>
        <AIRobot size={240} animateIn startFrame={5} />
      </div>

      {/* Title */}
      <AnimatedEntrance type="scale" delay={15} style={{position: 'absolute', left: 610, top: 480, zIndex: 10}}>
        <div style={{
          ...TYPOGRAPHY.title,
          fontSize: 80,
          textAlign: 'center',
        }}>
          AI 评委？
        </div>
      </AnimatedEntrance>

      {/* Question bubbles */}
      <QuestionBubble x={550} y={220} delay={30} />
      <QuestionBubble x={1300} y={250} delay={45} />
      <QuestionBubble x={920} y={130} delay={60} />

      {/* Subtitle */}
      <SubtitleSequence segments={AUDIO_SEGMENTS.hook} />
    </AbsoluteFill>
  );
};
