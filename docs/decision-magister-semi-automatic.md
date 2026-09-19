# Besluit: Magister voorlopig semi-automatisch

Datum: 19 september 2026

Status: **BESLOTEN VOOR 2026-ONTWERP**

## Besluit

De centrale Pantarijnweek-hub wordt voorlopig ontworpen met een **semi-automatische Magisterroute**.

De hub is de bron voor planning, capaciteit, doelgroep, dagdeel, titel en publicatiestatus. Magister blijft voorlopig een extern systeem waarin de feitelijke Keuzewerktijd- en Activiteitenrecords door een gebruiker worden aangemaakt of aangepast.

Volledige programmatische schrijf-integratie met Magister is **geen afhankelijkheid** voor de eerste operationele versie.

## Baseline workflow

De centrale hub genereert per benodigd Magisterrecord minimaal:

- dagdeel;
- titel;
- Magisterroute: Keuzewerktijd of Activiteit;
- doelgroep;
- capaciteit;
- eventuele OB/BB-splitsing;
- eventuele doelgroepreservering;
- status van verwerking;
- controle-/reconciliatiestatus.

De gebruiker voert alleen de noodzakelijke gegevens in Magister in en markeert daarna het record in de hub als verwerkt.

## Vereiste ondersteuning

De semi-automatische route moet zo weinig mogelijk denkwerk aan de Magisterkant overlaten.

Gewenste functies:

1. exact overzicht van alle nog aan te maken Magisterrecords;
2. automatische opsplitsing van één offering naar meerdere Magisterrecords waar nodig;
3. kopieerbare titel, doelgroep en capaciteit;
4. status `nog te doen`, `ingevoerd`, `gewijzigd na invoer`, `gecontroleerd`;
5. waarschuwing wanneer een bronrecord verandert nadat het al in Magister is ingevoerd;
6. preflight telling: verwacht aantal Magisterrecords versus ingevoerd/gecontroleerd;
7. aparte behandeling van Keuzewerktijd en Activiteiten;
8. audit trail van wijzigingen.

## Niet doen

De eerste versie is niet afhankelijk van:

- een niet-bevestigde Magister API;
- browserautomatisering die de Magisterinterface nabootst;
- handmatig opnieuw berekenen van capaciteit in Magister;
- losse Excelnotities om bij te houden wat al is ingevoerd.

## Latere uitbreiding

Als later een officieel ondersteunde import- of schrijfkoppeling beschikbaar blijkt, kan een automatische adapter de handmatige invoerstap vervangen zonder het centrale datamodel te wijzigen.
