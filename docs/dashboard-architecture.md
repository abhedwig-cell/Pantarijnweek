# Dashboard- en signaleringsarchitectuur

## Doel

De centrale hub moet niet alleen gegevens bewaren, maar de organisatie actief laten zien:
- hoe ver de voorbereiding is;
- waar gegevens ontbreken;
- waar een wijziging nieuwe problemen veroorzaakt;
- welke onderdelen vóór publicatie of inschrijving nog geblokkeerd zijn.

De dashboards zijn **afgeleide views**. Zij zijn nooit een tweede bronadministratie.

## Ontwerpprincipe

Een rood, oranje of groen signaal wordt niet handmatig ingekleurd.

Elk signaal moet herleidbaar zijn tot:
1. bronrecords in de centrale hub;
2. een expliciete berekenings- of validatieregel;
3. de actuele uitkomst van die regel;
4. het moment waarop de uitkomst opnieuw is berekend.

Als een bronrecord wijzigt, moeten alle relevante signalen opnieuw worden berekend.

## Dashboard 1 — Regie

Doel: in één oogopslag zien of de editie organisatorisch klaar is.

Voorbeelden van tegels/signalen:
- aantal activiteiten: concept / compleet / gepubliceerd;
- aantal offerings zonder dagdeel;
- aantal offerings zonder doelgroep;
- aantal offerings zonder lokaal;
- aantal offerings zonder voldoende begeleiding;
- aantal open buitenom-items;
- website: nog te publiceren / gepubliceerd / gewijzigd na publicatie;
- Magister: nog te doen / ingevoerd / gewijzigd na invoer / gecontroleerd;
- budgetstatus;
- preflightstatus voor hoofdinschrijving.

Het regiedashboard toont vooral uitzonderingen en voortgang, niet alle brondata.

## Dashboard 2 — Capaciteit

Doel: direct zien of er per dagdeel en doelgroep voldoende werkelijk beschikbare keuzeplaatsen zijn.

Per dagdeel minimaal:
- vrije-keuzevraag OB;
- beschikbare keuzeplaatsen OB;
- marge OB;
- vrije-keuzevraag BB;
- beschikbare keuzeplaatsen BB;
- marge BB;
- reserveringen;
- reeds geplaatste leerlingen;
- reserve-/noodcapaciteit;
- waarschuwing voor quota of doelgroepblokkades.

Voorbeeld:

```
Maandag ochtend
OB: vraag 412 | aanbod 438 | marge +26  -> groen
BB: vraag 291 | aanbod 294 | marge  +3  -> oranje
```

De precieze grens tussen groen/oranje/rood wordt pas vastgelegd wanneer de organisatie de gewenste veiligheidsmarge heeft bevestigd.

## Dashboard 3 — Magister en reconciliatie

Doel: voorkomen dat de centrale werkelijkheid en Magister uit elkaar lopen.

Minimaal:
- verwachte Magisterrecords;
- nog niet ingevoerd;
- ingevoerd maar nog niet gecontroleerd;
- centrale bron gewijzigd na Magisterinvoer;
- buitenom-records nog niet gematcht;
- verschillen in capaciteit of deelnemersaantal;
- laatste verificatiemoment.

Een nieuw rechtstreeks in Magister aangemaakt Activiteitenrecord moet hier zichtbaar worden totdat het centraal is gereconcilieerd.

## Dashboard 4 — Ruimtes en personeel

Doel: conflicten en ontbrekende resources vroeg zichtbaar maken.

Voorbeelden:
- dubbele lokaalboeking;
- offering zonder lokaal;
- special-room constraint niet vervuld;
- externe locatie zonder benodigde begeleiding;
- begeleider dubbel ingepland;
- begeleider unavailable;
- offering met onvoldoende bevestigde begeleiding.

De exacte personeelsnormen zijn nog niet volledig vastgesteld; onbekende regels moeten daarom als "nog niet beoordeelbaar" worden getoond, niet stilzwijgend groen.

## Signaalmodel

Een dashboardregel produceert conceptueel een HealthSignal:

- signal_id
- scope_type = edition / slot / offering / cohort / room / magister_record
- scope_id
- rule_id
- severity = info / ok / warning / critical / unknown
- title
- explanation
- observed_value
- threshold_or_expectation
- source_refs
- calculated_at

HealthSignal is een **afgeleid resultaat**, geen handmatig te beheren bronrecord.

De gebruiker moet vanuit een signaal kunnen doorklikken naar de bronrecords die het probleem veroorzaken.

## Wijzigingsimpact

Een belangrijk doel is directe feedback na wijzigingen.

Voorbeeld:

1. capaciteit van een workshop verandert van 30 naar 20;
2. Offering wordt opgeslagen;
3. capaciteitsberekening wordt opnieuw uitgevoerd;
4. dagdeelmarge zakt onder de ingestelde veiligheidsgrens;
5. dashboard verandert van groen naar rood;
6. de gebruiker ziet welke wijziging de waarschuwing heeft veroorzaakt.

Hetzelfde principe geldt voor:
- annuleren van een workshop;
- toevoegen van een verplichte activiteit;
- nieuwe Magister-voorinschrijvingen;
- wijziging van een lokaal;
- uitval van begeleiding;
- wijziging van doelgroepgeschiktheid.

## Backend

De backend heeft daarom naast CRUD op bronrecords minimaal nodig:
- deterministische berekening van afgeleide kengetallen;
- rule engine / validatielaag;
- dependency-aware herberekening na wijzigingen;
- timestamp en bronverwijzing per signaal;
- onderscheid tussen `unknown` en `ok`;
- mogelijkheid om historische signalen of wijzigingsmomenten te auditen.

In de eerste versie mag herberekening eenvoudig na elke wijziging volledig plaatsvinden. Optimalisatie naar alleen affected dependencies is pas nodig als performance daar aanleiding toe geeft.

## Geen Excelkleurcodes als authority

De 2025-Excel kan worden gezien als een vroege combinatie van:
- bronadministratie;
- rekenmodel;
- dashboard;
- handmatige statuscodering.

Die functies worden nu gescheiden.

De nieuwe dashboards mogen dezelfde praktische informatiebehoefte vervullen, maar:
- kleuren zijn afgeleid;
- formules zijn testbaar;
- bronwaarden zijn traceerbaar;
- wijzigingen worden centraal verwerkt;
- dezelfde feiten hoeven niet op meerdere plekken handmatig te worden bijgehouden.
