# Website-architectuur

## Doel

De Pantarijnweek-website wordt geen tweede administratie. Hij wordt opnieuw gegenereerd uit de centrale hub.

## Kernprincipe

Een wijziging aan een activiteit wordt in de hub uitgevoerd. De website wordt daarna opnieuw gegenereerd. Er wordt niet ook nog handmatig een tweede kopie van dezelfde activiteit aangepast.

## Versie 3

Versie 3 is een bewuste vereenvoudiging na evaluatie van versie 2.

De hoofdnavigatie bevat nog maar:
- Home;
- Programma;
- Doelgroepen;
- Mijn week;
- Informatie.

De acht dagdelen blijven bestaan, maar hangen onder Programma in plaats van allemaal tegelijk in de hoofdnavigatie te staan.

Workshopkaarten tonen op het overzicht alleen:
- beeld/pictogram;
- doelgroep;
- titel;
- één korte zin;
- alleen bij uitzondering een belangrijk label zoals verplicht of buiten school.

Locatie, volledige omschrijving en overige bijzonderheden staan pas in het detailvenster.

Zoeken blijft beschikbaar. Doelgroepfiltering is teruggebracht tot Alles / OB / BB. Categorieknoppen zijn uit de standaardinterface verwijderd om visuele drukte te voorkomen.

## Mijn week

Een leerling kan interessante workshops lokaal bewaren in de browser. Dit is:
- geen inschrijving;
- niet gekoppeld aan een leerlingaccount;
- niet opgeslagen in GitHub;
- alleen bedoeld als persoonlijke voorbereiding.

## Publicatiestroom

```
Activity + Offering + doelgroepregels + publicatiestatus
                         |
                         v
                   website build
                         |
        +----------------+----------------+
        |                |                |
  dagdeelpagina's   doelgroep-pagina's   overige publieke pagina's
```

## Publiceerbaarheid

De productie-generator neemt alleen offerings op met een toegestane publicatiestatus. Concepten, interne notities, personeelsinformatie en leerlinginformatie worden niet gepubliceerd.

In een volgende datamodelstap wordt publiceerbaarheid rechtstreeks gekoppeld aan PublicationState en OfferingAudience.

## Beeldmateriaal

De prototypes gebruiken eigen CSS-vormen en pictogrammen. Historische foto's en grafische bestanden worden pas opgenomen wanneer de organisatie de originele bestanden en gebruiksrechten beschikbaar heeft.

## Magister

De website is volledig automatisch genereerbaar. Magister blijft voorlopig een semi-automatische uitvoerroute. Beide komen uit dezelfde centrale bron, waardoor titel, doelgroep en capaciteit niet opnieuw bedacht hoeven te worden.
