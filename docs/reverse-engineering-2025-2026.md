# Reverse-engineering Pantarijnweek 2025-2026

## Doel

Deze notitie beschrijft wat uit de aangeleverde voorbeeldbestanden kan worden afgeleid over het bestaande planningsproces. Dit is geen reconstructie van intenties die niet in de bestanden staan.

## Bronnen

De analyse is gebaseerd op vijf aangeleverde bestanden:

1. Overzicht workshops en activiteiten 2025-2026 - Voorbeeld.xlsx
2. Lokalenoverzicht inclusief workshops 2025-2026 - Voorbeeld.xlsx
3. Leerjaar gebonden activiteiten voorbeeld van 2526.xlsx
4. Beschikbaarheid voorbeeld.xlsx
5. Pantarijnweek 25-26 - opstart.docx

De ruwe bestanden worden niet in deze openbare repository opgenomen omdat ze namen, interne codes en ten minste één contactgegeven bevatten.

## Huidige administratieve structuur

### 1. Workshops en activiteiten

Het hoofdwerkboek heeft acht aparte dagdeelbladen en een begrotingsblad. Per aanbodregel staan onder meer:

- controle Zermelo
- controle website
- controle Magister
- titel activiteit
- categorie
- doelgroep OB/BB
- keuze of verplicht
- verplichte doelgroep
- capaciteit OB
- capaciteit BB
- lokaal of locatie
- organiserende
- begeleiding
- budget
- extra informatie

In de acht dagdelen zijn 314 regels gevonden met een activiteitstitel. Op basis van alleen simpele normalisatie van hoofdletters en witruimte zijn dat 158 verschillende titels. Dit getal is niet hetzelfde als 158 semantisch unieke activiteiten. Kleine titelvarianten blijven mogelijk apart staan.

### 2. Lokalen

Een tweede werkboek zet lokalen tegen de acht dagdelen uit. Dezelfde activiteitstitel wordt daar opnieuw ingevoerd, meestal gecombineerd met een personeelscode. Voor sportzalen in De Vlinder bestaat nog een aparte matrix.

Dit bestand is daarmee feitelijk een afgeleid rooster, maar wordt handmatig naast het workshopbestand onderhouden.

### 3. Leerjaargebonden activiteiten

Een apart bestand legt per leerjaar, afdeling en weekdag vaste activiteiten vast, zoals excursies, CKV, gymnasiumdag, debatdag en SportXtra.

De notities onderaan mengen verschillende deelnameregels:
- verplicht
- op inschrijving
- vraagteken/onzeker
- doelgroepgebonden

Dagdeelprecisie ontbreekt meestal. Voor een centrale planning moet dit een expliciet veld worden.

### 4. Beschikbaarheid en toewijzing personeel

Het beschikbaarheidsbestand bevat twee versies. In de vroegere versie staan veel cellen als 1 of 0, gecombineerd met reeds bekende verplichtingen. In de latere versie zijn veel beschikbare cellen vervangen door concrete activiteiten of andere taken.

Daardoor worden twee verschillende concepten in één cel opgeslagen:
- beschikbaarheid
- daadwerkelijke toewijzing

Deze moeten in het nieuwe model apart worden opgeslagen. Anders verdwijnt de oorspronkelijke beschikbaarheidsinformatie tijdens het plannen.

### 5. Organisatie

De opstartnotitie verdeelt onder meer website, communicatie en de Excelpuzzel over verschillende organisatoren. Ook blijkt dat vaste activiteiten en bij excursies de begeleiding liefst al voor de kick-off worden vastgelegd.

## Kwantitatieve datakwaliteit in het workshopwerkboek

Van de 314 aanbodregels zijn onder meer gevonden:

- 11 zonder categorie
- 5 zonder doelgroep
- 15 zonder lokaal of locatie
- 24 zonder organiserende
- 7 met een niet-numerieke ingevulde budgetwaarde
- 11 regels die als verplicht zijn aangeduid maar geen expliciete verplichte doelgroep bevatten
- meerdere vrije tekstvarianten voor publicatiestatus, zoals x, x?, uit Magister, moet eruit en verplaatsen

Categorieën zijn eveneens vrije tekst. Bijvoorbeeld Kunst, kunst, Maatschappij, Maatschappelijk en combinaties met verschillende scheidingstekens. Een gecontroleerde lijst met meerdere categorieën per activiteit is daarom beter dan één vrij tekstveld.

## Capaciteit

De capaciteitsbalans staat nu als formule in de kolomkop. De verwachte aantallen leerlingen zijn per dagdeel direct als getal in de formule opgenomen. Voorbeelden zijn 562/433, 614/451 en 859/451 voor OB/BB.

Hieruit volgt dat het aantal leerlingen dat een vrije workshopplek nodig heeft per dagdeel kan verschillen. Dat hoort niet in een formulekop, maar moet worden afgeleid uit:
- cohortgrootte
- verplichte of vaste activiteiten
- deelname van andere locaties
- eventuele voorinschrijvingen

## Begroting: aantoonbare inconsistentie

Het maandagmorgenblad berekent een dagtotaal van EUR 656. Het begrotingsblad bevat voor maandagmorgen echter de vaste waarde EUR 100. De andere dagdelen verwijzen wel naar hun dagbladtotaal.

Daarom geldt in het aangeleverde bestand:
- som van de acht dagbladen: EUR 5.009
- totaal op het begrotingsblad: EUR 4.453
- verschil: EUR 556

Uit het bestand zelf kan niet worden vastgesteld of EUR 100 bewust is gecorrigeerd of dat de koppeling ontbreekt. Het nieuwe systeem moet dit soort dubbele waarheid uitsluiten.

## Mogelijke roosterconflicten die nog gereconcilieerd moeten worden

Een exacte vergelijking van ruimtevelden binnen hetzelfde dagdeel levert kandidaat-conflicten op. Een voorbeeld is lokaal 0.31 op donderdagmorgen, dat in het workshopoverzicht aan meer dan één activiteit is gekoppeld. Het lokalenoverzicht geeft voor datzelfde lokaal en dagdeel weer een andere activiteit.

Dit is nog geen bewijs welke bron correct is. Het is wel bewijs dat de huidige bestanden niet zonder reconciliatie als één consistente planning kunnen worden behandeld.

## Hoofdconclusie

De bestaande bestanden bevatten de juiste soorten informatie, maar de gegevensstructuur veroorzaakt dubbel onderhoud. Het nieuwe ontwerp moet daarom expliciet scheiden tussen:

1. stamgegevens
2. beschikbaarheid
3. vaste verplichtingen
4. aanbodmomenten
5. toewijzingen
6. afgeleide exports

Magister, Zermelo, website en Excel worden uitvoerkanalen van dezelfde bron.
