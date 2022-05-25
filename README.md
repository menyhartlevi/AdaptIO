# AdaptIO

Az alábbi fájlban az "Adaptív rendszerek modellezése" tárgy AdaptIO játékához készített agent kerül bemutatásra.

## A játékos stratégiája

Az agentnek a játék során folyamatosan 81 mezőből áll a látótere, az alábbi formában:
<img src="https://user-images.githubusercontent.com/82844655/170237011-0b819a23-5354-4739-9eec-ff33574b53d3.png" width="200" height="200">


És a lépései pedig az alábbiak lehetnek:

![Képernyőkép 2022-05-25 120252](https://user-images.githubusercontent.com/82844655/170237092-7003ad16-b784-45d1-99b3-1a125090f011.png)


Az X és Y irányú lépéseket külön vizsgáltuk. Minden döntéshozatalnál beleszámoltuk az összes látóteren belüli mező értékét a döntésbe. Attól függően, hogy az adott mezőn fal, étel, vagy másik játékos található, különbözően adtuk hozzá az értékét az összesített X-hez, illetve Y-hoz.

Ha egy mezőn fal található, akkor annak a X-ben, illetve Y-ban lévő távolságát számításba véve (a tanítás során meghatározott) súllyal hatványozva vonjuk ki az adott irányba való mozgás értékéból. Ezáltal a távolabbi fal értékek kevésbé, míg a közelebbiek jobban figyelembe vannak véve.

A kaják is hasonló megoldással, egy másik súllyal, illetve ellentétes előjellel vannak figyelembe véve. Így egy irányban minél több (és minél közelebbi) kaja található, az agent annál nagyobb valószínűséggel fog abba az irányba ellépni.

A többi játékost is le kellett kezelni. Ha egy mezőn olyan játékos van, melyet meg tud enni, akkor ennek értéke a játékos méretével megegyező kajaként fog beszámítani. Ha pedig az adott játékos nagyobb nála, a mező értéke -1-re vált, és ez a falakhoz hasonlóan, egy másik súllyal hatványozva taszítja az agentet.

Mivel a kaják is nagyobb valószínűséggel keletkeznek középen, illetve nem jár jól, ha szélen, a falak mellett vár, így beleraktunk egy szintén súllyal beszorzott értéket, amely minden pillanatban a pálya közepe felé "húzza" a játékost a közepétől való távolságot figyelembe véve.

Ezeket az értékeket minden lépésnél összegzi az agent, és ez alapján dönti el, hogy merre lépjen. Egy szintén súlyfüggő érték az, hogy legalább mekkora különbség legyen az X és Y-ban kiszámolt értékek között ahhoz, hogy azt dominánsnak ítélje, és csak abban az irányban, vízszintesen, vagy függőlegesen haladjon. Enélkül a feltétel nélkül mindig csak átlósan lépne.

Azért, hogy az agent ne kerüljön olyan ciklusba, ahol odavissza ugrál, elmentjük a kettővel ezelőtti pozíciót, és ha erre akarna visszalépni, inkább egy random lépést csinálunk helyette. 

 Összesen tehát 8 súlyunk lett, melyet a tanítás során módosítottunk

## A tanítás

A tanítás során genetikus algoritmust használtunk. Minden generációban 10 egyedünk volt, melyek mindegyike tartalmazta a 8 súlyt, 0 és 1 közötti float értékekként.
Ezek kezdetben random értékek voltak, melyek mindegyikével a játékot 5-ször lefuttattuk. A futások során az elért eredmények összege lett az adott egyed fittnesse. A 10 egyedből ezután a fittnessek alapján súlyozva kiválasztottunk 20 szülőt, melyekből lettek az új egyedek. Így a nagyobb fittnesst elért egyedek ezzel arányosan nagyobb valószínűséggel lettek kiválasztva szülőnek.
A szülőket párba állítva, a 0 és 1 közötti súlyértékeket 32bites bináris számokká alakítva hajtottuk végre a keresztezést. A számokat egy random ponton elvágva lettek keresztezve a szülők, majd a mutáció során az új egyedek mindegyik bitje egy 0.05-nek választott valószínűséggel fordul át és mutálódik. Ezután a súlyokat visszaalakítjuk decimális értékekké, és megkaptuk a következő generáció egyedeit.

A játékost több órán át, különböző játékosok ellen tanítva kaptuk meg a végleges súlyainkat.


## A játékos tesztelése

Az alábbi videóban látható több, hasonló súlyokkal futó agent egymás ellen:

https://user-images.githubusercontent.com/82844655/170246233-5e5a7e97-b08f-4598-8acb-39f2d20c7159.mp4


