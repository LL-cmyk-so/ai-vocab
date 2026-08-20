/* ============ AI 词汇本：逻辑 ============
   纯前端静态页面：读取 words.json，本地渲染、搜索、跳转。
   视图路由（hash）：# 首页 · #path 主线页 · #gallery 词库页 · #词条id 详情 */

'use strict';

const $ = (sel) => document.querySelector(sel);

const state = {
  data: null,   // words.json 全部数据
  query: '',
  entryId: null,
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

/* 一个词在主线中的位置（可能出现在多步，取第一步） */
function pathIndexOf(id) {
  if (!state.data) return -1;
  return state.data.path.findIndex((s) => s.ids.includes(id));
}

/* ---------- 静态内容渲染（数据加载后渲染一次） ---------- */
function renderStatic() {
  // 热门词快捷入口
  const hot = $('#hotChips');
  hot.innerHTML = '';
  state.data.hot.forEach((id) => {
    const w = byId(id);
    if (!w) return;
    const chip = document.createElement('span');
    chip.className = 'chip chip-hot';
    chip.textContent = w.title;
    chip.addEventListener('click', () => openEntry(w.id));
    hot.appendChild(chip);
  });

  // 主线 18 步列表
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

  // 层级分组（词库页）
  const wrap = $('#groups');
  wrap.innerHTML = '';
  state.data.layers.forEach((layer) => {
    const words = state.data.words.filter((w) => w.layer === layer.id);
    if (!words.length) return;
    const block = document.createElement('div');
    block.className = 'layer-block';
    block.innerHTML =
      '<div class="layer-head">' +
      '<span class="layer-name">' + escapeHtml(layer.id) + '</span>' +
      '<span class="layer-desc">' + escapeHtml(layer.desc) + ' · ' + words.length + ' 词</span>' +
      '</div>' +
      '<div class="chip-wrap"></div>';
    const chipWrap = block.querySelector('.chip-wrap');
    words.forEach((w) => {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = w.title;
      chip.addEventListener('click', () => openEntry(w.id));
      chipWrap.appendChild(chip);
    });
    wrap.appendChild(block);
  });
}

/* ---------- 视图路由 ---------- */
const VIEWS = ['homeView', 'pathView', 'galleryView', 'entryView'];

function showView(name) {
  VIEWS.forEach((v) => {
    $('#' + v).hidden = (v !== name);
  });
  window.scrollTo({ top: 0 });
}
const showHome = () => showView('homeView');
const showPath = () => showView('pathView');
const showGallery = () => showView('galleryView');
const showEntry = () => showView('entryView');

function route() {
  const h = decodeURIComponent(location.hash.slice(1));
  if (h === 'path') showPath();
  else if (h === 'gallery') showGallery();
  else if (h && byId(h)) {
    state.entryId = h;
    renderEntry();
  } else {
    showHome();
  }
}

window.addEventListener('hashchange', route);

/* ---------- 首页按钮 ---------- */
$('#startPathBtn').addEventListener('click', () => { location.hash = 'path'; });
$('#galleryBtn').addEventListener('click', () => { location.hash = 'gallery'; });

/* ---------- 搜索 ---------- */
$('#searchInput').addEventListener('input', (e) => {
  state.query = e.target.value.trim().toLowerCase();
  applySearch();
});

function applySearch() {
  const results = $('#searchResults');
  const list = $('#searchResultList');
  const homeMain = $('#homeMain');

  if (!state.query) {
    results.hidden = true;
    homeMain.hidden = false;
    return;
  }

  // 搜索时：回到首页，结果置顶显示，隐藏首页主体
  if (location.hash !== '') history.replaceState(null, '', '#');
  showHome();
  results.hidden = false;
  homeMain.hidden = true;

  const hits = state.data.words.filter((w) =>
    [w.title, w.en, w.zh, w.alias, w.def]
      .filter(Boolean)
      .some((t) => t.toLowerCase().includes(state.query))
  );

  if (!hits.length) {
    list.innerHTML = '<div class="muted small" style="padding:8px 4px">没有找到匹配的词，换个关键词试试～</div>';
    return;
  }

  list.innerHTML = '';
  hits.forEach((w) => {
    const item = document.createElement('div');
    item.className = 'result-item';
    const meta = [w.en, w.zh, w.alias].filter(Boolean).join(' · ');
    item.innerHTML =
      '<div class="result-title">' + escapeHtml(w.title) + '</div>' +
      '<div class="result-def">' + escapeHtml(w.def) + '</div>' +
      (meta ? '<div class="result-meta">' + escapeHtml(meta) + '</div>' : '');
    item.addEventListener('click', () => openEntry(w.id));
    list.appendChild(item);
  });
}

/* ---------- 词条详情 ---------- */
function openEntry(id) {
  const w = byId(id);
  if (!w) return;
  state.entryId = id;
  if (location.hash !== '#' + id) location.hash = id; // 触发 hashchange → route
  else renderEntry();
}

function renderEntry() {
  const w = byId(state.entryId);
  if (!w) return;

  showEntry();

  const box = $('#entryContent');
  const meta = [];
  if (w.en) meta.push('<b>英文</b>：' + escapeHtml(w.en));
  if (w.zh) meta.push('<b>中文</b>：' + escapeHtml(w.zh));
  if (w.alias) meta.push('<b>别名</b>：' + escapeHtml(w.alias));

  // 相关词 chips
  let relatedHtml = '';
  if (w.related && w.related.length) {
    relatedHtml =
      '<div class="related-block">' +
      '<div class="related-title">讲到这个词，你可能还想看：</div>';
    w.related.forEach((rid) => {
      const rw = byId(rid);
      if (rw) {
        relatedHtml +=
          '<span class="related-chip" data-id="' + rw.id + '">' + escapeHtml(rw.title) + '</span>';
      }
    });
    relatedHtml += '</div>';
  }

  // 主线导航
  const pi = pathIndexOf(w.id);
  let pathHtml = '';
  if (pi >= 0) {
    const total = state.data.path.length;
    const prevBtn = pi > 0
      ? '<button data-nav="' + (pi - 1) + '">← 上一步</button>'
      : '<button disabled>← 上一步</button>';
    const nextBtn = pi < total - 1
      ? '<button data-nav="' + (pi + 1) + '">下一步 →</button>'
      : '<button disabled>下一步 →</button>';
    pathHtml =
      '<div class="path-nav">' +
      '<div class="path-nav-progress">🚀 主线路径 · 第 ' + (pi + 1) + ' / ' + total + ' 步 · ' +
      escapeHtml(state.data.path[pi].note) + '</div>' +
      '<div class="path-nav-btns">' + prevBtn + nextBtn + '</div>' +
      '</div>';
  }

  box.innerHTML =
    '<div class="card entry-card">' +
    '<div class="entry-title">' + escapeHtml(w.title) + '</div>' +
    (meta.length ? '<div class="meta-line">' + meta.join('　') + '</div>' : '') +
    '<span class="layer-tag">' + escapeHtml(w.layer) + '</span>' +
    '<div class="entry-def">' + escapeHtml(w.def) + '</div>' +
    relatedHtml +
    pathHtml +
    '</div>';

  // 绑定相关词跳转
  box.querySelectorAll('.related-chip').forEach((el) => {
    el.addEventListener('click', () => openEntry(el.dataset.id));
  });
  // 绑定主线导航
  box.querySelectorAll('[data-nav]').forEach((el) => {
    el.addEventListener('click', () => {
      const step = state.data.path[Number(el.dataset.nav)];
      if (step) openEntry(step.ids[0]);
    });
  });
}

/* ---------- 返回按钮 ---------- */
function goBack() {
  if (history.length > 1) {
    history.back();
  } else {
    location.hash = '';
    showHome();
  }
}
document.querySelectorAll('[data-back]').forEach((btn) => {
  btn.addEventListener('click', goBack);
});
$('#backBtn').addEventListener('click', goBack);

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
