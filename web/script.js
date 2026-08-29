/* ============ AI 词汇本：逻辑 ============
   纯前端静态页面：读取 words.json，本地渲染、搜索、跳转。
   视图路由（hash）：# 首页(折叠树) · #path 18步列表 · #learn/N 学习模式 · #词条id 详情 */

'use strict';

const $ = (sel) => document.querySelector(sel);

const state = {
  data: null,   // words.json 全部数据
  query: '',
  entryId: null,
  learnIdx: 0,
};

/* ---------- 数据加载 ---------- */
function boot(data) {
  state.data = data;
  $('#siteTitle').textContent = data.title;
  $('#siteSubtitle').textContent = data.subtitle;
  renderStatic();
  route();
}

function byId(id) {
  return state.data ? state.data.words.find((w) => w.id === id) : null;
}

/* ---------- 静态内容渲染（数据加载后渲染一次） ---------- */
function renderStatic() {
  renderTree();
  renderPathList();
  renderHotLine();
}

/* 折叠目录树 */
function renderTree() {
  const tree = $('#tree');
  tree.innerHTML = '';
  const LAYER_COLOR = {
    '总纲': '#7c5cf0', '地基': '#4f6ef7', '模型本体': '#3b82f6',
    '交互层': '#14b8a6', '应用层': '#f59e0b', '生态与前沿': '#ef4444',
  };

  state.data.layers.forEach((layer) => {
    const words = state.data.words.filter((w) => w.layer === layer.id);
    if (!words.length) return;

    const el = document.createElement('div');
    el.className = 'tree-layer';

    // 层级头
    const head = document.createElement('div');
    head.className = 'tree-head';
    head.innerHTML =
      '<span class="tree-color" style="background:' + LAYER_COLOR[layer.id] + '"></span>' +
      '<span class="tree-name">' + escapeHtml(layer.id) + '</span>' +
      '<span class="tree-count">' + words.length + ' 词</span>' +
      '<span class="tree-arrow">▼</span>';
    el.appendChild(head);

    // 层内小节
    const body = document.createElement('div');
    body.className = 'tree-body';
    const secs = state.data.sections[layer.id] || [];
    if (secs.length) {
      secs.forEach((sec) => {
        const sub = document.createElement('div');
        sub.className = 'tree-sub';
        sub.innerHTML = '<div class="tree-sub-title">' + escapeHtml(sec[0]) + '</div><div class="chips"></div>';
        const chips = sub.querySelector('.chips');
        sec[1].forEach((id) => {
          const w = byId(id);
          if (w) chips.appendChild(makeChip(w));
        });
        body.appendChild(sub);
      });
    } else {
      // 总纲等无小节的层
      const sub = document.createElement('div');
      sub.className = 'tree-sub';
      sub.innerHTML = '<div class="chips"></div>';
      const chips = sub.querySelector('.chips');
      words.forEach((w) => chips.appendChild(makeChip(w)));
      body.appendChild(sub);
    }
    el.appendChild(body);

    // 折叠交互
    head.addEventListener('click', () => el.classList.toggle('closed'));
    tree.appendChild(el);
  });
}

function makeChip(w) {
  const chip = document.createElement('span');
  chip.className = 'chip' + (w.adv ? ' adv' : '');
  chip.textContent = w.title;
  chip.addEventListener('click', () => openEntry(w.id));
  return chip;
}

/* 18 步列表（辅助页） */
function renderPathList() {
  const ol = $('#pathList');
  ol.innerHTML = '';
  state.data.path.forEach((step, i) => {
    const li = document.createElement('li');
    li.innerHTML =
      '<span class="path-step-no">' + (i + 1) + '</span>' +
      '<span class="path-step-name">' + escapeHtml(step.ids.map(byId).map((w) => w.title).join(' / ')) + '</span>' +
      '<span class="path-step-note">' + escapeHtml(step.note) + '</span>';
    li.addEventListener('click', () => openEntry(step.ids[0]));
    ol.appendChild(li);
  });
}

/* 热门一行 */
function renderHotLine() {
  const line = $('#hotLine');
  line.innerHTML = '🔥 热门：';
  state.data.hot.forEach((id, i) => {
    const w = byId(id);
    if (!w) return;
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = w.title;
    a.addEventListener('click', (e) => { e.preventDefault(); openEntry(w.id); });
    line.appendChild(a);
    if (i < state.data.hot.length - 1) line.appendChild(document.createTextNode(' · '));
  });
}

/* ---------- 视图路由 ---------- */
const VIEWS = ['homeView', 'learnView', 'pathView', 'entryView'];

function showView(name) {
  VIEWS.forEach((v) => {
    $('#' + v).hidden = (v !== name);
  });
  window.scrollTo({ top: 0 });
}

function route() {
  const h = decodeURIComponent(location.hash.slice(1));
  if (h === 'path') {
    clearSplit();
    showView('pathView');
  } else if (h.startsWith('learn/')) {
    const n = parseInt(h.slice(6), 10);
    if (!isNaN(n) && n >= 0 && n < state.data.path.length) {
      clearSplit();
      showLearn(n);
    } else {
      location.hash = '';
    }
  } else if (h && byId(h)) {
    enterSplit(h);
  } else {
    clearSplit();
    showView('homeView');
  }
}

window.addEventListener('hashchange', route);

/* ---------- 分栏（宽屏：目录缩左 + 词条右侧；窄屏：保持全屏切换） ---------- */
function isWide() {
  return window.innerWidth >= 900;
}

function enterSplit(id) {
  state.entryId = id;
  if (!isWide()) {
    // 窄屏：保持原全屏切换
    showView('entryView');
    renderEntry();
    return;
  }
  // 宽屏：目录留在左侧，词条进右侧
  document.querySelector('.container').classList.add('split');
  $('#homeView').hidden = false;
  $('#entryView').hidden = false;
  $('#learnView').hidden = true;
  $('#pathView').hidden = true;
  window.scrollTo({ top: 0 });
  renderEntry();
}

function clearSplit() {
  document.querySelector('.container').classList.remove('split');
  $('#entryView').hidden = true;
}

/* 窗口宽度变化（桌面↔手机）时重新路由，切换分栏/全屏 */
window.addEventListener('resize', route);

/* ---------- 回首页（header 常驻 🏠） ---------- */
function goHome() {
  location.hash = '';
  clearSplit();
  showView('homeView');
}
$('#homeBtn').addEventListener('click', goHome);
$('#entryClose').addEventListener('click', goHome);

/* ---------- 搜索面板（点 🔍 在当前页展开，不跳转、不改变当前页面） ---------- */
function openSearch() {
  $('#searchDrop').hidden = false;
  $('#searchInput').value = state.query;
  $('#searchInput').focus();
  runSearch();
}

function closeSearch() {
  $('#searchDrop').hidden = true;
  state.query = '';
  $('#searchInput').value = '';
}

$('#searchToggle').addEventListener('click', () => {
  if ($('#searchDrop').hidden) openSearch();
  else closeSearch();
});
$('#searchClose').addEventListener('click', closeSearch);

$('#searchInput').addEventListener('input', (e) => {
  state.query = e.target.value.trim().toLowerCase();
  runSearch();
});

function runSearch() {
  const results = $('#searchDropResults');
  if (!state.query) {
    results.hidden = true;
    results.innerHTML = '';
    return;
  }
  results.hidden = false;

  const hits = state.data.words.filter((w) =>
    [w.title, w.en, w.zh, w.alias, w.def]
      .filter(Boolean)
      .some((t) => t.toLowerCase().includes(state.query))
  );

  if (!hits.length) {
    results.innerHTML = '<div class="muted small" style="padding:10px 4px">没有找到匹配的词，换个关键词试试～</div>';
    return;
  }

  results.innerHTML = '';
  hits.forEach((w) => {
    const item = document.createElement('div');
    item.className = 'result-item';
    const meta = [w.en, w.zh, w.alias].filter(Boolean).join(' · ');
    item.innerHTML =
      '<div class="result-title">' + escapeHtml(w.title) + (w.adv ? ' <span style="font-size:11px;color:#4f6ef7">进阶</span>' : '') + '</div>' +
      '<div class="result-def">' + escapeHtml(w.def) + '</div>' +
      (meta ? '<div class="result-meta">' + escapeHtml(meta) + '</div>' : '');
    item.addEventListener('click', () => {
      closeSearch();
      openEntry(w.id);
    });
    results.appendChild(item);
  });
}

/* ---------- 词条内容（词条页 / 学习模式共用） ---------- */
function wordContentHtml(w) {
  const meta = [];
  if (w.en) meta.push('<b>英文</b>：' + escapeHtml(w.en));
  if (w.zh) meta.push('<b>中文</b>：' + escapeHtml(w.zh));
  if (w.alias) meta.push('<b>别名</b>：' + escapeHtml(w.alias));

  // 通俗类比
  let analogyHtml = '';
  if (w.analogy) {
    analogyHtml =
      '<div class="entry-block analogy">' +
      '<div class="block-title">💡 通俗类比</div>' +
      '<div class="block-body">' + escapeHtml(w.analogy) + '</div>' +
      '</div>';
  }

  // 相关词（折叠区外，随时可点）
  let relatedHtml = '';
  if (w.related && w.related.length) {
    relatedHtml = '<div class="related-block"><div class="related-title">讲到这个词，你可能还想看：</div>';
    w.related.forEach((rid) => {
      const rw = byId(rid);
      if (rw) {
        relatedHtml += '<span class="related-chip" data-id="' + rw.id + '">' + escapeHtml(rw.title) + '</span>';
      }
    });
    relatedHtml += '</div>';
  }

  // 折叠区：场景 / 误区 / 混淆
  let tips = '';
  if (w.scene) tips += '<div class="tip-item"><span class="tip-label">📍 现实哪里会见到：</span>' + escapeHtml(w.scene) + '</div>';
  if (w.mistake) tips += '<div class="tip-item"><span class="tip-label">⚠️ 容易搞错的误区：</span>' + escapeHtml(w.mistake) + '</div>';
  if (w.confuse) tips += '<div class="tip-item"><span class="tip-label">🔀 容易混淆：</span>' + escapeHtml(w.confuse) + '</div>';
  const tipsHtml = tips
    ? '<details class="entry-tips"><summary>💡 更多小提示</summary><div class="tips-body">' + tips + '</div></details>'
    : '';

  return (
    '<div class="card entry-card">' +
    '<div class="entry-title">' + escapeHtml(w.title) + '</div>' +
    (meta.length ? '<div class="meta-line">' + meta.join('　') + '</div>' : '') +
    '<span class="layer-tag' + (w.adv ? ' adv' : '') + '">' + escapeHtml(w.layer) + '</span>' +
    (w.updated ? '<span class="entry-updated">更新于 ' + escapeHtml(w.updated) + '</span>' : '') +
    '<div class="entry-def"><span class="block-title">📖 是什么</span><div class="block-body">' + escapeHtml(w.def) + '</div></div>' +
    analogyHtml +
    relatedHtml +
    tipsHtml +
    '</div>'
  );
}

function bindEntryClicks(container) {
  container.querySelectorAll('.related-chip').forEach((el) => {
    el.addEventListener('click', () => openEntry(el.dataset.id));
  });
}

/* ---------- 词条详情（纯词条页） ---------- */
function openEntry(id) {
  const w = byId(id);
  if (!w) return;
  state.entryId = id;
  if (location.hash !== '#' + id) location.hash = id; // 触发 hashchange → route
  else enterSplit(id);
}

function renderEntry() {
  const w = byId(state.entryId);
  if (!w) return;
  const box = $('#entryContent');
  box.innerHTML = wordContentHtml(w);
  bindEntryClicks(box);
}

/* ---------- 学习模式（18 步，独立流程） ---------- */
function startLearn() {
  location.hash = 'learn/0';
}

function showLearn(idx) {
  state.learnIdx = idx;
  showView('learnView');

  const step = state.data.path[idx];
  const total = state.data.path.length;
  $('#learnProgress').textContent = '🚀 第 ' + (idx + 1) + ' / ' + total + ' 步 · ' + step.note;

  const body = $('#learnBody');
  body.innerHTML = wordContentHtml(byId(step.ids[0]));
  bindEntryClicks(body);

  $('#learnPrev').disabled = (idx === 0);
  $('#learnNext').disabled = (idx === total - 1);
  $('#learnNext').textContent = (idx === total - 1) ? '完成 🎉' : '下一步 →';
}

$('#startLearnBtn').addEventListener('click', (e) => { e.preventDefault(); startLearn(); });
$('#learnExit').addEventListener('click', goHome);
$('#learnAllLink').addEventListener('click', (e) => { e.preventDefault(); location.hash = 'path'; });
$('#learnPrev').addEventListener('click', () => {
  if (state.learnIdx > 0) location.hash = 'learn/' + (state.learnIdx - 1);
});
$('#learnNext').addEventListener('click', () => {
  if (state.learnIdx < state.data.path.length - 1) location.hash = 'learn/' + (state.learnIdx + 1);
});

/* ---------- 添加到桌面（统一入口，平台自适应，不自动弹） ---------- */
let deferredPrompt = null;
// Chrome / Edge 等支持原生安装提示的浏览器会触发此事件
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
});
window.addEventListener('appinstalled', () => { deferredPrompt = null; });

function detectPlatform() {
  const ua = navigator.userAgent;
  if (/iPhone|iPad|iPod/i.test(ua)) return 'ios';
  if (/Android/i.test(ua)) return 'android';
  return 'desktop';
}

function installStepsHtml(platform) {
  // 支持原生安装的浏览器：提供一键安装按钮
  let btnHtml = '';
  if (deferredPrompt) {
    btnHtml = '<button id="pwaInstallBtn" class="btn-primary modal-btn">📲 立即安装</button>';
  }

  let steps = '';
  if (platform === 'ios') {
    steps =
      '<div class="step"><span class="step-title">① 点浏览器底部的「分享」按钮</span><div class="step-desc">方框加向上箭头的图标</div></div>' +
      '<div class="step"><span class="step-title">② 选「添加到主屏幕」</span><div class="step-desc">列表往下滑能找到</div></div>' +
      '<div class="step"><span class="step-title">③ 点「添加」</span><div class="step-desc">桌面就有「词」字图标啦，点开全屏使用</div></div>';
  } else if (platform === 'android') {
    steps =
      '<div class="step"><span class="step-title">① 打开浏览器的「菜单」</span><div class="step-desc">一般在右上角或底部，不同手机浏览器位置不一样</div></div>' +
      '<div class="step"><span class="step-title">② 找「添加到主屏幕 / 安装应用」</span><div class="step-desc">找不到就在「分享」里找「添加到主屏幕」</div></div>' +
      '<div class="step"><span class="step-title">③ 确认添加</span><div class="step-desc">桌面就有「词」字图标啦</div></div>';
  } else {
    steps =
      '<div class="step"><span class="step-title">① 点浏览器右上角的「菜单」</span><div class="step-desc">或看地址栏右侧有没有「安装」图标</div></div>' +
      '<div class="step"><span class="step-title">② 选「安装 / 应用」</span></div>' +
      '<div class="step"><span class="step-title">③ 确认安装</span><div class="step-desc">桌面或开始菜单就有图标</div></div>';
  }
  return btnHtml + steps;
}

$('#installLink').addEventListener('click', (e) => {
  e.preventDefault();
  $('#installSteps').innerHTML = installStepsHtml(detectPlatform());
  $('#installModal').classList.add('open');

  const btn = $('#pwaInstallBtn');
  if (btn) {
    btn.addEventListener('click', async () => {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
      $('#installModal').classList.remove('open');
    });
  }
});
$('#installClose').addEventListener('click', () => { $('#installModal').classList.remove('open'); });
$('#installModal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) $('#installModal').classList.remove('open');
});

/* ---------- 反馈 & 纠错（弹窗） ---------- */
$('#feedbackLink').addEventListener('click', (e) => {
  e.preventDefault();
  $('#feedbackModal').classList.add('open');
});
$('#feedbackClose').addEventListener('click', () => { $('#feedbackModal').classList.remove('open'); });
$('#feedbackModal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) $('#feedbackModal').classList.remove('open');
});

/* ---------- 工具 ---------- */
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ---------- 启动（置于所有声明之后，避免 const 暂时性死区） ---------- */
const inlineData = window.__WORDS__ || null;
if (inlineData) {
  boot(inlineData);
} else {
  fetch('words.json')
    .then((r) => {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(boot)
    .catch((err) => {
      $('#homeView').innerHTML =
        '<div class="card">加载失败：' + escapeHtml(String(err)) +
        '<br>请确认 words.json 与页面在同一目录。</div>';
    });
}

/* ---------- PWA：注册 Service Worker（支持添加到桌面 / 离线） ---------- */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}
