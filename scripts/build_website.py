#!/usr/bin/env python3
import argparse, csv, html, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLOTS = [
    ("MO_AM","maandag","ochtend","ma-ochtend.html"),
    ("MO_PM","maandag","middag","ma-middag.html"),
    ("TU_AM","dinsdag","ochtend","di-ochtend.html"),
    ("TU_PM","dinsdag","middag","di-middag.html"),
    ("WE_AM","woensdag","ochtend","wo-ochtend.html"),
    ("WE_PM","woensdag","middag","wo-middag.html"),
    ("TH_AM","donderdag","ochtend","do-ochtend.html"),
    ("TH_PM","donderdag","middag","do-middag.html"),
]
NAV = [
    ("Home","index.html"),("MHV","mhv.html"),("VMBO","vmbo.html"),("PrO","pro.html"),
    *[(f"{d[:2].upper()} {p.upper()}",fn) for _,d,p,fn in SLOTS],
    ("Informatie","informatie.html")
]

def esc(v): return html.escape(str(v or ""), quote=True)

def load_demo():
    data = json.loads((ROOT/"site/demo_2025.json").read_text(encoding="utf-8"))
    return data["offerings"], data.get("notice","Prototype")

def load_canonical():
    activities = {}
    with (ROOT/"data/2026/activities.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            activities[row["activity_id"]] = row
    out = []
    with (ROOT/"data/2026/offerings.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            act = activities.get(row["activity_id"], {})
            if not act: continue
            status = (row.get("status") or "").lower()
            if status not in {"website_ready","published","approved","active"}: continue
            audience = row.get("audience") or act.get("default_audience") or ""
            out.append({
                "offering_id":row["offering_id"],"slot_id":row["slot_id"],
                "title":act.get("title",""),"description":act.get("description",""),
                "audience":audience,"tags":[row.get("choice_mode","choice")],
                "icon":"✦"
            })
    return out, "Actuele website uit de centrale Pantarijnweek-hub."

def nav():
    return '<nav class="menu wrap">' + ''.join(f'<a href="{href}">{esc(label)}</a>' for label,href in NAV) + '</nav>'

def shell(title, body, edition="Pantarijnweek"):
    return f"""<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Pantarijnweek</title>
<link rel="stylesheet" href="assets/styles.css"></head>
<body><header class="topbar"><div class="wrap"><a class="brand" href="index.html">Pantarijnweek</a><span class="edition">{esc(edition)}</span></div></header>
{nav()}
<main>{body}</main>
<footer class="footer"><div class="wrap">Datagedreven prototype. De centrale hub is de bron; deze pagina is afgeleide uitvoer.</div></footer>
<script src="assets/app.js"></script></body></html>"""

def card(o):
    tags = [o.get("audience","")] + list(o.get("tags") or [])
    chips = ''.join(f'<span class="chip {"audience" if i==0 else "warn" if str(t).lower() in {"verplicht","voorinschrijving","buiten school","hele dag"} else ""}">{esc(t)}</span>' for i,t in enumerate(tags) if t)
    return f"""<article class="card" data-card>
<div class="icon">{esc(o.get("icon","✦"))}</div>
<div class="chips">{chips}</div>
<h3>{esc(o["title"])}</h3>
<p>{esc(o.get("description",""))}</p>
</article>"""

def write(out, name, content):
    (out/name).write_text(content, encoding="utf-8")

def build(out, offerings, notice, edition):
    out.mkdir(parents=True, exist_ok=True)
    (out/"assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT/"site/assets/styles.css", out/"assets/styles.css")
    shutil.copyfile(ROOT/"site/assets/app.js", out/"assets/app.js")

    slot_links = ''.join(f'<a href="{fn}">{d.title()}<small>{p.title()}</small></a>' for _,d,p,fn in SLOTS)
    home = f"""<section class="hero"><div class="wrap hero-grid"><div>
<div class="kicker">Eén bron, acht dagdelen</div><h1>Ontdek jouw Pantarijnweek</h1>
<p>Workshops, activiteiten en excursies vanuit één centrale planning. Wijzigingen in de hub kunnen deze website opnieuw genereren zonder handmatig kopiëren.</p>
<div class="facts"><div class="fact"><b>8</b>dagdelen</div><div class="fact"><b>1×</b>centrale bron</div><div class="fact"><b>0×</b>dubbel websitebeheer</div></div>
</div><div class="hero-art"><div class="orb one">🎨</div><div class="orb two">🔬</div><div class="orb three">🏃</div></div></div></section>
<section class="section"><div class="wrap"><div class="notice">{esc(notice)}</div><div class="section-head"><div><div class="kicker">Programma</div><h2>Kies een dagdeel</h2></div></div><div class="slot-links">{slot_links}</div></div></section>"""
    write(out,"index.html",shell("Home",home,edition))

    for slot_id, day, part, filename in SLOTS:
        subset=[o for o in offerings if o.get("slot_id")==slot_id]
        cards=''.join(card(o) for o in subset) if subset else '<div class="empty">Nog geen gepubliceerde activiteiten voor dit dagdeel.</div>'
        body=f"""<section class="section"><div class="wrap"><div class="kicker">{esc(day)}</div><div class="section-head"><div><h2>{esc(day.title())} {esc(part)}</h2><p>De kaarten hieronder komen uit de centrale hub.</p></div></div>
<input class="search" data-search placeholder="Zoek op workshop, doelgroep of kenmerk…">
<div class="grid">{cards}</div></div></section>"""
        write(out,filename,shell(f"{day.title()} {part}",body,edition))

    audience_pages = {
      "mhv.html":("MHV","MHV gebruikt het reguliere workshopaanbod. In de definitieve versie kan de site alleen activiteiten tonen waarvoor deze doelgroep is toegelaten."),
      "vmbo.html":("VMBO","Voor donderdag kan de hub een apart inschrijfvenster en gereserveerde capaciteit beheren. De website kan automatisch alleen geschikte workshops tonen."),
      "pro.html":("PrO","Voor PrO kan de hub handmatige plaatsing en specifieke doelgroepgeschiktheid ondersteunen zonder capaciteit in de bron te overschrijven.")
    }
    for filename,(label,text) in audience_pages.items():
        body=f'<section class="section"><div class="wrap"><div class="kicker">Doelgroep</div><h2>{esc(label)}</h2><p style="max-width:760px;line-height:1.7;color:var(--muted)">{esc(text)}</p><div class="notice">Dit is een prototype. Definitieve deelname en inschrijfregels voor 2026 worden pas gepubliceerd nadat de organisatie ze heeft bevestigd.</div></div></section>'
        write(out,filename,shell(label,body,edition))

    info = """<section class="section"><div class="wrap"><div class="kicker">Informatie</div><h2>Hoe deze site werkt</h2>
<div class="grid"><article class="card"><div class="icon">🗂️</div><h3>Hub is leidend</h3><p>Activiteiten, doelgroepen, dagdelen en statussen worden centraal beheerd.</p></article>
<article class="card"><div class="icon">🔄</div><h3>Opnieuw genereren</h3><p>Na een goedgekeurde wijziging kan de website opnieuw worden gebouwd.</p></article>
<article class="card"><div class="icon">✅</div><h3>Alleen publiceerbaar</h3><p>Concepten blijven intern. Alleen records met een website-publicatiestatus komen online.</p></article></div></div></section>"""
    write(out,"informatie.html",shell("Informatie",info,edition))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--demo",action="store_true")
    p.add_argument("--output",default="site/public")
    args=p.parse_args()
    offerings,notice = load_demo() if args.demo else load_canonical()
    build(ROOT/args.output, offerings, notice, "Prototype 2025→2026" if args.demo else "Pantarijnweek 2026")
    print(f"Built {len(offerings)} offerings into {args.output}")

if __name__=="__main__": main()
