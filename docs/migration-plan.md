# Migratieplan naar één centrale hub

## Uitgangspunt

De voorbeeldbestanden worden eerst als historische testset behandeld. Ze worden niet rechtstreeks de nieuwe database. Eerst wordt vastgesteld welke informatie bron is en welke informatie afgeleid hoort te zijn.

## Fase 1: authority vastleggen

Samen met de organisatie vaststellen:
- welk bestand nu leidend is voor activiteitinhoud
- welk bestand leidend is voor lokalen
- welk bestand leidend is voor beschikbaarheid
- wat Zermelo en Magister terugschrijven of alleen consumeren
- wie wijzigingen mag autoriseren

Resultaat: per gegevenstype precies één eigenaar en één bron.

## Fase 2: 2025-2026 normaliseren

De voorbeeldbestanden worden omgezet naar:
- Activity
- Offering
- Room
- FixedActivity
- StaffAvailability
- Assignment
- PublicationState
- BudgetItem

Tijdens deze stap worden verschillen niet stil opgelost. Conflicten krijgen een expliciete reconcile-status.

## Fase 3: validator

De repository bevat een eerste validator. Die wordt uitgebreid met:
- referentiechecks
- dubbelboekingen
- personeelsconflicten
- ontbrekende verplichte doelgroepen
- capaciteitsbalans
- budgetcontrole
- publicatiecontrole

## Fase 4: 2026 invoer

Pas na authority en validatie worden de echte 2026-gegevens ingevoerd.

Het doel is dat een workshop eenmaal wordt aangemaakt en daarna alleen offerings per dagdeel krijgt.

## Fase 5: afgeleide uitvoer

Vanuit de centrale gegevens worden overzichten gegenereerd voor:
- organisatie
- lokalen
- docenten/begeleiders
- website
- Magister
- Zermelo
- budget
- evaluatie en historische analyse

Excel kan nog steeds een uitvoer- en controlescherm zijn, maar niet meer een tweede waarheid.

## Fase 6: planning ondersteunen

Pas als de harde en zachte planningsregels bekend zijn, wordt automatische ondersteuning toegevoegd.

Eerste niveau:
- conflict detecteren
- capaciteit berekenen
- ontbrekende gegevens tonen

Tweede niveau:
- alternatieve lokaal- of personeelsindeling voorstellen

Een volledige optimizer komt pas in beeld als duidelijk is dat de regels stabiel genoeg zijn.
