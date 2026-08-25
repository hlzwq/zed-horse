import {loadFont as loadNotoSC, fontFamily as notoSCFamily} from '@remotion/google-fonts/NotoSansSC';
import {loadFont as loadInter, fontFamily as interFamily} from '@remotion/google-fonts/Inter';

// ── Fonts ──────────────────────────────────────────────────
loadNotoSC();
loadInter();

export const FONTS = {
  chinese: notoSCFamily,
  english: interFamily,
};

// ── Colors (Deep Space Palette) ────────────────────────────
export const COLORS = {
  background: {
    dark: '#1a1a2e',
    medium: '#16213e',
    light: '#0f3460',
  },
  accent: {
    rose: '#e94560',
    yellow: '#f9ed69',
    teal: '#00b8a9',
  },
  neutral: {
    white: '#ffffff',
    lightGray: '#b2bec3',
    darkGray: '#636e72',
    muted: '#2d3436',
  },
  text: {
    primary: '#ffffff',
    secondary: '#dfe6e9',
    muted: '#b2bec3',
  },
  semantic: {
    positive: '#00b894',
    negative: '#e17055',
    neutral: '#74b9ff',
  },
  sceneBg: {
    space: ['#1a1a2e', '#16213e'],
  },
  models: {
    alpha: '#4facfe',
    beta: '#38ef7d',
    gamma: '#a855f7',
  },
};

// ── Typography ─────────────────────────────────────────────
export const FONT_SIZES = {
  title: 96,
  heading: 64,
  body: 48,
  caption: 36,
  tiny: 32,
  minimum: 32,
};

export const TYPOGRAPHY: Record<string, React.CSSProperties> = {
  title: {
    fontFamily: FONTS.chinese,
    fontSize: FONT_SIZES.title,
    fontWeight: 700,
    color: COLORS.text.primary,
    textShadow: '0 4px 20px rgba(0,0,0,0.5)',
  },
  heading: {
    fontFamily: FONTS.chinese,
    fontSize: FONT_SIZES.heading,
    fontWeight: 600,
    color: COLORS.text.primary,
  },
  body: {
    fontFamily: FONTS.chinese,
    fontSize: FONT_SIZES.body,
    fontWeight: 400,
    color: COLORS.text.primary,
  },
  caption: {
    fontFamily: FONTS.chinese,
    fontSize: FONT_SIZES.caption,
    fontWeight: 400,
    color: COLORS.text.secondary,
  },
  emphasis: {
    fontFamily: FONTS.chinese,
    fontSize: FONT_SIZES.body,
    fontWeight: 700,
    color: COLORS.accent.yellow,
  },
  number: {
    fontFamily: FONTS.english,
    fontSize: 72,
    fontWeight: 700,
    color: COLORS.text.primary,
  },
};

// ── Transitions ────────────────────────────────────────────
export const TRANSITION_DURATION = 15;
export const SCENE_PAD = 15;
export const SEGMENT_GAP = 6;

// ── Audio durations (from StepFun TTS, measured via music-metadata) ──
// hook: 3.77s=114f, doubt: 12.55s=377f, whatToEval: 10.03s=301f
// sevenDims_0: 16.13s=484f, sevenDims_1: 9.55s=287f (combined: 771f + 6gap = 777f)
// fourDims: 30.89s=927f, threeModels: 4.73s=142f, median: 6.00s=180f
// conclusion: 10.99s=330f

// ── Scenes (global frames — rebuilt from actual audio) ─────
// Algorithm: scene = PAD + segments(audioFrames + GAP) + PAD
// scene1:  15 + (114+6) + 15 = 150
// scene2:  15 + (377+6) + 15 = 413
// scene3:  15 + (301+6) + 15 = 337
// scene4:  15 + (484+6+287+6) + 15 = 813
// scene5:  15 + (927+6) + 15 = 963
// scene6:  15 + (142+6) + 15 = 178
// scene7:  15 + (180+6) + 15 = 216
// scene8:  15 + (330+6) + 15 = 366

export const SCENES = [
  {start: 0,    duration: 150},   // Scene 1: Hook
  {start: 165,  duration: 413},   // Scene 2: 质疑
  {start: 593,  duration: 337},   // Scene 3: 评什么引出
  {start: 945,  duration: 813},   // Scene 4: 文创七维度
  {start: 1773, duration: 963},   // Scene 5: 英语四维度+公示
  {start: 2751, duration: 178},   // Scene 6: 三模型独立
  {start: 2944, duration: 216},   // Scene 7: 中位数机制
  {start: 3175, duration: 366},   // Scene 8: 总结
];

export const TOTAL_FRAMES = 3541;

// ── Narration ──────────────────────────────────────────────
export const NARRATION = {
  hook: '如果你参加比赛，评委是AI——你会不会心里咯噔一下？',
  doubt: '评分标准谁定的？有没有人偷偷塞了小纸条？这些质疑，全部合理。但AI做评委，可以做到让人服气。前提是——把它关进笼子里。',
  whatToEval: '先说评什么。不是随便丢给AI说你挑最好的。而是先把什么叫好拆清楚，每个维度都有明确说法。',
  sevenDims: '文创和旅游推荐部分，七个维度：主题契合度，跟航线有关还是纯炫技？创意独特性，让人哇还是哦？视觉完成度，草稿级还是出版级？信息准确性，写的价格景点对不对？实用性，看完想不想真去？文案表达，人话还是机器话？传播效果，转发出去有人看吗？',
  fourDims: '英语口语展示部分，四个维度：表达流利度，是自然连贯，还是磕磕绊绊找词？用词准确性，用词地道还是中式英语硬翻？语音语调，发音清晰度、重音节奏对不对？内容表达力，能不能把航线亮点说清楚、说吸引人？所有维度，评审前公示，参赛队可以提意见。维度本身就是权力，必须公开。',
  threeModels: '再说怎么评。三个不同模型独立打分，互不通气。',
  median: '最后取三个模型的中位数，不是平均数。至少两个模型同意的结果才能站住。',
  conclusion: 'AI可以做评委。但前提不是相信它天生公正，是先把它关进一套足够硬的制度笼子里。笼子关好了，出来的结果，谁都服。',
};

// ── Audio Segments (LOCAL frames, from actual audio measurement) ──
export const AUDIO_SEGMENTS = {
  hook: [
    {text: NARRATION.hook, file: 'hook_0.mp3', startFrame: 15, endFrame: 135},
  ],
  doubt: [
    {text: NARRATION.doubt, file: 'doubt_0.mp3', startFrame: 15, endFrame: 398},
  ],
  whatToEval: [
    {text: NARRATION.whatToEval, file: 'whatToEval_0.mp3', startFrame: 15, endFrame: 322},
  ],
  sevenDims: [
    {text: NARRATION.sevenDims.slice(0, 60), file: 'sevenDims_0.mp3', startFrame: 15, endFrame: 505},
    {text: NARRATION.sevenDims.slice(60), file: 'sevenDims_1.mp3', startFrame: 511, endFrame: 798},
  ],
  fourDims: [
    {text: NARRATION.fourDims, file: 'fourDims_0.mp3', startFrame: 15, endFrame: 948},
  ],
  threeModels: [
    {text: NARRATION.threeModels, file: 'threeModels_0.mp3', startFrame: 15, endFrame: 163},
  ],
  median: [
    {text: NARRATION.median, file: 'median_0.mp3', startFrame: 15, endFrame: 201},
  ],
  conclusion: [
    {text: NARRATION.conclusion, file: 'conclusion_0.mp3', startFrame: 15, endFrame: 351},
  ],
};
