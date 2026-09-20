# Regiedashboard prototype

Dit dashboard is een afgeleide view op de centrale Pantarijnweek-hub.

## Belangrijkste regels

- Geen dashboardkleur is handmatig authority.
- De backend levert HealthSignals met een expliciete regel en bronverwijzing.
- Het dashboard presenteert die signalen alleen.
- `unknown` is een geldige en belangrijke status.
- Kritieke signalen worden bovenaan gezet.
- Een wijziging in de bron moet via herberekening zichtbaar worden.

## Demo

De demo gebruikt `dashboard/demo_scenario.json` als **inputfeiten**. De ernst van signalen staat daar niet in.

Build:

```bash
python scripts/build_dashboard_demo_signals.py --output /tmp/dashboard_demo_signals.json
python scripts/build_dashboard.py --input /tmp/dashboard_demo_signals.json --output dashboard/public
```

In het demonstratiescenario verlaagt één wijziging de capaciteit op maandag ochtend OB met 20 plaatsen. De signaalbuilder berekent vervolgens zelf:
- vraag 412;
- aanbod vóór wijziging 423;
- aanbod na wijziging 403;
- marge vóór +11;
- marge na -9;
- status critical, omdat de marge negatief is.

## Productie

Voor productie moet `scripts/build_dashboard.py` gevoed worden met de signalen uit `scripts/build_dashboard_signals.py`. De huidige 2026-brondata is nog niet volledig genoeg voor een zinvol operationeel dashboard.

Het dashboard mag nooit ontbrekende broninformatie als groen interpreteren.
