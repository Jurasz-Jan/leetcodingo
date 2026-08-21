"""Kurowane ćwiczenia typu `recognize-pattern`.

Jedyny typ, którego nie da się wygenerować mechanicznie: nie ma tu kodu do
zmutowania, jest opis zadania i pytanie, który wzorzec go rozwiązuje. Dlatego
treść jest pisana ręcznie i **wymaga przeglądu**, zanim trafi do sesji na serio.

Zasady, których trzymają się te ćwiczenia:

* Treści są własne. Zadania z NeetCode 75 są tu inspiracją, nie źródłem tekstu.
* `spec_ref` musi być dosłownym fragmentem `spec` i musi być tą przesłanką,
  która przesądza o odpowiedzi. Jeśli nie da się wskazać takiego fragmentu,
  zadanie jest źle postawione i nie ma czego rozpoznawać.
* Dystraktor ma być kuszący. Wzorzec, który nikomu nie przyszedłby do głowy,
  nie uczy niczego; uczy dopiero ten, który prawie pasuje.

`answer` to tekst poprawnej opcji, nie indeks. Indeks wylicza builder po
przetasowaniu, dzięki czemu nie da się tu przestawić odpowiedzi literówką.
"""

CORPUS = {
    "id": "recognize-pattern",
    "name": "Rozpoznaj wzorzec",
    "recognition_cues": [
        "przesłanka w treści przesądza o wzorcu",
        "dystraktor to wzorzec, który prawie pasuje",
    ],
}

DEFAULT_PROMPT = "Który wzorzec rozwiązuje to zadanie?"

EXERCISES = [
    # --- tablice i haszowanie ---
    dict(
        pattern="arrays-hashing",
        problem="duplikat",
        difficulty=1,
        spec="Tablica liczb całkowitych. Sprawdź, czy istnieje wartość powtórzona.",
        prompt="Który wzorzec daje odpowiedź w czasie liniowym?",
        options=["zbiór haszujący", "sortowanie i porównanie sąsiadów", "dwa wskaźniki", "okno przesuwne"],
        answer="zbiór haszujący",
        spec_ref="istnieje wartość powtórzona",
        explanation=(
            "Wystarczy jedno przejście i zbiór widzianych wartości. Sortowanie też odpowie "
            "poprawnie, ale kosztuje O(n log n) i niszczy kolejność, więc przy pytaniu o czas "
            "liniowy przegrywa."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="iloczyn-pozostalych",
        difficulty=3,
        spec=(
            "Dla każdego elementu tablicy podaj iloczyn wszystkich pozostałych elementów, "
            "bez używania dzielenia."
        ),
        options=["prefiksy i sufiksy", "okno przesuwne", "zbiór haszujący", "wyszukiwanie binarne"],
        answer="prefiksy i sufiksy",
        spec_ref="bez używania dzielenia",
        explanation=(
            "Dwa przejścia: iloczyny wszystkiego na lewo i wszystkiego na prawo od pozycji. "
            "Gdyby dzielenie było dozwolone, wystarczyłby iloczyn całości podzielony przez element, "
            "i to właśnie ten zakaz wymusza wzorzec."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="anagramy",
        difficulty=1,
        spec="Lista słów. Pogrupuj razem te słowa, które są swoimi anagramami.",
        options=[
            "słownik z kluczem kanonicznym",
            "dwa wskaźniki",
            "sortowanie całej listy",
            "okno przesuwne",
        ],
        answer="słownik z kluczem kanonicznym",
        spec_ref="są swoimi anagramami",
        explanation=(
            "Anagramy mają wspólną postać kanoniczną, na przykład posortowane litery albo licznik "
            "znaków. To ona jest kluczem słownika. Sortowanie całej listy grupuje anagramy obok "
            "siebie, ale wymaga potem drugiego przejścia i jest wolniejsze."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="k-najczestszych",
        difficulty=2,
        spec="Tablica liczb i wartość k. Podaj k wartości występujących najczęściej.",
        options=[
            "licznik wystąpień i kopiec rozmiaru k",
            "okno przesuwne",
            "dwa wskaźniki",
            "wyszukiwanie binarne po wartości",
        ],
        answer="licznik wystąpień i kopiec rozmiaru k",
        spec_ref="występujących najczęściej",
        explanation=(
            "Najpierw słownik zliczający, potem wybór k największych. Kopiec rozmiaru k daje "
            "O(n log k) zamiast O(n log n) za pełne sortowanie liczników."
        ),
    ),
    # --- dwa wskaźniki ---
    dict(
        pattern="two-pointers",
        problem="para-o-danej-sumie",
        difficulty=1,
        spec=(
            "Posortowana rosnąco tablica liczb i wartość docelowa. Znajdź dwa różne indeksy, "
            "których elementy sumują się do wartości docelowej."
        ),
        prompt="Który wzorzec wykorzystuje strukturę danych podaną w treści?",
        options=["dwa wskaźniki z obu końców", "słownik odwiedzonych wartości", "okno przesuwne", "kopiec"],
        answer="dwa wskaźniki z obu końców",
        spec_ref="Posortowana rosnąco",
        explanation=(
            "Suma zbyt mała, więc przesuń lewy w prawo; zbyt duża, więc prawy w lewo. Słownik też "
            "rozwiąże to w czasie liniowym, ale zużyje O(n) pamięci i w ogóle nie skorzysta z tego, "
            "że tablica jest posortowana."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="palindrom",
        difficulty=1,
        spec=(
            "Napis. Sprawdź, czy czytany od początku i od końca wygląda tak samo, pomijając "
            "znaki inne niż litery i cyfry."
        ),
        options=["dwa wskaźniki z obu końców", "stos", "okno przesuwne", "słownik liczników"],
        answer="dwa wskaźniki z obu końców",
        spec_ref="od początku i od końca",
        explanation=(
            "Wskaźniki idą ku sobie i pomijają znaki, które nie liczą się do porównania. Stos "
            "rozwiąże to samo, ale kosztem O(n) pamięci na odwrócenie napisu."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="usun-duplikaty",
        difficulty=2,
        spec=(
            "Posortowana tablica. Usuń powtórzenia w miejscu i zwróć liczbę pozostałych "
            "elementów, nie tworząc nowej tablicy."
        ),
        options=[
            "wskaźnik wolny i szybki",
            "zbiór haszujący",
            "okno przesuwne",
            "sortowanie z usuwaniem",
        ],
        answer="wskaźnik wolny i szybki",
        spec_ref="nie tworząc nowej tablicy",
        explanation=(
            "Szybki wskaźnik przegląda, wolny wyznacza miejsce zapisu następnej unikalnej wartości. "
            "Zbiór haszujący odpowiedziałby poprawnie, ale zużywa dodatkową pamięć, a treść tego "
            "właśnie zabrania."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="najwieksze-pole",
        difficulty=3,
        spec=(
            "Tablica wysokości pionowych linii. Wybierz parę linii, która razem z osią poziomą "
            "tworzy największe pole prostokąta."
        ),
        options=["dwa wskaźniki z obu końców", "okno przesuwne", "programowanie dynamiczne", "stos monotoniczny"],
        answer="dwa wskaźniki z obu końców",
        spec_ref="największe pole",
        explanation=(
            "Zaczynasz od najszerszej pary i przesuwasz ten wskaźnik, który wskazuje niższą linię, "
            "bo tylko wtedy pole ma szansę wzrosnąć. Okno przesuwne nie pasuje, bo wynik nie zależy "
            "od spójnego fragmentu, tylko od dwóch dowolnych pozycji."
        ),
    ),
    # --- okno przesuwne ---
    dict(
        pattern="sliding-window",
        problem="bez-powtorzen",
        difficulty=2,
        spec="Napis. Podaj długość najdłuższego spójnego fragmentu bez powtórzonego znaku.",
        options=["okno przesuwne ze słownikiem", "dwa wskaźniki z obu końców", "programowanie dynamiczne", "stos"],
        answer="okno przesuwne ze słownikiem",
        spec_ref="najdłuższego spójnego fragmentu",
        explanation=(
            "Okno rośnie w prawo, a gdy znak się powtórzy, lewa krawędź przeskakuje za poprzednie "
            "wystąpienie. Słowo „spójnego” jest tu przesłanką: gdyby fragment mógł być nieciągły, "
            "okno by nie działało."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="najlepszy-zysk",
        difficulty=2,
        spec=(
            "Ceny w kolejnych dniach. Podaj największy zysk z jednego kupna i jednej sprzedaży, "
            "przy czym sprzedaż musi nastąpić po kupnie."
        ),
        prompt="Który wzorzec wystarczy tutaj?",
        options=[
            "jedno przejście z zapamiętanym minimum",
            "okno przesuwne o zmiennej długości",
            "dwa wskaźniki z obu końców",
            "kopiec minimalny",
        ],
        answer="jedno przejście z zapamiętanym minimum",
        spec_ref="sprzedaż musi nastąpić po kupnie",
        explanation=(
            "Wystarczy pamiętać najniższą dotychczasową cenę i sprawdzać zysk względem niej. To "
            "wygląda jak okno przesuwne i często bywa tak nazywane, ale okna tu nie ma: nic nie "
            "wypada z lewej strony, lewa krawędź tylko skacze na nowe minimum."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="najkrotsze-pokrycie",
        difficulty=3,
        spec=(
            "Napis i wzorzec. Znajdź najkrótszy spójny fragment napisu, który zawiera wszystkie "
            "znaki wzorca, licząc powtórzenia."
        ),
        options=[
            "okno przesuwne z licznikiem brakujących znaków",
            "dwa wskaźniki z obu końców",
            "wyszukiwanie binarne po długości",
            "stos monotoniczny",
        ],
        answer="okno przesuwne z licznikiem brakujących znaków",
        spec_ref="najkrótszy spójny fragment",
        explanation=(
            "Okno rozszerza się, aż pokryje wzorzec, potem kurczy z lewej, dopóki pokrycie się "
            "utrzymuje. Licznik brakujących znaków pozwala sprawdzać warunek w czasie stałym "
            "zamiast porównywać słowniki przy każdym kroku."
        ),
    ),
    # --- stos ---
    dict(
        pattern="stack",
        problem="nawiasowanie",
        difficulty=1,
        spec="Napis złożony z trzech rodzajów nawiasów. Sprawdź poprawność nawiasowania.",
        options=["stos", "licznik otwarć i zamknięć", "dwa wskaźniki", "okno przesuwne"],
        answer="stos",
        spec_ref="trzech rodzajów nawiasów",
        explanation=(
            "Sam licznik wystarczyłby przy jednym rodzaju nawiasu, ale przy trzech trzeba pamiętać "
            "kolejność otwarć, żeby odrzucić „([)]”. To jest dokładnie zadanie dla stosu."
        ),
    ),
    dict(
        pattern="stack",
        problem="cieplejszy-dzien",
        difficulty=3,
        spec=(
            "Temperatury w kolejnych dniach. Dla każdego dnia podaj, ile dni trzeba czekać na "
            "pierwszy cieplejszy dzień, albo 0, gdy taki nie nadejdzie."
        ),
        options=["stos monotoniczny", "okno przesuwne", "wyszukiwanie binarne", "programowanie dynamiczne"],
        answer="stos monotoniczny",
        spec_ref="pierwszy cieplejszy dzień",
        explanation=(
            "Na stosie leżą dni czekające na cieplejszy. Nowy dzień zdejmuje z niego wszystkie "
            "chłodniejsze i od razu wypełnia ich odpowiedzi. Słowo „pierwszy” jest przesłanką: "
            "pytanie o najbliższy większy element z prawej to typowe zastosowanie stosu monotonicznego."
        ),
    ),
    # --- wyszukiwanie binarne ---
    dict(
        pattern="binary-search",
        problem="obrocona-tablica",
        difficulty=3,
        spec=(
            "Tablica posortowana rosnąco, a następnie obrócona o nieznaną liczbę pozycji. "
            "Znajdź najmniejszy element."
        ),
        options=["wyszukiwanie binarne", "jedno przejście liniowe", "dwa wskaźniki z obu końców", "kopiec minimalny"],
        answer="wyszukiwanie binarne",
        spec_ref="obrócona o nieznaną liczbę pozycji",
        explanation=(
            "Mimo obrotu jedna z połówek zawsze pozostaje posortowana, a to wystarczy, żeby w "
            "każdym kroku odrzucić połowę tablicy. Przejście liniowe da poprawny wynik, ale "
            "marnuje informację o porządku."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="szukanie-po-odpowiedzi",
        difficulty=3,
        spec=(
            "Szukasz najmniejszej przepustowości, przy której da się przewieźć cały ładunek w "
            "zadanym limicie dni. Sprawdzenie pojedynczej przepustowości jest łatwe i szybkie."
        ),
        prompt="Który wzorzec pasuje, choć w treści nie ma posortowanej tablicy?",
        options=[
            "wyszukiwanie binarne po odpowiedzi",
            "programowanie dynamiczne",
            "algorytm zachłanny bez szukania",
            "okno przesuwne",
        ],
        answer="wyszukiwanie binarne po odpowiedzi",
        spec_ref="Sprawdzenie pojedynczej przepustowości jest łatwe",
        explanation=(
            "Przesłanką nie jest posortowana tablica, tylko monotoniczność: jeśli dana "
            "przepustowość wystarcza, to każda większa też. Szukasz więc granicy w przestrzeni "
            "odpowiedzi, a nie w danych wejściowych."
        ),
    ),
    # --- listy ---
    dict(
        pattern="linked-list",
        problem="odwroc-liste",
        difficulty=1,
        spec="Lista jednokierunkowa. Odwróć kolejność elementów, nie tworząc nowej listy.",
        options=[
            "przepinanie wskaźników w jednym przejściu",
            "stos wszystkich węzłów",
            "rekurencja po tablicy pomocniczej",
            "dwa wskaźniki z obu końców",
        ],
        answer="przepinanie wskaźników w jednym przejściu",
        spec_ref="nie tworząc nowej listy",
        explanation=(
            "Trzy wskaźniki: poprzedni, bieżący, następny. Stos też odwróci listę, ale zużyje "
            "O(n) pamięci, a treść wymaga pracy w miejscu."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="cykl",
        difficulty=2,
        spec="Lista jednokierunkowa. Sprawdź, czy zawiera cykl, używając stałej pamięci.",
        options=[
            "wskaźnik wolny i szybki",
            "zbiór odwiedzonych węzłów",
            "wyszukiwanie binarne",
            "sortowanie węzłów",
        ],
        answer="wskaźnik wolny i szybki",
        spec_ref="używając stałej pamięci",
        explanation=(
            "Szybki przesuwa się o dwa, wolny o jeden; w cyklu muszą się spotkać. Zbiór "
            "odwiedzonych węzłów jest prostszy w zapisie i równie poprawny, ale zużywa O(n) "
            "pamięci, czego treść zabrania."
        ),
    ),
    # --- drzewa ---
    dict(
        pattern="trees",
        problem="poziomami",
        difficulty=1,
        spec="Drzewo binarne. Podaj jego wartości poziom po poziomie, od korzenia w dół.",
        options=["przeszukiwanie wszerz z kolejką", "przeszukiwanie w głąb", "stos monotoniczny", "kopiec"],
        answer="przeszukiwanie wszerz z kolejką",
        spec_ref="poziom po poziomie",
        explanation=(
            "Kolejka odwiedza węzły dokładnie w kolejności poziomów. Przeszukiwanie w głąb też "
            "potrafi to zrobić, ale dopiero gdy dołożysz jawne śledzenie głębokości i posortujesz "
            "wynik, co jest okrężną drogą."
        ),
    ),
    dict(
        pattern="trees",
        problem="czy-bst",
        difficulty=3,
        spec=(
            "Drzewo binarne. Sprawdź, czy jest drzewem BST, czyli czy każdy węzeł jest większy "
            "od wszystkich w lewym poddrzewie i mniejszy od wszystkich w prawym."
        ),
        options=[
            "przeszukiwanie w głąb z przedziałem dopuszczalnych wartości",
            "porównanie każdego węzła z jego dwoma dziećmi",
            "przeszukiwanie wszerz z kolejką",
            "sortowanie wartości i porównanie",
        ],
        answer="przeszukiwanie w głąb z przedziałem dopuszczalnych wartości",
        spec_ref="wszystkich w lewym poddrzewie",
        explanation=(
            "Porównanie z dziećmi to najczęstszy błędny odruch: przechodzi je drzewo, w którym "
            "wnuk łamie warunek względem dziadka. Treść mówi o wszystkich węzłach w poddrzewie, "
            "więc w dół trzeba przekazywać przedział, a nie pojedynczą wartość."
        ),
    ),
    dict(
        pattern="trees",
        problem="lustrzane",
        difficulty=2,
        spec="Drzewo binarne. Sprawdź, czy jest lustrzanym odbiciem samego siebie.",
        options=[
            "porównywanie dwóch poddrzew idących w przeciwnych kierunkach",
            "porównanie wypisania w porządku infiksowym",
            "kopiec",
            "okno przesuwne",
        ],
        answer="porównywanie dwóch poddrzew idących w przeciwnych kierunkach",
        spec_ref="lustrzanym odbiciem",
        explanation=(
            "Idziesz dwoma wskaźnikami naraz: lewym w lewo i prawym w prawo, potem odwrotnie. "
            "Porównanie wypisania infiksowego wygląda kusząco, ale nie odróżnia struktury, gdy "
            "w drzewie powtarzają się wartości."
        ),
    ),
    # --- drzewa trie ---
    dict(
        pattern="trie",
        problem="przedrostki",
        difficulty=2,
        spec=(
            "Zaprojektuj strukturę, która przyjmuje słowa i szybko odpowiada, czy któreś z "
            "dodanych słów zaczyna się danym przedrostkiem."
        ),
        options=["drzewo trie", "zbiór haszujący pełnych słów", "posortowana lista i wyszukiwanie binarne", "kopiec"],
        answer="drzewo trie",
        spec_ref="zaczyna się danym przedrostkiem",
        explanation=(
            "Zbiór haszujący odpowie tylko na pytanie o całe słowo, bo hasz przedrostka nie ma "
            "związku z haszem słowa. Trie schodzi znak po znaku i sam odpowiada na pytanie o "
            "przedrostek."
        ),
    ),
    # --- kopce ---
    dict(
        pattern="heap",
        problem="mediana-strumienia",
        difficulty=3,
        spec=(
            "Liczby napływają jedna po drugiej. Po każdej nowej wartości podaj medianę "
            "wszystkich dotychczasowych."
        ),
        options=[
            "dwa kopce, mniejsza i większa połowa",
            "sortowanie po każdej nowej wartości",
            "okno przesuwne",
            "wyszukiwanie binarne w tablicy",
        ],
        answer="dwa kopce, mniejsza i większa połowa",
        spec_ref="Po każdej nowej wartości",
        explanation=(
            "Kopiec maksymalny trzyma mniejszą połowę, minimalny większą; mediana leży na "
            "wierzchołkach. Sortowanie po każdej wartości daje poprawny wynik, ale koszt rośnie "
            "do O(n log n) na każdą aktualizację."
        ),
    ),
    dict(
        pattern="heap",
        problem="k-ty-najwiekszy",
        difficulty=2,
        spec="Tablica liczb i wartość k. Podaj k-ty co do wielkości element.",
        options=[
            "kopiec minimalny rozmiaru k",
            "pełne sortowanie tablicy",
            "okno przesuwne",
            "zbiór haszujący",
        ],
        answer="kopiec minimalny rozmiaru k",
        spec_ref="k-ty co do wielkości",
        explanation=(
            "Kopiec rozmiaru k trzyma k największych widzianych elementów, a na jego wierzchołku "
            "leży odpowiedź. Kosztuje O(n log k) zamiast O(n log n) za sortowanie całości."
        ),
    ),
    # --- backtracking ---
    dict(
        pattern="backtracking",
        problem="podzbiory",
        difficulty=2,
        spec="Zbiór różnych liczb. Wypisz wszystkie jego podzbiory.",
        options=["backtracking", "programowanie dynamiczne", "okno przesuwne", "algorytm zachłanny"],
        answer="backtracking",
        spec_ref="wszystkie jego podzbiory",
        explanation=(
            "Pytanie o wypisanie wszystkich rozwiązań, a nie o jedno najlepsze, prawie zawsze "
            "oznacza przeszukiwanie z nawrotami. Programowanie dynamiczne skraca liczenie wyniku, "
            "ale nie pomaga, gdy trzeba wypisać każdy wariant z osobna."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="hetmany",
        difficulty=3,
        spec=(
            "Szachownica n na n. Ustaw n hetmanów tak, żeby żadne dwa się nie atakowały, i podaj "
            "wszystkie takie ustawienia."
        ),
        options=[
            "backtracking z odcinaniem gałęzi",
            "algorytm zachłanny",
            "programowanie dynamiczne",
            "przeszukiwanie wszerz",
        ],
        answer="backtracking z odcinaniem gałęzi",
        spec_ref="żadne dwa się nie atakowały",
        explanation=(
            "Stawiasz hetmana w kolejnym wierszu, a gdy kolumna albo przekątna jest zajęta, "
            "odcinasz całą gałąź. Zachłanność zawodzi, bo lokalnie poprawne ustawienie potrafi "
            "zablokować dalsze wiersze."
        ),
    ),
    # --- grafy ---
    dict(
        pattern="graphs",
        problem="wyspy",
        difficulty=2,
        spec="Siatka pól wody i lądu. Policz spójne obszary lądu.",
        options=[
            "przeszukiwanie w głąb lub wszerz po siatce",
            "programowanie dynamiczne",
            "okno przesuwne",
            "sortowanie pól",
        ],
        answer="przeszukiwanie w głąb lub wszerz po siatce",
        spec_ref="spójne obszary",
        explanation=(
            "Siatka to graf, w którym sąsiedztwo to krawędź. Każde nieodwiedzone pole lądu "
            "zaczyna nowy obszar, a przeszukiwanie zalewa cały ten obszar naraz."
        ),
    ),
    dict(
        pattern="graphs",
        problem="kolejnosc-kursow",
        difficulty=3,
        spec=(
            "Lista kursów i par mówiących, że jeden kurs trzeba zaliczyć przed drugim. Sprawdź, "
            "czy da się zaliczyć wszystkie."
        ),
        options=[
            "sortowanie topologiczne albo wykrywanie cyklu",
            "przeszukiwanie wszerz od dowolnego wierzchołka",
            "algorytm zachłanny",
            "programowanie dynamiczne",
        ],
        answer="sortowanie topologiczne albo wykrywanie cyklu",
        spec_ref="trzeba zaliczyć przed drugim",
        explanation=(
            "Zależności tworzą graf skierowany, a odpowiedź brzmi „nie” dokładnie wtedy, gdy jest "
            "w nim cykl. Zwykłe przeszukiwanie wszerz sprawdzi osiągalność, ale nie odpowie na "
            "pytanie o cykliczność."
        ),
    ),
    dict(
        pattern="graphs",
        problem="najkrotsza-droga-siatka",
        difficulty=3,
        spec=(
            "Siatka z przeszkodami. Znajdź najkrótszą drogę z lewego górnego rogu do prawego "
            "dolnego, gdzie każdy krok kosztuje tyle samo."
        ),
        prompt="Który wzorzec wystarczy tutaj?",
        options=[
            "przeszukiwanie wszerz",
            "algorytm Dijkstry",
            "przeszukiwanie w głąb",
            "programowanie dynamiczne",
        ],
        answer="przeszukiwanie wszerz",
        spec_ref="każdy krok kosztuje tyle samo",
        explanation=(
            "Przy jednakowych kosztach przeszukiwanie wszerz odwiedza wierzchołki w kolejności "
            "rosnącej odległości, więc pierwsze dojście do celu jest już najkrótsze. Dijkstra da "
            "ten sam wynik, ale dokłada kolejkę priorytetową, która przy równych kosztach niczego "
            "nie wnosi."
        ),
    ),
    # --- programowanie dynamiczne ---
    dict(
        pattern="dp-1d",
        problem="schody",
        difficulty=1,
        spec=(
            "Schody o n stopniach, wchodzisz krokiem o jeden albo o dwa stopnie. Ile jest "
            "sposobów wejścia na szczyt?"
        ),
        options=[
            "programowanie dynamiczne",
            "backtracking bez zapamiętywania",
            "algorytm zachłanny",
            "okno przesuwne",
        ],
        answer="programowanie dynamiczne",
        spec_ref="Ile jest sposobów",
        explanation=(
            "Liczba sposobów na stopień n to suma sposobów na dwa poprzednie stopnie. Backtracking "
            "policzy to samo, ale bez zapamiętywania powtórzy te same podproblemy wykładniczo wiele razy."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="najwieksza-suma-fragmentu",
        difficulty=3,
        spec=(
            "Tablica, która może zawierać liczby ujemne. Podaj największą sumę spójnego, "
            "niepustego fragmentu."
        ),
        prompt="Który wzorzec tu zadziała?",
        options=[
            "programowanie dynamiczne w jednym przejściu",
            "okno przesuwne",
            "dwa wskaźniki z obu końców",
            "wyszukiwanie binarne",
        ],
        answer="programowanie dynamiczne w jednym przejściu",
        spec_ref="może zawierać liczby ujemne",
        explanation=(
            "To jest pułapka na okno przesuwne. Okno działa, gdy rozszerzanie go zmienia warunek "
            "monotonicznie, a przy liczbach ujemnych suma potrafi spaść i znów urosnąć, więc "
            "kurczenie okna z lewej nic nie gwarantuje. Trzeba pamiętać najlepszą sumę kończącą "
            "się na bieżącej pozycji."
        ),
    ),
    dict(
        pattern="dp-2d",
        problem="wspolny-podciag",
        difficulty=3,
        spec=(
            "Dwa napisy. Podaj długość najdłuższego wspólnego podciągu, czyli ciągu znaków "
            "występujących w obu w tej samej kolejności, niekoniecznie obok siebie."
        ),
        options=[
            "programowanie dynamiczne po dwóch wymiarach",
            "okno przesuwne",
            "dwa wskaźniki idące równolegle",
            "zbiór haszujący",
        ],
        answer="programowanie dynamiczne po dwóch wymiarach",
        spec_ref="niekoniecznie obok siebie",
        explanation=(
            "Ten fragment przesądza wszystko. Gdyby znaki musiały stać obok siebie, byłby to "
            "wspólny podnapis i wystarczyłoby okno. Skoro mogą być rozrzucone, stan zależy od "
            "pozycji w obu napisach naraz, czyli od tablicy dwuwymiarowej."
        ),
    ),
    # --- zachłanne ---
    dict(
        pattern="greedy",
        problem="skoki",
        difficulty=2,
        spec=(
            "Tablica, w której wartość pola mówi, o ile najwyżej stopni możesz z niego skoczyć. "
            "Sprawdź, czy da się dojść z pierwszego pola na ostatnie."
        ),
        prompt="Który wzorzec wystarczy, żeby odpowiedzieć w czasie liniowym?",
        options=[
            "algorytm zachłanny z najdalszym zasięgiem",
            "programowanie dynamiczne po każdym polu",
            "przeszukiwanie wszerz",
            "backtracking",
        ],
        answer="algorytm zachłanny z najdalszym zasięgiem",
        spec_ref="da się dojść z pierwszego pola na ostatnie",
        explanation=(
            "Wystarczy jedno przejście i pamiętanie najdalszego osiągalnego pola. Programowanie "
            "dynamiczne odpowie tak samo, ale w czasie kwadratowym, bo sprawdza każdy skok z osobna."
        ),
    ),
    # --- przedziały ---
    dict(
        pattern="intervals",
        problem="scalanie",
        difficulty=2,
        spec="Lista przedziałów. Scal te nachodzące na siebie i zwróć listę rozłącznych przedziałów.",
        options=[
            "sortowanie po początku i scalanie w jednym przejściu",
            "kopiec bez sortowania",
            "okno przesuwne",
            "programowanie dynamiczne",
        ],
        answer="sortowanie po początku i scalanie w jednym przejściu",
        spec_ref="nachodzące na siebie",
        explanation=(
            "Po posortowaniu po początku wystarczy porównywać każdy przedział z ostatnim scalonym. "
            "Bez sortowania trzeba by porównywać każdy z każdym."
        ),
    ),
    dict(
        pattern="intervals",
        problem="sale",
        difficulty=3,
        spec=(
            "Lista spotkań z godziną początku i końca. Podaj najmniejszą liczbę sal potrzebną, "
            "żeby żadne dwa spotkania nie kolidowały."
        ),
        options=[
            "kopiec czasów zakończenia",
            "sortowanie po długości spotkania",
            "okno przesuwne",
            "backtracking po przydziałach",
        ],
        answer="kopiec czasów zakończenia",
        spec_ref="najmniejszą liczbę sal",
        explanation=(
            "Sortujesz po godzinie rozpoczęcia, a kopiec trzyma czasy zakończenia zajętych sal. "
            "Rozmiar kopca w szczycie to odpowiedź. Sortowanie po długości spotkania jest kuszące, "
            "ale długość nie mówi nic o tym, ile spotkań nakłada się w jednej chwili."
        ),
    ),
    # --- bity i matematyka ---
    dict(
        pattern="bit-manipulation",
        problem="pojedyncza-liczba",
        difficulty=2,
        spec=(
            "Tablica, w której każda wartość występuje dokładnie dwa razy poza jedną. Znajdź tę "
            "jedną, używając stałej pamięci."
        ),
        options=["różnica symetryczna bitowa (XOR)", "zbiór haszujący", "sortowanie", "dwa wskaźniki"],
        answer="różnica symetryczna bitowa (XOR)",
        spec_ref="używając stałej pamięci",
        explanation=(
            "XOR pary identycznych liczb daje zero, więc po przejściu całej tablicy zostaje sama "
            "wartość niesparowana. Zbiór haszujący jest oczywistszy, ale zużywa O(n) pamięci, "
            "czego treść zabrania."
        ),
    ),
    dict(
        pattern="math",
        problem="obrot-macierzy",
        difficulty=2,
        spec="Macierz kwadratowa. Obróć ją o 90 stopni zgodnie z ruchem wskazówek zegara, w miejscu.",
        options=[
            "transpozycja i odbicie kolumn",
            "przepisanie do nowej macierzy",
            "przeszukiwanie w głąb",
            "sortowanie wierszy",
        ],
        answer="transpozycja i odbicie kolumn",
        spec_ref="w miejscu",
        explanation=(
            "Obrót to złożenie dwóch operacji, które da się wykonać na miejscu: zamiany elementów "
            "względem przekątnej i odbicia każdego wiersza. Przepisanie do nowej macierzy jest "
            "prostsze, ale łamie warunek pracy w miejscu."
        ),
    ),
]
