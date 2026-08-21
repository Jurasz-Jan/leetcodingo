"""Przypadki brzegowe z NeetCode 150 — typ `edge-case`.

Tu treść opisuje **podejście, które wygląda na poprawne**, a pytanie brzmi: co je łamie.
To jest inna umiejętność niż rozpoznanie wzorca i inna niż znalezienie sedna. Na
rozmowie najczęściej przegrywa się właśnie tutaj: rozwiązanie jest w zasadzie dobre,
a wykłada się na jednym wejściu, o którym nikt nie pomyślał.

Dobór jest celowy: każdy przypadek to pomyłka, którą realnie się popełnia, a nie
sztucznie skonstruowana złośliwość. Dlatego dystraktory są zawsze wejściami tego
samego rodzaju co poprawna odpowiedź — nie da się jej wskazać po samym kształcie.

`spec_ref` nie jest tu wymagany: odpowiedź uzasadnia prześledzenie podejścia na danym
wejściu, a nie cytat z treści. Wyjaśnienie musi za to podawać, co podejście zwraca
i co powinno zwrócić.

Treści są własne. Lista NeetCode wyznacza dobór zadań, nie brzmienie opisów.
"""

CORPUS = {
    "id": "neetcode-150",
    "name": "NeetCode 150 — sedno",
}

DEFAULT_TYPE = "edge-case"

EXERCISES = [
    dict(
        pattern="trees",
        problem="czy-bst-przypadek",
        difficulty=3,
        spec=(
            "Sprawdzasz, czy drzewo binarne jest drzewem BST, porównując w każdym węźle jego "
            "wartość z wartościami jego dwóch dzieci."
        ),
        prompt="Który układ przejdzie ten test, choć nie jest drzewem BST?",
        options=[
            "korzeń 5, prawe dziecko 7, a lewe dziecko siódemki to 4",
            "korzeń 5, lewe dziecko 7, bez innych węzłów",
            "korzeń 5, lewe dziecko 3, prawe dziecko 8",
            "korzeń 5 bez żadnych dzieci",
        ],
        answer="korzeń 5, prawe dziecko 7, a lewe dziecko siódemki to 4",
        explanation=(
            "Porównanie z dziećmi widzi tylko sąsiedztwo. Czwórka jest mniejsza od korzenia, a "
            "leży w jego prawym poddrzewie, więc drzewo nie jest BST — ale lokalnie wszystko się "
            "zgadza, bo 4 jest mniejsze od 7. Dlatego w dół trzeba przekazywać przedział "
            "dopuszczalnych wartości, a nie porównywać z pojedynczym węzłem."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="najwieksza-suma-przypadek",
        difficulty=3,
        spec=(
            "Liczysz największą sumę spójnego niepustego fragmentu tablicy. Zaczynasz od wyniku "
            "równego zero, dodajesz kolejne elementy, a gdy bieżąca suma zrobi się ujemna, zerujesz ją."
        ),
        prompt="Które wejście da zły wynik?",
        options=["[-3, -1, -2]", "[1, 2, 3]", "[-1, 5, -2]", "[0, 0, 0]"],
        answer="[-3, -1, -2]",
        explanation=(
            "Start od zera po cichu zakłada, że pusty fragment jest dopuszczalny. Dla samych liczb "
            "ujemnych podejście zwróci 0, a poprawną odpowiedzią jest -1, czyli największy "
            "pojedynczy element. Lekarstwem jest start od pierwszego elementu, nie od zera."
        ),
    ),
    dict(
        pattern="greedy",
        problem="reszta-zachlanna-przypadek",
        difficulty=2,
        spec=(
            "Wydajesz resztę, biorąc za każdym razem największy nominał, który mieści się w "
            "pozostałej kwocie, i tak aż do wyzerowania."
        ),
        prompt="Przy których nominałach i kwocie to podejście da za dużo monet?",
        options=[
            "nominały 1, 3, 4 i kwota 6",
            "nominały 1, 2, 5 i kwota 6",
            "nominały 1, 5, 10 i kwota 30",
            "nominały 2, 4, 8 i kwota 14",
        ],
        answer="nominały 1, 3, 4 i kwota 6",
        explanation=(
            "Zachłannie wychodzi 4 plus 1 plus 1, czyli trzy monety, a wystarczą dwie po 3. "
            "Reguła działa dla zestawów, w których każdy nominał jest wielokrotnością mniejszego, "
            "i dlatego wydaje się oczywista — prawdziwe waluty są tak zbudowane."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="usun-n-ty-przypadek",
        difficulty=2,
        spec=(
            "Usuwasz n-ty węzeł od końca listy jednokierunkowej: prowadzisz dwa wskaźniki "
            "oddalone o n węzłów i usuwasz ten, który stoi tuż za wolniejszym."
        ),
        prompt="Który przypadek wymaga osobnej obsługi?",
        options=[
            "lista ma trzy węzły, a n równa się trzy",
            "lista ma trzy węzły, a n równa się jeden",
            "lista ma trzy węzły, a n równa się dwa",
            "lista ma pięć węzłów, a n równa się dwa",
        ],
        answer="lista ma trzy węzły, a n równa się trzy",
        explanation=(
            "Gdy n równa się długości listy, usuwany jest pierwszy węzeł, a wtedy nie istnieje "
            "poprzednik, któremu można by przepiąć wskaźnik. Standardowym lekarstwem jest węzeł "
            "wartowniczy przed głową: usunięcie głowy przestaje być wyjątkiem i kod nie potrzebuje "
            "osobnej gałęzi."
        ),
    ),
    dict(
        pattern="stack",
        problem="nawiasy-licznikiem-przypadek",
        difficulty=3,
        spec=(
            "Sprawdzasz poprawność nawiasowania, licząc dla każdego rodzaju nawiasu osobno "
            "otwarcia i zamknięcia. Pilnujesz, żeby żaden licznik nie zszedł poniżej zera i żeby "
            "na końcu wszystkie wynosiły zero."
        ),
        prompt="Które wejście przejdzie, mimo że nawiasowanie jest błędne?",
        options=['"([)]"', '"(()"', '")("', '"([])"'],
        answer='"([)]"',
        explanation=(
            "Liczniki zgadzają się co do sztuk i nigdy nie schodzą poniżej zera, bo każdy rodzaj "
            "jest liczony osobno. Nie zgadza się natomiast zagnieżdżenie: nawias kwadratowy zostaje "
            "otwarty wewnątrz okrągłego, a zamknięty na zewnątrz. Kolejności nie da się sprawdzić "
            "licznikami, trzeba pamiętać, co zostało otwarte ostatnio, czyli użyć stosu."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="dekodowanie-przypadek",
        difficulty=3,
        spec=(
            "Liczysz, na ile sposobów da się odczytać napis cyfr, gdzie 1 to A, a 26 to Z. Dla "
            "każdej pozycji dodajesz wynik z pozycji poprzedniej oraz wynik sprzed dwóch pozycji, "
            "jeśli ostatnie dwie cyfry tworzą liczbę nie większą niż 26."
        ),
        prompt="Które wejście da zły wynik?",
        options=['"30"', '"26"', '"12"', '"11"'],
        answer='"30"',
        explanation=(
            "Napisu 30 nie da się odczytać w żaden sposób: 30 przekracza 26, a zero samo w sobie "
            "nie koduje litery, więc poprawną odpowiedzią jest zero sposobów. Podejście, które "
            "sprawdza tylko górne ograniczenie dwucyfrowego kodu, doda wynik z pozycji poprzedniej "
            "i wyliczy 1. Brakuje warunku, że pojedyncza cyfra musi być różna od zera."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="palindrom-przypadek",
        difficulty=2,
        spec=(
            "Sprawdzasz, czy napis jest palindromem: ustawiasz wskaźniki na obu końcach, "
            "przesuwasz je ku sobie i po drodze pomijasz znaki, które nie są literami ani cyframi."
        ),
        prompt="Który przypadek najłatwiej wywraca taką implementację?",
        options=[
            "napis złożony wyłącznie ze znaków interpunkcyjnych",
            "napis o parzystej długości",
            "napis zapisany samymi wielkimi literami",
            "napis o długości jeden",
        ],
        answer="napis złożony wyłącznie ze znaków interpunkcyjnych",
        explanation=(
            "Gdy wszystkie znaki są pomijane, wewnętrzne pętle przewijające wskaźniki wybiegają "
            "poza napis, o ile nie sprawdzają dodatkowo, czy wskaźniki się jeszcze nie minęły. "
            "Poprawną odpowiedzią jest wtedy „tak”, bo napis pusty po odfiltrowaniu jest palindromem."
        ),
    ),
    dict(
        pattern="intervals",
        problem="scalanie-przypadek",
        difficulty=2,
        spec=(
            "Scalasz przedziały: sortujesz je po początku i łączysz bieżący z ostatnim wtedy, gdy "
            "początek bieżącego jest ostro mniejszy od końca ostatniego."
        ),
        prompt="Która para zostanie potraktowana inaczej, niż zwykle się tego oczekuje?",
        options=[
            "przedziały [1, 2] oraz [2, 3]",
            "przedziały [1, 5] oraz [2, 3]",
            "przedziały [1, 2] oraz [5, 6]",
            "przedziały [1, 3] oraz [2, 4]",
        ],
        answer="przedziały [1, 2] oraz [2, 3]",
        explanation=(
            "Przy ostrej nierówności przedziały stykające się końcami nie zostaną scalone, choć "
            "zwykle chcemy z [1, 2] i [2, 3] dostać [1, 3]. To nie jest błąd w kodzie, tylko "
            "niezapisana decyzja projektowa — i dokładnie taki przypadek trzeba rozstrzygnąć w "
            "specyfikacji, zamiast zgadywać go z implementacji."
        ),
    ),
    dict(
        pattern="graphs",
        problem="bfs-oznaczanie-przypadek",
        difficulty=3,
        spec=(
            "Liczysz najkrótszą drogę przeszukiwaniem wszerz. Wierzchołek oznaczasz jako "
            "odwiedzony w chwili, gdy zdejmujesz go z kolejki."
        ),
        prompt="Co się przy tym psuje?",
        options=[
            "ten sam wierzchołek trafia do kolejki wiele razy, więc przy gęstym grafie kolejka puchnie",
            "wynikowa najkrótsza droga wychodzi za długa",
            "algorytm nie znajduje celu, gdy graf zawiera cykl",
            "kolejność odwiedzania przestaje odpowiadać poziomom",
        ],
        answer="ten sam wierzchołek trafia do kolejki wiele razy, więc przy gęstym grafie kolejka puchnie",
        explanation=(
            "Wynik pozostaje poprawny i poziomy się zgadzają, więc błąd nie objawia się złą "
            "odpowiedzią, tylko czasem i pamięcią. Zanim wierzchołek zostanie zdjęty, każdy jego "
            "sąsiad zdąży go dorzucić do kolejki. Oznaczanie w chwili wkładania usuwa problem."
        ),
    ),
    dict(
        pattern="heap",
        problem="dwa-kopce-przypadek",
        difficulty=3,
        spec=(
            "Utrzymujesz medianę strumienia: mniejszą połowę trzymasz w kopcu maksymalnym, "
            "większą w minimalnym, a po każdej wstawce wyrównujesz rozmiary obu kopców."
        ),
        prompt="Czego samo wyrównywanie rozmiarów nie zapewnia?",
        options=[
            "że wierzchołek kopca mniejszej połowy jest naprawdę mniejszy od wierzchołka większej",
            "że mediana leży na wierzchołku któregoś z kopców",
            "że kopce zawierają łącznie tyle elementów, ile wstawiono",
            "że pojedyncza wstawka kosztuje czas logarytmiczny",
        ],
        answer="że wierzchołek kopca mniejszej połowy jest naprawdę mniejszy od wierzchołka większej",
        explanation=(
            "Rozmiary mogą się idealnie zgadzać, a element i tak wylądował w niewłaściwej połowie: "
            "wstawiony do mniejszej okazuje się większy od wierzchołka większej. Dlatego po wstawce "
            "trzeba najpierw przełożyć wierzchołek między kopcami, a dopiero potem wyrównywać "
            "rozmiary. Sam podział na dwa kopce niczego nie gwarantuje."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="podzbiory-przypadek",
        difficulty=2,
        spec=(
            "Generujesz wszystkie podzbiory: przy każdym wywołaniu rekurencyjnym dopisujesz "
            "bieżący stan do wyniku, a przy powrocie zdejmujesz ostatni dołożony element."
        ),
        prompt="Jaki błąd najłatwiej tu popełnić?",
        options=[
            "dopisanie do wyniku tej samej listy zamiast jej kopii, przez co na końcu wszystkie wpisy są puste",
            "pominięcie zbioru pustego",
            "wygenerowanie każdego podzbioru dwa razy",
            "przekroczenie dopuszczalnej głębokości rekurencji przy kilku elementach",
        ],
        answer="dopisanie do wyniku tej samej listy zamiast jej kopii, przez co na końcu wszystkie wpisy są puste",
        explanation=(
            "Lista stanu jest modyfikowana w miejscu przy cofaniu się, więc wszystkie wpisy w "
            "wyniku pokazują na ten sam obiekt, a ten po zakończeniu rekurencji jest pusty. "
            "Objaw jest mylący: liczba podzbiorów się zgadza, tylko wszystkie są puste."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="obrocona-z-powtorzeniami-przypadek",
        difficulty=3,
        spec=(
            "Szukasz minimum w tablicy posortowanej i obróconej, porównując element środkowy z "
            "prawym skrajnym i odrzucając połowę, po której minimum leżeć nie może."
        ),
        prompt="Który przypadek psuje ten schemat?",
        options=["[2, 2, 2, 0, 2]", "[3, 4, 5, 1, 2]", "[1, 2, 3, 4, 5]", "[2, 1]"],
        answer="[2, 2, 2, 0, 2]",
        explanation=(
            "Gdy element środkowy równa się prawemu skrajnemu, porównanie nie mówi nic o tym, po "
            "której stronie leży minimum, i podział połówkowy przestaje rozstrzygać. Wersja z "
            "powtórzeniami musi wtedy zsuwać prawą granicę o jeden, przez co w najgorszym razie "
            "traci gwarancję czasu logarytmicznego i schodzi do liniowego."
        ),
    ),
]
