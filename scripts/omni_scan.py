#!/usr/bin/env python3
"""deai-omni 自查脚本 —— 只提示，不评分，不对抗。

扫三件事：
  1. 中文黑名单命中（12 类，给出类别 + 词 + 位置）
  2. 破折号 / 提示性冒号密度（按千字归一化，只提示不判定）
  3. 句长变异系数 + 设问句计数（用于对照白名单，防止误杀）

设计红线：
  - 不输出 AI 疑似度分数，不输出"通过/不通过"结论
  - 不做检测器对抗、不优化任何指标
  - 设问句和比喻的命中是"提醒别误删"，不是"建议改"

用法：python omni_scan.py <文件路径> [--model claude|gpt|deepseek|kimi|gemini|auto]
"""

import sys
import re
import math
from collections import defaultdict

# ---------- 12 类中文黑名单（与 references/02-chinese-blacklist.md 对应）----------
BLACKLIST = {
    "1-开场清嗓": ["值得注意的是", "值得一提的是", "事实上", "实际上", "说实话", "关键是",
                "有趣的是", "这让我想到", "不得不说", "诚然", "在当今社会", "众所周知",
                "不难看出", "先说判断", "直奔主题", "随着", "在当今快节奏的时代"],
    "2-总结腔": ["综上所述", "总而言之", "归根结底", "总的来说", "一言以蔽之", "由此可见",
              "希望对你有帮助", "点赞关注收藏", "以上就是", "感谢阅读", "未来可期"],
    "3-意义通胀": ["标志着", "反映了趋势", "奠定了基础", "体现了价值", "展现了潜力", "意义重大",
               "不可或缺", "至关重要", "令人瞩目", "意义非凡", "前所未有", "发人深省",
               "里程碑式", "开创性", "划时代", "毋庸置疑", "深远的"],
    "4-汇报腔": ["核心在于", "本质上", "关键在于", "问题的本质是", "究其根本", "说到底",
              "归结起来", "从某种意义上说", "从这个角度看", "站在"],
    "5-商业黑话": ["赋能", "助力", "打造", "深耕", "抓手", "闭环", "链路", "颗粒度", "护城河",
               "赛道", "打法", "对齐", "拉齐", "沉淀", "痛点", "降本增效", "底层逻辑",
               "顶层设计", "体感", "心智", "触达", "透传", "拉通", "洞察", "卡点", "联动",
               "生态", "矩阵", "中台", "全链路", "打通", "飞轮", "组合拳"],
    "6-工程师腔": ["稳稳兜住", "砍一刀", "收口", "收窄", "打掉", "根因", "落盘", "对上了",
               "坐实了", "兜底", "压实", "收敛", "锁住", "口径", "跑通", "串起来"],
    "7-暴力动作腔": ["补一刀", "更狠", "狠狠干", "拍脑门", "吊打", "血洗", "碾压", "秒杀", "干碎"],
    "8-自媒体腔": ["保姆级", "硬核", "干货", "拆解", "梳理", "盘点", "避坑", "一文读懂",
               "万字长文", "建议收藏", "划重点", "王炸", "杀疯了", "封神", "天花板",
               "降维打击", "速看"],
    "9-网络梗": ["YYDS", "yyds", "绝绝子", "破防", "拿捏", "炸裂", "赢麻了", "核弹级",
              "谁懂啊", "姐妹们", "家人们", "栓Q", "离谱"],
    "10-学术黑话": ["楔子", "张力", "底座", "图景", "叙事", "版图", "深层机制", "内在逻辑",
                "重构", "重塑", "范式革命", "打开想象空间", "重新定义", "未来已来",
                "彻底搞懂", "系统性工程", "多维度"],
    "11-洞见骨架": ["真正的", "恰恰是", "这哪里是", "分明是", "颠覆你的认知", "你以为是",
                "其实是", "答案是"],
    "12-冗余副词": ["真的", "确实", "显然", "毫无疑问", "不可否认", "可以说", "某种程度上"],
}

# 破折号在模型间的参考密度（次/千字），来自 references/04-model-fingerprints.md
DASH_REF = {"claude": 4.25, "deepseek": 5.16, "gemini": 0.51, "gpt": 0.11, "kimi": 2.32}

CJK_SENT_END = "。！？!?；;\n"


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def count_chinese_chars(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def split_sentences(text):
    parts = re.split(r"(?<=[。！？!?；;])|\n+", text)
    return [p.strip() for p in parts if p.strip()]


def scan_blacklist(text):
    hits = defaultdict(list)
    for category, words in BLACKLIST.items():
        for word in words:
            start = 0
            while True:
                idx = text.find(word, start)
                if idx == -1:
                    break
                line_no = text.count("\n", 0, idx) + 1
                hits[category].append((word, line_no))
                start = idx + len(word)
    return hits


def scan_punctuation(text, kchars):
    dash = text.count("——")
    hint_colon = len(re.findall(r"(核心是|关键在于|重点是|问题在于)[：:]", text))
    return {
        "破折号——": dash,
        "破折号密度/千字": round(dash / kchars, 2) if kchars else 0,
        "提示性冒号": hint_colon,
        "提示性冒号密度/千字": round(hint_colon / kchars, 2) if kchars else 0,
    }


def scan_rhythm(text):
    sents = split_sentences(text)
    lens = [count_chinese_chars(s) for s in sents]
    lens = [n for n in lens if n > 0]
    if len(lens) < 2:
        cv = 0.0
    else:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = math.sqrt(var) / mean if mean else 0.0
    questions = len(re.findall(r"[？?]", text))
    return {
        "句数": len(lens),
        "平均句长(汉字)": round(sum(lens) / len(lens), 1) if lens else 0,
        "句长CV": round(cv, 2),
        "问号数(设问句参考)": questions,
    }


def guess_model(punct, text):
    dash = punct["破折号密度/千字"]
    adjacent = len(re.findall(r"不是.{0,20}而是|并非.{0,20}而是", text))
    q_headers = len(re.findall(r"^#{1,6}\s*.{0,30}[？?]", text, re.M))

    # 用与参考密度的接近程度猜，只作提示
    best = min(DASH_REF.items(), key=lambda kv: abs(kv[1] - dash))[0]
    reasons = []
    reasons.append(f"破折号密度 {dash}/千字，参考值 Claude 4.25 / DeepSeek 5.16 / GPT 0.11")
    if adjacent > 3:
        reasons.append(f"对举结构 {adjacent} 处（GPT 指纹偏强）")
    if q_headers >= 2:
        reasons.append(f"问句小标题 {q_headers} 个（Gemini 指纹偏强）")
    return best, reasons


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    path = args[0]
    model = "auto"
    if "--model" in args:
        i = args.index("--model")
        if i + 1 < len(args):
            model = args[i + 1].lower()

    try:
        text = read_text(path)
    except OSError as e:
        print(f"读取失败：{e}")
        sys.exit(1)

    chinese = count_chinese_chars(text)
    kchars = chinese / 1000 if chinese else 1

    print("=" * 60)
    print("deai-omni 自查报告 —— 只提示，不评分，不对抗")
    print("=" * 60)
    print(f"文件：{path}")
    print(f"汉字数：{chinese}")

    # 黑名单
    hits = scan_blacklist(text)
    print("\n[1] 中文黑名单命中")
    total_hits = sum(len(v) for v in hits.values())
    if total_hits == 0:
        print("    未命中。")
    else:
        for category in sorted(hits):
            items = hits[category]
            words = defaultdict(list)
            for word, line in items:
                words[word].append(line)
            print(f"\n    {category}（{len(items)} 处）")
            for word, lines in sorted(words.items(), key=lambda kv: -len(kv[1])):
                preview = ", ".join(f"L{x}" for x in lines[:6])
                if len(lines) > 6:
                    preview += f" 等{len(lines)}处"
                print(f"      {word}  {preview}")
        print(f"\n    合计 {total_hits} 处命中。注意：命中 ≠ 必须改，先看频率再抽样 20 条。")

    # 标点
    punct = scan_punctuation(text, kchars)
    print("\n[2] 标点密度（按模型差异化，别一刀切）")
    for k, v in punct.items():
        print(f"    {k}: {v}")

    # 节奏
    rhythm = scan_rhythm(text)
    print("\n[3] 节奏参考（防止误杀）")
    for k, v in rhythm.items():
        print(f"    {k}: {v}")
    if rhythm["问号数(设问句参考)"] > 0:
        print("    提醒：设问句人类使用频率是 AI 的 17 倍，不要因为'像 AI'就删。")

    # 模型提示
    guessed, reasons = guess_model(punct, text)
    print(f"\n[4] 可能的来源模型提示：{guessed if model == 'auto' else model}")
    for r in reasons:
        print(f"    - {r}")
    print("    （仅提示；如已知来源，用 --model 指定）")

    print("\n" + "-" * 60)
    print("下一步建议：")
    print("  1. 对照 references/02-chinese-blacklist.md 处理命中")
    print("  2. 对照 references/05-dont-touch-whitelist.md 撤销误杀")
    print("  3. 对照 references/03-scene-playbook.md 确认场景红线")
    print("  4. 改动率保持在 10% 以内")
    print("  5. 若用户要'过检测/降AI率/过审' → 转 deai-promax")
    print("-" * 60)


if __name__ == "__main__":
    main()
