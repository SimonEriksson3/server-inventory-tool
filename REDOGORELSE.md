# Redogörelse

## 1. Tre konstruktioner:

### get_multiple_choices(min, max, prompt)
Finns i `menu.py`. Funktionen tar emot tre argument: ett minsta värde (`min`), högsta värde (`max`) och en prompt (`prompt`). Det som returneras är en lista av heltal.
Användaren kan välja mellan att ange ett eller flera värden samtidigt, genom att separera värdena med kommatecken.
Allting körs i en loop för att kunna iterera tills vi lyckas få tillbaka korrekta val. I loopen anropas `input` och inmatningen tar bort mellanslag på båda sidor, sedan delas inmatningen upp med `split` 
med ett kommatecken som delimiter. Varje del vi får tillbaka av `split` försöker vi omvandla till heltal samt kontrollera om siffran är inom intervallet `min` och `max`. 
Om vi lyckas och det stämmer så läggs siffran till i en lista av heltal sålänge talet inte redan finns i listan. Till slut returneras hela listan och används för att kunna påverka flera servrar samtidigt.
Om användaren anger annat än siffror eller ingenting alls så skrivs ett felmeddelande ut och användaren får försöka igen i nästa iteration. Dock om användaren blandar siffror, ogiltiga tecken och 
ogiltiga val så kommer endast siffror som är giltiga val att läggas till i listan och returneras. Funktionen används för att kunna välja en eller flera servrar samtidigt.

### match/case-sats
I `run()` funktionen i `menu.py` använder jag en match/case-sats för menyvalen och detta är varför Python v3.10 är ett krav.
match/case-satser är samma som Javas switch-cases. Jag brukar använda switch-cases (eller match-cases för Python) för menyval och liknande då det är lättläst och logiskt.
Satsen utgår från heltalet `choice` som vi får tillbaka när vi anropar `get_user_choice`, och varje case representerar ett av menyvalen. T.ex har vi case 1 som listar alla servrar, eller case 4 som tar bort
en server. Istället för att skriva många if/else-villkor så kan vi låta match/case direkt hoppa till rätt val. Om vi saknar ett case för heltalet `choice` så kan man använda case _ för att ange ett
standardvärde. Eftersom jag redan innan validerar `choice` i `get_user_choice` så har jag redan säkerställt att `choice` ligger inom rätt intervall (menyvalen 1-7). 

### for-loop i list_servers()
I `cli.py` har jag en funktion som skriver ut alla servrar, men den beter sig på olika sätt beroende på om användaren har valt att filtrera efter miljö eller inte.
Om den globala variabeln `environment_filter` inte pekar på ett värde (`None`) så skriver vi ut alla servrar som vanligt.
Om den däremot innehåller ett värde så kör vi istället en for-loop som itererar genom alla servrar i listan. För varje iteration så representerar variabeln `server` en enskild dictionary från serverlistan.
Inuti loopen så kollar vi på värdet av `miljo` och om värdet matchar `environment_filter` så skriver vi ut servern. Om den inte matchar så fortsätter vi till nästa iteration, eller avslutar om loopen 
är färdig.

## 2. Varför lista med dictionaries?
En enskild server har ett antal värden vi behöver lagra, en dictionary passar bra eftersom den kan lagra information i par (en nyckel och ett värde). Då kan vi inte bara lagra värdet men också vad värdet
i sig representerar, t.ex kan nyckeln "adress" ha värdet 127.0.0.1. När vi då har en färdig dictionary så behöver vi lagra den i en lista för att kunna hantera flera servrar. Då har vi en lista av dictionaries.
Värdena inuti en server i vårt fall består av strängar för namn, adress, miljö, roll, status och datum för senaste kontroll.
I `add_server()` i `storage.py` så ser vi att en dictionary skapas med värdena från parametrarna. Sedan appendar vi serverlistan med den färdiga dictionaryn.

## 3. Varför sparar du data i JSON men exporterar rapporten som CSV?
CSV är väldigt bra för tabeller och lagras genom att separera värden med kommatecken. Varje värde mellan dessa kommatecken blir då sin egen kolumn om man skulle importera datan till t.ex Microsoft Excel.
Om vi ska exportera våra rapporter så är CSV-formatet perfekt att använda för att kunna bearbeta vidare datan i en spreadsheet programvara.
JSON är lättläst för en människa och datan är strukturerad. Det är alltså enkelt för en människa att t.ex läsa och ändra konfigurationen direkt i filen. Datan i vår config.json och servrar.json är
strukturerad på samma sätt som listor och dictionaries i Python, och python har också färdiga bibliotek som låter oss spara och läsa in data enkelt utan att ändra strukturen.
Exempel på detta ser vi `load_servers()`, `save_servers()` och `export_report()`, samtliga i `storage.py`.

## 4. Hur är programmet uppdelat i moduler och funktioner? Vilket ansvar har varje fil?
Programmet är uppdelat i moduler och funktioner för att separera ansvaret så mycket som möjligt rent logiskt men också för att göra det lättläst, återanvändbart och enkelt att förändra och felsöka.
Vi har `menu` som hanterar menyn & menyval, `cli` som hanterar programmet i CLI-läge, `checker` 
som kontrollerar servrar, `storage` som jobbar med filhantering och serverlistan, `config` som hanterar konfigurationen och till slut `main` som är startpunkten och binder ihop allting genom att anropa 
antingen `menu` eller `cli` beroende på hur programmet ska köras. I en enskild modul så delar vi upp ansvaret till små funktioner som ska göra en liten del utav huvudansvaret.
Ett konkret exempel på hur jag delar upp ansvarsområden i koden är i t.ex `list_all_servers()` i `menu.py`. Funktionen anropas när användaren väljer "1. Lista alla servrar" i huvudmenyn. `menu.py` ska endast
hantera huvudmenyn och menyvalen så i funktionen hämtar vi istället serverlistan tillfälligt med `storage.get_servers()` för att kunna skriva ut information om servrarna.

## 5. Vilka moduler från standardbiblioteket använder du och till vad?
Programmet använder följande moduler:
- sys - används för att kontrollera vilket operativsystem som används (hämtar operativsystemet med `sys.platform` i `checker`), för att avsluta med exit-koder (`sys.exit()` i `cli`) samt för att kontrollera 
om användaren angav argument eller inte (`sys.argv` i `main`). 
- subprocess - används i `checker` för att starta `ping`-processen med `subprocess.run()`.
- argparse - används i `cli` för att tolka argument som skickas med i terminalen. Ett ArgumentParser-objekt skapas där vi lägger till argument med `add_argument`-funktionen.
- json - när vi hämtar och lagrar i JSON-filer (`json.load` och `json.dump` i `storage` samt `config`). Modulen importeras också i `menu` för att undantaget `JSONDecodeError` fångas och ger felmeddelande 
där när vi inte lyckas läsa serverlistans JSON-fil.
- os - modulen behövs för att kunna hämta miljövariabeln `INVENTORY_DATAFIL`, vilket vi gör i `config` med `os.environ.get()`.
- pathlib - vi använder funktionen Path från pathlib i `config` när vi ber om filsökvägen till konfigurationsfilen, serverlistan samt mappen där vi lagrar rapporter. 
- csv - används i `export_report()` i `storage` för att exportera CSV-rapporter. Då skapar vi ett DictWriter-objekt och anropar funktionerna `writeheader` för att skriva ut fältnamnen och `writerows` för 
att skriva ut varje rad till CSV-filen.
- datetime - används för att hämta tidsstämpel med hjälp av `datetime.now()` i `storage`. Vi använder också `strftime` för att kontrollera formateringen och lagra som en sträng.

## 6. Ge tre exempel på god praxis från din kod och förklara varför de är bra.
### Ansvarsfördelning (Separation of concerns)
I min kod är ansvaret tydligt uppdelat. Exempelvis hanterar `storage` endast läsning/hämtning och lagring av data och gör inga utskrifter i terminalen. Utskrift sker istället i `menu` eller `cli`. 
Detta är bra praxis eftersom det gör koden återanvändbar. Ett konkret exempel: jag började med att skriva huvudmenyn och när jag senare skulle skriva CLI-läget kunde jag fokusera helt på det nya gränssnittet.
Jag behövde inte skriva om kod för datahantering eller serverkontroller eftersom jag direkt kunde anropa funktionerna i `storage` och `checker`. Funktionerna fungerar precis likadant oavsett hur programmet startas.
### Hjälpfunktioner för input validering
Vi kan inte lita blint på att användaren anger ett giltigt värde. Genom att validera inmatning säkerställer vi att vi får tillbaka ett giltigt värde som vi vet att vi kan arbeta vidare med. Så genom att 
styra vad användaren matar programmet med ser vi till att vi kan fortsätta utan problem och förhindra att programmet kraschar. Att använda en hjälpfunktion för att validera inmatningen innebär att vi får kod 
som är mer läsbar, enkel att underhålla och ändra samt att det går fortare om vi slipper skriva om samma kod flera gånger. 
Exempel på detta i min kod är `get_user_choice()`, `get_multiple_choices()`, `get_user_input()`, `get_environment()` och `get_confirmation()`  i `menu.py`.
### Konfigurationsfil 
Istället för att hårdkoda filsökvägar direkt i koden så använder jag en konfigurationsfil (`config.json`) som hanteras via `config.py`. Det är bra praxis eftersom det gör programmet flexibelt. Man kan ändra
var programmet läser serverlistan ifrån och var programmet ska lagra rapporterna, utan att behöva bygga om programmet. Man behöver alltså inte flera olika versioner av programmet för flera olika användare 
eller servrar. Det räcker att ändra konfigurationsfilen. 

## 7. Vilka källor och hjälpmedel har du använt och till vad?
Jag har arbetat med följade hjälpmedel till:
- Presentationerna från lektionerna: syntax för nya koncept och för att repetera koncepten.
- Google och dokumentation: för att kolla upp hur moduler och funktioner fungerar (delvis via Google och delvis via den inbyggda dokumentationen i PyCharm, Pythons docstrings) samt för att felsöka felmeddelanden.
- Gemini: för ledtrådar och förklaringar när jag kört fast eller glömt syntax, för att kolla om jag missat att kommentera något viktigt, att jag förstått och uppfyller kraven från uppgiften samt hjälp att formulera
min utskrift. Jag använde Gemini för att bolla idéer och jag gav instruktion om att inte generera någon färdig kod (vilket den ofta behövde påminnas om men jag skrev all kod själv).