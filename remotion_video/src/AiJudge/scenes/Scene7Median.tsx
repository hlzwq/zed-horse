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

export const Scene7Median: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const segStart = AUDIO_SEGMENTS.median[0].startFrame;

  const scores = [85, 88, 82];
  const sorted = [...scores].sort((a, b) => a - b);
  const median = sorted[1];
  const avg = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);

  // Score lines animate in
  const lineProgress = spring({frame: frame - (segStart + 10), fps, config: SPRING.smooth});

  // Average crossed out
  const crossProgress = spring({frame: frame - (segStart + 50), fps, config: {damping: 200}});

  // Median highlighted
  const highlightProgress = spring({frame: frame - (segStart + 70), fps, config: SPRING.bouncy});

  const scoreColors = [COLORS.models.alpha, COLORS.models.gamma, COLORS.models.beta];
  const sortedColors = [scoreColors[2], scoreColors[0], scoreColors[1]]; // sorted order colors

  return (
    <AbsoluteFill>
      <SceneBg />
      <AmbientParticles seed={7} />

      {/* Title */}
      <AnimatedEntrance type="fade" delay={segStart} style={{position: 'absolute', left: 100, top: 60}}>
        <div style={{
          ...TYPOGRAPHY.heading,
          fontSize: 44,
          color: COLORS.accent.yellow,
        }}>
          取中位数，不取平均数
        </div>
      </AnimatedEntrance>

      {/* Left: Average (crossed out) */}
      <AnimatedEntrance type="slideRight" delay={segStart + 10}
        style={{position: 'absolute', left: 120, top: 220}}>
        <div style={{
          background: COLORS.background.medium,
          border: `2px solid ${COLORS.neutral.darkGray}`,
          borderRadius: 16,
          padding: '32px 40px',
          width: 400,
          opacity: lineProgress,
        }}>
          <div style={{
            ...TYPOGRAPHY.caption,
            fontSize: 28,
            color: COLORS.neutral.lightGray,
            marginBottom: 16,
          }}>
            平均数
          </div>
          <div style={{
            fontFamily: 'Inter, sans-serif',
            fontSize: 64,
            fontWeight: 700,
            color: COLORS.neutral.darkGray,
            position: 'relative',
            display: 'inline-block',
          }}>
            ({scores.join(' + ')}) ÷ 3 = {avg}
            {/* Cross-out line */}
            {frame >= segStart + 50 && (
              <div style={{
                position: 'absolute',
                left: -10,
                top: '50%',
                width: '120%',
                height: 4,
                background: COLORS.accent.rose,
                transform: `scaleX(${crossProgress})`,
                transformOrigin: 'left',
                borderRadius: 2,
              }} />
            )}
          </div>
          <div style={{
            ...TYPOGRAPHY.caption,
            fontSize: 24,
            color: COLORS.accent.rose,
            marginTop: 12,
          }}>
            ✘ 容易被极端值拉偏
          </div>
        </div>
      </AnimatedEntrance>

      {/* Right: Median (highlighted) */}
      <AnimatedEntrance type="slideUp" delay={segStart + 30}
        style={{position: 'absolute', right: 150, top: 200}}>
        <div style={{
          background: COLORS.background.medium,
          border: `3px solid ${COLORS.accent.yellow}`,
          borderRadius: 16,
          padding: '32px 40px',
          width: 500,
          boxShadow: `0 0 30px ${COLORS.accent.yellow}33`,
        }}>
          <div style={{
            ...TYPOGRAPHY.caption,
            fontSize: 28,
            color: COLORS.accent.yellow,
            marginBottom: 16,
          }}>
            中位数 ✓
          </div>

          {/* Three score bars */}
          <div style={{display: 'flex', flexDirection: 'column', gap: 16}}>
            {sorted.map((s, i) => {
              const isMedian = s === median;
              const barW = interpolate(s, [0, 100], [0, 350]);
              const hlScale = isMedian ? highlightProgress : 1;
              return (
                <div key={i} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  transform: isMedian ? `scale(${1 + (hlScale - 1) * 0.08})` : 'none',
                  transformOrigin: 'left',
                }}>
                  <div style={{
                    fontFamily: 'Inter, sans-serif',
                    fontSize: 32,
                    fontWeight: 700,
                    color: sortedColors[i],
                    width: 50,
                    textAlign: 'right',
                  }}>
                    {s}
                  </div>
                  <div style={{
                    width: barW,
                    height: 20,
                    borderRadius: 10,
                    background: sortedColors[i],
                    opacity: isMedian ? 1 : 0.5,
                    boxShadow: isMedian ? `0 0 12px ${sortedColors[i]}` : 'none',
                  }} />
                  {isMedian && (
                    <div style={{
                      ...TYPOGRAPHY.caption,
                      fontSize: 24,
                      color: COLORS.accent.yellow,
                      fontWeight: 700,
                    }}>
                      ← 中位数
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div style={{
            ...TYPOGRAPHY.caption,
            fontSize: 24,
            color: COLORS.accent.teal,
            marginTop: 20,
          }}>
            至少两个模型同意才能站住
          </div>
        </div>
      </AnimatedEntrance>

      <SubtitleSequence segments={AUDIO_SEGMENTS.median} />
    </AbsoluteFill>
  );
};
