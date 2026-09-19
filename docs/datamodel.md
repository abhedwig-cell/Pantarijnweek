# Datamodel centrale Pantarijnweek-hub

## Kernidee

De centrale fout in de huidige administratie is dat één rij tegelijk activiteit, rooster, ruimte, personele inzet en publicatiestatus probeert te zijn. Het nieuwe model splitst deze concepten.

Het belangrijkste onderscheid is:

**Activity** = wat de activiteit is.

**Offering** = wanneer en voor wie die activiteit in een concreet dagdeel wordt aangeboden.

Een activiteit kan dus meerdere offerings hebben.

## Entiteiten

### Edition

Een editie van de Pantarijnweek.

Velden:
- edition_id
- school_year
- status
- notes

### TimeSlot

Eén planbaar dagdeel.

Velden:
- slot_id
- day
- part
- sequence
- start_time
- end_time

Datums en tijden worden pas ingevuld nadat de organisatie die voor 2026 heeft bevestigd.

### Cohort

Een groep leerlingen waarvoor planning en capaciteit worden berekend.

Velden:
- cohort_id
- year
- track
- location
- build
- student_count

Voorbeelden van build zijn OB en BB. Track en locatie blijven afzonderlijke dimensies.

### Activity

De canonieke beschrijving van een workshop of activiteit.

Velden:
- activity_id
- title
- description
- categories
- default_audience
- delivery_type
- external
- requirements
- status

De beschrijving staat hier precies één keer.

### Offering

Een concrete uitvoering van een Activity in een TimeSlot.

Velden:
- offering_id
- activity_id
- slot_id
- audience
- capacity_ob
- capacity_bb
- choice_mode
- mandatory_target
- location_id
- room_id
- budget_eur
- status
- notes

Choice mode krijgt een gecontroleerde waarde, bijvoorbeeld:
- choice
- mandatory
- preregistration
- fixed

Voor een mandatory offering is mandatory_target verplicht.

### Location

Een schoollocatie of externe locatie.

Velden:
- location_id
- name
- kind
- address_or_meeting_point
- external
- notes

### Room

Een concrete ruimte binnen een Location.

Velden:
- room_id
- location_id
- name
- type
- capacity
- exclusive
- notes

Een sportcomplex met meerdere zalen wordt dus niet als één vrij tekstveld behandeld.

### PersonRef

In de openbare repository worden alleen niet-herleidbare identifiers gebruikt.

Velden:
- person_id
- role_type
- active

Een eventuele koppeling van person_id naar echte naam, e-mail of telefoon hoort niet in deze openbare repository.

### StaffAvailability

Beschikbaarheid van een persoon, onafhankelijk van de uiteindelijke taak.

Velden:
- person_id
- slot_id
- availability
- note

Availability krijgt een enum:
- available
- unavailable
- constrained
- unknown

### Assignment

Een concrete personele taak.

Velden:
- assignment_id
- person_id
- offering_id
- slot_id
- role
- status

Hierdoor wordt beschikbaarheid nooit overschreven door de planning.

### FixedActivity

Een leerjaar-, vak- of groepsgebonden activiteit die de vrije keuze beïnvloedt.

Velden:
- fixed_activity_id
- title
- slot_id
- cohort_id
- participation_mode
- student_count
- location_id
- room_id
- status
- notes

Participation mode:
- mandatory
- preregistration
- optional
- unknown

### PublicationState

Status van één offering in een extern kanaal.

Velden:
- offering_id
- channel
- status
- note

Channel:
- website
- magister
- zermelo

Status:
- not_ready
- ready
- published
- removed
- blocked

Hiermee verdwijnen vrije opmerkingen als x?, is eruit en verpl.n.di uit het kernrooster.

### BudgetItem

Een bedrag wordt als eigen record beheerd.

Velden:
- budget_item_id
- offering_id
- amount_eur
- status
- note

Dag- en weektotalen worden berekend en nooit handmatig nogmaals ingevoerd.

## Relaties

```
Activity 1 --- n Offering n --- 1 TimeSlot
                     |
                     +--- 0..1 Room --- 1 Location
                     |
                     +--- n Assignment n --- 1 PersonRef
                     |
                     +--- n PublicationState
                     |
                     +--- n BudgetItem

Cohort 1 --- n FixedActivity n --- 1 TimeSlot
PersonRef 1 --- n StaffAvailability n --- 1 TimeSlot
```

## Stamgegevens versus planning

Stamgegevens:
- Activity
- Location
- Room
- PersonRef
- Cohort

Jaar- en roostergebonden gegevens:
- TimeSlot
- Offering
- FixedActivity
- StaffAvailability
- Assignment
- PublicationState
- BudgetItem

Dit onderscheid maakt hergebruik in volgende edities mogelijk zonder een oud rooster te kopiëren en vervolgens cel voor cel te veranderen.
