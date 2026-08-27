#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成单词详解卡（直接用网站词条完整内容，保证口径一致）。
用法：python3 tools/make_detail_cards.py → 生成 html → 再跑 Chrome 截图。"""
import pathlib, json

BASE = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (BASE / 'xiaohongshu-cards' / 'detail-template.html').read_text(encoding='utf-8')
WORDS = json.load(open(BASE / 'web' / 'words.json', encoding='utf-8'))['words']
OUT_DIR = BASE / 'xiaohongshu-cards' / 'html'

# 目标词（第一批详解卡）
TARGETS = ['agent', 'hallucination', 'rag']

def fill(card_name, w):
    related = [next(x for x in WORDS if x['id'] == r) for r in w['related']]
    chips = ''.join(f'<span class="chip">{x["title"]}</span>' for x in related)
    html = TEMPLATE
    html = html.replace('{TITLE}', w['title'].replace('（', '\n（') if len(w['title']) > 8 else w['title'])
    html = html.replace('{EN}', w['en'] or '')
    html = html.replace('{WHAT}', w['def'])
    html = html.replace('{ANALOGY}', w['analogy'])
    html = html.replace('{MISTAKE}', w['mistake'])
    html = html.replace('{CONFUSE}', w['confuse'])
    html = html.replace('{SCENE}', w['scene'])
    html = html.replace('{RELATED_CHIPS}', chips)
    out = OUT_DIR / f'detail-{card_name}.html'
    out.write_text(html, encoding='utf-8')
    print('生成:', out.name)

if __name__ == '__main__':
    for wid in TARGETS:
        w = next(x for x in WORDS if x['id'] == wid)
        fill(wid, w)
