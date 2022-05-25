# AdaptIO

Az alábbi fájlban a "Adaptív rendszerek modellezése" tárgy AdaptIO játékához készített agent kerül bemutatásra.

## A játékos stratégiája

A játékosn a játék során folyamatosan  81 mezőből áll a látótere,  az alábbi formában:

![Képernyőkép 2022-05-25 120222](https://user-images.githubusercontent.com/82844655/170237011-0b819a23-5354-4739-9eec-ff33574b53d3.png)


És a lépései pedig az alábbiak lehetnek:

![Képernyőkép 2022-05-25 120252](https://user-images.githubusercontent.com/82844655/170237092-7003ad16-b784-45d1-99b3-1a125090f011.png)


Az X és Y irányú lépéseket külön vizsgáltuk. Minden döntéshozatalnál beleszámoltuk az összes látóteren belüli mező értékét a döntésbe. Attól függően, hogy az adott mezőn fal, étel, vagy másik játékos található, különbözően adtuk hozzá az értékét az összesített X, illetve Y-hoz.

Ha egy mezőn fal található, akkor annak a X-ben, illetve Y-ban lévő távolságát figyelembe véve (a tanítás során meghatározott) súllyal hatványozva vonjuk ki az adott irányba való mozgás értékéból. Ezáltal a távolabbi fal értékek kevésbé, míg a közelebbiek jobban figyelembe vannak véve.

A kaják is hasonló megoldással, egy másik súllyal, illetve ellentétes előjellel vannak figyelembe véve. Így egy irányban minél több (és minél közelebbi) kaja található, az agent abba az irányba fog ellépni.

A többi játékost is le kellett kezelni. Ha egy mezőn olyan játékos van, melyet meg tud enni, akkor ennek értéke a játékos méretével megegyező kajaként fog beszámítani. Ha pedig az adott játékos nagyobb nála, a mező értéke -1 -re vált, és ez a falakhoz hasonlóan, egy másik súllyal hatványozva taszítja az agentet.

Mivel a kaják is nagyobb valószínűséggel keletkeznek középen, illetve nem jár jól, ha szélen, a falak mellett vár, így beleraktunk egy szintén súllyal beszorzott értéket, amely minden pillanatban a pálya közepe felé "húzza" a játékost.

Ezeket az értékeket minden lépésnél összegzi az agent, és ez alapján dönti el, hogy merre lépjen. Egy szintén súlyfüggő érték az, hogy legalább mekkora különbség legyen az X és Y-ban kiszámolt értékek között ahhoz, hogy azt dominánsnak ítélje, és csak abban az irányban, vízszintesen, vagy függőlegesen lépjen. Enélkül a feltétel nélkül mindig csak átlósan lépne.

## A tanítás

