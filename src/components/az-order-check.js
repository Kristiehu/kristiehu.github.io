/* az-order-check — the route viewer as a custom element.
 *
 *   <az-order-check src="/az-order-check-data.json"></az-order-check>
 *
 * It draws inside a shadow root, so the page's CSS and its own cannot reach each
 * other — but custom properties still inherit in, so it takes its colours and
 * fonts from the site's own tokens and follows the light/dark switch with no
 * JavaScript of its own.
 *
 * Generated from web/template.html by demo/build_embed.py — edit that, not this.
 */
const CSS = '\n/* Layout: one cable at a time - ID in, numbered sequence on the base map,\n   the discrepancy named beside it. Nothing else on the page. */\n:host{\n  /* Everything is derived from the host site\'s own tokens, so the widget follows\n     its light/dark switch with no JavaScript - custom properties inherit straight\n     through a shadow boundary. One accent, var(--blue): the route and the ordinary\n     positions are drawn in ink, and blue is kept for the positions the check wants\n     you to look at. */\n  --az-plane: rgb(var(--paper));\n  --az-surface: rgb(var(--paper));\n  --az-surface-2: rgba(var(--ink), 0.035);\n  --az-inset: rgba(var(--ink), 0.06);\n  --az-ink: rgb(var(--black));\n  --az-ink-2: rgba(var(--ink), 0.72);\n  --az-ink-3: rgba(var(--ink), 0.5);\n  --az-rule: rgba(var(--ink), 0.13);\n  --az-block: rgba(var(--ink), 0.055);\n  --az-street: rgb(var(--paper));\n  /* open space, tinted from the page colour so it follows the theme */\n  --az-park: color-mix(in srgb, rgb(var(--paper)) 86%, #3a7d44);\n  /* the route and its ordinary positions are the site accent; a position the\n     check flags is the Data systems red from src/data/directions.ts, so the\n     widget introduces no colour the site does not already use */\n  --az-accent: var(--blue);\n  --az-accent-soft: rgba(var(--blue-rgb), 0.12);\n  --az-alert: rgb(216, 58, 31);\n  --az-alert-soft: color-mix(in srgb, rgb(var(--paper)) 88%, rgb(216, 58, 31));\n  --az-warn: rgba(var(--ink), 0.6);\n  --az-warn-soft: rgba(var(--ink), 0.05);\n  --az-good: rgba(var(--ink), 0.6);\n  --az-good-soft: rgba(var(--ink), 0.05);\n  --az-marker-ink: #fff;\n  /* the site\'s three type roles, used the way the site uses them: sentences in\n     the text face, small uppercase labels in the UI face, identifiers in mono */\n  --az-sans: var(--font-text);\n  --az-label: var(--font-ui);\n  --az-mono: var(--font-mono);\n  --az-r: 4px;\n}\n\n*{box-sizing:border-box}\nbody{margin:0;background:var(--az-plane);color:var(--az-ink);font-family:var(--az-sans);\n  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}\n.wrap{max-width:1180px;margin:0 auto;padding-inline:16px;padding-block:30px 48px;\n  display:flex;flex-direction:column;gap:20px}\nh1{margin:0;text-wrap:balance;letter-spacing:-.014em;\n  font-size:clamp(1.6rem,4vw,2.3rem);font-weight:700;line-height:1.15}\np{margin:0}\n.eyebrow{font-family:var(--az-mono);font-size:.69rem;font-weight:500;letter-spacing:.13em;\n  text-transform:uppercase;color:var(--az-ink-3)}\n.lede{color:var(--az-ink-2);max-width:68ch;font-size:1.02rem}\n.card{background:var(--az-surface);border:1px solid var(--az-rule);border-radius:var(--az-r)}\n:focus-visible{outline:2px solid var(--az-accent);outline-offset:2px;border-radius:3px}\nheader{display:flex;flex-direction:column;gap:10px}\n\n/* ---- controls ---- */\n.controls{display:flex;flex-wrap:wrap;gap:9px 14px;align-items:center;\n  padding:13px 18px;border-bottom:1px solid var(--az-rule)}\n.field{display:flex;align-items:center;gap:8px}\n.field label{font-family:var(--az-label);font-size:.68rem;letter-spacing:.1em;\n  text-transform:uppercase;color:var(--az-ink-3)}\ninput[type="text"]{font:inherit;font-family:var(--az-mono);font-size:.86rem;width:17ch;\n  padding:5px 9px;border:1px solid var(--az-rule);border-radius:var(--az-r);\n  background:var(--az-surface-2);color:var(--az-ink)}\n.btn{font:inherit;font-size:.8rem;font-family:var(--az-label);background:var(--az-surface-2);\n  color:var(--az-ink-2);border:1px solid var(--az-rule);border-radius:var(--az-r);\n  padding:5px 11px;cursor:pointer}\n.btn:hover{background:var(--az-inset);color:var(--az-ink)}\n.btn.step{padding:5px 9px}\n.spacer{margin-left:auto}\n.toggle{display:flex;align-items:center;gap:7px;font-size:.8rem;color:var(--az-ink-2);cursor:pointer}\n.miss{font-size:.8rem;color:var(--az-alert)}\n\n/* ---- map ---- */\n.viewer{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);align-items:stretch}\n.mapcol{border-right:1px solid var(--az-rule);min-width:0}\n.mapwrap{position:relative}\nsvg.map{display:block;width:100%;height:auto;aspect-ratio:4/3.3;max-width:100%;\n  background:var(--az-street)}\n.run{stroke:var(--az-accent);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round;\n  vector-effect:non-scaling-stroke}\n.other{stroke:var(--az-ink-3);stroke-width:1;fill:none;opacity:.35;vector-effect:non-scaling-stroke}\n.mk-halo{fill:var(--az-surface)}\n.mk{fill:var(--az-accent)}\n.mk.bad{fill:var(--az-alert)}\n.mk-txt{fill:var(--az-marker-ink);font-family:var(--az-mono);font-weight:600;\n  text-anchor:middle;dominant-baseline:central;pointer-events:none}\n.mk-txt.bad{font-weight:700}\n.end-txt{fill:var(--az-ink);font-family:var(--az-label);font-weight:600;text-anchor:middle;\n  paint-order:stroke;stroke:var(--az-surface);stroke-width:3px;stroke-linejoin:round}\n.maplabel{position:absolute;font-family:var(--az-label);font-size:.66rem;color:var(--az-ink-3);\n  letter-spacing:.06em;pointer-events:none;z-index:2}\n.scalebar{left:12px;bottom:10px;display:flex;flex-direction:column;gap:3px;align-items:flex-start}\n.scalebar .bar{height:5px;border:1px solid var(--az-ink-3);border-top:none;box-sizing:content-box}\n.north{right:12px;top:10px;text-align:center;line-height:1.1}\n.basenote{left:12px;top:10px;background:var(--az-surface);border:1px solid var(--az-rule);\n  border-radius:3px;padding:2px 7px}\n.legend{display:flex;flex-wrap:wrap;gap:6px 16px;padding:11px 16px;border-top:1px solid var(--az-rule);\n  font-size:.76rem;color:var(--az-ink-2)}\n.legend span{display:flex;align-items:center;gap:7px;white-space:nowrap}\n.legend i{width:20px;height:0;border-top-width:2px;border-top-style:solid;flex:none}\n.legend b.dot{width:14px;height:14px;border-radius:50%;flex:none;display:block}\n\n/* ---- panel ---- */\n.panel{display:flex;flex-direction:column;min-width:0;overflow:hidden}\n.verdict{padding:15px 18px;border-bottom:1px solid var(--az-rule);display:flex;\n  flex-direction:column;gap:7px}\n.verdict .top{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:baseline}\n.verdict .cid{font-family:var(--az-mono);font-size:1.05rem;font-weight:600}\n.verdict .say{font-size:.95rem}\n.verdict .say.bad{color:var(--az-alert);font-weight:450}\n.ends{display:flex;gap:16px;flex-wrap:wrap;font-size:.8rem;color:var(--az-ink-3)}\n.ends b{font-family:var(--az-mono);color:var(--az-ink-2);font-weight:450}\n.pill{display:inline-block;font-family:var(--az-label);font-size:.64rem;letter-spacing:.08em;\n  text-transform:uppercase;padding:1px 6px;border-radius:3px;border:1px solid;white-space:nowrap}\n.v-likely_error{color:var(--az-alert);border-color:var(--az-alert);background:var(--az-alert-soft)}\n.v-review{color:var(--az-warn);border-color:var(--az-warn);background:var(--az-warn-soft)}\n.v-unverified{color:var(--az-ink-2);border-color:var(--az-rule);background:var(--az-surface-2)}\n.v-ok,.v-clean{color:var(--az-good);border-color:var(--az-good);background:var(--az-good-soft)}\n.planted{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 18px;\n  border-bottom:1px solid var(--az-rule);background:var(--az-surface-2);font-size:.82rem;color:var(--az-ink-2)}\n.seqhead{display:flex;justify-content:space-between;align-items:baseline;gap:10px;\n  padding:12px 18px 0}\n.seqhead span{font-family:var(--az-label);font-size:.67rem;letter-spacing:.09em;\n  text-transform:uppercase;color:var(--az-ink-3)}\n.strip{display:flex;flex-wrap:wrap;gap:3px;padding:8px 18px 14px;border-bottom:1px solid var(--az-rule)}\n.pos{font-family:var(--az-mono);font-size:.7rem;padding:2px 6px;border:1px solid var(--az-rule);\n  border-radius:3px;color:var(--az-ink-2);background:var(--az-surface-2);\n  font-variant-numeric:tabular-nums;cursor:default}\n.pos b{color:var(--az-ink-3);font-weight:600;margin-right:4px}\n.pos.bad{border-color:var(--az-alert);color:var(--az-alert);background:var(--az-alert-soft);font-weight:600}\n.pos.bad b{color:var(--az-alert)}\n.pos.ghost{border-style:dashed;color:var(--az-ink-3)}\n.panelbody{flex:1;min-height:0;overflow-y:auto}\n.panelbody.more{-webkit-mask-image:linear-gradient(to bottom,#000 calc(100% - 26px),transparent);\n  mask-image:linear-gradient(to bottom,#000 calc(100% - 26px),transparent)}\n.fixes{margin:0;padding:10px 18px 16px 18px;\n  list-style:none;counter-reset:fix;display:flex;flex-direction:column;gap:9px}\n.fixes li{counter-increment:fix;display:grid;grid-template-columns:1.5rem minmax(0,1fr);\n  gap:10px;font-size:.88rem;line-height:1.5}\n.fixes li::before{content:counter(fix) ".";font-family:var(--az-mono);font-size:.8rem;\n  color:var(--az-ink-3);text-align:right;padding-top:.1em}\n.fixes b{font-family:var(--az-mono);font-weight:600;font-size:.84rem;color:var(--az-ink)}\n.fixes li.none span{color:var(--az-ink-3)}\n.fixes li.none::before{content:""}\n\nfooter{font-size:.84rem;color:var(--az-ink-2);max-width:68ch;\n  display:flex;flex-direction:column;gap:8px}\nfooter b{color:var(--az-ink);font-weight:600}\n\n@container (max-width:880px){\n  svg.map{aspect-ratio:16/9}\n  .viewer{grid-template-columns:1fr}\n  .mapcol{border-right:0;border-bottom:1px solid var(--az-rule)}\n  .spacer{margin-left:0}\n}\n@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}\n\n:host{display:block;min-height:520px;background:var(--az-plane);color:var(--az-ink);\n  font-family:var(--az-sans);font-size:15px;line-height:1.55;\n  container-type:inline-size}\n:host *{box-sizing:border-box}\n:host :focus-visible{outline:2px solid var(--blue);outline-offset:2px;border-radius:3px}\n.loading{padding:22px 18px;color:var(--az-ink-3);font-size:.9rem}\n.loading code{font-family:var(--az-mono);font-size:.82rem;word-break:break-all}\n';
const MARKUP = '<section class="card">\n  <div class="controls">\n    <div class="field">\n      <label for="cable">Cable ID</label>\n      <input type="text" id="cable" list="ids" autocomplete="off" spellcheck="false">\n      <datalist id="ids"></datalist>\n    </div>\n    <button class="btn step" type="button" id="prev" aria-label="Previous cable">←</button>\n    <button class="btn step" type="button" id="next" aria-label="Next cable">→</button>\n    <button class="btn" type="button" id="rndBad">A cable with a discrepancy</button>\n    <button class="btn" type="button" id="rndOk">One that checks out</button>\n    <span class="miss" id="miss" hidden>No cable with that ID.</span>\n  </div>\n\n  <div class="viewer">\n    <div class="mapcol">\n      <div class="mapwrap">\n        <svg class="map" id="map" role="img" aria-label="The selected cable\'s recorded sequence\n          drawn over a synthetic street grid, each structure numbered in order."></svg>\n        <div class="maplabel basenote">generated data</div>\n        <div class="maplabel north">N<br>▲</div>\n        <div class="maplabel scalebar"><div class="bar" id="sbar"></div><span id="slab"></span></div>\n      </div>\n      <div class="legend">\n        <span><b class="dot" style="background:var(--az-accent)"></b>sequence position</span>\n        <span><b class="dot" style="background:var(--az-alert)"></b>position the check flags</span>\n        <span><i style="border-color:var(--az-accent);border-top-width:3px"></i>recorded order</span>\n        <span><i style="border-color:var(--az-ink-3);opacity:.5"></i>other cables nearby</span>\n      </div>\n    </div>\n    <div class="panel" id="panel"></div>\n  </div>\n</section>';

function mount(root, data) {
  const _off = [];
  const on = (t, e, f) => { t.addEventListener(e, f); _off.push(() => t.removeEventListener(e, f)); };

  const DATA = data;
  const $ = s => root.querySelector(s);
  const N = DATA.nodes, L = DATA.lines;
  const FLAGGED = new Set(["likely_error", "review", "unverified"]);

  /* ---------- projection ---------- */
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (const [x, y] of N) {
    if (x < minX) minX = x; if (x > maxX) maxX = x;
    if (y < minY) minY = y; if (y > maxY) maxY = y;
  }
  const step = DATA.grid.spacing, PAD = step;
  const X0 = minX - PAD, Y0 = minY - PAD;
  const W = maxX - minX + 2 * PAD, H = maxY - minY + 2 * PAD;
  const sx = x => x - X0;
  const sy = y => H - (y - Y0);                       // north up
  const d = ids => ids.map((i, k) => (k ? "L" : "M") +
    sx(N[i][0]).toFixed(1) + " " + sy(N[i][1]).toFixed(1)).join(" ");

  const byLabel = Object.fromEntries(L.map(l => [l.label, l]));
  const ranked = [...L].sort((a, b) => b.risk - a.risk || (a.id < b.id ? -1 : 1));

  /* ---------- base map, drawn once ---------- */
  const svg = $("#map"), ns = "http://www.w3.org/2000/svg";
  const el = (t, a, txt) => {
    const e = document.createElementNS(ns, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  };
  const gBase = el("g", {}), gOther = el("g", {}), gRun = el("g", {});
  svg.append(gBase, gOther, gRun);

  gBase.appendChild(el("rect", { x: 0, y: 0, width: W, height: H, fill: "var(--az-block)" }));
  /* two parks, so the ground reads as a place rather than graph paper */
  for (const [cx, cy, w, h] of [[6, 18, 3, 2], [17, 7, 2, 3]]) {
    gBase.appendChild(el("rect", {
      x: sx(X0 + cx * step), y: sy(Y0 + (cy + h) * step),
      width: w * step, height: h * step, fill: "var(--az-park)"
    }));
  }
  const gStreet = el("g", { stroke: "var(--az-street)", "stroke-width": 24, fill: "none" });
  for (let v = Math.ceil(X0 / step) * step; v <= X0 + W; v += step) {
    gStreet.appendChild(el("line", { x1: sx(v), y1: 0, x2: sx(v), y2: H }));
  }
  for (let v = Math.ceil(Y0 / step) * step; v <= Y0 + H; v += step) {
    gStreet.appendChild(el("line", { x1: 0, y1: sy(v), x2: W, y2: sy(v) }));
  }
  gBase.appendChild(gStreet);

  /* ---------- viewBox ---------- */
  let vb = [0, 0, W, H], anim;
  function setVB(to, tween) {
    const apply = v => { svg.setAttribute("viewBox", v.join(" ")); vb = v; scalebar(); };
    if (!tween || matchMedia("(prefers-reduced-motion:reduce)").matches) return apply(to);
    cancelAnimationFrame(anim);
    const from = vb.slice(), t0 = performance.now(), dur = 300;
    const tick = t => {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      apply(from.map((v, i) => v + (to[i] - v) * e));
      if (k < 1) anim = requestAnimationFrame(tick);
    };
    anim = requestAnimationFrame(tick);
  }
  function scalebar() {
    const px = svg.getBoundingClientRect().width;
    if (!px) return;
    const target = [2000, 1000, 500, 200, 100, 50].find(v => v <= vb[2] * 0.3) || 50;
    $("#sbar").style.width = (target / vb[2] * px).toFixed(1) + "px";
    $("#slab").textContent = target + " m";
  }
  on(window, "resize", scalebar);

  /* ---------- draw one cable ---------- */
  function draw(l, tween) {
    const AR = svg.clientWidth / svg.clientHeight || 4 / 3.3;
    const xs = l.order.map(i => sx(N[i][0])), ys = l.order.map(i => sy(N[i][1]));
    const m = Math.max(step * 1.15, 130);
    let x0 = Math.min(...xs) - m, y0 = Math.min(...ys) - m;
    let w = Math.max(...xs) + m - x0, h = Math.max(...ys) + m - y0;
    if (w / h < AR) { const nw = h * AR; x0 -= (nw - w) / 2; w = nw; }
    else { const nh = w / AR; y0 -= (nh - h) / 2; h = nh; }
    setVB([x0, y0, w, h], tween);

    // markers scale with the run's own spacing, so a tight sequence does not
    // collide and a sparse one does not turn into confetti
    const hops = l.order.slice(1).map((n, k) => Math.hypot(
      sx(N[n][0]) - sx(N[l.order[k]][0]), sy(N[n][1]) - sy(N[l.order[k]][1]))).sort((a, b) => a - b);
    const medHop = hops.length ? hops[hops.length >> 1] : w * 0.05;
    const R = Math.max(w * 0.008, Math.min(w * 0.019, medHop * 0.3));
    const FS = R * 1.2;
    const bad = new Set();
    for (const f of l.findings) if (f.sev === "high") for (const p of f.at) bad.add(p);

    gOther.replaceChildren();
    const near = new Set(l.order);
    for (const o of L) {
      if (o.id === l.id || o.order.length < 2) continue;
      if (o.order.some(i => near.has(i) ||
          (sx(N[i][0]) > x0 && sx(N[i][0]) < x0 + w && sy(N[i][1]) > y0 && sy(N[i][1]) < y0 + h))) {
        gOther.appendChild(el("path", { d: d(o.order), class: "other" }));
      }
    }

    gRun.replaceChildren();
    gRun.appendChild(el("path", { d: d(l.order), class: "run" }));
    l.order.forEach((n, i) => {
      const cx = sx(N[n][0]), cy = sy(N[n][1]);
      const hit = bad.has(i);
      const r = hit ? R * 1.3 : R;
      const g = el("g", {});
      // a halo in the surface colour so a marker never sits on top of a street line
      g.appendChild(el("circle", { cx, cy, r: r * 1.3, class: "mk-halo" }));
      g.appendChild(el("circle", { cx, cy, r, class: "mk" + (hit ? " bad" : "") }));
      g.appendChild(el("text", { x: cx, y: cy, class: "mk-txt" + (hit ? " bad" : ""),
        "font-size": FS * (hit ? 1.15 : 1) }, String(i + 1)));
      const end = i === 0 ? "A end" : i === l.order.length - 1 ? "Z end" : "";
      if (end) {
        g.appendChild(el("text", { x: cx, y: cy - R * 1.6, class: "end-txt",
          "font-size": FS * 1.05 }, end));
      }
      g.appendChild(el("title", {}, `${i + 1} · ${N[n][2]} · ${N[n][3]}`));
      gRun.appendChild(g);
    });
  }

  /* ---------- panel ---------- */
  const M = v => v >= 1000 ? (v / 1000).toFixed(1) + " km" : Math.round(v) + " m";
  const P = i => i + 1;

  // What to do, where, and the one number behind it. The verb is the point: two
  // findings that both read "re-check" tell a reviewer nothing about which to open.
  const FIX = {
    TOPOLOGY: () => "Fix the segment ends first (they don't chain into a single run, so there is no order to check yet)",
    SELF_CROSSING: f => `Swap the order around positions <b>${P(f.at[0])} to ${P(f.at[1])}</b> (the run crosses itself there)`,
    ORDER_REVERSAL: f => `Check position <b>${P(f.at[0])}</b> (${f.nodes[0]}) against the splice record [${M(f.m)} back toward the A end]`,
    DUPLICATE_NODE: f => `Repoint one of the two ends at <b>${f.nodes[0]}</b> [recorded at positions ${P(f.at[0])} and ${P(f.at[1])}]`,
    BACKTRACK: f => `Check whether position <b>${P(f.at[0])}</b> (${f.nodes[0]}) belongs on this cable [${M(f.m)} of detour]`,
    ENDPOINT_SUSPECT: f => `Confirm which structures are the A and Z ends (<b>${f.nodes[0]}</b> and <b>${f.nodes[1]}</b> sit further apart than the recorded pair)`,
    MISSING_GEOMETRY: f => `Place <b>${f.nodes.join(", ")}</b> on the map (no coordinates, so ${f.nodes.length > 1 ? "their" : "its"} place in the order can't be checked)`,
  };

  function panel(l) {
    const bad = new Set();
    for (const f of l.findings) if (f.sev === "high") for (const p of f.at) bad.add(p);
    const fixes = l.findings.filter(f => FIX[f.check]);

    const list = items => `<ol class="fixes">${
      items.map(f => `<li><span>${FIX[f.check](f)}</span></li>`).join("")}</ol>`;

    $("#panel").innerHTML = `
      <div class="verdict">
        <div class="top">
          <span class="cid">${l.label}</span>
          <span class="pill v-${l.verdict}">${l.verdict.replace("_", " ")}</span>
        </div>
        <div class="ends">
          <span>A end <b>${N[l.order[0]][2]}</b></span>
          <span>Z end <b>${N[l.order[l.order.length - 1]][2]}</b></span>
          <span>positions <b>${l.n}</b></span>
        </div>
      </div>
      <div class="seqhead"><span>Recorded sequence</span><span>A \u2192 Z</span></div>
      <div class="strip">${
        l.order.map((n, i) => `<span class="pos${bad.has(i) ? " bad" : ""}"
          title="${N[n][3]}"><b>${i + 1}</b>${N[n][2]}</span>`).join("") +
        l.unplaced.map(() => `<span class="pos ghost">not placed</span>`).join("")}</div>
      <div class="panelbody">
        <div class="seqhead"><span>${fixes.length ? "Suggested fixes" : "Result"}</span></div>
        ${fixes.length ? list(fixes) : `<ol class="fixes"><li class="none"><span>Nothing to flag (the recorded order matches where the structures sit)</span></li></ol>`}
      </div>`;
  }

  /* ---------- selection ---------- */
  let cur = null;
  const wide = { get matches() { return root.host.clientWidth >= 881; } };
  function fitPanel() {
    // side by side, the findings scroll inside the map's height rather than
    // stretching the row and leaving the map column half empty
    // measure the map column's own content, not the grid row it was stretched to
    const natural = $(".mapwrap").offsetHeight + $(".legend").offsetHeight;
    $("#panel").style.maxHeight = wide.matches && natural > 200 ? natural + "px" : "";
    const f = $(".panelbody");
    if (f) f.classList.toggle("more", f.scrollHeight > f.clientHeight + 2);
  }
  on(window, "resize", fitPanel);


  function show(l, tween = true) {
    if (!l) return;
    cur = l;
    $("#cable").value = l.label;
    $("#miss").hidden = true;
    draw(l, tween);
    panel(l);
    fitPanel();
  }
  const pick = want => {
    const pool = ranked.filter(l => FLAGGED.has(l.verdict) === want);
    return pool[Math.floor(Math.random() * pool.length)];
  };

  $("#ids").innerHTML = ranked.map(l => `<option value="${l.label}">`).join("");
  $("#cable").addEventListener("change", e => {
    const l = byLabel[e.target.value.trim().toUpperCase()];
    if (l) show(l); else $("#miss").hidden = false;
  });
  $("#prev").addEventListener("click", () => {
    const i = ranked.indexOf(cur); show(ranked[(i - 1 + ranked.length) % ranked.length]);
  });
  $("#next").addEventListener("click", () => {
    const i = ranked.indexOf(cur); show(ranked[(i + 1) % ranked.length]);
  });
  $("#rndBad").addEventListener("click", () => show(pick(true)));
  $("#rndOk").addEventListener("click", () => show(pick(false)));


  /* open on a cable whose fault is legible at a glance, not the busiest one */
  const opener = ranked.find(l => FLAGGED.has(l.verdict) && l.n >= 6 && l.n <= 11 &&
    ["swap_pair", "reverse_run", "foreign_insert", "teleport"].includes(l.planted)) || ranked[0];
  show(opener, false);
  requestAnimationFrame(() => { scalebar(); fitPanel(); });

  return () => _off.forEach(f => f());
}

class AzOrderCheck extends HTMLElement {
  async connectedCallback() {
    if (this._root) return;
    this._root = this.attachShadow({ mode: "open" });
    this._root.innerHTML = `<style>${CSS}</style>${MARKUP}`;

    const panel = this._root.querySelector("#panel");
    panel.innerHTML = '<div class="loading">Loading the cable set…</div>';

    const src = this.getAttribute("src") || "/az-order-check-data.json";
    let data;
    try {
      const res = await fetch(src);
      if (!res.ok) throw new Error(res.status + " " + res.statusText);
      data = await res.json();
    } catch (err) {
      panel.innerHTML = '<div class="loading">Could not load the cable set from ' +
        '<code>' + src + '</code>.<br>' + String(err) + '</div>';
      return;
    }
    this._off = mount(this._root, data);
  }

  disconnectedCallback() {
    this._off?.();
    this._off = this._root = null;
  }
}

if (!customElements.get("az-order-check")) {
  customElements.define("az-order-check", AzOrderCheck);
}

export default AzOrderCheck;
