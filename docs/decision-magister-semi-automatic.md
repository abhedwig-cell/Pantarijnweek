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
- exacte start- en eindtijd uit TimeSlot;
- titel;
- Magisterroute: Keuzewerktijd of Activiteit;
- doelgroep;
- capaciteit;
- eventuele OB/BB-splitsing;
- eventuele doelgroepreservering;
- status van verwerking;
- controle-/reconciliatiestatus.

De gebruiker voert alleen de noodzakelijke gegevens in Magister in en markeert daarna het record in de hub als verwerkt.

Er is daarnaast een ondersteunde **outside-in route** voor het geval een record toch eerst rechtstreeks in Magister wordt aangemaakt. Zo'n record wordt via een buitenom-inbox teruggebracht in de centrale regie en gekoppeld aan een bestaande Offering/FixedActivity of aan een minimale centrale stub.

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
8. audit trail van wijzigingen;
9. buitenom-inbox voor records die eerst in Magister zijn aangemaakt;
10. snelle capture met minimaal titel + dagdeel + Magisterroute;
11. optionele veilige import van export, screenshot of foto als invoerhulp;
12. reconciliatiestatus totdat centraal en Magister weer overeenkomen;
13. invoer van de echte workshopduur: ochtend 10:00–12:30 en middag 13:15–15:45;
14. geen terugval op de historische lesuur-2/lesuur-5-workaround.

## Niet doen

De eerste versie is niet afhankelijk van:

- een niet-bevestigde Magister API;
- browserautomatisering die de Magisterinterface nabootst;
- handmatig opnieuw berekenen van capaciteit in Magister;
- losse Excelnotities om bij te houden wat al is ingevoerd;
- foto's of screenshots met leerlinggegevens opslaan in de openbare GitHub-repository.

## Latere uitbreiding

Als later een officieel ondersteunde import- of schrijfkoppeling beschikbaar blijkt, kan een automatische adapter de handmatige invoerstap vervangen zonder het centrale datamodel te wijzigen.

## Magister MX en absentie

Sinds de overstap van de school naar Magister MX voor absentie kan de Pantarijnweek met de daadwerkelijke workshopblokken in de leerlingagenda worden gezet.

Voor 2026 geldt:
- ochtend: 10:00–12:30;
- middag: 13:15–15:45.

De vroegere koppeling aan alleen lesuur 2 en lesuur 5 was een technische workaround voor absentie en is geen 2026-planningsregel meer. De centrale TimeSlot is authority voor deze tijden.
