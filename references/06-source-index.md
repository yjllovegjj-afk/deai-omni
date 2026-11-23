# 来源索引与可信度分级

本技能所有规则都来自下列来源。可信度分三级：**权威**（官方文件/学术研究/主流媒体）、**行业·有数据**（带样本的量化研究）、**自媒体**（具体可落地但需自行验证）。规则正文每条都标了对应来源编号 [Sxx]，可按此表回溯。

## 权威

| 编号 | 来源 | URL | 用在哪 |
|---|---|---|---|
| S01 | Wikipedia: Signs of AI writing（WikiProject AI Cleanup 维护） | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing | 24 模式底本、历史指标/无效指标分级 |
| S02 | scriptgrain 转录（Wikipedia 现行版条目交叉验证） | https://scriptgrain.com/blog/wikipedia-signs-of-ai-writing | 破折号降级为历史指标、2022–2026.9 时间范围 |
| S03 | IEEE Spectrum / aiincontext 采访 cleanup editor | https://aiincontext.com/articles/up-to-20-percent-of-new-wikipedia-articles-are-ai-generated-cleanup-editor-says-7e207f05 | delve 移入历史指标、2026 新词表 |
| S04 | seymourdigitalmedia（2026 新词表转录） | https://seymourdigitalmedia.com/is-that-facebook-comment-written-by-ai/ | quietly/steady/practical/matters/leverage、8–20 词短句化 |
| S05 | OpenAI GPT-6 Astra 开发者文档"个性与写作风格"（2025.9.5，微信转录） | http://mp.weixin.qq.com/s?__biz=MzE5OTAwMzAxOA==&mid=2247484561&idx=1&sn=8b17237dad924f4d3a7e0c59db0c1c88 | 官方禁词 8 类 + 扩展词表 |
| S06 | Anthropic Claude 官方提示词指南 | https://docs.anthropic.com/claude/docs | 禁浮夸隐喻、直白表达优先 |
| S07 | Graphite 研究（1万篇人类文章 vs AI 改写，约13000 特征短语，中文转录） | https://dong.xs91.com/archives/11347.html | this matters 116×、纠正式表达 100×+、模型口癖 |
| S08 | 光明日报"AI 新八股"（2026.5.17） | https://epaper.gmw.cn/gmrb/html/content/202605/17/content_13811.html | 结构固化/正确空话/内容同质化三表现 |
| S09 | 番茄小说官方公告（AI 创作标注与审核） | https://fanqienovel.com/writer/zone/article/7642544663915675672 | 番茄 AI 占比红线、200+ 维扫描 |
| S10 | 起点 AI 占比规则报道（新浪） | https://k.sina.cn/article_7879848900_1d5acf3c406803cvdu.html | >10% 撤榜砍流量 |
| S11 | 晋江 AI 使用规则（微信转录） | http://mp.weixin.qq.com/s?__biz=MzA5Mjc1NTE4Mw==&mid=2651295331&idx=1&sn=b7c5d97a03ed2c82147df4204486e981 | 仅许最低限度文字修正 |
| S12 | 微信公众号"非真人创作行为"条款（2026.3.27） | https://www.jxxy.net/ai/articles/xionghuanwei-2077214449849549198/ | 公众号新规、暗限流 4 维 |
| S13 | 小红书 AI 托管账号治理（2026.3.10，处理 60万+ 低质笔记） | https://www.jxxy.net/ai/articles/xionghuanwei-2077214449849549198/ | 小红书红线 |
| S14 | Google Cloud 统计 tells 研究（Karl Weinmeister, 2025.6） | https://devengoratela.com/2025/06/detecting-ai-generated-text-by-uncovering-its-statistical-tells-by-karl-weinmeister-google-cloud-community-jun-2025/ | 统计特征 |
| S15 | AI Writing Benchmark（模型"最不像 AI"对比） | https://aiwritingbenchmark.com/insights/which-ai-sounds-least-like-ai | Claude/GPT/Gemini 检测率 |

## 行业·有数据

| 编号 | 来源 | URL | 用在哪 |
|---|---|---|---|
| S16 | lieflat 283 万字语料研究（wiselychen） | https://ai-coding.wiselychen.com/lieflat-less-ai-tone-corpus-study-em-dash | 5 模型倍率表、AI vs 人类倍率、26 项假设仅 11 项成立 |
| S17 | XINGMENG2333 dsh-plugin-optimize-ai-reply 核对报告 | https://github.com/XINGMENG2333/dsh-plugin-optimize-ai-reply/blob/main/docs/source-notes.md | 模型指纹交叉验证、推翻项 |
| S18 | freeyong 转录（283 万字研究讨论） | https://www.freeyong.com/5538.html | 设问句 17 倍、句长 CV 无差异的复述 |
| S19 | humanizethisai 模型对比 | https://humanizethisai.com/blog/rewrite-ai-text-sound-human | 模型偏好词、检测率 |
| S20 | 连享会（学术写作去 AI 味） | https://mp.weixin.qq.com/s/do_6C0YsBqVQV8Y1m5xYzA | 中文学术黑话、翻译腔 |
| S21 | SkillMD content-craft / de-ai-writing | https://www.skillmd.com/ | 翻译腔四件套、中文词表 |
| S22 | 素笔 AI（去 AI 味替换原则） | https://www.sub.ai/ | "写出具体动作或可验证信息，写不出就整句删" |
| S23 | ContentAny（各平台人味标准） | https://www.contentany.cn/ | 公众号/小红书/短视频人味差异 |
| S24 | AiLv 降低 AI 率指南 | https://www.ailv.run/cn/blog/manual-reduce-ai | 25–30% 安全线、平台差异 |
| S25 | seoskill: AI slop 清单 | https://seoskill.dev/blog/ai-slop | 破折号弱指标、2026 套话 |

## 自媒体（具体可用，自行验证）

| 编号 | 来源 | URL | 用在哪 |
|---|---|---|---|
| S26 | 青蓝智慧 17 项 AI 特征 | https://icyanblue.com/post/7889.html | 2026 新中文套话（真正/恰恰等） |
| S27 | 觉醒学院（平台新规解读） | https://www.jxxy.net/ai/articles/xionghuanwei-2077214449849549198/ | 四场景红线 |

## 本机已有技能（借鉴来源）

| 技能 | 路径 | 借鉴了什么 |
|---|---|---|
| humanizer v2.1.1 | `$HOME/.workbuddy/skills/humanizer/` | 24 模式底本（英文维基旧版） |
| deai-promax v1.0 | `$HOME/.workbuddy/skills/deai-promax/` | 误杀防护白名单思想、改动率红线<10%、场景化分支、前置诊断思路 |

## 检索方法说明

- Wikipedia 原页两次网络阻断，用 S02/S03/S04 三个独立转录源交叉验证现行版内容。
- 文心一言等国产模型未找到可信量化数据，相关条目标 `TBD-需实测`，不编造。
- 剔除纯鸡汤类内容（"用AI要真诚"等），只保留具体、可操作、有例子的规则。
