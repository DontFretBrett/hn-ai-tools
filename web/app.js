'use strict';
const $ = (s, root = document) => root.querySelector(s);
const number = n => new Intl.NumberFormat('en-US').format(n);
const dateLabel = date => new Date(`${date}T12:00:00Z`).toLocaleDateString('en-US', {month:'short',year:'numeric',timeZone:'UTC'});
const fullDate = date => new Date(`${date}T12:00:00Z`).toLocaleDateString('en-US', {month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});
const node = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; };
const safeURL = value => { try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : '#'; } catch { return '#'; } };
const external = (url, cls, text) => { const a = node('a', cls, text); a.href = safeURL(url); a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; };
let tools = [], meta, filtered = [], shown = 40, current = {}, rank = new Map(), years = [], cutoff;
const searchIndex = new Map();
const params = new URLSearchParams(location.search);
const allowedSorts = ['score','comments','authors','last_seen','first_seen'];
current = { q: params.get('q') || '', category: params.get('category') || '', sort: allowedSorts.includes(params.get('sort')) ? params.get('sort') : 'score', recent: params.get('recent') === '1' };

function setTheme(theme) { document.documentElement.dataset.theme = theme; $('#theme').setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`); }
try { const theme = localStorage.getItem('hn-ai-theme'); if (theme === 'light' || theme === 'dark') setTheme(theme); } catch {}
$('#theme').addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light');
  const next = theme === 'dark' ? 'light' : 'dark'; setTheme(next); try { localStorage.setItem('hn-ai-theme', next); } catch {}
});

function updateURL() {
  const p = new URLSearchParams();
  if (current.q) p.set('q', current.q);
  if (current.category) p.set('category', current.category);
  if (current.sort !== 'score') p.set('sort', current.sort);
  if (current.recent) p.set('recent','1');
  history.replaceState(null, '', `${location.pathname}${p.size ? '?' + p : ''}${location.hash}`);
}

function sparkline(tool) {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg'); svg.classList.add('spark'); svg.setAttribute('height', '56'); svg.setAttribute('role', 'img');
  const label = years.map(y => `${y}: ${number(tool.by_year[y] || 0)} recommendations`).join(', ');
  svg.setAttribute('aria-label', label);
  const title = document.createElementNS(ns, 'title'); title.textContent = label; svg.append(title);
  const make = (tag, attrs) => { const n = document.createElementNS(ns, tag); for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v); return n; };
  const max = Math.max(1, ...years.map(y => tool.by_year[y] || 0));
  svg.append(make('line',{x1:0,y1:32,x2:'100%',y2:32}));
  const width = 100 / years.length;
  years.forEach((y,i) => {
    const count = tool.by_year[y] || 0, height = count ? Math.max(2,24*count/max) : 1;
    svg.append(make('rect',{x:`${i*width+width*.15}%`,y:32-height,width:`${width*.7}%`,height,rx:1}));
    const text = make('text',{x:`${i*width+width/2}%`,y:52,'text-anchor':'middle','font-size':14}); text.textContent = String(y).slice(2); svg.append(text);
  });
  return svg;
}

function chooseCategory(category) { current.category = current.category === category ? '' : category; shown = 40; render(); }

function card(tool) {
  const article = node('article', 'tool');
  const r = rank.get(tool.key);
  article.append(node('div', `rank${r <= 3 ? ' top-rank' : ''}`, String(r).padStart(2,'0')));
  const body = node('div', 'tool-body'), nameRow = node('div', 'tool-name-row');
  const heading = node('h3'); heading.style.margin = '0';
  const name = external(tool.url, 'tool-name', tool.name); const arrow = node('span', 'out-arrow','↗'); arrow.setAttribute('aria-hidden','true'); name.append(arrow); heading.append(name); nameRow.append(heading);
  nameRow.append(node('span', 'tool-key', tool.key)); body.append(nameRow);
  if (tool.links?.length) {
    const links = node('div', 'tool-links'); links.setAttribute('aria-label', 'Secondary links');
    for (const link of tool.links) links.append(external(link.url, '', `${link.label} ↗`));
    body.append(links);
  }
  body.append(node('p','tool-description',tool.description));
  const tags = node('div', 'tool-tags');
  for (const category of tool.categories) { const tag = node('button', 'tag', category); tag.type = 'button'; tag.setAttribute('aria-label',`Filter by ${category}`); tag.addEventListener('click',() => { chooseCategory(category); $('.directory').scrollIntoView({behavior:'instant'}); }); tags.append(tag); }
  body.append(tags);
  const stats = node('div','tool-meta');
  for (const [value,label] of [[tool.comments,'recommendations'],[tool.authors,'authors'],[tool.months,'months active']]) { const span = node('span'); span.append(node('b','',number(value)), document.createTextNode(` ${label}`)); stats.append(span); }
  stats.append(node('span','dates',`${dateLabel(tool.first_seen)} → ${dateLabel(tool.last_seen)}`)); body.append(stats); article.append(body);
  const chart = node('div','chart-col'); const score = node('div','score',tool.score.toFixed(1));
  score.title = `Score: ${tool.score}. Months active + ½ log₂(1 + authors) + up to 2 points for strong recommendations.`;
  chart.append(score,node('div','score-label','REC SCORE'),sparkline(tool)); article.append(chart);
  if (tool.snippets.length) {
    const details = node('details','evidence'); const summary = node('summary','',`In the comments · ${tool.snippets.length} excerpts`); details.append(summary);
    const quotes = node('div','quotes');
    for (const quote of tool.snippets) {
      const block = node('blockquote','quote'); block.append(node('p','',quote.text));
      const footer = node('footer'); const cite = node('cite','',`${quote.author} · ${fullDate(quote.date)}`);
      footer.append(cite,external(quote.url,'','View on HN ↗')); block.append(footer); quotes.append(block);
    }
    details.append(quotes); article.append(details);
  }
  return article;
}

function matchesBase(tool) {
  return (!current.q || searchIndex.get(tool.key).includes(current.q.toLocaleLowerCase())) && (!current.recent || tool.last_seen >= cutoff);
}

function renderChips(base) {
  const root = $('#categories'); root.replaceChildren();
  for (const [category, count] of [['',base.length], ...meta.categories.map(c => [c,base.filter(t => t.categories.includes(c)).length])]) {
    const button = node('button','chip',category || 'All tools'); button.type = 'button'; button.setAttribute('aria-pressed',String(current.category === category)); button.append(node('span','',number(count))); button.addEventListener('click',()=> chooseCategory(category)); root.append(button);
  }
}

function renderList() {
  const root = $('#results'); root.replaceChildren();
  if (!filtered.length) {
    const empty = node('div','empty'); empty.append(node('h3','','No matching tools'), node('p','','Try a different search or clear the filters.'));
    const clear = node('button','','Clear filters'); clear.addEventListener('click',()=> { current.q=''; current.category=''; current.recent=false; $('#search').value=''; $('#recent').checked=false; render(); }); empty.append(clear); root.append(empty);
  } else {
    const fragment = document.createDocumentFragment(); for (const tool of filtered.slice(0,shown)) fragment.append(card(tool)); root.append(fragment);
  }
  root.setAttribute('aria-busy','false');
  $('#load-more').hidden = shown >= filtered.length;
  $('#page-count').textContent = filtered.length ? `${number(Math.min(shown,filtered.length))} of ${number(filtered.length)} tools` : '';
}

function render() {
  if (!meta) return;
  const base = tools.filter(matchesBase); renderChips(base);
  filtered = base.filter(t => !current.category || t.categories.includes(current.category));
  filtered.sort((a,b) => {
    const comparison = ['first_seen','last_seen'].includes(current.sort) ? b[current.sort].localeCompare(a[current.sort]) : b[current.sort] - a[current.sort];
    return comparison || b.score-a.score || a.key.localeCompare(b.key);
  });
  const result = $('#result-count'); result.replaceChildren(node('strong','',number(filtered.length)), document.createTextNode(` tools${current.category ? ' in '+current.category : ' in the index'}`));
  renderList(); updateURL();
}

$('#search').value = current.q; $('#sort').value = current.sort; $('#recent').checked = current.recent;
let debounce;
$('#search').addEventListener('input', e => { clearTimeout(debounce); debounce = setTimeout(()=> { current.q=e.target.value.trim(); shown=40; render(); },120); });
$('#sort').addEventListener('change', e => { current.sort=e.target.value; shown=40; render(); });
$('#recent').addEventListener('change', e => { current.recent=e.target.checked; shown=40; render(); });
$('#load-more').addEventListener('click',()=> { const count = Math.min(shown,filtered.length); shown+=40; renderList(); const next = $('#results').children[count]?.querySelector('a'); if (next) next.focus({preventScroll:true}); });
document.addEventListener('keydown',e => { if (e.key==='/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName) && !$('#about').open) { e.preventDefault(); $('#search').focus(); } });
const about = $('#about');
function syncAbout() { if (location.hash === '#about' && !about.open) about.showModal(); else if (location.hash !== '#about' && about.open) about.close(); }
window.addEventListener('hashchange',syncAbout);
$('#close-about').addEventListener('click',()=> about.close());
about.addEventListener('click',e => { const r=about.getBoundingClientRect(); if (e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom) about.close(); });
about.addEventListener('close',()=> { if (location.hash==='#about') history.replaceState(null,'',location.pathname+location.search); });
syncAbout();

async function load() {
  try {
    const responses = await Promise.all(['data/tools.json','data/meta.json'].map(url => fetch(url,{cache:'no-cache'})));
    if (responses.some(r => !r.ok)) throw new Error('The index data could not be loaded.');
    [tools, meta] = await Promise.all(responses.map(r => r.json()));
    if (!Array.isArray(tools) || !meta.date_range) throw new Error('The index data has an unexpected format.');
    if (meta.tools_listed !== tools.length) throw new Error('The index is being updated. Please try again.');
    if (current.category && !meta.categories.includes(current.category)) current.category='';
    tools.forEach((tool,i) => { rank.set(tool.key,i+1); searchIndex.set(tool.key,[tool.name,tool.key,tool.description,...(tool.links || []).map(link=>link.label),...tool.snippets.map(q=>q.text)].join(' ').toLocaleLowerCase()); });
    const firstYear = Number(meta.date_range.start.slice(0,4)), lastYear = Number(meta.date_range.end.slice(0,4));
    years = Array.from({length:lastYear-firstYear+1},(_,i) => firstYear+i);
    const last = new Date(`${meta.date_range.end}T00:00:00Z`); last.setUTCFullYear(last.getUTCFullYear()-1); cutoff=last.toISOString().slice(0,10);
    $('#stat-comments').textContent = number(meta.comments_scanned); $('#stat-tools').textContent = number(tools.length);
    $('#stat-range').textContent = `${dateLabel(meta.date_range.start)} — ${dateLabel(meta.date_range.end)}`;
    $('#stat-months').textContent = `${number(meta.months_processed.length)} months in the archive`;
    $('#edition').textContent = `/ ${firstYear}—${lastYear}`;
    $('#updated').textContent = `Index updated ${new Date(meta.generated_at).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}`;
    $('#about-data').textContent = `${number(meta.comments_scanned)} comments scanned · ${number(meta.comments_with_links)} with outbound links · ${number(meta.months_processed.length)} monthly files · ${fullDate(meta.date_range.start)} to ${fullDate(meta.date_range.end)}.${meta.topup_comments ? ' Includes '+number(meta.topup_comments)+' additional Algolia comments.' : ''}`;
    render();
  } catch (error) {
    const root = $('#results'); root.replaceChildren(); root.setAttribute('aria-busy','false');
    const block = node('div','empty'); block.append(node('h3','','The archive hasn’t loaded yet.'),node('p','',location.protocol==='file:' ? 'Serve the web folder over HTTP to load the index data. See README.md for the command.' : error.message));
    const retry = node('button','','Try again'); retry.addEventListener('click',load); block.append(retry); root.append(block); $('#result-count').textContent='Index unavailable';
  }
}
load();
