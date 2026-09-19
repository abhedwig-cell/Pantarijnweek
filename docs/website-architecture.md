# Website-architectuur

## Doel

De Pantarijnweek-website wordt geen tweede administratie. Hij wordt opnieuw gegenereerd uit de centrale hub.

## Gereconstrueerde structuur

De publieke 2025-site gebruikt:
- doelgroep-pagina's voor MHV, VMBO en PrO;
- afzonderlijke pagina's voor de acht dagdelen;
- een vrijdagpagina;
- Mijn Pantarijnweek;
- Impressie;
- Informatie & contact;
- informatieblokken zoals verplicht, buiten school, voorinschrijving en hele dag.

Versie 2 behoudt die herkenbare informatiearchitectuur, maar bouwt de inhoud volledig uit gestructureerde hubdata.

## Versie 2

De tweede prototypeversie voegt toe:
- mobile-first navigatie;
- compactere workshopkaarten;
- categorie- en doelgroepfilters;
- zoeken;
- detailvensters zonder de overzichtspagina vol tekst te zetten;
- een lokale shortlist "Mijn Pantarijnweek";
- visuele categorieën;
- nieuws- en waarschuwingselementen;
- aparte pagina's voor vrijdag en impressie.

De shortlist gebruikt alleen browser-localStorage. Er wordt geen leerlingidentiteit naar GitHub of de publieke site gestuurd en het is nadrukkelijk geen inschrijving.

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

## Belangrijkste regel

Een wijziging aan een activiteit wordt in de hub uitgevoerd. De website wordt daarna opnieuw gegenereerd. Er wordt niet ook nog handmatig een tweede kopie van dezelfde activiteit aangepast.

## Publiceerbaarheid

De productie-generator neemt alleen offerings op met een toegestane publicatiestatus. In een volgende datamodelstap wordt dit rechtstreeks gekoppeld aan PublicationState en OfferingAudience.

Concepten, interne notities, personeelsinformatie en leerlinginformatie worden niet gepubliceerd.

## Beeldmateriaal

Versie 2 gebruikt eigen CSS-vormen en pictogrammen. Historische foto's en grafische bestanden worden pas opgenomen wanneer de organisatie de originele bestanden en gebruiksrechten beschikbaar heeft.

## Magister

De website is volledig automatisch genereerbaar. Magister blijft voorlopig een semi-automatische uitvoerroute. Beide komen wel uit dezelfde centrale bron, waardoor titel, doelgroep en capaciteit niet opnieuw bedacht hoeven te worden.
