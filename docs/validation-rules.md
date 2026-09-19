# Validatieregels

De validator is bedoeld om fouten vroeg te vinden. Niet alle regels zijn al definitief. Regels waarvoor nog besluitvorming van de organisatie nodig is, staan als voorlopig gemarkeerd.

## Harde dataconsistentie

1. Elke primaire ID is uniek.
2. Elke foreign key verwijst naar een bestaand record.
3. Elke Offering verwijst naar precies één Activity en één TimeSlot.
4. Budgetbedragen zijn leeg of numeriek en niet negatief.
5. Een mandatory Offering heeft een mandatory_target.
6. Een Assignment verwijst naar hetzelfde slot als de gekoppelde Offering.
7. Een persoon kan niet twee exclusieve assignments in hetzelfde slot hebben.
8. Een exclusieve Room kan niet twee gelijktijdige offerings bevatten.
9. Een assigned persoon mag niet als unavailable in hetzelfde slot staan.
10. Publicatiestatussen gebruiken alleen bekende kanalen en statussen.

## Capaciteit

Per slot moet de benodigde vrije-keuzecapaciteit worden berekend vanuit cohortgroottes en reeds vastgelegde activiteiten. De aantallen worden niet hardcoded in kolomkoppen en niet als verborgen handmatige tussenuitkomst beheerd.

Minimaal wordt apart gecontroleerd:
- OB-vraag en OB-capaciteit;
- BB-vraag en BB-capaciteit;
- locatie/onderwijsvorm;
- doelgroepbeperkingen;
- verplichte plaatsingen;
- vrijwillige voorinschrijvingen die al vóór de hoofdinschrijving vaststaan;
- examen-/eigen programma's voor zover die de vrije-keuzevraag reduceren;
- reserve-/noodcapaciteit.

De gewenste veiligheidsmarge voor overcapaciteit is nog door de organisatie te bepalen.

## Capaciteitsreserveringen en inschrijfvensters

Tijdelijke doelgroeptoegang mag de broncapaciteit van een offering niet overschrijven.

Voor elke offering geldt:
- som van actieve reserveringen mag de totale capaciteit niet overschrijden;
- geplaatste deelnemers + resterende actieve reserveringen voor andere groepen mogen de totale capaciteit niet overschrijden;
- een doelgroep mag alleen inschrijven binnen een geldig EnrollmentWindow;
- een doelgroep moet volgens OfferingAudience toegelaten zijn;
- ongebruikte capaciteit mag alleen volgens de vastgelegde release_policy vrijkomen;
- na vrijgave moet de resterende algemene capaciteit opnieuw berekenbaar zijn uit bronrecords;
- oorspronkelijke capaciteit moet altijd behouden en auditbaar blijven.

Een workflow waarbij iemand capaciteit handmatig verlaagt, het oude getal onthoudt en later opnieuw invult, wordt niet als geldige operationele route beschouwd.

## Capaciteits-preflight vóór inschrijving

Een historische fout in de Excel-berekening heeft ertoe geleid dat bij openstelling van de inschrijving veel aanbod vrijwel direct vol zat. Daarom wordt een expliciete preflight-gate onderdeel van de nieuwe werkwijze.

De hoofdinschrijving mag pas worden vrijgegeven wanneer:

1. de bron van het totale aantal leerlingen per doelgroep bekend en vastgelegd is;
2. alle verplichte plaatsingen per relevant slot zijn afgetrokken;
3. alle reeds bekende vrijwillige voorinschrijvingen per relevant slot zijn afgetrokken;
4. deelnemers van andere locaties/onderwijsvormen die vooraf zijn geplaatst of gereserveerd correct zijn verwerkt;
5. benodigde vrije-keuzecapaciteit en aangeboden capaciteit onafhankelijk opnieuw zijn berekend;
6. OB en BB afzonderlijk de ingestelde veiligheidsmarge halen;
7. quota/reserveringen per doelgroep niet leiden tot overboeking of verborgen capaciteitsverlies;
8. afwijkingen ten opzichte van een tweede berekening of controletotaal verklaard zijn;
9. de gebruikte aannames en bronwaarden zichtbaar zijn;
10. de validaties zonder kritieke fouten slagen.

Een rekenresultaat moet herleidbaar zijn naar bronwaarden. Een wijziging in leerlingaantal, vaste activiteit, voorinschrijving, reservering of offering moet de capaciteitsuitkomst reproduceerbaar veranderen.

## Doelgroepgeschiktheid

Per offering moet expliciet vastliggen welke cohorten/locaties/onderwijsvormen mogen deelnemen.

Een offering die voor een doelgroep niet geschikt of niet opengesteld is, mag niet via een inschrijfvenster toch beschikbaar worden.

Doelgroepgeschiktheid wordt niet afgeleid uit vrije tekst of uit de workshoptitel.

## Handmatige plaatsing

Wanneer een doelgroep via een lijst wordt aangeleverd in plaats van zelf in te schrijven:
- moet de bron van die lijst bekend zijn;
- moet het geplaatste aantal expliciet worden verwerkt;
- moet de capaciteit automatisch worden gereduceerd;
- mag geen tweede handmatige aftrek nodig zijn;
- moeten persoonslijsten buiten de openbare repository blijven.

## Lokalen

Een room_id is een echte resource. Externe locaties en locaties met meerdere parallelle ruimtes moeten daarom afzonderlijke rooms of expliciete gedeelde capaciteit krijgen.

Een tekst als "PRO", "VMBO" of een adres mag niet automatisch als één exclusieve ruimte worden geïnterpreteerd.

## Hele dag

Een hele-dagactiviteit moet als zodanig gemodelleerd worden en alle betrokken slots blokkeren. De precieze representatie wordt vastgesteld op basis van de feitelijke Magister-werkwijze.

## Magister-routes

Er zijn minstens twee operationeel verschillende Magister-routes:

- **Keuzewerktijd** voor de reguliere vrije workshopinschrijving;
- **Activiteiten** voor bepaalde speciale voorinschrijvingen, bijvoorbeeld een betaalde ski-dag.

De centrale hub moet deze routes expliciet onderscheiden. Een speciale activiteit die vooraf een leerling bezet, moet de benodigde vrije-keuzecapaciteit van het betreffende slot reduceren.

Voor betaalde activiteiten moeten deelname en betaalstatus niet als hetzelfde gegeven worden behandeld.

## Publicatie

De inhoudelijke publicatie-/inschrijfroutes die nu bevestigd zijn, zijn website en Magister.

Zermelo maakt geen deel uit van de inhoudelijke Pantarijnweekdatastroom. Wel blijft als externe randvoorwaarde gelden dat het reguliere rooster voor de betreffende week correct moet zijn leeggezet.

## Nog te bevestigen met Susanne en organisatie

- exacte betekenis van 0 en 1 in beide beschikbaarheidsbladen;
- bron van personeelsbeschikbaarheid;
- welke planningsregels hard zijn en welke voorkeur;
- bron van leerlingaantallen per doelgroep en slot;
- maximale en minimale groepsgrootte en formele uitzonderingsregel;
- gewenste overcapaciteitsmarge;
- gewenste reserve-/noodcapaciteit;
- prioriteit bij lokaalconflicten;
- regel voor begeleiding bij externe activiteiten;
- welke locaties/onderwijsvormen in 2026 deelnemen en op welke dagdelen;
- exacte voorinschrijftijden en quota voor andere locaties;
- technische route voor VMBO-voorinschrijving;
- technische route voor PrO-handplaatsing;
- actuele status van ISK-deelname;
- objectieve criteria voor doelgroepgeschiktheid;
- technische route Forms -> Excel/centrale hub;
- exacte betaal-/deelnamestatus bij speciale activiteiten;
- technische import-/exportmogelijkheden van Magister.
