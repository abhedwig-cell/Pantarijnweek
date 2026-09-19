# Pantarijnweek planning hub

Centrale, versiebeheerde planning voor de Pantarijnweek.

## Doel

Voor de editie 2026 wordt toegewerkt naar één bron van waarheid voor activiteiten, dagdelen, doelgroepen, personeel, lokalen, vaste activiteiten, capaciteit en budget.

De website en Magisterverwerking zijn afgeleide uitvoer. Zermelo is geen inhoudelijk publicatiekanaal voor de Pantarijnweek; het blijft alleen relevant als externe rooster-randvoorwaarde.

## Status

De foundation, eerste organisatie-interviews, capaciteitsregels, donderdagquota en de semi-automatische Magisterbaseline zijn vastgelegd.

Er is nu ook een eerste datagedreven websiteprototype:
- generator: `scripts/build_website.py`
- bron-/demodata: `site/`
- gegenereerde uitvoer: `site/public/`
- architectuur: `docs/website-architecture.md`

Belangrijkste documenten:
- [Reverse-engineering 2025-2026](docs/reverse-engineering-2025-2026.md)
- [Datamodel](docs/datamodel.md)
- [Validatieregels](docs/validation-rules.md)
- [Migratieplan](docs/migration-plan.md)
- [Interviewcheckpoint](docs/interview-checkpoint-2026-09-19.md)
- [Website-architectuur](docs/website-architecture.md)
- [Magisterbaseline](docs/decision-magister-semi-automatic.md)

De genormaliseerde 2026-structuur staat in [data/2026](data/2026). `scripts/validate_data.py` controleert de basisstructuur automatisch.

## Privacy

Deze repository is openbaar. Plaats hier daarom geen leerlinggegevens, Magisterexports, telefoonnummers, privé-e-mailadressen of andere herleidbare persoonsgegevens. Ruwe bronbestanden blijven buiten Git totdat de opslaglocatie en toegangsrechten daarvoor expliciet zijn geregeld.

## Ontwerpprincipe

```
brondata -> normalisatie -> validatie -> planning
                                      |-> gegenereerde website
                                      |-> semi-automatisch Magisterwerkpakket
                                      |-> Excel/controleoverzichten
```

Een gegeven wordt één keer beheerd en waar mogelijk automatisch hergebruikt.

## Websiteprototype

Demo bouwen:

```
python scripts/build_website.py --demo
```

Productieversie uit de 2026-hub bouwen:

```
python scripts/build_website.py
```

De demo gebruikt historische voorbeeldtitels om de vorm en generator te testen. Het is geen actuele inschrijfinformatie.

## Eerstvolgende stappen

- open interviewpunten sluiten met de betreffende proceseigenaren;
- definitieve 2026-branding en eigen beeldassets vaststellen;
- publicatiestatus en doelgroepregels direct aan de websitegenerator koppelen;
- daarna de website via de gekozen hosting publiceren.
