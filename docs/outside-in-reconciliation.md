# Buitenom-inbox en Magister-reconciliatie

## Probleem

Een activiteit kan buiten de centrale hub om rechtstreeks in Magister Activiteiten of een andere operationele route worden aangemaakt.

Als zo'n activiteit leerlingen bezet, capaciteit consumeert of een dagdeel blokkeert, maar niet in de centrale hub bekend is, ontstaat een tweede werkelijkheid. Dat is een direct risico voor capaciteitsberekeningen, planning, communicatie en last-minute herplaatsing.

## Ontwerpprincipe

**Elke activiteit die leerlingen, capaciteit, personeel, ruimte of een dagdeel beïnvloedt moet centraal bekend zijn, ongeacht de inschrijfroute.**

De voorkeursroute blijft hub-first:

```
hub -> Magisterwerkpakket -> handmatige invoer in Magister -> controle
```

Maar de hub krijgt daarnaast een ondersteunde outside-in route voor situaties waarin iemand eerst in Magister handelt:

```
Magister / lijst / screenshot
        |
        v
buitenom-inbox
        |
        v
match bestaand Offering
of maak minimale activity/offering-stub
        |
        v
verwerk plaatsingen/capaciteit
        |
        v
reconciled + verified
```

## Buitenom-inbox

De invoer moet bewust zeer licht zijn.

Minimaal:
- korte titel;
- betrokken dagdeel of dagdelen;
- externe route, bijvoorbeeld Magister Activiteiten;
- indien bekend: capaciteit of aantal deelnemers;
- optioneel een Magister-recordnummer;
- optioneel een screenshot, foto of bestand als tijdelijke invoerbron.

De gebruiker hoeft op dit moment niet nogmaals alle workshopmetadata in te voeren.

De hub maakt een InboxItem en probeert dit te koppelen aan een bestaand Activity/Offering-record. Als geen match bestaat, ontstaat een minimale stub die later kan worden aangevuld.

## Foto of screenshot

Een foto of screenshot van een deelnemerslijst kan een bruikbare **invoerhulp** zijn, maar is niet de canonieke bron in de openbare GitHub-repository.

Een dergelijke afbeelding kan namen, leerlingnummers of andere persoonsgegevens bevatten. Daarom geldt:

- geen deelnemersfoto's of Magister-screenshots in de publieke repository;
- alleen verwerken in een daarvoor geschikte private/secure operationele omgeving;
- na extractie minimaal het aantal geplaatste leerlingen en relevante cohortverdeling verwerken;
- persoonsniveau alleen bewaren waar dat operationeel nodig en passend beveiligd is;
- de publieke hub kan hooguit een niet-herleidbare secure_evidence_ref en geaggregeerde telling bevatten.

## Reconciliatiestatus

Een buitenom-record doorloopt:

- `captured` — snel geregistreerd;
- `unreconciled` — nog niet gekoppeld aan centrale planning;
- `matched` — gekoppeld aan bestaand Offering/FixedActivity;
- `created` — centrale stub is aangemaakt omdat nog geen record bestond;
- `verified` — aantallen, dagdeel en route gecontroleerd;
- `superseded` — vervangen door een nieuwer of correcter record.

Een record dat nog `unreconciled` is mag niet stil verdwijnen.

## Capaciteitswerking

Zodra een externe activiteit deelnemers bezet, wordt de relevante PlacementSummary bijgewerkt.

Bijvoorbeeld:

```
ski-activiteit maandag
18 bevestigde deelnemers BB
        |
        v
PlacementSummary:
placement_type = preregistered
placed_count = 18
source = Magister Activiteiten
        |
        v
18 leerlingen minder vrije-keuzevraag
in de betrokken dagdelen
```

Er mag daarna geen tweede handmatige aftrek in Excel of elders plaatsvinden.

## Dagelijkse/periodieke controle

De hub toont een klein reconciliatieblok:

- buitenom-items nog niet gekoppeld;
- Magisterrecords nog niet geverifieerd;
- participant counts die veranderd zijn sinds laatste controle;
- activiteiten die wel capaciteit beïnvloeden maar geen Offering/FixedActivity hebben;
- centrale records die als ingevoerd in Magister staan maar geen recente verificatie hebben.

Doel is niet extra administratie, maar juist zichtbaar maken waar de centrale werkelijkheid mogelijk achterloopt.

## Gewenste gebruikerservaring

De ideale exception flow is ongeveer:

1. Suzanne maakt of ontdekt een activiteit in Magister.
2. Zij kiest in de hub **Nieuwe buitenom-activiteit**.
3. Zij vult alleen titel + dagdeel in en kiest **Magister Activiteiten**.
4. Eventueel maakt/uploadt zij een foto of screenshot in de beveiligde operationele omgeving.
5. De hub haalt daar waar mogelijk aantallen/metadata uit.
6. De gebruiker bevestigt de match.
7. Capaciteit en centrale status zijn direct bijgewerkt.

Het ontwerp moet dit sneller maken dan dezelfde informatie nogmaals handmatig in meerdere spreadsheets invoeren.
