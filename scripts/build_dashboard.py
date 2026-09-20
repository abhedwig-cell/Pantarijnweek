#!/usr/bin/env python3
"""Render a static no-JavaScript regie dashboard from derived HealthSignals."""

from __future__ import annotations

import argparse
import html
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def severity_label(value):
    return {
        "ok": "OK",
        "warning": "Let op",
        "critical": "Kritiek",
        "unknown": "Onbekend",
        "info": "Info",
    }.get(value, value)


def signal_card(s):
    sev = s["severity"]
    value = s.get("observed_value")
    metric = "" if value is None else f'<div class="metric">{esc(value)}</div>'
    refs = " · ".join(s.get("source_refs") or [])
    return f"""<article class="signal {esc(sev)}">
<div class="signal-head"><h3>{esc(s["title"])}</h3><span class="pill {esc(sev)}">{esc(severity_label(sev))}</span></div>
<p>{esc(s.get("explanation",""))}</p>
{metric}
<div class="source">{esc(refs)}</div>
</article>"""


def capacity_rows(signals):
    caps = [s for s in signals if s.get("scope_type") == "slot" and "metrics" in s]
    rows = ['<div class="cap-row header"><div>Dagdeel / groep</div><div>Vraag</div><div>Aanbod</div><div>Voor wijziging</div><div>Marge</div></div>']
    for s in caps:
        m = s["metrics"]
        rows.append(
            f'<div class="cap-row">'
            f'<div><b>{esc(s["title"])}</b><div class="small">doel: +{esc(s["threshold_or_expectation"])} plaatsen</div></div>'
            f'<div>{esc(m["demand"])}</div>'
            f'<div>{esc(m["supply_after"])}</div>'
            f'<div>{esc(m["supply_before"])}</div>'
            f'<div class="cap-status {esc(s["severity"])}">{m["margin_after"]:+d}</div>'
            f'</div>'
        )
    return "".join(rows)


def render(payload):
    signals = payload["signals"]
    counts = Counter(s["severity"] for s in signals)
    progress = payload.get("progress") or {}
    total = int(progress.get("activities_total") or 0)
    complete = int(progress.get("activities_complete") or 0)
    fraction = float(progress.get("activities_fraction") or 0)
    pct = round(100 * fraction)

    change = payload.get("change_event") or {}
    change_html = ""
    if change:
        change_html = f"""<div class="change">
<b>Laatste wijziging in deze demo</b>
{esc(change.get("detail",""))}<br><span class="small">{esc(change.get("source",""))}</span>
</div>"""

    capacity = [s for s in signals if s.get("scope_type") == "slot"]
    workflow = [s for s in signals if s.get("scope_type") != "slot"]
    critical = [s for s in signals if s["severity"] == "critical"]
    warnings = [s for s in signals if s["severity"] == "warning"]

    top_priority = critical + warnings
    priority_html = "".join(signal_card(s) for s in top_priority[:6])
    if not priority_html:
        priority_html = '<article class="signal ok"><div class="signal-head"><h3>Geen open waarschuwingen</h3><span class="pill ok">OK</span></div><p>Alle berekende signalen zijn groen.</p></article>'

    workflow_html = "".join(signal_card(s) for s in workflow)

    details = "".join(
        f"""<details>
<summary>{esc(s["title"])} — {esc(severity_label(s["severity"]))}</summary>
<div class="details-body">
<p>{esc(s.get("explanation",""))}</p>
<p><b>Regel:</b> {esc(s.get("rule_id",""))}<br>
<b>Scope:</b> {esc(s.get("scope_type",""))} / {esc(s.get("scope_id",""))}<br>
<b>Bron:</b> {esc(" · ".join(s.get("source_refs") or []))}</p>
</div></details>"""
        for s in signals
    )

    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pantarijnweek regiedashboard</title>
<link rel="stylesheet" href="assets/dashboard.css">
</head>
<body>
<header class="top"><div class="wrap top-row">
<div class="brand">Pantarijnweek · regiedashboard</div>
<span class="badge-demo">{esc(payload.get("edition",""))}</span>
</div></header>
<nav><div class="wrap nav">
<a href="#overzicht">Overzicht</a><a href="#capaciteit">Capaciteit</a><a href="#workflow">Workflow</a><a href="#controle">Controleerbaarheid</a>
</div></nav>
<main class="wrap">
<section id="overzicht" class="hero">
<div class="hero-panel">
<div class="eyebrow">Centrale regie</div>
<h1>{esc(payload.get("scenario_title","Regiedashboard"))}</h1>
<p>Dit scherm bevat geen handmatig gekozen kleuren. De statussen hieronder zijn berekend uit bronwaarden en expliciete regels.</p>
<div class="progress"><span style="width:{pct}%"></span></div>
<div class="small">{complete} van {total} activiteiten compleet · {pct}%</div>
{change_html}
</div>
<div class="summary-panel">
<div class="eyebrow">Signalen</div>
<div class="summary-list">
<div class="summary-row"><span>Kritiek</span><b>{counts.get("critical",0)}</b></div>
<div class="summary-row"><span>Let op</span><b>{counts.get("warning",0)}</b></div>
<div class="summary-row"><span>Onbekend</span><b>{counts.get("unknown",0)}</b></div>
<div class="summary-row"><span>OK</span><b>{counts.get("ok",0)}</b></div>
</div>
</div>
</section>

<section class="section">
<div class="section-head"><div><div class="eyebrow">Eerst oplossen</div><h2>Wat vraagt nu aandacht?</h2></div><p>De grootste afwijkingen worden automatisch bovenaan gezet.</p></div>
<div class="grid">{priority_html}</div>
</section>

<section id="capaciteit" class="section">
<div class="section-head"><div><div class="eyebrow">Capaciteit</div><h2>Vraag en aanbod per dagdeel</h2></div><p>Een negatieve marge is kritiek; een positieve marge onder de veiligheidsgrens geeft een waarschuwing.</p></div>
<div class="capacity-table">{capacity_rows(capacity)}</div>
</section>

<section id="workflow" class="section">
<div class="section-head"><div><div class="eyebrow">Werkstroom</div><h2>Publicatie, Magister en resources</h2></div><p>Alleen uitzonderingen en voortgang; brondata blijft in de centrale hub.</p></div>
<div class="grid">{workflow_html}</div>
</section>

<section id="controle" class="section">
<div class="section-head"><div><div class="eyebrow">Transparantie</div><h2>Waarom staat iets rood?</h2></div><p>Elk signaal toont de regel en bron waarop het is gebaseerd.</p></div>
{details}
</section>
</main>
<footer><div class="wrap">Prototype · signalen zijn afgeleid; het dashboard is geen tweede administratie.</div></footer>
</body>
</html>"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="dashboard/public")
    args = p.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "dashboard/assets/dashboard.css", out / "assets/dashboard.css")
    (out / "index.html").write_text(render(payload), encoding="utf-8")
    print(f"Dashboard built: {out / 'index.html'}")


if __name__ == "__main__":
    main()
