# Pantarijnweek planning hub

Centrale, versiebeheerde planning voor de Pantarijnweek.

## Doel

Voor de editie 2026 wordt toegewerkt naar één bron van waarheid voor activiteiten, dagdelen, doelgroepen, personeel, lokalen, vaste activiteiten, capaciteit en budget. Website-, Magister-, Zermelo- en Exceloverzichten zijn afgeleide uitvoer en geen afzonderlijke administraties.

## Status

De repository is gestart met een reverse-engineering van de voorbeeldbestanden uit 2025-2026. De eerste stap is het datamodel en de planningsregels vastleggen. Daarna worden de historische bestanden gecontroleerd gemigreerd en gebruikt als testset.

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
