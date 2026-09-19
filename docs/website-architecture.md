# Website-architectuur

## Doel

De Pantarijnweek-website wordt geen tweede administratie. Hij wordt opnieuw gegenereerd uit de centrale hub.

## Gereconstrueerde structuur

De publieke 2025-site heeft een vaste navigatie met doelgroep-pagina's en afzonderlijke pagina's voor de acht dagdelen. Workshopitems herhalen dezelfde basisstructuur: titel, doelgroep, beschrijving en aanvullende informatieblokken.

De prototype-generator behoudt dat herkenbare model, maar haalt de inhoud uit gestructureerde data.

## Publicatiestroom

```
Activity + Offering + doelgroepregels + publicatiestatus
                         |
                         v
                   website build
                         |
              +----------+----------+
              |                     |
        dagdeelpagina's        doelgroeppagina's
```

## Belangrijkste regel

Een wijziging aan een activiteit wordt in de hub uitgevoerd. De website wordt daarna opnieuw gegenereerd. Er wordt niet ook nog handmatig een tweede kopie van dezelfde activiteit aangepast.

## Beeldmateriaal

De eerste prototypeversie gebruikt eigen CSS-vormen en pictogrammen. Historische foto's en grafische bestanden worden pas opgenomen wanneer de organisatie de originele bestanden en gebruiksrechten beschikbaar heeft.

## Veiligheid

De publieke website bevat geen leerlingnamen, personeelsroosters of andere herleidbare interne gegevens.
