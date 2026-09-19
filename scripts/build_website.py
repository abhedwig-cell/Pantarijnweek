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
    ("Home","index.html"),
    ("Programma","programma.html"),
    ("Doelgroepen","doelgroepen.html"),
    ("Mijn week","mijn-pantarijnweek.html"),
    ("Informatie","informatie.html"),
]

def esc(v):
    return html.escape(str(v or ""), quote=True)

def load_demo():
    data = json.loads((ROOT/"site/demo_2025.json").read_text(encoding="utf-8"))
    return data, data["offerings"]

def load_canonical():
    activities = {}
    with (ROOT/"data/2026/activities.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            activities[row["activity_id"]] = row

    offerings = []
    with (ROOT/"data/2026/offerings.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            act = activities.get(row["activity_id"])
            if not act:
                continue
            status = (row.get("status") or "").strip().lower()
            if status not in {"website_ready","published","approved","active"}:
                continue
            cats = [x.strip() for x in (act.get("categories") or "").replace("|",",").split(",") if x.strip()]
            offerings.append({
                "offering_id": row["offering_id"],
                "slot_id": row["slot_id"],
                "title": act.get("title",""),
                "short": (act.get("description") or "")[:150],
                "description": act.get("description",""),
                "audience": row.get("audience") or act.get("default_audience") or "",
                "category": cats[0].lower() if cats else "overig",
                "tags": [row.get("choice_mode") or "keuze"],
                "icon": "✦",
                "location": row.get("location_id") or row.get("room_id") or "Nog te bepalen",
            })
    return {
        "edition":"Pantarijnweek 2026",
        "date_line":"Week voor de kerstvakantie",
        "notice":"Definitieve informatie verschijnt zodra de organisatie deze heeft vrijgegeven.",
    }, offerings

def offerings_json(offerings):
    return json.dumps(offerings, ensure_ascii=False).replace("</","<\\/")

def nav():
    return '<nav class="nav">' + ''.join(
        f'<a class="{"cta" if label == "Mijn week" else ""}" href="{href}">{esc(label)}</a>'
        for label, href in NAV
    ) + '</nav>'

def dialog():
    return """<dialog class="dialog" id="detail-dialog">
<div class="dialog-inner">
  <div class="dialog-head">
    <h2 data-dialog-title></h2>
    <button class="dialog-close" data-close-dialog aria-label="Sluiten">×</button>
  </div>
  <p class="dialog-lead" data-dialog-description></p>
  <div class="detail-list">
    <div class="detail-row"><b>Doelgroep</b><span data-dialog-audience></span></div>
    <div class="detail-row"><b>Locatie</b><span data-dialog-location></span></div>
    <div class="detail-row"><b>Bijzonder</b><span data-dialog-special></span></div>
  </div>
  <div style="margin-top:20px">
    <button class="button secondary" data-dialog-save data-save="">♡ Bewaar</button>
  </div>
</div>
</dialog>"""

def shell(title, body, edition, offerings):
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff">
<title>{esc(title)} | Pantarijnweek</title>
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="index.html">Pantarijn<span>week</span></a>
    {nav()}
  </div>
</header>
<main>{body}</main>
<footer class="footer"><div class="wrap">Pantarijnweek · automatisch opgebouwd vanuit de centrale planning.</div></footer>
{dialog()}
<script type="application/json" id="offerings-data">{offerings_json(offerings)}</script>
<script src="assets/app.js"></script>
</body>
</html>"""

def day_cards():
    groups = {}
    for slot_id, day, part, filename in SLOTS:
        groups.setdefault(day, []).append((part, filename))
    return ''.join(
        f"""<article class="day-card"><h3>{esc(day.title())}</h3>
<div class="day-links">{''.join(f'<a href="{fn}">{esc(part.title())} →</a>' for part,fn in parts)}</div></article>"""
        for day, parts in groups.items()
    )

def special_label(tags):
    tags = [str(t).lower() for t in tags or []]
    labels = []
    if "verplicht" in tags: labels.append("Verplicht")
    if "voorinschrijving" in tags: labels.append("Voorinschrijving")
    if "buiten school" in tags: labels.append("Buiten school")
    if "hele dag" in tags: labels.append("Hele dag")
    return " · ".join(labels)

def card(o):
    special = special_label(o.get("tags"))
    return f"""<article class="workshop-card" data-card data-detail="{esc(o.get('offering_id'))}"
data-audience="{esc(o.get('audience',''))}" data-category="{esc(o.get('category','overig'))}">
  <div class="visual">{esc(o.get('icon','✦'))}</div>
  <div class="workshop-copy">
    <span class="audience">{esc(o.get('audience',''))}</span>
    <h3>{esc(o.get('title',''))}</h3>
    <p>{esc(o.get('short') or o.get('description',''))}</p>
    {f'<div class="special">{esc(special)}</div>' if special else ''}
  </div>
</article>"""

def write(out, name, content):
    (out/name).write_text(content, encoding="utf-8")

def build(out, payload, offerings):
    out.mkdir(parents=True, exist_ok=True)
    (out/"assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT/"site/assets/styles.css", out/"assets/styles.css")
    shutil.copyfile(ROOT/"site/assets/app.js", out/"assets/app.js")
    edition = payload.get("edition","Pantarijnweek")

    home = f"""<section class="hero"><div class="wrap hero-grid">
<div>
  <div class="eyebrow">Week voor de kerstvakantie</div>
  <h1>Ontdek wat jij wilt doen.</h1>
  <p>Vier dagen vol workshops, activiteiten en excursies. Bekijk rustig het programma en bewaar een paar favorieten voor later.</p>
  <div class="hero-actions">
    <a class="button primary" href="programma.html">Bekijk het programma</a>
    <a class="button secondary" href="doelgroepen.html">Hoe werkt deelname?</a>
  </div>
</div>
<div class="hero-art">
  <div class="shape a">🎨</div><div class="shape b">🏃</div><div class="shape c">🔬</div>
  <div class="hero-label">{esc(payload.get('date_line','Pantarijnweek'))}</div>
</div>
</div></section>
<section class="section alt"><div class="wrap">
  <div class="section-title"><div><div class="eyebrow">Programma</div><h2>Kies je dag</h2></div><p>Maandag tot en met donderdag, steeds een ochtend en een middag.</p></div>
  <div class="day-grid">{day_cards()}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-title"><div><div class="eyebrow">Voorbereiden</div><h2>Mijn week</h2></div><p>Bewaar interessante workshops. Dit is alleen jouw eigen lijst op dit apparaat, geen inschrijving.</p></div>
  <a class="button primary" href="mijn-pantarijnweek.html">Bekijk mijn lijst (<span data-saved-count>0</span>)</a>
</div></section>"""
    write(out,"index.html",shell("Home",home,edition,offerings))

    programma = f"""<section class="section"><div class="wrap">
<div class="section-title"><div><div class="eyebrow">Programma</div><h2>Alle dagdelen</h2></div><p>Kies eerst een dagdeel. Daarna zie je alleen de workshops die daar zijn ingepland.</p></div>
<div class="day-grid">{day_cards()}</div>
<p class="program-note">Vrijdag is een afsluitdag en valt buiten de gewone workshopkeuze.</p>
</div></section>"""
    write(out,"programma.html",shell("Programma",programma,edition,offerings))

    for slot_id, day, part, filename in SLOTS:
        subset = [o for o in offerings if o.get("slot_id") == slot_id]
        cards = ''.join(card(o) for o in subset) if subset else '<div class="empty">Voor dit dagdeel zijn nog geen workshops gepubliceerd.</div>'
        body = f"""<section class="section"><div class="wrap" data-search-root data-audience-filter="all">
<div class="section-title"><div><div class="eyebrow">{esc(day)}</div><h2>{esc(part.title())}</h2></div><p>Tik op een workshop voor alle details.</p></div>
<div class="searchbar">
  <input data-search placeholder="Zoek een workshop…">
  <div class="segmented">
    <button class="active" data-audience-filter="all">Alles</button>
    <button data-audience-filter="OB">OB</button>
    <button data-audience-filter="BB">BB</button>
  </div>
</div>
<div class="workshop-grid">{cards}</div>
</div></section>"""
        write(out,filename,shell(f"{day.title()} {part}",body,edition,offerings))

    doelgroep = """<section class="section"><div class="wrap">
<div class="section-title"><div><div class="eyebrow">Deelname</div><h2>Voor wie is wat bedoeld?</h2></div><p>De definitieve regels voor 2026 worden hier pas gepubliceerd zodra de organisatie ze heeft bevestigd.</p></div>
<div class="audience-grid">
<article class="audience-card"><h3>MHV</h3><p>Het reguliere workshopprogramma voor onderbouw en bovenbouw.</p><a href="mhv.html">Meer uitleg →</a></article>
<article class="audience-card"><h3>VMBO</h3><p>Op donderdag kan een apart inschrijfvenster en een geselecteerd aanbod gelden.</p><a href="vmbo.html">Meer uitleg →</a></article>
<article class="audience-card"><h3>PrO</h3><p>Deelname kan via een andere route verlopen dan gewone vrije inschrijving.</p><a href="pro.html">Meer uitleg →</a></article>
</div></div></section>"""
    write(out,"doelgroepen.html",shell("Doelgroepen",doelgroep,edition,offerings))

    pages = {
        "mhv.html":("MHV","Voor MHV-leerlingen bestaat het programma uit vrije workshops plus eventuele verplichte of vooraf vastgelegde activiteiten."),
        "vmbo.html":("VMBO","Voor donderdag kan een geselecteerd deel van het aanbod voor VMBO worden opengesteld. De precieze inschrijfroute voor 2026 moet nog worden bevestigd."),
        "pro.html":("PrO","Voor PrO kan deelname via lijsten of handmatige plaatsing verlopen. De precieze route voor 2026 moet nog worden bevestigd."),
    }
    for filename,(title,text) in pages.items():
        body=f"""<section class="section"><div class="wrap"><div class="eyebrow">Doelgroep</div><h2 style="font-size:3rem;margin:0 0 18px">{esc(title)}</h2>
<p style="max-width:720px;color:var(--muted);line-height:1.7">{esc(text)}</p>
<div class="notice">Prototype: nog geen definitieve inschrijfinstructie voor 2026.</div>
<a class="button primary" href="programma.html">Naar het programma</a></div></section>"""
        write(out,filename,shell(title,body,edition,offerings))

    myweek = """<section class="section"><div class="wrap">
<div class="section-title"><div><div class="eyebrow">Persoonlijk</div><h2>Mijn week</h2></div><p>Een tijdelijke lijst met workshops die jij interessant vindt.</p></div>
<div class="notice">Dit is geen inschrijving. De lijst blijft alleen in deze browser staan.</div>
<div class="saved-list" data-saved-list></div>
</div></section>"""
    write(out,"mijn-pantarijnweek.html",shell("Mijn week",myweek,edition,offerings))

    info = """<section class="section"><div class="wrap">
<div class="section-title"><div><div class="eyebrow">Informatie</div><h2>Over de Pantarijnweek</h2></div></div>
<p style="max-width:760px;color:var(--muted);line-height:1.75">Deze nieuwe website wordt automatisch opgebouwd uit de centrale Pantarijnweekplanning. Daardoor hoeft workshopinformatie niet meer op meerdere plekken handmatig te worden bijgehouden.</p>
<div class="notice">Definitieve contactgegevens, inschrijfdata en instructies voor 2026 worden later gepubliceerd.</div>
</div></section>"""
    write(out,"informatie.html",shell("Informatie",info,edition,offerings))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--demo",action="store_true")
    p.add_argument("--output",default="site/public")
    args=p.parse_args()
    payload, offerings = load_demo() if args.demo else load_canonical()
    build(ROOT/args.output, payload, offerings)
    print(f"Built {len(offerings)} offerings into {args.output}")

if __name__=="__main__":
    main()
