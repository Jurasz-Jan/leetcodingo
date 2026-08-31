# Roadmapa

Stan na 2026-08-24, po przejściu P0.4 z opisu projektu: aplikacja jest w regularnym
użyciu. To zmienia priorytety — od tej chwili liczy się to, co psuje codzienne
korzystanie, a nie to, czego jeszcze nie ma.

## Gdzie jesteśmy

| | |
|---|---|
| Korpus | 214 ćwiczeń, 18 wzorców, 8 typów |
| Wygenerowane mechanicznie | 57, z **2 problemów** (sliding window) |
| Kurowane | 155, wszystkie z `reviewed: false` |
| Sesja | ~4,8 ćwiczenia, średnio 37 s na ćwiczenie |
| Wyczerpanie korpusu | po **~45 sesjach** |
| Renderer | 1084 linie Kotlina, bez backendu i bez kont |

---

## P0 — psuje codzienne użycie

### 1. Powtórki nie działają tak, jak się wydaje

Trzy osobne usterki, w kolejności rosnącej trudności.

**Postęp ginie przy przerwanej sesji.** `markSeen` wywołuje się wyłącznie po naciśnięciu
„Dalej" na ostatnim zadaniu. Zwinięcie aplikacji w połowie sesji oznacza, że nic się nie
zapisze. W aplikacji projektowanej do używania w kolejce do kasy przerwanie w połowie
jest przypadkiem typowym, nie wyjątkowym. To defekt, nie decyzja projektowa.
**Naprawa: oznaczać ćwiczenie jako widziane w momencie odpowiedzi.** Kilka linijek.

**Wyścig przy „Jeszcze raz".** `next()` odpala zapis w osobnej korutynie i natychmiast
pokazuje ekran końcowy. Naciśnięcie „Jeszcze raz" czyta stan, którego zapis może jeszcze
nie zdążyć. Ta sama naprawa co wyżej usuwa i ten problem.

**Po wyczerpaniu korpusu nie ma żadnych odstępów.** Gdy wszystkie 214 trafi do zbioru
widzianych, sesja to losowanie jednostajne i to samo ćwiczenie może wypaść dwa razy pod
rząd. Przy regularnym używaniu ten stan nastąpi za jakieś półtora miesiąca.
**Naprawa: zamienić zbiór identyfikatorów na mapę `id → (liczba pokazów, ostatnio
widziane, ostatni wynik)` i losować spośród najdawniej widzianych.** To już jest
fundament pod SM-2, czyli P1 punkt 5 z opisu projektu.

### 2. Wydanie, żeby aktualizacja nie kasowała postępu

Workflow i klucz są gotowe, brakuje czterech sekretów w repozytorium. Dopóki instalujesz
build debugowy, każda zmiana maszyny albo klucza oznacza odinstalowanie aplikacji, czyli
utratę całego postępu. Im dłużej to zwlekasz, tym więcej masz do stracenia.

### 3. Przegląd 155 kurowanych ćwiczeń

To jedyna część korpusu bez **jakiegokolwiek** dowodu poprawności: nie ma tam kodu, więc
nie ma czego uruchomić. Treść, dobór dystraktorów i uzasadnienia to decyzje autora.
Przy 155 pozycjach to już nie formalność.

Warto zacząć od przeglądu w trakcie używania: gdy ćwiczenie wygląda podejrzanie, zapisać
jego identyfikator. Narzędzie do szybkiej akceptacji jest w P2, ale nie jest potrzebne,
żeby zacząć.

---

## P1 — przestać zgadywać, zacząć mierzyć

### 4. Kalibracja `est_seconds`

Obecne wartości pochodzą z wzoru, który wymyśliłem bez danych: `30 + 10 × trudność` dla
`find-bug` i tak dalej. Średnia wychodzi 37 s, czyli 4,8 ćwiczenia na trzyminutową sesję,
podczas gdy opis projektu mówi o mikrodecyzjach trwających 15 sekund. Jedno z dwojga jest
nieprawdą i bez pomiaru nie wiadomo które.

**Aplikacja powinna zapisywać rzeczywisty czas od pokazania do odpowiedzi.** Po dwóch
tygodniach danych da się przeliczyć `est_seconds` z mediany zamiast z wzoru. To jedyna
zmiana, która naprawia długość sesji bez kolejnego strzelania.

### 5. Statystyki: skuteczność per wzorzec i per typ

Bez tego nie wiadomo, czego nie umiesz. Mając dane z punktu 4 i wyniki odpowiedzi,
ekran statystyk to głównie praca renderera. Wartość: pokazuje, który wzorzec wybrać
w sesji tematycznej, zamiast zgadywać.

### 6. Adaptacyjna trudność

Łatwiejsze mutacje na start, trudniejsze po serii trafień. Ma sens dopiero po 4 i 5,
bo bez danych o skuteczności nie ma czym sterować.

---

## P2 — więcej treści, ale najtańszą drogą

### 7. Rozszerzyć pipeline mutacyjny na kolejne wzorce

**To jest najbardziej niedoceniona pozycja na tej liście.** Dziś cały mechanicznie
generowany korpus pochodzi z **dwóch** problemów. Każdy nowy plik w `patterns/`, czyli
poprawna implementacja plus zestaw testów, daje około **30 ćwiczeń zwalidowanych
uruchomieniem** — z dowodem poprawności, którego nie ma żadne ćwiczenie kurowane.

Koszt jednego problemu to godzina pracy. Dwa pierwsze wzorce warte dołożenia:
dwa wskaźniki i wyszukiwanie binarne, bo mają bogaty zestaw sensownych mutacji.

Proporcja z opisu projektu miała wynosić 80% generowane, 20% pisane ręcznie. Dziś jest
odwrotnie: 27% generowane, 73% kurowane. Ten punkt naprawia to najtaniej.

### 8. Dokończyć pokrycie NeetCode 150

Najcieńsze kategorie: `math`, `bit-manipulation`, `advanced-graphs`, `trie` i `dp-2d`,
po 3–4 ćwiczenia. Do pełnego pokrycia listy brakuje jeszcze sporo.

### 9. Narzędzie do przeglądu korpusu

Prosty tryb w aplikacji albo skrypt: pokaż ćwiczenie, zaakceptuj albo odrzuć jednym
ruchem, zapisz `reviewed: true` do modułu źródłowego. Sensowne dopiero, gdy punkt 3
okaże się zbyt żmudny do zrobienia ręcznie.

---

## P3 — nowe typy ćwiczeń

Kolejność według stosunku wartości do pracy. Pierwsze dwa nie wymagają pisania treści.

**Przypadek brzegowy, generowany.** Kod plus wejście graniczne, opcje: zwraca wartość,
wyrzuca wyjątek, zapętla się. `runner.py` **już teraz** klasyfikuje przebiegi na `pass`,
`fail`, `error` i `timeout` — odpowiedź leży gotowa w danych, których nie używamy.

**Który nie pasuje.** Cztery opisy zadań, trzy z jednego wzorca, jeden z innego.
Darmowe: 155 kurowanych ćwiczeń ma już etykiety wzorców, generator tylko je składa.

**Czy te dwie wersje robią to samo.** Wymaga rodziny operatorów **zachowujących**
zachowanie (`for` na `while`, prawa De Morgana), których poprawność potwierdzają testy.
Uczy odróżniania różnicy kosmetycznej od semantycznej. Pytanie musi brzmieć „czy któryś
z tych testów wykryje różnicę", a nie „czy to jest to samo", bo testy dowodzą tylko
nierozróżnialności przez ten konkretny zestaw.

**Dopasuj pary i bank tokenów.** Najbardziej „duolingowe" formaty, ale każdy wymaga
nowego `ui` w rendererze, który z założenia ma zostać cienki. Dopiero gdy poprzednie
się sprawdzą.

---

## Znane usterki

| Rzecz | Stan |
|---|---|
| Zoom kodu dwoma palcami | zaimplementowany, **nigdy nie sprawdzony na żywo** — `adb` nie umie gestu dwupalcowego |
| `est_seconds` | wartości z wzoru, nie z pomiaru |
| Wydanie `v0.1.0` | tag wypchnięty, workflow czeka na sekrety |
| Korpus na urządzeniu | `adb push` działa, ale nadpisuje **cały** korpus, nie scala |

---

## Świadomie nie robimy

XP, streaków, osiągnięć i lig — z powodu, który opis projektu podaje najlepiej: to jest
najczęstszy sposób, w jaki takie projekty umierają, z dwunastoma osiągnięciami i
piętnastoma zadaniami. Mechaniką retencji mają być powtórki rozłożone w czasie, nie
seria dni.

Kont, chmury i synchronizacji. Edytora i uruchamiania kodu użytkownika. Pobierania
korpusu z sieci — wymagałoby uprawnienia `INTERNET` i oddałoby właściwość, że aplikacja
technicznie nie ma jak zadzwonić do domu.

---

## Co zrobiłbym najpierw

Punkt 1, pierwsza usterka: **oznaczanie ćwiczenia jako widzianego w momencie odpowiedzi**.
Kilka linijek, usuwa dwie usterki naraz i dotyczy czegoś, co tracisz przy każdej
przerwanej sesji, czyli prawdopodobnie codziennie.

Zaraz potem punkt 2, bo koszt zwłoki rośnie z każdym dniem używania.

Trzeci byłby punkt 7 — dwa nowe wzorce w pipelinie mutacyjnym dodadzą około 60 ćwiczeń
z dowodem poprawności, za jakieś dwie godziny pracy. Żaden inny punkt nie ma takiego
stosunku wartości do kosztu.
