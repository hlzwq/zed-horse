import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {SPRING} from '../components/SharedComponents';
import {
  SceneBg,
  AmbientParticles,
  AnimatedEntrance,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

export const Scene3WhatToEval: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // "拆方块" 动画
  const splitProgress = spring({frame: frame - 40, fps, config: {damping: 25, stiffness: 100}});
  const blockSize = 80;
  const gap = interpolate(splitProgress, [0, 1], [0, 12]);

  // 11 small blocks (7+4 = 11 dimensions)
  const blocks = Array.from({length: 11}).map((_, i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const isBlue = i < 7;
    const baseX = 760;
    const baseY = 350;
    const offsetX = (col - 1.5) * (blockSize + gap);
    const offsetY = (row - 1) * (blockSize + gap);
    return {x: baseX + offsetX, y: baseY + offsetY, color: isBlue ? COLORS.accent.teal : COLORS.accent.rose};
  });

  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={3} />

      {/* Left: "你挑最好的？" */}
      <AnimatedEntrance type="slideRight" delay={5} style={{position: 'absolute', left: 100, top: 250}}>
        <div style={{
          border: `2px dashed ${COLORS.neutral.darkGray}`,
          borderRadius: 12,
          padding: '24px 32px',
          opacity: 0.5,
        }}>
          <div style={{...TYPOGRAPHY.body, color: COLORS.neutral.darkGray, fontSize: 36}}>
            你挑最好的？
          </div>
          <div style={{fontSize: 48, color: COLORS.neutral.darkGray, textAlign: 'center'}}>🤷</div>
        </div>
      </AnimatedEntrance>

      {/* Arrow */}
      <AnimatedEntrance type="fade" delay={25} style={{position: 'absolute', left: 480, top: 330}}>
        <svg width={100} height={60} viewBox="0 0 100 60">
          <defs>
            <linearGradient id="arrowGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={COLORS.neutral.darkGray} />
              <stop offset="100%" stopColor={COLORS.accent.teal} />
            </linearGradient>
          </defs>
          <line x1="0" y1="30" x2="75" y2="30" stroke="url(#arrowGrad)" strokeWidth="4" />
          <polygon points="70,15 95,30 70,45" fill={COLORS.accent.teal} />
        </svg>
      </AnimatedEntrance>

      {/* Right: Split blocks */}
      <AnimatedEntrance type="scale" delay={30} style={{position: 'absolute', right: 200, top: 200}}>
        <div style={{...TYPOGRAPHY.heading, fontSize: 44, color: COLORS.accent.teal, marginBottom: 20}}>
          拆清楚！
        </div>
      </AnimatedEntrance>

      {/* Splitting animation */}
      <div style={{position: 'absolute', left: 600, top: 300, zIndex: 5}}>
        {blocks.map((b, i) => {
          const blockDelay = 40 + i * 3;
          const bp = spring({frame: frame - blockDelay, fps, config: SPRING.snappy});
          if (frame < blockDelay) return null;
          return (
            <div key={i} style={{
              position: 'absolute',
              left: b.x - 600,
              top: b.y - 300,
              width: blockSize,
              height: blockSize,
              borderRadius: 10,
              background: b.color,
              opacity: bp,
              transform: `scale(${bp})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: 'Inter, sans-serif',
              fontSize: 24,
              fontWeight: 700,
              color: COLORS.background.dark,
              boxShadow: `0 0 15px ${b.color}44`,
            }}>
              {i + 1}
            </div>
          );
        })}
      </div>

      {/* Labels */}
      <AnimatedEntrance type="slideUp" delay={80} style={{position: 'absolute', left: 650, top: 620}}>
        <div style={{
          ...TYPOGRAPHY.caption,
          color: COLORS.accent.teal,
          fontSize: 24,
        }}>
          7个文创维度 + 4个口语维度
        </div>
      </AnimatedEntrance>

      <SubtitleSequence segments={AUDIO_SEGMENTS.whatToEval} />
    </AbsoluteFill>
  );
};
