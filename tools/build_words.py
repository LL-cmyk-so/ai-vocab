#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 drafts/batch-*.md 词条 + 关系标注整合为 web/words.json。
用法：python3 tools/build_words.py
输出：web/words.json（56 词 + 主线路径 + 层级定义）
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = os.path.join(BASE, 'drafts')
OUT = os.path.join(BASE, 'web', 'words.json')

# ---- 标题 -> id 映射（56 词，与 README 冻结词单一致）----
ID_MAP = {
    '人工智能（AI）': 'ai', '图灵测试': 'turing-test',
    '机器学习': 'machine-learning', '深度学习': 'deep-learning',
    '神经网络': 'neural-network', '训练': 'training', '推理': 'inference',
    '参数': 'parameter', '权重': 'weight', '数据集': 'dataset',
    '算法': 'algorithm', '算力': 'compute', 'GPU': 'gpu',
    '大语言模型（LLM）': 'llm', '生成式 AI': 'generative-ai',
    '自然语言处理（NLP）': 'nlp', 'Transformer': 'transformer',
    '注意力机制': 'attention', 'Token（词元）': 'token',
    '上下文窗口': 'context-window', '预训练': 'pretraining',
    '微调': 'fine-tuning', '强化学习与 RLHF': 'rlhf', '多模态': 'multimodal',
    '提示词（Prompt）': 'prompt', '提示工程': 'prompt-engineering',
    '嵌入（Embedding）': 'embedding', '向量': 'vector',
    '向量数据库': 'vector-database', '语义搜索': 'semantic-search',
    '检索增强生成（RAG）': 'rag', '知识库': 'knowledge-base',
    '幻觉': 'hallucination', '聊天机器人 / 对话式 AI': 'chatbot',
    'AI 助手': 'ai-assistant', 'Copilot（编程副驾驶）': 'copilot',
    '文生图': 'text-to-image', '文生视频': 'text-to-video',
    '语音识别': 'speech-recognition', '语音合成': 'speech-synthesis',
    '数字人': 'digital-human', 'Agent（智能体）': 'agent',
    '工作流': 'workflow', '工具调用': 'tool-calling', '记忆': 'memory',
    '多智能体': 'multi-agent', 'API': 'api',
    '开源模型 / 闭源模型': 'open-source-model', '本地部署': 'local-deployment',
    '模型评测': 'model-evaluation', '对齐（Alignment）': 'alignment',
    '可解释性': 'explainability', 'AGI（通用人工智能）': 'agi',
    '具身智能': 'embodied-ai', '世界模型': 'world-model',
    '越狱 / 提示词注入': 'jailbreak',
}

# ---- 层级归一化与展示 ----
LAYER_ORDER = ['总纲', '地基', '模型本体', '交互层', '应用层', '生态与前沿']
LAYER_DESC = {
    '总纲': '从这里开始认识 AI',
    '地基': 'AI 是怎么工作的',
    '模型本体': '大模型本身',
    '交互层': '怎么跟 AI 打交道',
    '应用层': 'AI 能干的事',
    '生态与前沿': '行业与未来',
}

def norm_layer(raw):
    r = (raw or '').strip()
    if r.startswith('第 0 词'):
        return '总纲'
    if r.startswith('生态与前沿'):
        return '生态与前沿'
    return r

# ---- 精选跳转（id -> [id]，与 relations.md 一致）----
RELATED = {
    'ai': ['machine-learning', 'deep-learning', 'llm', 'agi'],
    'turing-test': ['ai', 'agi'],
    'machine-learning': ['ai', 'deep-learning', 'training', 'dataset'],
    'deep-learning': ['machine-learning', 'neural-network', 'parameter'],
    'neural-network': ['deep-learning', 'parameter', 'weight'],
    'training': ['inference', 'dataset', 'pretraining'],
    'inference': ['training', 'api'],
    'parameter': ['weight', 'training', 'llm'],
    'weight': ['parameter', 'neural-network'],
    'dataset': ['training', 'pretraining', 'fine-tuning'],
    'algorithm': ['machine-learning', 'compute'],
    'compute': ['gpu', 'training', 'local-deployment'],
    'gpu': ['compute', 'training', 'local-deployment'],
    'llm': ['token', 'transformer', 'context-window', 'generative-ai'],
    'generative-ai': ['llm', 'text-to-image', 'text-to-video', 'multimodal'],
    'nlp': ['llm', 'transformer'],
    'transformer': ['attention', 'llm'],
    'attention': ['transformer'],
    'token': ['llm', 'context-window', 'api'],
    'context-window': ['token', 'memory', 'llm'],
    'pretraining': ['fine-tuning', 'training', 'llm'],
    'fine-tuning': ['pretraining', 'dataset', 'alignment'],
    'rlhf': ['training', 'alignment', 'fine-tuning'],
    'multimodal': ['generative-ai', 'text-to-image', 'text-to-video', 'digital-human'],
    'prompt': ['prompt-engineering', 'llm', 'jailbreak'],
    'prompt-engineering': ['prompt', 'agent'],
    'embedding': ['vector', 'semantic-search', 'rag'],
    'vector': ['embedding', 'vector-database', 'semantic-search'],
    'vector-database': ['vector', 'rag', 'memory'],
    'semantic-search': ['vector', 'vector-database'],
    'rag': ['knowledge-base', 'vector-database', 'hallucination', 'embedding'],
    'knowledge-base': ['rag', 'vector-database'],
    'hallucination': ['rag', 'alignment', 'prompt'],
    'chatbot': ['llm', 'ai-assistant', 'nlp'],
    'ai-assistant': ['chatbot', 'agent', 'tool-calling'],
    'copilot': ['ai-assistant', 'llm'],
    'text-to-image': ['generative-ai', 'text-to-video'],
    'text-to-video': ['text-to-image', 'world-model'],
    'speech-recognition': ['speech-synthesis', 'digital-human'],
    'speech-synthesis': ['speech-recognition', 'digital-human'],
    'digital-human': ['speech-synthesis', 'speech-recognition', 'llm'],
    'agent': ['tool-calling', 'memory', 'multi-agent', 'ai-assistant'],
    'workflow': ['agent', 'tool-calling', 'prompt-engineering'],
    'tool-calling': ['agent', 'api'],
    'memory': ['vector-database', 'context-window', 'agent'],
    'multi-agent': ['agent', 'workflow'],
    'api': ['tool-calling', 'token', 'llm'],
    'open-source-model': ['local-deployment', 'api', 'model-evaluation'],
    'local-deployment': ['open-source-model', 'gpu', 'compute'],
    'model-evaluation': ['llm', 'open-source-model'],
    'alignment': ['rlhf', 'hallucination', 'agi'],
    'explainability': ['alignment', 'agi'],
    'agi': ['ai', 'world-model', 'alignment', 'embodied-ai'],
    'embodied-ai': ['world-model', 'agi', 'multimodal'],
    'world-model': ['agi', 'embodied-ai', 'text-to-video'],
    'jailbreak': ['prompt', 'alignment'],
}

# ---- 主线路径（18 步，每步可含多个词）----
PATH = [
    ['ai'],
    ['machine-learning'],
    ['deep-learning'],
    ['neural-network'],
    ['training'],
    ['parameter'],
    ['inference'],
    ['compute', 'gpu'],
    ['llm'],
    ['token'],
    ['context-window'],
    ['pretraining', 'fine-tuning'],
    ['prompt'],
    ['hallucination'],
    ['chatbot', 'ai-assistant'],
    ['agent'],
    ['rag'],
    ['agi'],
]
PATH_NOTE = [
    '总纲：AI 到底是什么',
    'AI 的核心方法：让机器自己学会',
    '机器学习里最厉害的流派',
    '深度学习的"大脑"长什么样',
    '怎么"教"这个大脑（上学）',
    '训练到底在调什么（旋钮）',
    '学完之后怎么用（考试）',
    '训练为什么这么烧钱（马力）',
    '集大成者：AI 时代的主角登场',
    '大模型怎么"读"文字（积木块）',
    '大模型一次能记住多少',
    '大模型是怎么造出来的',
    '你和大模型对话的入口',
    '用之前必须知道的坑',
    '最常见的 AI 产品形态',
    'AI 从"说"到"做"的进化',
    '让 AI 用上你的私有资料',
    '终点站：AI 要去哪',
]

# ---- 热门词（首页快捷入口，6 个）----
HOT = ['agent', 'token', 'rag', 'hallucination', 'agi', 'multimodal']

FIELD_KEYS = {'英文名': 'en', '中文名': 'zh', '别名': 'alias', '层级': 'layer', '白话解释': 'def'}

def parse_batch(path):
    items = []
    cur = None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n').strip()
        m = re.match(r'^###\s+(.+)$', line)
        if m:
            if cur:
                items.append(cur)
            cur = {'title': m.group(1).strip()}
            continue
        if cur is None:
            continue
        fm = re.match(r'^-\s*\*\*(.+?)\*\*：\s*(.*)$', line)
        if fm:
            key, val = fm.group(1).strip(), fm.group(2).strip()
            fk = FIELD_KEYS.get(key)
            if fk:
                cur[fk] = val
    if cur:
        items.append(cur)
    return items

def clean_alias(s):
    return '' if s in ('无', '') else s

def main():
    words, seen = [], set()
    for fname in sorted(os.listdir(DRAFTS)):
        if not fname.startswith('batch-') or not fname.endswith('.md'):
            continue
        for it in parse_batch(os.path.join(DRAFTS, fname)):
            title = it['title']
            wid = ID_MAP.get(title)
            if wid is None:
                print('WARN: 未映射 id:', title, file=sys.stderr)
                continue
            if wid in seen:
                print('WARN: 重复 id:', wid, file=sys.stderr)
                continue
            seen.add(wid)
            words.append({
                'id': wid,
                'title': title,
                'en': it.get('en', ''),
                'zh': it.get('zh', ''),
                'alias': clean_alias(it.get('alias', '')),
                'layer': norm_layer(it.get('layer', '')),
                'def': it.get('def', ''),
                'related': RELATED.get(wid, []),
            })

    missing = set(ID_MAP) - {w['title'] for w in words}
    for t in missing:
        print('WARN: 词条缺失:', t, file=sys.stderr)

    data = {
        'title': 'AI 词汇本',
        'subtitle': '从 Agent 到 Token，用大白话看懂 AI 时代',
        'layers': [
            {'id': lid, 'desc': LAYER_DESC[lid]}
            for lid in LAYER_ORDER
        ],
        'path': [
            {'ids': step, 'note': note}
            for step, note in zip(PATH, PATH_NOTE)
        ],
        'hot': HOT,
        'words': words,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f'OK: {len(words)} 词 -> {OUT}')

if __name__ == '__main__':
    main()
