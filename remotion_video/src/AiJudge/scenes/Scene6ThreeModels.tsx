import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {
  SceneBg,
  AmbientParticles,
  AnimatedEntrance,
  BrainSVG,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

// Wall divider between models
const Wall: React.FC<{x: number; delay: number}> = ({x, delay}) => {
  const frame = useCurrentFrame();
  if (frame < delay) return null;

  return (
    <div style={{
      position: 'absolute',
      left: x,
      top: 200,
      width: 6,
      height: 500,
      background: `linear-gradient(to bottom, transparent, ${COLORS.neutral.darkGray}, transparent)`,
      borderRadius: 3,
      opacity: 0.6,
    }} />
  );
};

export const Scene6ThreeModels: React.FC = () => {
  const frame = useCurrentFrame();
  const scores = [85, 88, 82];

  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={6} />

      {/* Title */}
      <AnimatedEntrance type="fade" delay={5} style={{position: 'absolute', left: 100, top: 60}}>
        <div style={{
          ...TYPOGRAPHY.heading,
          fontSize: 44,
          color: COLORS.accent.yellow,
        }}>
          怎么评？三个脑袋比一个好
        </div>
      </AnimatedEntrance>

      {/* Three model brains */}
      <div style={{
        position: 'absolute',
        top: 200,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        gap: 120,
        zIndex: 5,
      }}>
        <BrainSVG size={180} color={COLORS.models.alpha} score={scores[0]} delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 10} label="模型 A" />
        <BrainSVG size={180} color={COLORS.models.beta} score={scores[1]} delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 25} label="模型 B" />
        <BrainSVG size={180} color={COLORS.models.gamma} score={scores[2]} delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 40} label="模型 C" />
      </div>

      {/* Walls (互不通气) */}
      <Wall x={720} delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 50} />
      <Wall x={1200} delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 55} />

      {/* Label: 互不通气 */}
      <AnimatedEntrance type="fade" delay={AUDIO_SEGMENTS.threeModels[0].startFrame + 60}
        style={{position: 'absolute', left: 650, top: 650}}>
        <div style={{
          ...TYPOGRAPHY.caption,
          fontSize: 28,
          color: COLORS.neutral.lightGray,
          textAlign: 'center',
          width: 600,
        }}>
          🔒 独立评分 · 互不通气
        </div>
      </AnimatedEntrance>

      <SubtitleSequence segments={AUDIO_SEGMENTS.threeModels} />
    </AbsoluteFill>
  );
};
