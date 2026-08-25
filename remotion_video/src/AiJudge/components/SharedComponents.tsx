import React from 'react';
import {spring, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {COLORS} from '../constants';

// ── Spring presets ──────────────────────────────────────────
export const SPRING = {
  smooth: {damping: 200},
  snappy: {damping: 20, stiffness: 200},
  bouncy: {damping: 8},
  gentle: {damping: 30, stiffness: 50},
};

// ── Scene Background ───────────────────────────────────────
export const SceneBg: React.FC<{id?: string}> = ({id}) => (
  <div
    style={{
      position: 'absolute',
      inset: 0,
      background: `linear-gradient(135deg, ${COLORS.background.dark} 0%, ${COLORS.background.medium} 100%)`,
      zIndex: 0,
    }}
    id={id}
  />
);

// ── Ambient Particles ──────────────────────────────────────
export const AmbientParticles: React.FC<{count?: number; seed?: number}> = React.memo(
  ({count = 25, seed = 42}) => {
    const particles = React.useMemo(() => {
      const arr = [];
      for (let i = 0; i < count; i++) {
        const s = seed + i * 7;
        arr.push({
          x: ((s * 13) % 1920),
          y: ((s * 17) % 1080),
          r: 2 + (s % 4),
          opacity: 0.1 + (s % 5) * 0.06,
          delay: (s * 3) % 60,
        });
      }
      return arr;
    }, [count, seed]);

    const frame = useCurrentFrame();

    return (
      <div style={{position: 'absolute', inset: 0, zIndex: 1, pointerEvents: 'none'}}>
        {particles.map((p, i) => {
          const y = p.y + Math.sin((frame + p.delay) * 0.02) * 8;
          const x = p.x + Math.cos((frame + p.delay) * 0.015) * 5;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: p.r,
                height: p.r,
                borderRadius: '50%',
                background: COLORS.accent.teal,
                opacity: p.opacity,
              }}
            />
          );
        })}
      </div>
    );
  },
);
AmbientParticles.displayName = 'AmbientParticles';

// ── AnimatedEntrance ───────────────────────────────────────
interface AnimatedEntranceProps {
  children: React.ReactNode;
  type?: 'fade' | 'scale' | 'slideLeft' | 'slideRight' | 'slideUp';
  delay?: number;
  style?: React.CSSProperties;
}

export const AnimatedEntrance: React.FC<AnimatedEntranceProps> = ({
  children,
  type = 'fade',
  delay = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: SPRING.smooth,
  });

  const getTransform = () => {
    switch (type) {
      case 'scale':
        return `scale(${progress})`;
      case 'slideLeft':
        return `translateX(${interpolate(progress, [0, 1], [-80, 0])}px)`;
      case 'slideRight':
        return `translateX(${interpolate(progress, [0, 1], [80, 0])}px)`;
      case 'slideUp':
        return `translateY(${interpolate(progress, [0, 1], [60, 0])}px)`;
      default:
        return 'none';
    }
  };

  if (frame < delay) return null;

  return (
    <div
      style={{
        opacity: progress,
        transform: getTransform(),
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// ── AI Robot SVG ───────────────────────────────────────────
export const AIRobot: React.FC<{
  size?: number;
  color?: string;
  animateIn?: boolean;
  startFrame?: number;
  style?: React.CSSProperties;
}> = ({size = 200, color, animateIn, startFrame = 0, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const mainColor = color || COLORS.accent.teal;

  const scale = animateIn
    ? spring({frame: frame - startFrame, fps, config: SPRING.bouncy})
    : 1;

  const eyeGlow = interpolate(
    Math.sin(frame * 0.08),
    [-1, 1],
    [0.6, 1],
  );

  if (animateIn && frame < startFrame) return null;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      style={{transform: `scale(${scale})`, ...style}}
    >
      <defs>
        <radialGradient id="robotGlow" cx="50%" cy="30%" r="60%">
          <stop offset="0%" stopColor={COLORS.accent.yellow} stopOpacity="0.3" />
          <stop offset="100%" stopColor={mainColor} stopOpacity="0" />
        </radialGradient>
        <linearGradient id="robotBody" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={mainColor} />
          <stop offset="100%" stopColor={COLORS.background.light} />
        </linearGradient>
      </defs>
      {/* Body */}
      <rect x="50" y="70" width="100" height="90" rx="20" fill="url(#robotBody)" stroke={mainColor} strokeWidth="3" />
      {/* Head */}
      <rect x="55" y="30" width="90" height="60" rx="16" fill={COLORS.background.medium} stroke={mainColor} strokeWidth="2" />
      {/* Eyes */}
      <circle cx="80" cy="55" r="10" fill={COLORS.accent.yellow} opacity={eyeGlow} />
      <circle cx="120" cy="55" r="10" fill={COLORS.accent.yellow} opacity={eyeGlow} />
      <circle cx="80" cy="55" r="5" fill={COLORS.background.dark} />
      <circle cx="120" cy="55" r="5" fill={COLORS.background.dark} />
      {/* Antenna */}
      <line x1="100" y1="30" x2="100" y2="10" stroke={mainColor} strokeWidth="3" strokeLinecap="round" />
      <circle cx="100" cy="8" r="6" fill={COLORS.accent.rose} />
      {/* Glow */}
      <circle cx="100" cy="100" r="90" fill="url(#robotGlow)" />
      {/* Arms */}
      <rect x="25" y="85" width="25" height="12" rx="6" fill={mainColor} opacity="0.8" />
      <rect x="150" y="85" width="25" height="12" rx="6" fill={mainColor} opacity="0.8" />
    </svg>
  );
};

// ── Question Bubble ────────────────────────────────────────
export const QuestionBubble: React.FC<{
  x: number;
  y: number;
  delay?: number;
}> = ({x, y, delay = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = spring({frame: frame - delay, fps, config: SPRING.bouncy});
  const float = Math.sin((frame - delay) * 0.05) * 5;

  if (frame < delay) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y + float,
        fontSize: 48,
        color: COLORS.accent.yellow,
        opacity: scale,
        transform: `scale(${scale})`,
        fontFamily: 'Inter, sans-serif',
        fontWeight: 700,
        textShadow: `0 0 20px ${COLORS.accent.yellow}`,
      }}
    >
      ?
    </div>
  );
};

// ── Cage SVG ───────────────────────────────────────────────
export const CageSVG: React.FC<{
  size?: number;
  labels?: string[];
  animateIn?: boolean;
  startFrame?: number;
  glowing?: boolean;
}> = ({size = 400, labels, animateIn, startFrame = 0, glowing}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = animateIn
    ? spring({frame: frame - startFrame, fps, config: SPRING.bouncy})
    : 1;

  const glowOpacity = glowing
    ? interpolate(Math.sin(frame * 0.04), [-1, 1], [0.2, 0.6])
    : 0;

  if (animateIn && frame < startFrame) return null;

  const barCount = labels ? labels.length + 2 : 5;
  const barSpacing = (size * 0.7) / (barCount - 1);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{transform: `scale(${scale})`}}>
      <defs>
        <radialGradient id="cageGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={COLORS.accent.yellow} stopOpacity={String(glowOpacity)} />
          <stop offset="100%" stopColor={COLORS.accent.teal} stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Glow aura */}
      <circle cx={size/2} cy={size/2} r={size*0.45} fill="url(#cageGlow)" />
      {/* Dome top */}
      <ellipse cx={size/2} cy={size*0.15} rx={size*0.38} ry={size*0.08}
        fill="none" stroke={COLORS.accent.teal} strokeWidth="3" />
      {/* Base */}
      <line x1={size*0.1} y1={size*0.85} x2={size*0.9} y2={size*0.85}
        stroke={COLORS.accent.teal} strokeWidth="4" strokeLinecap="round" />
      {/* Bars */}
      {Array.from({length: barCount}).map((_, i) => {
        const x = size * 0.15 + i * barSpacing;
        return (
          <g key={i}>
            <line x1={x} y1={size*0.15} x2={x} y2={size*0.85}
              stroke={COLORS.accent.teal} strokeWidth="3" strokeLinecap="round" />
            {labels && labels[i - 1] && (
              <text
                x={x}
                y={size * 0.75}
                textAnchor="middle"
                fill={COLORS.accent.yellow}
                fontSize="16"
                fontFamily="NotoSansSC, sans-serif"
                fontWeight="600"
                transform={`rotate(-90, ${x}, ${size * 0.75})`}
              >
                {labels[i - 1]}
              </text>
            )}
          </g>
        );
      })}
      {/* Lock icon */}
      <rect x={size/2 - 12} y={size*0.82} width="24" height="18" rx="4"
        fill={COLORS.accent.rose} />
      <path d={`M${size/2 - 8},${size*0.82} L${size/2 - 8},${size*0.76} A8,8 0 0,1 ${size/2 + 8},${size*0.76} L${size/2 + 8},${size*0.82}`}
        fill="none" stroke={COLORS.accent.rose} strokeWidth="2" />
    </svg>
  );
};

// ── Dimension Node (FlowNode pattern) ──────────────────────
interface DimNodeProps {
  icon: React.ReactNode;
  label: string;
  sublabel: string;
  color: string;
  delay?: number;
  x: number;
  y: number;
}

export const DimensionNode: React.FC<DimNodeProps> = ({
  icon,
  label,
  sublabel,
  color,
  delay = 0,
  x,
  y,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const progress = spring({frame: frame - delay, fps, config: SPRING.snappy});
  const slideX = interpolate(progress, [0, 1], [-60, 0]);

  if (frame < delay) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: x + slideX,
        top: y,
        opacity: progress,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        background: `${COLORS.background.medium}`,
        border: `2px solid ${color}`,
        borderRadius: 12,
        padding: '12px 20px',
        minWidth: 320,
        boxShadow: `0 0 20px ${color}33`,
      }}
    >
      <div style={{flexShrink: 0}}>{icon}</div>
      <div>
        <div style={{
          fontFamily: 'NotoSansSC, sans-serif',
          fontSize: 28,
          fontWeight: 700,
          color,
        }}>
          {label}
        </div>
        <div style={{
          fontFamily: 'NotoSansSC, sans-serif',
          fontSize: 20,
          color: COLORS.text.secondary,
          marginTop: 4,
        }}>
          {sublabel}
        </div>
      </div>
    </div>
  );
};

// ── Radar Chart ────────────────────────────────────────────
export const RadarChart: React.FC<{
  x: number;
  y: number;
  size: number;
  activeAxes: number;
  color: string;
}> = ({x, y, size, activeAxes, color}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const axes = 7;
  const cx = size / 2;
  const cy = size / 2;
  const r = size * 0.4;

  const progress = spring({
    frame: frame - 30,
    fps,
    config: {damping: 30, stiffness: 60},
  });

  const points = Array.from({length: axes}).map((_, i) => {
    const angle = (Math.PI * 2 * i) / axes - Math.PI / 2;
    const isActive = i < activeAxes;
    const val = isActive ? r * 0.8 * progress : 0;
    return {
      x: cx + val * Math.cos(angle),
      y: cy + val * Math.sin(angle),
      gridX: cx + r * Math.cos(angle),
      gridY: cy + r * Math.sin(angle),
      active: isActive,
    };
  });

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
      style={{position: 'absolute', left: x, top: y}}>
      {/* Grid circles */}
      {[0.3, 0.6, 1].map((s, i) => (
        <circle key={i} cx={cx} cy={cy} r={r * s}
          fill="none" stroke={COLORS.neutral.darkGray} strokeWidth="1" opacity="0.3" />
      ))}
      {/* Grid lines */}
      {points.map((p, i) => (
        <line key={i} x1={cx} y1={cy} x2={p.gridX} y2={p.gridY}
          stroke={COLORS.neutral.darkGray} strokeWidth="1" opacity="0.3" />
      ))}
      {/* Data polygon */}
      {activeAxes > 0 && (
        <polygon
          points={points.filter(p => p.active).map(p => `${p.x},${p.y}`).join(' ')}
          fill={`${color}33`}
          stroke={color}
          strokeWidth="2"
        />
      )}
      {/* Axis dots */}
      {points.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={4}
          fill={p.active ? color : COLORS.neutral.darkGray} />
      ))}
    </svg>
  );
};

// ── Brain SVG ──────────────────────────────────────────────
export const BrainSVG: React.FC<{
  size?: number;
  color: string;
  score?: number;
  delay?: number;
  label?: string;
}> = ({size = 160, color, score, delay = 0, label}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = spring({frame: frame - delay, fps, config: SPRING.bouncy});

  if (frame < delay) return null;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 12,
      opacity: scale,
      transform: `scale(${scale})`,
    }}>
      <svg width={size} height={size} viewBox="0 0 160 160">
        <defs>
          <radialGradient id={`brainGrad-${color}`} cx="50%" cy="40%" r="60%">
            <stop offset="0%" stopColor={color} stopOpacity="0.4" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </radialGradient>
        </defs>
        <circle cx="80" cy="80" r="70" fill={`url(#brainGrad-${color})`} />
        {/* Brain shape */}
        <path d="M80,30 C50,30 30,55 30,80 C30,105 50,130 80,130 C110,130 130,105 130,80 C130,55 110,30 80,30 Z"
          fill={COLORS.background.medium} stroke={color} strokeWidth="3" />
        {/* Brain grooves */}
        <path d="M55,65 Q80,50 105,65" fill="none" stroke={color} strokeWidth="2" opacity="0.6" />
        <path d="M50,85 Q80,70 110,85" fill="none" stroke={color} strokeWidth="2" opacity="0.6" />
        <path d="M55,105 Q80,90 105,105" fill="none" stroke={color} strokeWidth="2" opacity="0.6" />
        {/* Center pulse */}
        <circle cx="80" cy="80" r="8" fill={color} opacity={0.5 + Math.sin(frame * 0.1) * 0.3} />
      </svg>
      {score !== undefined && (
        <div style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 48,
          fontWeight: 700,
          color,
          textShadow: `0 0 15px ${color}`,
        }}>
          {score}
        </div>
      )}
      {label && (
        <div style={{
          fontFamily: 'NotoSansSC, sans-serif',
          fontSize: 24,
          color: COLORS.text.secondary,
        }}>
          {label}
        </div>
      )}
    </div>
  );
};

// ── Stamp Effect ───────────────────────────────────────────
export const Stamp: React.FC<{
  text: string;
  color?: string;
  delay?: number;
}> = ({text, color, delay = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const progress = spring({frame: frame - delay, fps, config: {...SPRING.bouncy, stiffness: 300}});
  const scale = interpolate(progress, [0, 0.6, 1], [2, 0.9, 1]);

  if (frame < delay) return null;

  return (
    <div style={{
      transform: `scale(${scale})`,
      opacity: progress,
      border: `4px solid ${color || COLORS.accent.rose}`,
      borderRadius: 12,
      padding: '16px 32px',
      fontFamily: 'NotoSansSC, sans-serif',
      fontSize: 48,
      fontWeight: 700,
      color: color || COLORS.accent.rose,
      textShadow: `0 0 20px ${color || COLORS.accent.rose}66`,
      background: `${COLORS.background.dark}cc`,
    }}>
      {text}
    </div>
  );
};
