import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {SPRING} from '../components/SharedComponents';
import {
  SceneBg,
  AmbientParticles,
  AnimatedEntrance,
  CageSVG,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

const NoteIcon: React.FC<{x: number; y: number; delay: number; text: string}> = ({x, y, delay, text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({frame: frame - delay, fps, config: SPRING.snappy});
  if (frame < delay) return null;

  return (
    <div style={{
      position: 'absolute', left: x, top: y,
      opacity: progress,
      transform: `translateX(${(1 - progress) * -80}px)`,
      background: COLORS.background.medium,
      border: `2px solid ${COLORS.accent.rose}`,
      borderRadius: 8,
      padding: '10px 16px',
      fontFamily: 'NotoSansSC, sans-serif',
      fontSize: 24,
      color: COLORS.accent.rose,
      whiteSpace: 'nowrap',
    }}>
      📝 {text}
    </div>
  );
};

export const Scene2Doubt: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const checkProgress = spring({frame: frame - 60, fps, config: SPRING.bouncy});
  const cageProgress = spring({frame: frame - 100, fps, config: SPRING.bouncy});

  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={2} />

      {/* Doubt notes */}
      <NoteIcon x={100} y={200} delay={10} text="评分标准谁定的？" />
      <NoteIcon x={100} y={300} delay={25} text="偷偷塞了小纸条？" />

      {/* Check mark — "质疑合理" */}
      {frame >= 60 && (
        <div style={{
          position: 'absolute', left: 200, top: 450,
          opacity: checkProgress,
          transform: `scale(${checkProgress})`,
        }}>
          <svg width={120} height={120} viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="55" fill={COLORS.semantic.positive} opacity="0.2" stroke={COLORS.semantic.positive} strokeWidth="3" />
            <path d="M30,60 L50,80 L90,40" fill="none" stroke={COLORS.semantic.positive} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <div style={{
            fontFamily: 'NotoSansSC, sans-serif',
            fontSize: 28,
            color: COLORS.semantic.positive,
            textAlign: 'center',
            marginTop: 8,
          }}>
            质疑全部合理
          </div>
        </div>
      )}

      {/* Cage concept */}
      {frame >= 100 && (
        <div style={{
          position: 'absolute', right: 150, top: 180,
          opacity: cageProgress,
          transform: `scale(${cageProgress})`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 20,
        }}>
          <CageSVG size={350} animateIn startFrame={100} />
          <div style={{
            ...TYPOGRAPHY.heading,
            fontSize: 48,
            color: COLORS.accent.yellow,
            textAlign: 'center',
            textShadow: `0 0 20px ${COLORS.accent.yellow}66`,
          }}>
            关进笼子里
          </div>
        </div>
      )}

      <SubtitleSequence segments={AUDIO_SEGMENTS.doubt} />
    </AbsoluteFill>
  );
};
