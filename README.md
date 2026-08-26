# leetcodingo - wajbkodowana apka do ćwiczenia leetcode'a


Dwa niezależne moduły, kontraktem między nimi jest JSON:

```
generator/  →  corpus/*.json  →  app/  (cienki renderer)
```

Renderer nie wie nic o generowaniu treści i nigdy nie zawiera treści na sztywno.
Korpus przebudowuje się bez dotykania aplikacji.

## Stan

| Cel | Stan |
|---|---|
| P0.1 pipeline mutacyjny z walidacją testami | gotowe |
| P0.2 jeden wzorzec, ~40 ćwiczeń | gotowe: sliding window, 59 ćwiczeń, 2 problemy |
| wszystkie typy reprezentowane | gotowe |
| pokrycie NeetCode 150 | w toku: 18 rodzin wzorców, 105 ćwiczeń kurowanych, wszystkie do przeglądu |
| P0.3 renderer | gotowe: działa na emulatorze (Android 16), pełna ścieżka pytanie → odpowiedź → wyjaśnienie |
| P0.4 test na sobie przez 2 tygodnie | przed nami |

Korpus liczy 164 ćwiczenia w 18 wzorcach: 59 wygenerowanych mechanicznie ze sliding window
i 105 kurowanych, pokrywających rodziny wzorców z NeetCode 150.

Te 105 czeka na przegląd. Jako jedyne w korpusie nie mają za sobą żadnego dowodu
poprawności: nie ma tam kodu, więc nie ma czego zmutować ani na czym uruchomić testów.
Build o tym przypomina przy każdym uruchomieniu i liczy je po polu `reviewed`.

## Budowanie korpusu

```bash
python generator/build.py
```

Kod wyjścia różny od zera oznacza, że walidator odrzucił korpus. Testy pipeline'u:

```bash
python -m pytest generator/tests -q
```

## generator/

```
patterns/<wzorzec>/_pattern.json   metadane wzorca
patterns/<wzorzec>/<problem>.py    poprawna implementacja + spec + zestaw testów
mutations.py                       operatory mutacji na AST
runner.py                          uruchamianie testów na mutancie (subprocess + timeout)
exercises.py                       budowanie ćwiczeń ze zwalidowanych mutantów
build.py                           CLI + walidator korpusu
curated/<nazwa>.py                 ćwiczenia pisane ręcznie, osobny plik korpusu
tests/                             testy pipeline'u
```

### Kiedy mutant NIE trafia do korpusu

1. **Przechodzi wszystkie testy.** Ćwiczenie nie ma wtedy poprawnej odpowiedzi.
   To także sygnał, że zestaw testów ma lukę.
2. **Wywala się na niezdefiniowanej nazwie** (`NameError`, `UnboundLocalError`).
   Taki błąd widać po tym, że zmienna nie istnieje, a nie po zrozumieniu wzorca.

Mutacje potrafią zapętlić kod, więc każdy przebieg idzie do podprocesu z twardym
limitem czasu. Po zawieszeniu pozostałe testy są dobijane osobnym przebiegiem,
żeby zapętlenie na teście nr 3 nie oznaczyło testów 4–8 jako niezdanych.

### Typy ćwiczeń

| Typ | Skąd się bierze | Co dowodzi poprawności |
|---|---|---|
| `find-bug` (który test) | zabity mutant + jego wyniki na testach | mutant oblewa dokładnie ten jeden test |
| `find-bug` (która linia) | zabity mutant o jednej zmienionej linii | mutant oblewa testy |
| `fill-gap` | mutant `drop_stmt` + warianty tej samej linii | bez linii testy failują, każdy dystraktor też |
| `predict-output` | poprawny kod + wyniki mutantów na tym wejściu | uruchomienie kodu |
| `complexity` | metadane wzorca | ręcznie, w metadanych |
| `order-steps` | opis bloków w module wzorca | ręcznie |
| `recognize-pattern` | `generator/curated/` | nic, czeka na przegląd |
| `key-insight` | `generator/curated/` | nic, czeka na przegląd |
| `edge-case` | `generator/curated/` | nic, czeka na przegląd |

Trzy typy kurowane pytają o trzy różne rzeczy o tym samym zadaniu i nie zastępują się
nawzajem. `recognize-pattern`: **który** wzorzec. `key-insight`: ta jedna obserwacja,
bez której wzorzec i tak nie zadziała albo zadziała za wolno. `edge-case`: co łamie
podejście, które wygląda na poprawne.

`order-steps` ma własne sito, mocniejsze niż dobre chęci. Każdy krok deklaruje w polu
`deps`, których wcześniejszych kroków efekt zużywa. Build robi z tego sortowanie
topologiczne i **odrzuca ćwiczenie, jeśli na którymkolwiek etapie dwa kroki są gotowe
naraz**: dałoby się je wtedy zamienić miejscami, więc poprawnych odpowiedzi byłyby dwie,
czyli w praktyce żadna. To jest dla tego typu tym, czym filtr testowy dla mutantów.

Przy wprowadzaniu tej reguły okazało się, że **dziewięć z 32 istniejących ćwiczeń było
niejednoznacznych** — zwykle przez dwie niezależne inicjalizacje albo dwie gałęzie tego
samego warunku. Wszystkie zostały przepisane.

`key-insight` wymaga `spec_ref` i to jest tam najostrzejsze sito: jeśli nie da się
wskazać w treści fragmentu, na którym obserwacja się zawiesza, zwykle znaczy to, że
odpowiedź jest prawdziwą uwagą, a nie sednem. `edge-case` `spec_ref` nie wymaga, bo
uzasadnia go prześledzenie podejścia na danym wejściu, a nie cytat.

`predict-output` pokazuje **poprawną** implementację i pyta, co zwróci dla podanego
wejścia. Dystraktory to wyniki, jakie na tym samym wejściu zwróciły zabite mutanty:
każdy jest więc błędny z definicji i wiarygodny z definicji, bo powstał z realistycznej
pomyłki, a nie z fantazji autora. Wybierane są trzy leżące najbliżej poprawnego wyniku,
bo odpowiedź odległa o rząd wielkości odpada na pierwszy rzut oka i niczego nie sprawdza.

Ten typ nie ma `spec_ref` i nie potrzebuje go: odpowiedź uzasadnia uruchomienie kodu,
a wartość `expect` jest niezależnie potwierdzona implementacją brute-force w testach
pipeline'u. To mocniejszy dowód niż cytat ze specyfikacji.

### Operatory mutacji i trudność

| Operator | Trudność | Przykład |
|---|---|---|
| `swap_vars` | 1 | `total -= nums[left]` → `nums[right]`, w jednej instrukcji |
| `op_swap` | 2 | `+` → `-`, `min()` → `max()` |
| `const_change` | 2 | `0` → `1` |
| `drop_stmt` | 2 | usunięta instrukcja |
| `cmp_swap` | 3 | `>=` → `>` |
| `off_by_one` | 3 | `right - left + 1` → `right - left` |

Trudność jest cechą operatora, klasyfikowaną raz przy generowaniu.

### Dodanie nowego problemu

Jeden plik w `patterns/<wzorzec>/`, z `PATTERN`, `PROBLEM`, `FUNC`, `SPEC`,
`SPEC_REFS`, `LINE_SPEC_REFS`, `COMPLEXITY`, `TESTS`, `BLOCKS`, `SWAPPABLE_VARS`
i funkcją `solution`.
Do `generator/tests/test_pipeline.py` dopisz niezależną implementację brute-force —
wartości `expect` nie mogą pochodzić z tej samej implementacji, którą sprawdzają.

`LINE_SPEC_REFS` mapuje linię kodu na fragment speca i ma pierwszeństwo przed
`SPEC_REFS`, które trafia po operatorze. Sam operator nie wystarcza: `const_change`
na `else 0` uzasadnia zdanie o zwracaniu zera, ale ten sam operator na `left = 0`
już nie. Cytat, który niczego nie dowodzi, jest gorszy niż jego brak, bo walidator
go przepuszcza.

## app/ — renderer

Kotlin + Jetpack Compose, jeden moduł, bez backendu i bez kont.
minSdk 26, compileSdk 36, AGP 8.13, Gradle 8.14.3 (wrapper), JDK 17 jako target.

```bash
cd app
./gradlew assembleDebug testDebugUnitTest
```

Wymaga `JAVA_HOME` i `ANDROID_HOME`; scoop ustawia oba na stałe.

Uruchomienie na emulatorze, w dwóch terminalach:

```bash
emulator -avd leetcodingo
```

```bash
cd app && ./gradlew installDebug && adb shell am start -n pl.leetcodingo/.MainActivity
```

`installDebug` sam buduje i wgrywa APK, więc osobne `adb install` jest potrzebne
tylko wtedy, gdy chcesz wgrać gotowy plik:

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Na telefonie zamiast emulatora: opcje programisty, debugowanie USB, kabel,
potwierdzenie autoryzacji na ekranie telefonu, dalej to samo `installDebug`.

Gotowy plik leży w `app/app/build/outputs/apk/debug/app-debug.apk`.

Uwaga na przyszłość, gdyby projekt kiedyś trafił do folderu synchronizowanego przez
OneDrive: sync odsyła pliki do chmury i zostawia placeholder (atrybut `ReparsePoint`),
którego Gradle nie potrafi zsnapshotować, przez co build wywala się losowo na
`Cannot snapshot ... not a regular file`. Lekarstwem jest wtedy przekierowanie
`layout.buildDirectory` poza katalog synchronizowany albo, lepiej, trzymanie projektu
poza OneDrive.

Korpus trafia do APK zadaniem `copyCorpus`, które kopiuje `corpus` do assetów przy
każdym buildzie. Renderer czyta wszystko z assetów i nie zna żadnej treści na sztywno,
więc przebudowa korpusu nie wymaga zmiany kodu aplikacji.

Sesja to budżet czasu (180 s), nie liczba zadań: ćwiczenia są dobierane, aż suma
`est_seconds` wyczerpie budżet, najpierw te jeszcze niewidziane. Widziane ćwiczenia
pamięta DataStore. Właściwa mechanika retencji, czyli powtórki rozłożone w czasie,
to P1 i jeszcze jej nie ma.

## Schemat ćwiczenia

```json
{
  "id": "sliding-window/min-subarray/cmp-swap-00",
  "pattern": "sliding-window",
  "problem": "min-subarray",
  "type": "find-bug",
  "ui": "choice",
  "difficulty": 3,
  "spec": "Zwraca długość najkrótszego spójnego podciągu o sumie >= target...",
  "prompt": "Który test wykryje błąd?",
  "code": "def solution(nums, target): ...",
  "options": ["nums=[7], target=7", "..."],
  "answer": 1,
  "explanation": "Dla nums=[7], target=7 poprawną odpowiedzią jest 1, a kod zwraca 0...",
  "spec_ref": "sumie >= target",
  "est_seconds": 60,
  "source": "generated",
  "tags": ["which-test", "cmp_swap"]
}
```

`ui` mówi rendererowi, jak przyjąć odpowiedź: `choice` (jedna z opcji, `answer` to
indeks) albo `ordering` (`answer` to permutacja indeksów opcji).

`spec` jest obowiązkowy dla każdego typu: bez opisu, co kod ma robić, „znajdź błąd"
jest formalnie nierozstrzygalne.

`spec_ref` to walidator jakości: jeśli odpowiedzi nie da się uzasadnić fragmentem
speca, ćwiczenie leci do poprawki. Build sprawdza, że `spec_ref` występuje dosłownie
w `spec`, i wymaga go dla typów `find-bug`, `fill-gap` i `recognize-pattern`.

`reviewed` mówi, czy ćwiczenie ma za sobą jakikolwiek dowód poprawności.
Wygenerowane dostają `true`, bo przeszły filtr testowy; kurowane `false`, dopóki
człowiek ich nie przejrzy.

### Ćwiczenia kurowane

Moduł w `generator/curated/` podaje `CORPUS` z identyfikatorem i listę `EXERCISES`.
Moduły o tym samym identyfikatorze korpusu build scala w jeden plik, więc treść można
dzielić tematycznie: `recognize_pattern.py` to podstawy, `recognize_pattern_medium.py`
to poziom medium z NeetCode 150.
Każdy wpis ma `pattern`, `problem`, `difficulty`, `spec`, `options`, `answer`,
`explanation` i `spec_ref`. Build dokłada resztę pól i zapisuje osobny plik korpusu.

`answer` jest **tekstem poprawnej opcji, nie indeksem**. Indeks wylicza się sam po
przetasowaniu, więc nie da się rozjechać odpowiedzi z opcjami przy edycji.

Zasady treści: własne sformułowania, nigdy przepisane z LeetCode; `spec_ref` musi być
tą przesłanką w treści, która przesądza o wzorcu; dystraktorem ma być wzorzec, który
prawie pasuje, bo tylko taki czegoś uczy.
