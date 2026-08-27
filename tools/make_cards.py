#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成小红书卡片图 HTML（每词一张，1080x1440 3:4）→ 用 Chrome 截图即可。
用法：python3 tools/make_cards.py  生成 html；再跑 chrome 截图循环（见脚本注释）。"""
import pathlib, json

BASE = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (BASE / 'xiaohongshu-cards' / 'template.html').read_text(encoding='utf-8')
OUT_DIR = BASE / 'xiaohongshu-cards' / 'html'

# 9 个热门词卡片内容（小红书文案风格：短、有网感）
CARDS = [
    {
        'num': 1, 'title': 'Agent 智能体', 'en': 'Agent',
        'what': '会自己拆任务、动手干活的 AI，不只是陪聊。',
        'analogy': '交给助理一个任务，它自己拆步骤、查资料、把事情办完。',
        'mistake': 'Agent 没有自我思想，只是按规则干活，照样会犯错、会跑偏。',
        'scene': 'AI 帮你订机票、整理文件、自动比价。',
    },
    {
        'num': 2, 'title': 'Token 词元', 'en': 'Token',
        'what': 'AI 读文字的基本单位，也是按它计费的。',
        'analogy': '把一句话切成小积木，一块就是一个 Token。',
        'mistake': 'Token 不等于汉字个数，一个汉字可能占 1~2 个 Token。',
        'scene': 'AI 对话页面显示"本次消耗 xx tokens"。',
    },
    {
        'num': 3, 'title': '幻觉', 'en': 'Hallucination',
        'what': 'AI 一本正经地胡说八道。',
        'analogy': '死要面子的学生：不会的题硬编一份像模像样的答案。',
        'mistake': 'AI 不是故意骗人，它天生只会"编通顺的话"。',
        'scene': 'AI 编造不存在的文献、虚构数据。',
    },
    {
        'num': 4, 'title': 'RAG 检索增强生成', 'en': 'Retrieval-Augmented Generation',
        'what': '先查资料、再回答的 AI 技术，答案还能附出处。',
        'analogy': '开卷考试带小抄：先翻书再作答。',
        'mistake': '不是把文档丢进去 AI 就全懂，检索质量决定上限。',
        'scene': '企业 AI 客服"先查公司文档再回答"。',
    },
    {
        'num': 5, 'title': '大语言模型', 'en': 'LLM · Large Language Model',
        'what': 'ChatGPT 背后的"大脑"。',
        'analogy': '读过整个图书馆的学者，跟谁都能聊几句。',
        'mistake': 'LLM 只是很会接话，不代表它说的都对。',
        'scene': '豆包、Kimi、文心一言背后都是它。',
    },
    {
        'num': 6, 'title': '提示词', 'en': 'Prompt',
        'what': '你跟 AI 说的那句话，直接决定回答质量。',
        'analogy': '点菜：说"随便"和说"少油微辣"得到的完全不同。',
        'mistake': '不是字越多越好，关键是说清楚要求。',
        'scene': '每次跟 AI 对话，你输入的内容都是提示词。',
    },
    {
        'num': 7, 'title': 'AI 换脸', 'en': 'Deepfake',
        'what': '用 AI 伪造视频、音频，换脸又换声，难辨真假。',
        'analogy': 'AI 换脸橡皮泥：把真人的脸捏到任何画面里。',
        'mistake': '换脸技术本身中性，被滥用去诈骗才危险。',
        'scene': '明星换脸视频、冒充亲友声音的诈骗。',
    },
    {
        'num': 8, 'title': '多模态', 'en': 'Multimodal',
        'what': '能同时看懂图、听懂话、理解文字的 AI。',
        'analogy': '发张照片给 AI，它能回答"桌上有几个杯子"。',
        'mistake': '不是多加个功能，是能同时理解图文声。',
        'scene': 'AI 看图识物、语音对话、拍照搜题。',
    },
    {
        'num': 9, 'title': 'AGI 通用人工智能', 'en': 'Artificial General Intelligence',
        'what': 'AI 的终极目标：跟人一样全能。',
        'analogy': '现在的 AI 是"偏科专才"，AGI 是"全能人类"。',
        'mistake': '现在还没有 AGI，别把聊天 AI 当成全能。',
        'scene': '新闻和发布会里常说的"通往 AGI"。',
    },
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for c in CARDS:
        html = TEMPLATE
        for k, v in c.items():
            html = html.replace('{' + k.upper() + '}', str(v))
        out = OUT_DIR / f'card-{c["num"]:02d}.html'
        out.write_text(html, encoding='utf-8')
        print('生成:', out.name)

if __name__ == '__main__':
    main()
