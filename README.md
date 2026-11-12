# Server Inventory Tool

## Om verktyget
Server Inventory Tool hjälper systemadministratörer och utvecklare att hantera & övervaka sina servrar. Det är ett textbaserat verktyg skrivet i Python och körs direkt i terminalen.
Programmet kan användas för att: 
- lista alla servrar 
- lägga till servrar 
- ta bort servrar 
- kontrollera servrar 
- exportera rapporter till CSV-filer för vidare datahantering.

## Struktur
Funktionaliteten delas upp i moduler och varje modul har sitt eget ansvar.

```text
server-inventory-tool/
│
├── main.py            ← Startpunkten (meny/CLI)
├── cli.py             ← Hanterar argument (CLI)
├── menu.py            ← Textmeny och validering av inmatning.
├── storage.py         ← JSON-lagring, CSV-export och hantering av serverlistan
├── checker.py         ← Statuskontroll av servrar via ping
├── config.py          ← Konfigurationshantering
├── config.json        ← Konfigurationsfil för sökvägar
└── servrar.json       ← Lagrad serverdata    
```

## Krav
För att köra programmet behöver du: 

- Python v3.10 eller senare. Anledningen är att koden innehåller match satser som introducerades i Python 3.10.
- Tillgång till `ping` för att kunna kontrollera serverstatus.

## Användning

Verktyget kan användas på två sätt: i ett textbaserat användargränssnitt eller i CLI-läge.
<br>

### Starta med textbaserat användargränssnitt:
Kör utan argument.
```bash
python main.py
```
### Använda CLI:
Kör med argument. T.ex:
```bash
python main.py --miljo prod --kontrollera-alla
```
<br>

### Tillgängliga CLI-argument:
Genom att skicka med argument så kan åtgärder utföras direkt i terminalen.
| Kommando | Beskrivning |
| :--- | :---- |
| `--help` | Skriver ut meddelande med alla tillgängliga flaggor och vad de gör.|
| `--lista` | Listar alla servrar.|
| `--miljo [miljö]` | Filtrerar baserat på miljö. Fungerar ihop med `--lista`, `--kontrollera-alla` samt `--export`. Giltiga miljöer är `dev`, `test` och `prod`.|
| `--server [namn]` | Visar en specifik server.|
| `--kontrollera [namn]` | Kontrollerar om en specifik server svarar på `ping` och uppdaterar serverns status. Detta kräver att `ping` är tillgängligt. |
| `--kontrollera-alla` | Kontrollerar samtliga servrar (eller filtrerade servrar) en i taget.|
| `--export` | Exporterar en rapport i CSV-format.|

### Exit-koder
När programmet avslutas från CLI-läge returneras ett av följande exit koder:
| Kod | Betydelse |
| :--- | :--- |
| 0 | Programmet avslutades utan fel.
| 1 | Minst 1 server kunde inte nås eller kunde inte hittas.
| 2 | Lyckades inte skriva eller läsa till fil.

## Konfiguration
Programmet lagrar servrar i en JSON-fil. Vilken fil som används bestäms i följande ordning:
1. **Miljövariabel:** Om miljövariabeln `INVENTORY_DATAFIL` är satt så används den som sökväg.
2. **Konfigurationsfil:** Annars läses sökvägen från konfigurationsfilen `config.json`.
3. **Standardvärde:** Om konfigurationsfilen inte finns eller inte kan läsas så startar programmet med `servrar.json` som standardvärde.

## Fördjupningar
Fördjupningar som finns implementerade i programmet:
1. **Konfigurationsfil**: Programmet hämtar sin konfiguration från `config.json` där man kan ange sökväg till `servrar.json` samt sökväg till var rapporter ska lagras.
2. **Säkrare inmatning:** I textmenyn valideras all inmatning i en loop för att säkerställa att korrekt inmatning ges så att programmet kan fortsätta utan att krasha.