# Reflektion

## 1. Designval

### Val 1: Att spara efter varje ändring istället för bara när programmet avslutas. 

Jag valde att spara efter varje ändring som görs i programmet. I `storage.py` har jag funktionen `save_servers()` som anropas efter att vi kontrollerar servrar, lägger till en ny eller tar bort en server. Funktionen skriver över hela serverlistan (JSON-filen) med ny data. Det har som konsekvens bland annat att man inte kan ångra några ändringar, förändringen blir permanent direkt om man inte har backup. 
Alternativet hade varit att spara endast en gång när programmet avslutas, eller låta användaren själv välja när vi ska spara genom ett nytt menyval. Att spara efter varje ändring förbrukar mer systemresurser vilket kan vara ett problem om vi har enorma mängder servrar att skriva över, men det är samtidigt mer säkert än att endast spara vid avslut. Om man gör många ändringar till serverlistan så kan allting gå förlorat om programmet kraschar innan vi hinner spara. 
Om förutsättningarna ändrades så hade jag istället valt en lättviktig SQL-databas (som SQLite) som 
kan hantera en större mängd servrar, samt så att man även kan spara utan att behöva skriva över all existerande data.	

### Val 2: Att konfigurera datafilen med en miljövariabel istället för att skriva filnamnet i koden. 

I programmet blir en satt miljövariabel prioriterad högst, om den är satt är det alltså den sökvägen till datafilen vi använder. Vi kan se i `config.py` att vår konfiguration hämtas först från `config.json`-filen (`get_config()`) och till sist kontrollerar vi om en miljövariabel är satt eller inte, isåfall används miljövariabeln (sista raden i `config.py`) för datafilen. 
Att använda en miljövariabel är smidigt då vi slipper ändra i koden, slipper hålla reda på flera versioner av programmet, och vi kan snabbt och enkelt ändra miljövariabeln när vi behöver det. 
Alternativen hade varit att hårdkoda sökvägen, ange sökvägen som argument eller helt förlita oss på konfigurationsfilen. Att hårdkoda sökvägen gör det omständigt att ändra i koden för varje unik sökväg/server vi behöver och samtidigt hålla koll på vilken version som ska användas när vi har flera olika servrar. Att skicka med det som argument lägger till ett extra steg som behöver utföras varje gång programmet startas. Att endast använda sig av konfigurationsfilen gör automatisering mer omständigt eftersom man tvingas bygga om konfigurationsfilen direkt i skriptet, om vi använder miljövariabel så kan skriptet enkelt ändra den med endast 1 rad. 
En nackdel med att använda miljövariabel kan vara att det kanske inte är lika tydligt om en miljövariabel är satt eller inte, vi kan ju se att konfigurationsfilen har ett fält för sökvägen till datafilen som vi kan ändra, men om miljövariabeln är satt så är det den som används först. Vi kan ha glömt att vi satt miljövariabeln eller så är det en oerfaren användare som inte har koll på att miljövariabeln prioriteras, så arbetar personen med helt fel fil utan att kanske veta om det. Att använda miljövariabler för våra konfigurationer är inte heller lika smidigt längre om vi bygger ut programmet så att det helt plötsligt behöver 20 olika konfigurationer, då passar en konfigurationsfil mycket bättre. Man hade också kunnat ha en databas för att lagra inställningarna istället.

### Val 3: Hur programmet är uppdelat i moduler och funktioner och hur det påverkar möjligheten att bygga vidare på det.

Jag delade upp programmet i flera moduler där varje modul har sitt eget ansvar; exempelvis `main` som startar flödet, `checker` som kontrollerar servrar, `config` hanterar konfiguration, och `cli` som hanterar CLI-läget. I varje modul delar vi upp ansvaret till flera funktioner, till exempel har `storage` sin `load_servers()`, `save_servers()`, `add_server()` och `update_status()`.
Alternativet hade varit att ha hela kodbasen i en enda stor fil. Jag delar gärna upp i flera moduler eftersom koden blir mycket tydligare, enklare att läsa och se vad som händer. En naturlig effekt av det blir ju också att det är mycket enklare att ändra och bygga vidare på. Om vi istället hade haft koden i en enda stor fil så hade det varit betydligt svårare att se var vi behöver leta för att ändra något eller bygga vidare. Eftersom varje modul har sitt eget ansvar så blir det logiskt var vi bör börja kolla. 
En negativ konsekvens av att dela upp programmet i moduler kan ju vara att vi behöver hoppa mellan flera filer istället för att endast jobba med en enskild fil, flödet kan vara svårare att gå igenom. Men det beror nog på. Är det ett litet program så kan det vara bättre att skriva koden rakt upp och ner, då ser vi också flödet enkelt. Men ju större programmet blir desto svårare blir det att följa flödet, om vi då börjar dela upp det så går vi tillbaka till att flödet blir enklare att läsa. 
Jag hade valt att skriva allt i en enda fil om programmet hade haft en enda simpel uppgift.

### Val 4: Att använda sig av loopar i meny och validering.

Jag har många loopar i min `menu`-modul, exempelvis används en loop för huvudmenyn (`menu.run()`) och i hjälpmetoderna för inmatningsvalidering (`menu.get_user_input()` med mera). 
Valideringen stoppar tomma fält, ogiltiga val och ogiltiga tecken (t.ex bokstäver där vi förväntar oss endast siffror).
Alternativet hade kunnat vara att bara avbryta och skicka tillbaka användaren till menyn om inmatningen blir fel. Jag föredrar lösningen att loopa tills att inmatningen blir korrekt eftersom vi ska slippa börja om från början om vi råkat göra ett litet fel. 
En konsekvens (i min nuvarande kod) är att om användaren ångrar sig så finns det ingen lösning för att avbryta. Man kan bygga ut programmet för att tillåta ett alternativ för att avbryta (ange 0 för att avbryta t.ex) vilket jag tycker överväger alternativet. Om vi istället använder ett grafiskt användargränssnitt så hade vi inte behövt en loop eftersom vi kan tvinga korrekt inmatning på andra sätt.

## 2. Om verktyget skulle användas i en större miljö

Det finns ett par saker att ha i åtanke när det gäller skalning av programmet. 

Just nu lagras serverlistan i en JSON-fil (`storage.py`). När vi sparar ändringar så skriver vi över hela filen (`storage.save_servers()`), så även om vi endast gör en liten ändring så skriver vi ändå över all data i filen. Detta fungerar just nu för våra 4 servrar, men om vi har 10000 servrar så hade det varit bättre med en SQL-databas så att vi både kan göra små ändringar utan att skriva över allting men även hämta servrar snabbare och mer optimerat. Om vi skriver enorma mängder data till en JSON-fil så riskerar vi också att något kraschar eller 
går fel innan vi hunnit skriva över allt.
När vi kontrollerar en server så skickar vi en `ping` till adressen och väntar på svar (`checker.ping_server()`). När vi kontrollerar flera eller samtliga servrar så utförs kontrollerna en efter en (`check_server()` i `menu`). Samma här, det fungerar bra just nu och tar knappt 10 sekunder för våra 4 servrar. Men med tusentals servrar så hade det tagit betydligt längre tid eftersom `ping` väntar på antingen svar eller timeout (10 sekunder i detta fallet). Då hade vi istället kunnat köra flera kontroller samtidigt på flera trådar parallellt.
En annan sak som hade varit bra när man tänker på stora mängder servrar är hur vi presenterar alla (`list_all_servers()` i `menu` eller t.ex `list_servers()` i `cli`). Har vi 10 servrar är 
det inte ett problem. Om vi har 10000 servrar så blir det otroligt mycket text och svårt att läsa. Man hade då kunnat dela upp listan i flera sidor så att man kan bläddra mellan dem.
Om vi istället för många servrar har många användare (flera administratörer som hanterar programmet samtidigt) eller en användare och en pipeline samtidigt, så hade vi med en JSON-fil riskerat att skriva över användares ändringar. Här hade en SQL-databas också varit ett bättre alternativ, den kan hantera ändringar som sker samtidigt åt oss.
