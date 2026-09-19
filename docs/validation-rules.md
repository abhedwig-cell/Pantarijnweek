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

Per slot moet de benodigde vrije-keuzecapaciteit worden berekend vanuit cohortgroottes en vaste activiteiten. De aantallen worden niet hardcoded in kolomkoppen.

Minimaal wordt apart gecontroleerd:
- OB-vraag en OB-capaciteit
- BB-vraag en BB-capaciteit
- doelgroepbeperkingen
- verplichte plaatsingen
- voorinschrijving

De gewenste veiligheidsmarge voor overcapaciteit is nog door de organisatie te bepalen.

## Lokalen

Een room_id is een echte resource. Externe locaties en locaties met meerdere parallelle ruimtes moeten daarom afzonderlijke rooms of expliciete gedeelde capaciteit krijgen.

Een tekst als "PRO", "VMBO" of een adres mag niet automatisch als één exclusieve ruimte worden geïnterpreteerd.

## Hele dag

Een hele-dagactiviteit moet als zodanig gemodelleerd worden en beide betrokken slots blokkeren. De precieze representatie wordt vastgesteld na bespreking van de huidige Magister/Zermelo-werkwijze.

## Publicatie

Website, Magister en Zermelo krijgen elk een eigen statusrecord. De kernplanning verandert niet doordat iets tijdelijk uit één kanaal wordt gehaald.

## Nog te bevestigen met Susanne en organisatie

- exacte betekenis van 0 en 1 in beide beschikbaarheidsbladen
- bron van personeelsbeschikbaarheid
- welke planningsregels hard zijn en welke voorkeur
- manier waarop hele-dagactiviteiten in Magister en Zermelo worden ingevoerd
- maximale en minimale groepsgrootte
- prioriteit bij lokaalconflicten
- regel voor begeleiding bij externe activiteiten
- wijze waarop deelname van vmbo, PrO, ISK en andere locaties per dag wordt verwerkt
- gewenste reservecapaciteit per doelgroep en slot
