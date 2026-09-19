# Gegenereerde Pantarijnweek-website

Deze map bevat de eerste datagedreven websiteprototype.

## Principe

```
data/2026/*.csv
      |
      v
scripts/build_website.py
      |
      v
site/public/*.html
```

De website is dus afgeleide uitvoer. Dezelfde titel of doelgroep wordt niet opnieuw handmatig in een webeditor beheerd.

## Demo bouwen

```
python scripts/build_website.py --demo
```

De demo gebruikt `site/demo_2025.json` met enkele historische voorbeeldtitels en nieuwe placeholderteksten. Het is nadrukkelijk geen actuele inschrijfinformatie.

## Productieversie bouwen

```
python scripts/build_website.py
```

De productieversie leest `data/2026/activities.csv` en `data/2026/offerings.csv`. Alleen offerings met een geschikte publicatiestatus worden opgenomen.

## Nog te doen

- definitieve 2026-branding en eigen beeldassets;
- expliciete website-publicatiestatus uit `PublicationState` gebruiken;
- doelgroepfiltering via `OfferingAudience`;
- publicatie via GitHub Pages of de uiteindelijke schoolhosting;
- historische site-inhoud alleen migreren waar die voor 2026 bewust wordt hergebruikt.
