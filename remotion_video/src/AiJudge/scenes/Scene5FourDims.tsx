import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {SPRING} from '../components/SharedComponents';
import {
  SceneBg,
  AmbientParticles,
  DimensionNode,
  Stamp,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

const DIMS = [
  {icon: '🌊', label: '表达流利度', sub: '自然连贯，还是磕磕绊绊？', color: COLORS.models.alpha},
  {icon: '📖', label: '用词准确性', sub: '地道还是中式英语硬翻？', color: COLORS.models.beta},
  {icon: '🎵', label: '语音语调', sub: '发音清晰度、重音节奏', color: COLORS.models.gamma},
  {icon: '🎤', label: '内容表达力', sub: '把亮点说清楚、说吸引人', color: COLORS.accent.rose},
];

// Waveform visualization
const Waveform: React.FC<{x: number; y: number; active: number}> = ({x, y, active}) => {
  const frame = useCurrentFrame();
  const bars = 40;
  return (
    <svg width={450} height={200} viewBox="0 0 450 200" style={{position: 'absolute', left: x, top: y}}>
      {Array.from({length: bars}).map((_, i) => {
        const isActive = i < active * 10;
        const h = isActive
          ? 30 + Math.sin((frame * 0.08 + i * 0.3)) * 40 + Math.cos(i * 0.5) * 20
          : 10;
        const color = isActive ? COLORS.accent.teal : COLORS.neutral.darkGray;
        return (
          <rect key={i} x={i * 11} y={100 - h / 2} width={7} height={h} rx={3}
            fill={color} opacity={isActive ? 0.8 : 0.3} />
        );
      })}
    </svg>
  );
};

export const Scene5FourDims: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const stampDelay = AUDIO_SEGMENTS.fourDims[0].endFrame - 60;

  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={5} />

      {/* Title */}
      <div style={{
        position: 'absolute',
        left: 100,
        top: 70,
        ...TYPOGRAPHY.heading,
        fontSize: 44,
        color: COLORS.accent.rose,
      }}>
        英语口语展示 · 四个维度
      </div>

      {/* Left: dimension nodes */}
      {DIMS.map((d, i) => (
        <DimensionNode
          key={i}
          icon={<span style={{fontSize: 36}}>{d.icon}</span>}
          label={d.label}
          sublabel={d.sub}
          color={d.color}
          delay={AUDIO_SEGMENTS.fourDims[0].startFrame + i * 30}
          x={80}
          y={160 + i * 130}
        />
      ))}

      {/* Right: waveform */}
      <Waveform x={1050} y={200} active={frame > 50 ? 4 : frame > 30 ? 2 : 0} />

      {/* Stamp: 公示 */}
      <div style={{position: 'absolute', right: 200, top: 500}}>
        <Stamp text="公 示" delay={stampDelay} />
      </div>

      {/* 公示说明 */}
      {frame >= stampDelay + 10 && (
        <div style={{
          position: 'absolute',
          right: 140,
          top: 620,
          ...TYPOGRAPHY.caption,
          fontSize: 24,
          color: COLORS.text.secondary,
          textAlign: 'center',
          maxWidth: 350,
        }}>
          维度本身就是权力，必须公开
        </div>
      )}

      <SubtitleSequence segments={AUDIO_SEGMENTS.fourDims} />
    </AbsoluteFill>
  );
};
