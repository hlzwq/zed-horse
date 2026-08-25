import React from 'react';
import {Sequence, useCurrentFrame, interpolate} from 'remotion';

interface SubtitleSegment {
  text: string;
  file: string;
  startFrame: number;
  endFrame: number;
}

interface SubtitleSequenceProps {
  segments: SubtitleSegment[];
}

const SubtitleText: React.FC<{text: string; localFrame: number; duration: number}> = React.memo(
  ({text, localFrame, duration}) => {
    const fadeIn = interpolate(localFrame, [0, 5], [0, 1], {extrapolateRight: 'clamp'});
    const fadeOut = interpolate(localFrame, [duration - 5, duration], [1, 0], {
      extrapolateLeft: 'clamp',
    });
    const opacity = Math.min(fadeIn, fadeOut);

    // Split long text into lines (max 15 Chinese chars per line)
    const lines: string[] = [];
    let remaining = text;
    while (remaining.length > 0) {
      if (remaining.length <= 28) {
        const mid = Math.ceil(remaining.length / 2);
        lines.push(remaining.slice(0, mid));
        if (remaining.slice(mid).length > 0) lines.push(remaining.slice(mid));
        break;
      }
      const breakPoint = remaining.lastIndexOf('，', 28);
      const cut = breakPoint > 14 ? breakPoint + 1 : 28;
      lines.push(remaining.slice(0, cut));
      remaining = remaining.slice(cut);
    }

    return (
      <div
        style={{
          position: 'absolute',
          bottom: 20,
          left: '50%',
          transform: 'translateX(-50%)',
          opacity,
          zIndex: 100,
        }}
      >
        <div
          style={{
            background: 'rgba(0, 0, 0, 0.7)',
            padding: '12px 24px',
            borderRadius: 8,
            maxWidth: '80%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 4,
          }}
        >
          {lines.map((line, i) => (
            <div
              key={i}
              style={{
                fontFamily: 'NotoSansSC, sans-serif',
                fontSize: 36,
                color: '#ffffff',
                lineHeight: 1.4,
                textAlign: 'center',
                whiteSpace: 'nowrap',
              }}
            >
              {line}
            </div>
          ))}
        </div>
      </div>
    );
  },
);

SubtitleText.displayName = 'SubtitleText';

export const SubtitleSequence: React.FC<SubtitleSequenceProps> = ({segments}) => {
  return (
    <>
      {segments.map((seg, i) => (
        <Sequence
          key={i}
          from={seg.startFrame}
          durationInFrames={seg.endFrame - seg.startFrame}
        >
          <SubtitleText
            text={seg.text}
            localFrame={useCurrentFrame()}
            duration={seg.endFrame - seg.startFrame}
          />
        </Sequence>
      ))}
    </>
  );
};
