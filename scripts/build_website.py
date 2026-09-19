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
    ("WE_PM","woensdag","middag","di-middag.html".replace("di-","wo-")),
    ("TH_AM","donderdag","ochtend","do-ochtend.html"),
    ("TH_PM","donderdag","middag","do-middag.html"),
]
NAV = [
    ("Home","index.html"),("MHV","mhv.html"),("VMBO","vmbo.html"),("PrO","pro.html"),
    *[(f"{d[:2].upper()} {p.upper()}",fn) for _,d,p,fn in SLOTS],
    ("Vrijdag","vrijdag.html"),("Mijn Pantarijnweek","mijn-pantarijnweek.html"),
    ("Impressie","impressie.html"),("Informatie & contact","informatie.html")
]

def esc(v): return html.escape(str(v or ""), quote=True)

def demo_payload():
    data = json.loads((ROOT/"site/demo_2025.json").read_text(encoding="utf-8"))
    return data, data["offerings"]

def canonical_payload():
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
                "short": (act.get("description") or "")[:180],
                "description": act.get("description",""),
                "audience": row.get("audience") or act.get("default_audience") or "",
                "category": cats[0].lower() if cats else "overig",
                "tags": [row.get("choice_mode") or "keuze"],
                "icon": "✦",
                "location": row.get("location_id") or row.get("room_id") or "Nog te bepalen",
            })
    payload = {
        "edition":"Pantarijnweek 2026",
        "date_line":"Week voor de kerstvakantie",
        "notice":"Controleer vóór inschrijving altijd of het aanbod nog is gewijzigd.",
        "news":"Actuele mededelingen worden vanuit de centrale hub gepubliceerd.",
    }
    return payload, offerings

def nav():
    return '<div class="menu-wrap"><nav class="menu wrap">' + ''.join(
        f'<a href="{href}">{esc(label)}</a>' for label,href in NAV
    ) + '</nav></div>'

def offerings_json(offerings):
    return json.dumps(offerings, ensure_ascii=False).replace("</","<\\/")

def dialog():
    return """<dialog class="dialog" id="detail-dialog">
<div class="dialog-inner">
<div class="dialog-head"><div><div class="kicker">Workshop</div><h2 data-dialog-title></h2></div>
<button class="dialog-close" data-close-dialog aria-label="Sluiten">×</button></div>
<p class="lead" data-dialog-description></p>
<div class="detail-meta">
<div><b>Doelgroep</b><span data-dialog-audience></span></div>
<div><b>Locatie</b><span data-dialog-location></span></div>
<div><b>Categorie</b><span data-dialog-category></span></div>
<div><b>Bijzonderheden</b><span data-dialog-tags></span></div>
</div>
<div style="margin-top:18px"><button class="button secondary" data-dialog-save data-save="">♡ Bewaar</button></div>
</div></dialog>"""

def shell(title, body, edition, offerings):
    return f"""<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#161a2a">
<title>{esc(title)} | Pantarijnweek</title>
<link rel="stylesheet" href="assets/styles.css"></head>
<body>
<header class="topbar"><div class="wrap"><a class="brand" href="index.html">Pantarijnweek</a><span class="edition">{esc(edition)}</span></div></header>
{nav()}
<main>{body}</main>
<footer class="footer"><div class="wrap">Pantarijnweek · gegenereerd vanuit de centrale planning · publieke pagina bevat geen persoonlijke leerlinggegevens.</div></footer>
{dialog()}
<script type="application/json" id="offerings-data">{offerings_json(offerings)}</script>
<script src="assets/app.js"></script>
</body></html>"""

def chip(t, cls=""):
    if not t: return ""
    return f'<span class="chip {cls}">{esc(t)}</span>'

def card(o):
    tags = list(o.get("tags") or [])
    warn = {"verplicht","voorinschrijving","buiten school","hele dag","betaald"}
    chips = chip(o.get("audience",""),"audience") + "".join(
        chip(t,"warn" if str(t).lower() in warn else "") for t in tags
    )
    return f"""<article class="card" data-card data-audience="{esc(o.get('audience',''))}" data-category="{esc(o.get('category','overig'))}" data-tags="{esc(' '.join(tags))}">
<div class="card-visual"><span class="card-icon">{esc(o.get('icon','✦'))}</span><span class="category">{esc(o.get('category','overig'))}</span></div>
<div class="card-body">
<div class="chips">{chips}</div>
<h3>{esc(o.get('title',''))}</h3>
<p>{esc(o.get('short') or o.get('description',''))}</p>
<div class="meta">⌖ {esc(o.get('location','Nog te bepalen'))}</div>
<div class="card-actions">
<button class="button primary" data-detail="{esc(o.get('offering_id',''))}">Meer info</button>
<button class="button secondary" data-save="{esc(o.get('offering_id',''))}">♡ Bewaar</button>
</div></div></article>"""

def write(out, name, content):
    (out/name).write_text(content, encoding="utf-8")

def filters():
    return """<div class="toolbar">
<input class="search" data-search placeholder="Zoek op workshop, onderwerp of locatie…">
<div class="filters">
<button class="filter-btn active" data-filter="all">Alles</button>
<button class="filter-btn" data-filter="OB">OB</button>
<button class="filter-btn" data-filter="BB">BB</button>
<button class="filter-btn" data-filter="sport">Sport</button>
<button class="filter-btn" data-filter="creatief">Creatief</button>
<button class="filter-btn" data-filter="techniek">Techniek</button>
</div></div>"""

def build(out, payload, offerings):
    out.mkdir(parents=True, exist_ok=True)
    (out/"assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT/"site/assets/styles.css", out/"assets/styles.css")
    shutil.copyfile(ROOT/"site/assets/app.js", out/"assets/app.js")
    edition = payload.get("edition","Pantarijnweek")

    slot_links = ''.join(
        f'<a href="{fn}"><span class="day-dot"></span>{d.title()}<small>{p.title()}</small></a>'
        for _,d,p,fn in SLOTS
    )
    home = f"""<section class="hero"><div class="wrap hero-grid"><div>
<div class="kicker">Kies · ontdek · doe mee</div>
<h1>Ontdek jouw Pantarijnweek</h1>
<p>Bekijk workshops, activiteiten en excursies, maak je eigen voorlopige lijst en controleer vlak voor inschrijving of er iets is veranderd.</p>
<div class="notice">{esc(payload.get('notice',''))}</div>
</div><div class="hero-art"><div class="orb one">🎨</div><div class="orb two">🔬</div><div class="orb three">🏃</div><div class="hero-ribbon">{esc(payload.get('date_line',''))}</div></div></div></section>
<section class="section"><div class="wrap">
<div class="news"><span class="news-badge">NIEUWS</span><p>{esc(payload.get('news',''))}</p></div>
<div class="section-head"><div><div class="kicker">Programma</div><h2>Kies een dagdeel</h2></div><p>Acht dagdelen, van maandag tot en met donderdag.</p></div>
<div class="slot-links">{slot_links}</div>
</div></section>
<section class="section"><div class="wrap"><div class="callout"><div><div class="kicker" style="color:#bdb0ff">Voorbereiden</div><h2 style="margin:0">Maak jouw voorlopige topkeuzes</h2><p>Bewaar interessante workshops tijdens het rondkijken. Dit is alleen een persoonlijke shortlist in jouw browser, geen inschrijving.</p></div><a class="button" href="mijn-pantarijnweek.html">Mijn Pantarijnweek (<span data-saved-count>0</span>)</a></div></div></section>"""
    write(out,"index.html",shell("Home",home,edition,offerings))

    for slot_id, day, part, filename in SLOTS:
        subset=[o for o in offerings if o.get("slot_id")==slot_id]
        cards=''.join(card(o) for o in subset) if subset else '<div class="empty">Nog geen gepubliceerde activiteiten voor dit dagdeel.</div>'
        body=f"""<section class="section"><div class="wrap" data-filter-root data-active-filter="all">
<div class="kicker">{esc(day)}</div>
<div class="section-head"><div><h2>{esc(day.title())} {esc(part)}</h2></div><p>Let op doelgroep en informatieblokken. Open een kaart voor meer details.</p></div>
{filters()}<div class="grid">{cards}</div></div></section>"""
        write(out,filename,shell(f"{day.title()} {part}",body,edition,offerings))

    audience_pages = {
      "mhv.html":("MHV","Bekijk het reguliere workshopaanbod en gebruik de dagdeelpagina's om je voorlopige keuzes te bewaren."),
      "vmbo.html":("VMBO","De donderdag kan een aparte deelname- en inschrijfroute hebben. Alleen workshops die voor VMBO zijn opengesteld horen in de definitieve versie zichtbaar te zijn."),
      "pro.html":("PrO","Voor PrO kan deelname via mentor of handmatige plaatsing verlopen. De definitieve werkwijze voor 2026 wordt pas gepubliceerd nadat deze is bevestigd.")
    }
    for filename,(label,text) in audience_pages.items():
        body=f"""<section class="section"><div class="wrap"><div class="kicker">Doelgroep</div><h2>{esc(label)}</h2>
<p style="max-width:760px;line-height:1.7;color:var(--muted)">{esc(text)}</p>
<div class="notice">Prototype: definitieve deelname, begeleiding en inschrijfregels voor 2026 zijn nog niet gepubliceerd.</div>
<div class="callout"><div><h3 style="margin:0">Bekijk het programma</h3><p>Ga naar een dagdeel, filter op doelgroep en bewaar je favorieten.</p></div><a class="button" href="do-ochtend.html">Naar donderdag</a></div>
</div></section>"""
        write(out,filename,shell(label,body,edition,offerings))

    friday = """<section class="section"><div class="wrap"><div class="kicker">Vrijdag</div><h2>Afsluitdag</h2>
<p style="max-width:760px;line-height:1.7;color:var(--muted)">Vrijdag valt buiten de gewone vrije workshopinschrijving. De definitieve invulling van de afsluitdag voor 2026 wordt later vanuit de centrale planning gepubliceerd.</p>
<div class="notice">Er verschijnen hier pas onderdelen zodra ze door de organisatie als publiceerbaar zijn gemarkeerd.</div></div></section>"""
    write(out,"vrijdag.html",shell("Vrijdag",friday,edition,offerings))

    myweek = """<section class="section"><div class="wrap"><div class="kicker">Voorbereiden</div><div class="section-head"><div><h2>Mijn Pantarijnweek</h2><p>Jouw persoonlijke shortlist op dit apparaat.</p></div></div>
<div class="notice">Dit is géén inschrijving. Je keuzes worden alleen lokaal in deze browser bewaard en niet naar school verzonden.</div>
<div class="saved-list" data-saved-list></div></div></section>"""
    write(out,"mijn-pantarijnweek.html",shell("Mijn Pantarijnweek",myweek,edition,offerings))

    impressie = """<section class="section"><div class="wrap"><div class="kicker">Impressie</div><div class="section-head"><div><h2>Zo kan de week eruitzien</h2></div><p>Voorlopige grafische placeholders. Eigen Pantarijnfoto's kunnen later automatisch worden gekoppeld.</p></div>
<div class="gallery"><div>🎭</div><div>🏐</div><div>🎨</div><div>🔬</div><div>🍳</div></div></div></section>"""
    write(out,"impressie.html",shell("Impressie",impressie,edition,offerings))

    info = """<section class="section"><div class="wrap"><div class="kicker">Informatie & contact</div><h2>Zo werkt deze nieuwe site</h2>
<div class="info-grid">
<div class="info-card"><b>1 bron</b><p>Workshopinformatie wordt centraal beheerd en niet opnieuw in een losse webeditor getypt.</p></div>
<div class="info-card"><b>Automatisch</b><p>Na een goedgekeurde wijziging kan de publieke site opnieuw worden opgebouwd.</p></div>
<div class="info-card"><b>Veilig</b><p>Interne planningsgegevens en leerlinginformatie horen niet op de publieke website.</p></div>
</div>
<div class="notice">Contactgegevens en definitieve instructies voor 2026 worden pas gepubliceerd wanneer de organisatie ze heeft bevestigd.</div></div></section>"""
    write(out,"informatie.html",shell("Informatie & contact",info,edition,offerings))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--demo",action="store_true")
    p.add_argument("--output",default="site/public")
    args=p.parse_args()
    payload, offerings = demo_payload() if args.demo else canonical_payload()
    build(ROOT/args.output, payload, offerings)
    print(f"Built {len(offerings)} offerings into {args.output}")

if __name__=="__main__":
    main()
