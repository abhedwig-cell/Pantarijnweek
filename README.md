# Pantarijnweek planning hub

Centrale, versiebeheerde planning voor de Pantarijnweek.

## Doel

Voor de editie 2026 wordt toegewerkt naar één bron van waarheid voor activiteiten, dagdelen, doelgroepen, personeel, lokalen, vaste activiteiten, capaciteit en budget. Website-, Magister-, Zermelo- en Exceloverzichten zijn afgeleide uitvoer en geen afzonderlijke administraties.

## Status

De repository is gestart met een reverse-engineering van de voorbeeldbestanden uit 2025-2026. De huidige foundation staat op de werkbranch `work/central-hub-foundation`.

Belangrijkste documenten:
- [Reverse-engineering 2025-2026](docs/reverse-engineering-2025-2026.md)
- [Datamodel](docs/datamodel.md)
- [Validatieregels](docs/validation-rules.md)
- [Migratieplan](docs/migration-plan.md)
- [Vragen voor Susanne](docs/questions-for-susanne.md)

De genormaliseerde 2026-structuur staat in [data/2026](data/2026). `scripts/validate_data.py` controleert de basisstructuur automatisch.

## Privacy

Deze repository is openbaar. Plaats hier daarom geen leerlinggegevens, Magisterexports, telefoonnummers, privé-e-mailadressen of andere herleidbare persoonsgegevens. Ruwe bronbestanden blijven buiten Git totdat de opslaglocatie en toegangsrechten daarvoor expliciet zijn geregeld.

## Ontwerpprincipe

```
brondata -> normalisatie -> validatie -> planning -> afgeleide exports
                                             |-> website
                                             |-> Magister
                                             |-> Zermelo
                                             |-> Excel/controleoverzichten
```

Een gegeven wordt één keer beheerd en waar mogelijk automatisch hergebruikt.

## Eerstvolgende stap

Voor echte migratie wordt met de organisatie vastgesteld welke bron per gegevenstype leidend is en welke planningsregels hard of zacht zijn. Verschillen tussen de 2025-2026-bestanden worden niet stil opgelost, maar expliciet gereconcilieerd.
