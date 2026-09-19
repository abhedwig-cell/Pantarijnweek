# Aanvulling organisatie-interview, 19 september 2026

Deze aanvulling legt nieuwe informatie vast die na het eerste interviewcheckpoint is toegevoegd. Alleen expliciet bevestigde informatie wordt als feit opgenomen. Onzekere herinneringen blijven als onzeker gemarkeerd.

## 1. Historische capaciteitsfout in Excel

De organisatie beschrijft een incident in de vorige editie waarbij de capaciteitsberekening in Excel fout was. De precieze technische oorzaak is nog niet bekend, maar volgens de herinnering waren formules onjuist en/of was van verkeerde uitgangspunten uitgegaan.

Gevolg:
- leerlingen gingen inschrijven;
- veel of alle workshops liepen vrijwel direct vol;
- de organisatie ontdekte pas tijdens of vlak na opening van de inschrijving dat de capaciteit verkeerd was berekend;
- dit leidde tot acute herstelwerkzaamheden en veel stress.

De precieze fout, betrokken formule en brongegevens moeten nog met de collega's die de berekening beheren worden gereconstrueerd.

### Ontwerpconsequentie

Capaciteitsberekening wordt in de nieuwe hub geen verborgen Excel-formule die zonder controle leidend is.

Minimaal nodig:
- expliciete bron van leerlingaantallen per dagdeel;
- expliciete aftrek van verplichte/vooraf geplaatste activiteiten;
- expliciete OB/BB-splitsing;
- automatische totalen per dagdeel;
- onafhankelijke sanity checks;
- waarschuwing wanneer beschikbare capaciteit dicht bij of onder benodigde capaciteit komt;
- testbare berekeningslogica in versiebeheer;
- zichtbare aannames, zodat een wijziging in één uitgangspunt traceerbaar is.

## 2. Twee verschillende Magister-routes

De eerdere formulering dat de Pantarijnweek "via Keuzewerktijd en niet via Activiteiten" loopt, is te algemeen.

### Keuzewerktijd

De reguliere vrije workshopinschrijving van de Pantarijnweek loopt via Magister Keuzewerktijd, omdat deze workshops als onderwijstijd gelden.

### Activiteiten

Bepaalde bijzondere onderdelen worden al vóór de hoofdinschrijving via de gewone Magister-module Activiteiten georganiseerd.

Bevestigd voorbeeld:
- op maandag is er een ski-dag voor bovenbouwleerlingen;
- deelname is vrijwillig;
- leerlingen schrijven zich vooraf in;
- er zijn kosten aan verbonden;
- ouderlijke betaling/toestemming speelt een rol;
- deelname is vóór de hoofdinschrijving van de Pantarijnweek al bekend.

Daarmee moet de centrale planning rekening houden: leerlingen die aan zo'n activiteit deelnemen hoeven op het betreffende dagdeel/de betreffende dag geen gewone workshopcapaciteit meer te krijgen.

## 3. Betalingen en betaalde activiteiten

Bij betaalde vrijwillige activiteiten moet worden gecontroleerd of betaling is voldaan voordat deelname definitief is.

De exacte technische route in Magister en het betalingssysteem is nog niet gereconstrueerd.

Onzeker / nog te bevestigen:
- of alle betaalde activiteiten via dezelfde route lopen;
- hoe betaling formeel wordt gekoppeld aan deelname;
- wie de gezaghebbende status van betaling beheert;
- of verplichte activiteiten principieel kosteloos zijn. Tijdens het gesprek werd vermoed dat verplichte activiteiten geen directe deelnemerskosten hebben, maar dit is niet bevestigd.

## 4. Vooraf bekende speciale activiteiten reduceren capaciteitsvraag

Naast verplichte activiteiten zijn er dus ook vrijwillige voorinschrijvingen die vóór de hoofdinschrijving bekend zijn.

Voor de capaciteitsberekening moeten daarom minstens drie soorten leerlingstatus worden onderscheiden:

1. **verplicht geplaatst**
   Leerling moet deelnemen aan een vaste activiteit.

2. **vooraf vrijwillig geplaatst**
   Leerling heeft zich al voor een speciale activiteit ingeschreven, eventueel met betaling.

3. **vrije keuze nodig**
   Leerling moet nog capaciteit krijgen in het gewone workshopaanbod.

De centrale hub moet de benodigde workshopcapaciteit per dagdeel berekenen op basis van groep 3, niet op basis van het totale aantal leerlingen.

## 5. Vervolginterview moet meerdere proceseigenaren bevatten

Tijdens het gesprek is expliciet aangegeven dat enkele collega's beter weten hoe de capaciteitsberekeningen en andere deelprocessen precies worden uitgevoerd.

Voor het vervolginterview moeten daarom in ieder geval de beheerders van:
- capaciteitsberekening;
- workshop-/lokalenplanning;
- Forms/Excel-verwerking;
- betalingen/speciale activiteiten

worden betrokken.

De gesproken namen "Robin" en "Niels" kwamen naar voren, maar de exacte spelling en roltoedeling worden niet als canoniek vastgelegd totdat dit is bevestigd.

## 6. Stakeholderobservatie over de weekopzet

Er is een persoonlijke observatie uitgesproken dat de concentratie van zeer veel activiteiten in één week organisatorisch zwaar is en dat spreiding van activiteiten over het schooljaar mogelijk rustiger zou zijn.

Dit is:
- **geen huidige beleidsregel**;
- **geen besluit voor 2026**;
- wel een relevante stakeholderervaring voor een latere evaluatie van het concept.

Voor 2026 blijft het uitgangspunt dat de Pantarijnweek doorgaat in de bestaande weekvorm.

## 7. Nieuwe harde ontwerpregels

Op basis van deze aanvulling gelden voor het ontwerp nu aanvullend:

- capaciteitslogica moet testbaar en auditbaar zijn;
- een capaciteitsresultaat moet herleidbaar zijn naar bronwaarden;
- speciale voorinschrijvingen moeten capaciteit reduceren vóór de hoofdinschrijving;
- de hub moet meerdere Magister-publicatieroutes kunnen onderscheiden;
- betaling/deelname moet als aparte status kunnen worden vastgelegd voor betaalde activiteiten;
- foutdetectie vóór openstelling van de inschrijving wordt een expliciete kwaliteitsgate.
