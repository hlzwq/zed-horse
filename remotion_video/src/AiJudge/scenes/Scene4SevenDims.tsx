import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {
  SceneBg,
  AmbientParticles,
  DimensionNode,
  RadarChart,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

const DIMS = [
  {icon: '🎯', label: '主题契合度', sub: '跟航线有关还是纯炫技？', color: COLORS.accent.rose},
  {icon: '💡', label: '创意独特性', sub: '让人"哇"还是"哦"？', color: COLORS.accent.yellow},
  {icon: '🎨', label: '视觉完成度', sub: '草稿级还是出版级？', color: COLORS.accent.teal},
  {icon: '✅', label: '信息准确性', sub: '写的价格景点对不对？', color: COLORS.semantic.positive},
  {icon: '🧭', label: '实用性', sub: '看完想不想真去？', color: COLORS.semantic.neutral},
  {icon: '💬', label: '文案表达', sub: '人话还是机器话？', color: COLORS.accent.rose},
  {icon: '📢', label: '传播效果', sub: '转发出去有人看吗？', color: COLORS.accent.yellow},
];

export const Scene4SevenDims: React.FC = () => {
  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={4} />

      {/* Title */}
      <div style={{
        position: 'absolute',
        left: 100,
        top: 70,
        ...TYPOGRAPHY.heading,
        fontSize: 44,
        color: COLORS.accent.teal,
      }}>
        文创 & 旅游推荐 · 七个维度
      </div>

      {/* Left: dimension nodes (staggered) */}
      {DIMS.map((d, i) => (
        <DimensionNode
          key={i}
          icon={<span style={{fontSize: 36}}>{d.icon}</span>}
          label={d.label}
          sublabel={d.sub}
          color={d.color}
          delay={AUDIO_SEGMENTS.sevenDims[0].startFrame + i * 25}
          x={80}
          y={140 + i * 110}
        />
      ))}

      {/* Right: radar chart */}
      <RadarChart
        x={1100}
        y={120}
        size={550}
        activeAxes={7}
        color={COLORS.accent.teal}
      />

      <SubtitleSequence segments={AUDIO_SEGMENTS.sevenDims} />
    </AbsoluteFill>
  );
};
