/**
 * StepFun TTS Audio Generator for AiJudge video
 * Uses stepaudio-2.5-tts model with contextual instructions
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const API_KEY = process.env.STEP_API_KEY || '58Qtik5K5LO9ZSV4GrHf6gdkiYHWoZPw6vCZJFQfDdr0w0XSQVA5Bq5bdUicnvrPy';
const API_URL = 'https://api.stepfun.com/v1/audio/speech';
const MODEL = 'stepaudio-2.5-tts';
const VOICE = 'cixingnansheng'; // 慈祥男声 — 适合解说风格
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'audio', 'narration');

// Narration segments
const SEGMENTS = [
  {key: 'hook', text: '如果你参加比赛，评委是AI——你会不会心里咯噔一下？',
   instruction: '语速中等偏快，带悬念感，像在跟观众抛出一个有趣的问题'},
  {key: 'doubt', text: '评分标准谁定的？有没有人偷偷塞了小纸条？这些质疑，全部合理。但AI做评委，可以做到让人服气。前提是——把它关进笼子里。',
   instruction: '前两句快速带质疑语气，中间转折加重语气，最后"关进笼子里"放慢加重，有戏剧感'},
  {key: 'whatToEval', text: '先说评什么。不是随便丢给AI说你挑最好的。而是先把什么叫好拆清楚，每个维度都有明确说法。',
   instruction: '解说风格，语速适中，条理清晰，像老师在讲解一个概念'},
  {key: 'sevenDims', text: '文创和旅游推荐部分，七个维度：主题契合度，跟航线有关还是纯炫技？创意独特性，让人哇还是哦？视觉完成度，草稿级还是出版级？信息准确性，写的价格景点对不对？实用性，看完想不想真去？文案表达，人话还是机器话？传播效果，转发出去有人看吗？',
   instruction: '每个维度名字稍微加重，后面的解释快速带过，像在快速盘点清单。保持节奏感，不拖沓'},
  {key: 'fourDims', text: '英语口语展示部分，四个维度：表达流利度，是自然连贯，还是磕磕绊绊找词？用词准确性，用词地道还是中式英语硬翻？语音语调，发音清晰度、重音节奏对不对？内容表达力，能不能把航线亮点说清楚、说吸引人？所有维度，评审前公示，参赛队可以提意见。维度本身就是权力，必须公开。',
   instruction: '前四个维度节奏与上一段类似，"所有维度评审前公示"开始放慢，"必须公开"加重语气，有宣告感'},
  {key: 'threeModels', text: '再说怎么评。三个不同模型独立打分，互不通气。',
   instruction: '语速偏快，简洁有力，"三个不同模型"加重，"互不通气"稍停顿后强调'},
  {key: 'median', text: '最后取三个模型的中位数，不是平均数。至少两个模型同意的结果才能站住。',
   instruction: '解说的同时带一点得意感，"中位数"和"不是平均数"形成对比强调，最后一句稳重收尾'},
  {key: 'conclusion', text: 'AI可以做评委。但前提不是相信它天生公正，是先把它关进一套足够硬的制度笼子里。笼子关好了，出来的结果，谁都服。',
   instruction: '整体放慢，语气沉稳有力，像在做最后的总结陈词。"笼子关好了"停顿，"谁都服"放慢加重，收束有力'},
];

function generateTTS(segment) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      voice: VOICE,
      input: segment.text,
      instruction: segment.instruction,
    });

    const options = {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    };

    const req = https.request(API_URL, options, (res) => {
      if (res.statusCode !== 200) {
        let errData = '';
        res.on('data', (chunk) => errData += chunk);
        res.on('end', () => {
          reject(new Error(`HTTP ${res.statusCode}: ${errData}`));
        });
        return;
      }

      const outputPath = path.join(OUTPUT_DIR, `${segment.key}_0.mp3`);
      const ws = fs.createWriteStream(outputPath);
      res.pipe(ws);
      ws.on('finish', () => {
        const stats = fs.statSync(outputPath);
        console.log(`  ✓ ${segment.key}_0.mp3 (${(stats.size / 1024).toFixed(1)}KB)`);
        resolve(outputPath);
      });
      ws.on('error', reject);
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  // Ensure output directory exists
  fs.mkdirSync(OUTPUT_DIR, {recursive: true});

  console.log(`Generating TTS for ${SEGMENTS.length} segments using StepFun ${MODEL}...`);
  console.log(`Voice: ${VOICE}`);
  console.log(`Output: ${OUTPUT_DIR}\n`);

  for (let i = 0; i < SEGMENTS.length; i++) {
    const seg = SEGMENTS[i];
    console.log(`[${i + 1}/${SEGMENTS.length}] ${seg.key}...`);
    try {
      await generateTTS(seg);
    } catch (err) {
      console.error(`  ✗ Failed: ${err.message}`);
      // Retry once
      console.log(`  Retrying...`);
      try {
        await generateTTS(seg);
      } catch (err2) {
        console.error(`  ✗ Retry failed: ${err2.message}`);
      }
    }
    // Small delay between requests
    await new Promise(r => setTimeout(r, 500));
  }

  console.log('\nDone! All TTS files generated.');
}

main().catch(console.error);
