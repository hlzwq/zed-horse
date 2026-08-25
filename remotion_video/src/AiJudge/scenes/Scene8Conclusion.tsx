import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {COLORS, TYPOGRAPHY, AUDIO_SEGMENTS} from '../constants';
import {SPRING} from '../components/SharedComponents';
import {
  SceneBg,
  AmbientParticles,
  AnimatedEntrance,
  AIRobot,
  CageSVG,
} from '../components/SharedComponents';
import {SubtitleSequence} from '../components/SubtitleSequence';

export const Scene8Conclusion: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const segStart = AUDIO_SEGMENTS.conclusion[0].startFrame;

  // Cage labels animation
  const cageLabels = ['维度公开', '独立评分', '中位数'];
  const labelDelays = [segStart + 80, segStart + 100, segStart + 120];

  // Final slogan
  const sloganProgress = spring({frame: frame - (segStart + 140), fps, config: SPRING.gentle});

  // Global fade out at end
  const sceneDur = AUDIO_SEGMENTS.conclusion[0].endFrame - segStart;
  const globalFade = interpolate(frame, [segStart + sceneDur - 30, segStart + sceneDur], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{opacity: globalFade}}>
      <SceneBg />
      <AmbientParticles seed={8} count={30} />

      {/* AI Robot in cage */}
      <div style={{position: 'absolute', left: 610, top: 100, zIndex: 5}}>
        <AIRobot size={160} animateIn startFrame={segStart + 5} />
      </div>

      {/* Cage over robot */}
      <div style={{position: 'absolute', left: 510, top: 30, zIndex: 6}}>
        <CageSVG
          size={450}
          animateIn
          startFrame={segStart + 30}
          labels={cageLabels}
          glowing
        />
      </div>

      {/* Main conclusion text */}
      <AnimatedEntrance type="slideUp" delay={segStart + 10}
        style={{position: 'absolute', left: 100, top: 600}}>
        <div style={{
          ...TYPOGRAPHY.body,
          fontSize: 40,
          maxWidth: 800,
          lineHeight: 1.6,
        }}>
          前提不是相信它天生公正
        </div>
      </AnimatedEntrance>

      <AnimatedEntrance type="slideUp" delay={segStart + 40}
        style={{position: 'absolute', left: 100, top: 680}}>
        <div style={{
          ...TYPOGRAPHY.body,
          fontSize: 40,
          color: COLORS.accent.yellow,
          fontWeight: 700,
        }}>
          是先把它关进一套足够硬的制度笼子里
        </div>
      </AnimatedEntrance>

      {/* Final slogan */}
      {frame >= segStart + 140 && (
        <div style={{
          position: 'absolute',
          left: '50%',
          top: 850,
          transform: `translateX(-50%) scale(${sloganProgress})`,
          opacity: sloganProgress,
        }}>
          <div style={{
            ...TYPOGRAPHY.title,
            fontSize: 72,
            color: COLORS.accent.yellow,
            textAlign: 'center',
            textShadow: `0 0 40px ${COLORS.accent.yellow}66`,
          }}>
            笼子关好了，谁都服
          </div>
        </div>
      )}

      <SubtitleSequence segments={AUDIO_SEGMENTS.conclusion} />
    </AbsoluteFill>
  );
};
