#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 drafts/batch-*.md 词条 + 关系标注整合为 web/words.json。
用法：python3 tools/build_words.py
输出：web/words.json（56 词 + 主线路径 + 层级定义）
"""
import json, os, re, sys
from datetime import date

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
    # ---- 第六批新增（21 词）----
    '推理模型 / 深度思考': 'reasoning-model',
    '联网搜索': 'web-search',
    'AI 搜索': 'ai-search',
    '用量限制 / 限流': 'rate-limit',
    '电脑操控': 'computer-use',
    'AI 生成内容标识': 'ai-content-label',
    'MCP（模型上下文协议）': 'mcp',
    '思维链': 'chain-of-thought',
    'ReAct': 'react',
    '规划': 'planning',
    '反思': 'reflection',
    '智能体技能（Skill）': 'skill',
    '结构化输出': 'structured-output',
    '流式输出': 'streaming',
    '温度': 'temperature',
    '系统提示词': 'system-prompt',
    '分块': 'chunking',
    '全文检索（FTS5）': 'full-text-search',
    '提示词缓存': 'prompt-caching',
    '量化': 'quantization',
    'MMLU': 'mmlu',
    # ---- 第八批新增（7 词）----
    'AIGC': 'aigc',
    'Deepfake（深度伪造）': 'deepfake',
    'AI 生成内容版权': 'ai-copyright',
    '小模型（SLM）': 'slm',
    '计算机视觉（CV）': 'cv',
    'ASI（超级人工智能）': 'asi',
    'AI 泥浆（AI-Slop）': 'ai-slop',
    # ---- 第十一批新增（2 词）----
    '手搓感': 'hand-rolling',
    'Guardrails（护栏）': 'guardrails',
    # ---- 第十二批新增（3 词）----
    'MoE（混合专家）': 'moe',
    '数据飞轮': 'data-flywheel',
    'Spec Coding': 'spec-coding',
    # ---- 第十三批新增（5 词）----
    '召回（Recall）': 'recall',
    '重排序（Rerank）': 'rerank',
    '小样本 / 零样本（Few-shot / Zero-shot）': 'few-shot',
    'VLM（视觉语言模型）': 'vlm',
    'AI 偏见（Bias）': 'bias',
    # ---- 第十四批新增（11 词）----
    '随机鹦鹉（Stochastic Parrot）': 'stochastic-parrot',
    'AI 谄媚（Sycophancy）': 'sycophancy',
    '模型崩溃（Model Collapse）': 'model-collapse',
    '数据投毒（Data Poisoning）': 'data-poisoning',
    'AI 洗白（AI Washing）': 'ai-washing',
    '幽灵工作（Ghost Work）': 'ghost-work',
    '伊丽莎效应（ELIZA Effect）': 'eliza-effect',
    '死亡互联网理论（Dead Internet Theory）': 'dead-internet',
    '数字去技能化（Deskilling）': 'deskilling',
    '自动化自满（Automation Complacency）': 'automation-complacency',
    '粉红肉渣新闻（Pink Slime Journalism）': 'pink-slime',
    # ---- 第十七批新增（4 词）----
    'AI 普惠': 'ai-inclusion',
    '一人公司（OPC）': 'one-person-company',
    'Loop（循环）': 'loop',
    'Harness（智能体框架）': 'harness',
    # ---- 第九批新增（2 词）----
    '模型蒸馏（Distillation）': 'distillation',
    '合成数据（Synthetic Data）': 'synthetic-data',
    # ---- 第十八批新增（7 词）----
    '智能经济': 'intelligent-economy',
    '数据要素': 'data-element',
    '数据治理': 'data-governance',
    '不透明递归': 'opaque-recurrence',
    '内存荒': 'ramageddon',
    '扩散模型': 'diffusion-model',
    '编程智能体': 'coding-agent',
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
    'compute': ['gpu', 'training', 'local-deployment', 'ramageddon'],
    'gpu': ['compute', 'training', 'local-deployment', 'ramageddon'],
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
    'copilot': ['ai-assistant', 'llm', 'coding-agent'],
    'text-to-image': ['generative-ai', 'text-to-video', 'diffusion-model'],
    'text-to-video': ['text-to-image', 'world-model', 'diffusion-model'],
    'speech-recognition': ['speech-synthesis', 'digital-human'],
    'speech-synthesis': ['speech-recognition', 'digital-human'],
    'digital-human': ['speech-synthesis', 'speech-recognition', 'llm'],
    'agent': ['tool-calling', 'memory', 'multi-agent', 'ai-assistant', 'coding-agent'],
    'workflow': ['agent', 'tool-calling', 'prompt-engineering'],
    'tool-calling': ['agent', 'api'],
    'memory': ['vector-database', 'context-window', 'agent'],
    'multi-agent': ['agent', 'workflow'],
    'api': ['tool-calling', 'token', 'llm'],
    'open-source-model': ['local-deployment', 'api', 'model-evaluation'],
    'local-deployment': ['open-source-model', 'gpu', 'compute'],
    'model-evaluation': ['llm', 'open-source-model'],
    'alignment': ['rlhf', 'hallucination', 'agi'],
    'explainability': ['alignment', 'agi', 'opaque-recurrence'],
    'agi': ['ai', 'world-model', 'alignment', 'embodied-ai'],
    'embodied-ai': ['world-model', 'agi', 'multimodal'],
    'world-model': ['agi', 'embodied-ai', 'text-to-video'],
    'jailbreak': ['prompt', 'alignment'],
    # ---- 第六批新增（21 词）----
    'reasoning-model': ['llm', 'chain-of-thought', 'rlhf', 'opaque-recurrence'],
    'web-search': ['llm', 'rag', 'ai-search'],
    'ai-search': ['semantic-search', 'web-search', 'llm'],
    'rate-limit': ['api', 'token', 'prompt-caching'],
    'computer-use': ['agent', 'tool-calling', 'multimodal'],
    'ai-content-label': ['alignment', 'model-evaluation', 'data-governance'],
    'mcp': ['agent', 'tool-calling', 'api'],
    'chain-of-thought': ['reasoning-model', 'prompt', 'transformer', 'opaque-recurrence'],
    'react': ['agent', 'tool-calling', 'planning'],
    'planning': ['agent', 'react', 'multi-agent'],
    'reflection': ['agent', 'react', 'alignment'],
    'skill': ['agent', 'tool-calling', 'mcp'],
    'structured-output': ['tool-calling', 'api', 'prompt'],
    'streaming': ['inference', 'api', 'token'],
    'temperature': ['hallucination', 'inference', 'reasoning-model'],
    'system-prompt': ['prompt', 'prompt-engineering', 'alignment'],
    'chunking': ['rag', 'vector-database', 'full-text-search'],
    'full-text-search': ['semantic-search', 'rag', 'vector-database'],
    'prompt-caching': ['token', 'api', 'context-window'],
    'quantization': ['local-deployment', 'gpu', 'open-source-model'],
    'mmlu': ['model-evaluation', 'llm', 'open-source-model'],
    # ---- 第八批新增（7 词）----
    'aigc': ['generative-ai', 'llm', 'multimodal', 'ai-content-label'],
    'deepfake': ['text-to-image', 'digital-human', 'speech-synthesis', 'ai-content-label'],
    'ai-copyright': ['ai-content-label', 'generative-ai', 'alignment'],
    'slm': ['llm', 'local-deployment', 'quantization'],
    'cv': ['nlp', 'multimodal', 'text-to-image'],
    'asi': ['agi', 'alignment', 'world-model'],
    'ai-slop': ['generative-ai', 'ai-content-label', 'hallucination'],
    # ---- 第十一批新增（2 词）----
    'hand-rolling': ['generative-ai', 'ai-slop', 'prompt'],
    'guardrails': ['jailbreak', 'alignment', 'ai-content-label'],
    # ---- 第十二批新增（3 词）----
    'moe': ['llm', 'parameter', 'distillation'],
    'data-flywheel': ['llm', 'synthetic-data', 'dataset', 'data-element'],
    'spec-coding': ['prompt-engineering', 'structured-output', 'tool-calling', 'coding-agent'],
    # ---- 第十三批新增（5 词）----
    'recall': ['rag', 'rerank', 'semantic-search', 'model-evaluation'],
    'rerank': ['rag', 'recall', 'vector-database', 'semantic-search'],
    'few-shot': ['prompt-engineering', 'llm', 'fine-tuning'],
    'vlm': ['multimodal', 'cv', 'llm'],
    'bias': ['alignment', 'guardrails', 'dataset', 'model-evaluation'],
    # ---- 第十四批新增（11 词）----
    'stochastic-parrot': ['llm', 'hallucination', 'agi'],
    'sycophancy': ['rlhf', 'alignment', 'hallucination'],
    'model-collapse': ['synthetic-data', 'data-flywheel', 'training'],
    'data-poisoning': ['jailbreak', 'dataset', 'guardrails', 'alignment', 'data-governance'],
    'ai-washing': ['generative-ai', 'ai-slop'],
    'ghost-work': ['dataset', 'ai-slop', 'training'],
    'eliza-effect': ['chatbot', 'agi', 'hallucination'],
    'dead-internet': ['ai-slop', 'generative-ai', 'ai-content-label'],
    'deskilling': ['ai-assistant', 'copilot'],
    'automation-complacency': ['hallucination', 'alignment', 'ai-assistant'],
    'pink-slime': ['ai-slop', 'generative-ai', 'ai-content-label'],
    # ---- 第十七批新增（4 词）----
    'ai-inclusion': ['generative-ai', 'one-person-company', 'llm', 'intelligent-economy'],
    'one-person-company': ['agent', 'ai-assistant', 'ai-inclusion', 'generative-ai', 'intelligent-economy'],
    'loop': ['agent', 'react', 'planning', 'reflection'],
    'harness': ['agent', 'tool-calling', 'guardrails', 'mcp'],
    # ---- 第九批新增（2 词）----
    'distillation': ['fine-tuning', 'slm', 'quantization', 'llm'],
    'synthetic-data': ['training', 'dataset', 'fine-tuning'],
    # ---- 第十八批新增（7 词）----
    'intelligent-economy': ['one-person-company', 'ai-inclusion', 'data-flywheel', 'agent'],
    'data-element': ['data-flywheel', 'data-governance', 'dataset', 'ai-copyright'],
    'data-governance': ['data-element', 'ai-content-label', 'data-poisoning', 'ai-copyright'],
    'opaque-recurrence': ['chain-of-thought', 'explainability', 'reasoning-model', 'alignment'],
    'ramageddon': ['gpu', 'compute', 'local-deployment'],
    'diffusion-model': ['text-to-image', 'text-to-video', 'generative-ai'],
    'coding-agent': ['agent', 'copilot', 'spec-coding', 'tool-calling'],
}

# ---- 进阶标注（面向开发者，页面显示"进阶"徽标；与用户确认的原型一致）----
ADV = {
    'mcp', 'react', 'planning', 'reflection', 'skill',
    'structured-output', 'streaming', 'temperature', 'system-prompt',
    'chunking', 'full-text-search', 'prompt-caching', 'quantization', 'mmlu',
    'slm', 'distillation', 'synthetic-data',
    'guardrails', 'moe', 'spec-coding', 'recall', 'rerank', 'few-shot', 'vlm', 'bias',
    'stochastic-parrot', 'sycophancy', 'model-collapse', 'data-poisoning',
    'eliza-effect', 'deskilling', 'automation-complacency',
    'loop', 'harness',
    # ---- 第十八批（3 个进阶词）----
    'opaque-recurrence', 'diffusion-model', 'coding-agent',
}

# ---- 层内小节（77 词版折叠树：layer -> [(小节名, [词id])]）----
SECTIONS = {
    '地基': [
        ('学习与方法', ['machine-learning', 'deep-learning', 'neural-network', 'training', 'inference', 'algorithm', 'dataset']),
        ('模型内部与资源', ['parameter', 'weight', 'compute', 'gpu', 'ramageddon']),
    ],
    '模型本体': [
        ('大模型家族', ['llm', 'generative-ai', 'aigc', 'reasoning-model', 'slm', 'multimodal', 'nlp', 'cv']),

        ('训练方法', ['pretraining', 'fine-tuning', 'rlhf', 'distillation', 'synthetic-data', 'model-collapse']),
        ('内部机制', ['transformer', 'attention', 'token', 'context-window', 'chain-of-thought', 'temperature', 'moe', 'vlm', 'stochastic-parrot', 'opaque-recurrence']),
    ],
    '交互层': [
        ('提示与生成', ['prompt', 'prompt-engineering', 'system-prompt', 'structured-output', 'streaming', 'hallucination']),
        ('检索与知识', ['embedding', 'vector', 'vector-database', 'semantic-search', 'full-text-search', 'chunking', 'rag', 'knowledge-base', 'recall', 'rerank', 'web-search', 'ai-search']),
        ('提示技巧', ['few-shot']),
    ],
    '应用层': [
        ('Agent 智能体', ['agent', 'harness', 'loop', 'tool-calling', 'memory', 'multi-agent', 'workflow', 'react', 'planning', 'reflection', 'skill', 'computer-use', 'one-person-company', 'coding-agent']),
        ('内容生成', ['text-to-image', 'text-to-video', 'deepfake', 'diffusion-model']),
        ('语音与形象', ['speech-recognition', 'speech-synthesis', 'digital-human']),
        ('助手形态', ['chatbot', 'ai-assistant', 'copilot']),
        ('AI 应用开发', ['spec-coding']),
    ],
    '生态与前沿': [
        ('API 工程', ['api', 'rate-limit', 'prompt-caching', 'mcp', 'local-deployment', 'open-source-model', 'quantization']),
        ('评测与安全', ['model-evaluation', 'mmlu', 'alignment', 'explainability', 'jailbreak', 'guardrails', 'bias', 'sycophancy', 'data-poisoning', 'eliza-effect', 'deskilling', 'automation-complacency', 'ai-content-label', 'ai-copyright', 'ai-slop', 'hand-rolling']),
        ('内容生态现象', ['ai-washing', 'ghost-work', 'dead-internet', 'pink-slime']),
        ('未来方向', ['agi', 'asi', 'embodied-ai', 'world-model', 'ai-inclusion', 'intelligent-economy']),
        ('数据与飞轮', ['data-flywheel', 'data-element', 'data-governance']),
    ],
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

# ---- 收录历程（手写常量：[批次标题, 该批首次收录的词 id]）----
# 数据来源 = drafts/batch-*.md 里各词条的首次出现（2026-09-23 一次性抽取后固化）。
# 故意不写日期：updated 只有两个日期（历史日期曾被旧构建逻辑刷掉），
# 批次顺序本身就是时间线，编造日期不如不写。
HISTORY = [
    ('第一批：第 0 词 + 地基层（13 条）', ['ai', 'turing-test', 'machine-learning', 'deep-learning', 'neural-network', 'training', 'inference', 'parameter', 'weight', 'dataset', 'algorithm', 'compute', 'gpu']),
    ('第二批：模型本体层（11 条）', ['llm', 'generative-ai', 'nlp', 'transformer', 'attention', 'token', 'context-window', 'pretraining', 'fine-tuning', 'rlhf', 'multimodal']),
    ('第三批：交互层（9 条）', ['prompt', 'prompt-engineering', 'embedding', 'vector', 'vector-database', 'semantic-search', 'rag', 'knowledge-base', 'hallucination']),
    ('第四批：应用层（13 条）', ['chatbot', 'ai-assistant', 'copilot', 'text-to-image', 'text-to-video', 'speech-recognition', 'speech-synthesis', 'digital-human', 'agent', 'workflow', 'tool-calling', 'memory', 'multi-agent']),
    ('第五批：生态与前沿（10 条）', ['api', 'open-source-model', 'local-deployment', 'model-evaluation', 'alignment', 'explainability', 'agi', 'embodied-ai', 'world-model', 'jailbreak']),
    ('第六批：新增词汇（21 词）', ['reasoning-model', 'web-search', 'ai-search', 'rate-limit', 'computer-use', 'ai-content-label', 'mcp', 'chain-of-thought', 'react', 'planning', 'reflection', 'skill', 'structured-output', 'streaming', 'temperature', 'system-prompt', 'chunking', 'full-text-search', 'prompt-caching', 'quantization', 'mmlu']),
    ('第七批：V1.1 首批 24 词（类比 + 场景 + 误区 + 混淆）', []),
    ('第八批：新增 7 词（AIGC / Deepfake / AI 版权 / CV / SLM / ASI / AI-Slop）', ['aigc', 'deepfake', 'ai-copyright', 'cv', 'slm', 'asi', 'ai-slop']),
    ('第九批：新增 2 词（模型蒸馏 / 合成数据）', ['distillation', 'synthetic-data']),
    ('第十批：V1.1 补全 A 档（6 词 · 4 字段）', []),
    ('第十一批：新增 2 词（手搓感 / guardrails 护栏）', ['hand-rolling', 'guardrails']),
    ('第十二批：新增 3 词（MoE / 数据飞轮 / Spec Coding）', ['moe', 'data-flywheel', 'spec-coding']),
    ('第十三批：新增 5 词（召回 / 重排序 / 小样本零样本 / VLM / AI 偏见）', ['recall', 'rerank', 'few-shot', 'vlm', 'bias']),
    ('第十四批：新增 11 词（随机鹦鹉 / AI谄媚 / 模型崩溃 / 数据投毒 / AI洗白 / 幽灵工作 / ELIZA效应 / 死亡互联网 / 去技能化 / 自动化自满 / 粉红肉渣）', ['stochastic-parrot', 'sycophancy', 'model-collapse', 'data-poisoning', 'ai-washing', 'ghost-work', 'eliza-effect', 'dead-internet', 'deskilling', 'automation-complacency', 'pink-slime']),
    ('第十五批：P1「练习」样例（3 词）', []),
    ('第十六批：P1「练习」高频词补全（17 词）', []),
    ('第十七批：新增 4 词（AI 普惠 / 一人公司 / Loop / Harness）', ['ai-inclusion', 'one-person-company', 'loop', 'harness']),
    ('第十八批：新增 7 词（智能经济 / 数据要素 / 数据治理 / 不透明递归 / 内存荒 / 扩散模型 / 编程智能体）', ['intelligent-economy', 'data-element', 'data-governance', 'opaque-recurrence', 'ramageddon', 'diffusion-model', 'coding-agent']),
    ('第二十批：高频 20 词结构升级（标准定义 + 辨析 + 问答）', []),
]

FIELD_KEYS = {'英文名': 'en', '中文名': 'zh', '别名': 'alias', '层级': 'layer', '白话解释': 'def', '进阶': 'adv_raw', '类比': 'analogy', '场景': 'scene', '误区': 'mistake', '混淆': 'confuse', '练习': 'practice', '标准定义': 'formal'}

# 对照型字段：同名可重复出现，每行用全角 ｜ 切成两半 → 辨析: vs[{name,text}] / 问答: faq[{q,a}]
PAIR_FIELDS = {'辨析': 'vs', '问答': 'faq'}

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
            pk = PAIR_FIELDS.get(key)
            if pk:
                k1, k2 = ('name', 'text') if pk == 'vs' else ('q', 'a')
                left, _, right = val.partition('｜')
                if not right:
                    print(f'WARN: {key} 缺 ｜ 分隔:', val[:30], file=sys.stderr)
                cur.setdefault(pk, []).append({k1: left.strip(), k2: right.strip()})
                continue
            fk = FIELD_KEYS.get(key)
            if fk:
                cur[fk] = val
    if cur:
        items.append(cur)
    return items

def clean_alias(s):
    return '' if s in ('无', '') else s

def load_prev():
    """读上一次构建的 words.json，用来判断"内容没变就别刷 updated 日期"。
    旧实现是无条件 str(date.today())：每次构建都把全部词条刷成今天，
    既让"更新于"失去意义，也让按日期做更新日志变得不可能。"""
    if not os.path.exists(OUT):
        return {}
    try:
        with open(OUT, encoding='utf-8') as f:
            return {w['id']: w for w in json.load(f).get('words', [])}
    except Exception:
        return {}


def main():
    words, seen = {}, set()
    prev = load_prev()
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
                # 合并更新模式：后批次补充 analogy/scene/mistake/confuse/practice 等字段
                w = words[wid]
                for f in ('analogy', 'scene', 'mistake', 'confuse', 'practice', 'formal', 'vs', 'faq'):
                    if it.get(f):
                        w[f] = it[f]
                continue
            seen.add(wid)
            adv_raw = it.get('adv_raw', '否')
            entry = {
                'id': wid,
                'title': title,
                'en': it.get('en', ''),
                'zh': it.get('zh', ''),
                'alias': clean_alias(it.get('alias', '')),
                'layer': norm_layer(it.get('layer', '')),
                'def': it.get('def', ''),
                'analogy': it.get('analogy', ''),
                'scene': it.get('scene', ''),
                'mistake': it.get('mistake', ''),
                'confuse': it.get('confuse', ''),
                'practice': it.get('practice', ''),
                'adv': (adv_raw == '是') or (wid in ADV),
                'related': RELATED.get(wid, []),
                'updated': None,
            }
            # 可选字段：只有词条里写了才输出，未写的词 JSON 里不出现这些键
            for f in ('formal', 'vs', 'faq'):
                if it.get(f):
                    entry[f] = it[f]
            # updated 统一在**所有批次处理完之后**再定（见下面 words_list 之后）：
            # 同一词条可能在多个批次里被合并覆盖，创建时取到的只是中间态
            words[wid] = entry
    words_list = list(words.values())

    # updated：内容真的变了才刷新（除 updated 外逐字段完全相等 = 没变，保留原日期）。
    # 必须放在全部批次合并完成之后——词条可能在多个批次里被覆盖，
    # 拿创建时的中间态去比会把"没变"误判成"变了"（2026-09-23 修）。
    for w in words_list:
        old = prev.get(w['id'])
        prev_base = {k: v for k, v in old.items() if k != 'updated'} if old else None
        cur_base = {k: v for k, v in w.items() if k != 'updated'}
        w['updated'] = old['updated'] if (prev_base is not None and prev_base == cur_base) else str(date.today())

    missing = set(ID_MAP) - {w['title'] for w in words_list}
    for t in missing:
        print('WARN: 词条缺失:', t, file=sys.stderr)

    # 辨析条目的名称反查词条 id：匹配得上就带 ref（页面可点击跳转），匹配不上保持纯文本
    name_to_id = {}
    for w in words_list:
        cands = [w['title'], w['zh'], w['en']]
        cands += [re.sub(r'（.*?）|\(.*?\)', '', c).strip() for c in list(cands)]
        if w['alias']:
            cands += [a.strip() for a in re.split(r'[、,，]', w['alias'])]
        for c in cands:
            if c:
                name_to_id.setdefault(c, w['id'])
    for w in words_list:
        for v in w.get('vs', []):
            ref = name_to_id.get(v['name']) or name_to_id.get(re.sub(r'（.*?）|\(.*?\)', '', v['name']).strip())
            if ref and ref != w['id']:
                v['ref'] = ref

    data = {
        'title': 'AI 词汇本',
        'subtitle': '零基础 AI 术语词典，不用懂编程，小白也能轻松读懂AI名词',
        'layers': [
            {'id': lid, 'desc': LAYER_DESC[lid]}
            for lid in LAYER_ORDER
        ],
        'sections': SECTIONS,
        'path': [
            {'ids': step, 'note': note}
            for step, note in zip(PATH, PATH_NOTE)
        ],
        'history': [{'title': t, 'ids': ids} for t, ids in HISTORY],
        'words': words_list,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f'OK: {len(words_list)} 词 -> {OUT}')

if __name__ == '__main__':
    main()
