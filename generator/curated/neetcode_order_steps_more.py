"""Kolejne szkielety rozwiązań z NeetCode 150 — typ `order-steps`, druga partia.

Uzupełnia kategorie, które nie miały ani jednego ćwiczenia tego typu (operacje
bitowe, matematyka) oraz te najcieńsze.

Każdy wpis podaje `deps`: dla kolejnego kroku listę wcześniejszych, których efekt
ten krok zużywa. Build sprawdza z nich, czy kolejność jest **jedyna możliwa** —
jeśli na którymkolwiek etapie dwa kroki są gotowe naraz, ćwiczenie ma dwie poprawne
odpowiedzi i zostaje odrzucone.

Przyjęta konwencja: krok zależy od poprzedniego również wtedy, gdy działa wewnątrz
pętli albo na strukturze, którą tamten założył. Dzięki temu „przygotuj kopiec”
i „weź kolejny element” nie są traktowane jako niezależne.
"""

CORPUS = {
    "id": "neetcode-150",
    "name": "NeetCode 150 — sedno",
}

DEFAULT_TYPE = "order-steps"

CHAIN = [[], [0], [1], [2], [3], [4]]

EXERCISES = [
    dict(
        pattern="bit-manipulation",
        problem="liczenie-bitow-kroki",
        difficulty=3,
        spec=(
            "Dla każdej liczby od zera do n podaj, ile ma jedynek w zapisie binarnym, "
            "w łącznym czasie liniowym."
        ),
        steps=[
            "utwórz tablicę wyników o długości n plus jeden i wpisz zero na pozycji zerowej",
            "przechodź liczby od jeden do n",
            "przesuń bieżącą liczbę o jeden bit w prawo",
            "odczytaj z tablicy gotowy wynik dla tak otrzymanej mniejszej liczby",
            "dodaj do niego najmłodszy bit bieżącej liczby",
            "zapisz sumę na pozycji bieżącej liczby",
        ],
        deps=CHAIN,
        explanation=(
            "Przesunięcie w prawo daje liczbę mniejszą, więc jej wynik jest już policzony. "
            "To zamienia liczenie bitów w programowanie dynamiczne o stałym koszcie na liczbę."
        ),
    ),
    dict(
        pattern="bit-manipulation",
        problem="suma-bez-plusa-kroki",
        difficulty=3,
        spec="Dodaj dwie liczby całkowite, nie używając operatora dodawania ani odejmowania.",
        steps=[
            "policz naraz dwie rzeczy: XOR obu liczb jako sumę bez przeniesień oraz AND jako miejsca przeniesień",
            "przesuń wynik AND o jeden bit w lewo, bo przeniesienie działa na pozycji wyższej",
            "podstaw sumę bez przeniesień jako nową pierwszą liczbę",
            "podstaw przesunięte przeniesienia jako nową drugą liczbę",
            "powtórz cały krok, dopóki druga liczba jest różna od zera",
            "gdy przeniesienia znikną, pierwsza liczba jest szukaną sumą",
        ],
        deps=CHAIN,
        explanation=(
            "Rozbicie dodawania na sumę bez przeniesień i same przeniesienia, powtarzane aż do "
            "wyzerowania tych drugich, odtwarza dokładnie działanie sumatora sprzętowego."
        ),
    ),
    dict(
        pattern="math",
        problem="spirala-kroki",
        difficulty=2,
        spec="Wypisz elementy macierzy, obchodząc ją spiralnie od lewego górnego rogu.",
        steps=[
            "zawiąż cztery granice: górny i dolny wiersz oraz lewą i prawą kolumnę",
            "przejdź górny wiersz od lewej do prawej i przesuń górną granicę w dół",
            "przejdź prawą kolumnę od góry do dołu i przesuń prawą granicę w lewo",
            "jeśli górna granica nie minęła dolnej, przejdź dolny wiersz od prawej do lewej i podnieś dolną granicę",
            "jeśli lewa granica nie minęła prawej, przejdź lewą kolumnę od dołu do góry i przesuń lewą granicę w prawo",
            "powtarzaj cały obieg, dopóki granice się nie miną",
        ],
        deps=CHAIN,
        explanation=(
            "Dwa sprawdzenia w środku nie są ozdobnikiem: bez nich macierz o jednym wierszu albo "
            "jednej kolumnie zostaje przejściem wypisana drugi raz w przeciwną stronę."
        ),
    ),
    dict(
        pattern="math",
        problem="zerowanie-macierzy-kroki",
        difficulty=3,
        spec=(
            "Jeśli komórka macierzy zawiera zero, wyzeruj cały jej wiersz i kolumnę. "
            "Bez dodatkowej pamięci rosnącej z rozmiarem macierzy."
        ),
        steps=[
            "sprawdź osobno, czy pierwszy wiersz i pierwsza kolumna zawierają zero, i zapamiętaj to w dwóch zmiennych",
            "przejdź pozostałe komórki i dla każdego zera wpisz znacznik w pierwszej komórce jego wiersza i kolumny",
            "przejdź pozostałe komórki drugi raz, czytając znaczniki z brzegów",
            "wyzeruj komórkę, jeśli jej wiersz albo kolumna ma znacznik",
            "gdy znaczniki są już zużyte, wróć do samych brzegów",
            "wyzeruj pierwszy wiersz i pierwszą kolumnę zgodnie z zapamiętanymi na początku zmiennymi",
        ],
        deps=CHAIN,
        explanation=(
            "Brzegi trzeba rozstrzygnąć na samym początku i wyzerować na samym końcu, bo w "
            "międzyczasie pełnią rolę znaczników. Zerowanie ich wcześniej skasowałoby informację, "
            "z której korzysta krok czwarty."
        ),
    ),
    dict(
        pattern="dp-2d",
        problem="unikalne-sciezki-kroki",
        difficulty=2,
        spec=(
            "Policz, na ile sposobów da się przejść z lewego górnego rogu siatki do prawego "
            "dolnego, ruszając się tylko w prawo albo w dół."
        ),
        steps=[
            "utwórz tablicę o wymiarach siatki",
            "wpisz jedynkę w całym pierwszym wierszu i w całej pierwszej kolumnie, bo prowadzi tam jedna droga",
            "przechodź pozostałe komórki wierszami, od lewej do prawej",
            "zsumuj liczbę dróg do komórki nad bieżącą i do komórki po jej lewej",
            "zapisz tę sumę w bieżącej komórce",
            "po wypełnieniu tablicy odczytaj wynik z prawego dolnego rogu",
        ],
        deps=CHAIN,
        explanation=(
            "Do każdego pola da się wejść tylko z góry albo z lewej, więc liczba dróg jest sumą "
            "tych dwóch. Brzegi wypełnia się osobno, bo tam jedna z tych możliwości nie istnieje."
        ),
    ),
    dict(
        pattern="advanced-graphs",
        problem="dijkstra-kroki",
        difficulty=3,
        spec=(
            "Graf skierowany z dodatnimi wagami. Podaj najkrótsze odległości od zadanego "
            "wierzchołka do wszystkich pozostałych."
        ),
        steps=[
            "zbuduj listy sąsiedztwa wraz z wagami krawędzi",
            "przygotuj kopiec minimalny i wrzuć do niego wierzchołek startowy z kosztem zero",
            "zdejmij z kopca wierzchołek o najmniejszym znanym koszcie",
            "pomiń go, jeśli był już domknięty, a w przeciwnym razie zapisz jego koszt jako ostateczny",
            "dla każdego sąsiada policz koszt dojścia przez ten wierzchołek",
            "wrzuć sąsiada na kopiec, jeśli tak policzony koszt jest lepszy od dotychczas znanego",
        ],
        deps=CHAIN,
        explanation=(
            "Sprawdzenie, czy wierzchołek był już domknięty, zastępuje kosztowne usuwanie "
            "nieaktualnych wpisów z kopca. To dlatego ten sam wierzchołek może w kopcu leżeć "
            "kilka razy i nie jest to błąd."
        ),
    ),
    dict(
        pattern="trie",
        problem="trie-kroki",
        difficulty=2,
        spec="Zaprojektuj strukturę pozwalającą wstawiać słowa i sprawdzać ich obecność oraz przedrostki.",
        steps=[
            "zawiąż węzeł korzenia z pustą mapą dzieci i znacznikiem końca słowa",
            "przy wstawianiu idź od korzenia znak po znaku",
            "gdy dziecka dla bieżącego znaku nie ma, utwórz je i wpisz do mapy",
            "zejdź do tego dziecka i przejdź do następnego znaku",
            "po ostatnim znaku ustaw w bieżącym węźle znacznik końca słowa",
            "wyszukiwanie idzie tą samą ścieżką i różni się tylko tym, czy na końcu wymaga znacznika",
        ],
        deps=CHAIN,
        explanation=(
            "Cała różnica między pytaniem o słowo a pytaniem o przedrostek siedzi w ostatnim "
            "kroku: przedrostkowi wystarczy dojście do węzła, słowo wymaga jeszcze znacznika."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="najdluzszy-ciag-kroki",
        difficulty=3,
        spec=(
            "Podaj długość najdłuższego ciągu kolejnych liczb występujących w tablicy, "
            "w czasie liniowym."
        ),
        steps=[
            "wrzuć wszystkie liczby do zbioru haszującego",
            "przechodź liczby ze zbioru",
            "sprawdź, czy w zbiorze jest liczba o jeden mniejsza od bieżącej",
            "gdy jest, pomiń bieżącą liczbę, bo nie zaczyna ciągu",
            "gdy jej nie ma, licz w górę, dopóki kolejne następniki są w zbiorze",
            "zaktualizuj najlepszy wynik długością policzonego ciągu",
        ],
        deps=[[], [0], [1], [2], [2, 3], [4]],
        explanation=(
            "Warunek z kroku trzeciego jest tym, co daje liniowość: bez niego ten sam ciąg byłby "
            "przechodzony od każdego swojego elementu i całość zrobiłaby się kwadratowa."
        ),
    ),
    dict(
        pattern="graphs",
        problem="zbedna-krawedz-kroki",
        difficulty=3,
        spec=(
            "Graf nieskierowany powstały z drzewa przez dodanie jednej krawędzi. Wskaż tę "
            "krawędź, która domyka cykl."
        ),
        steps=[
            "zawiąż tablicę rodziców, w której każdy wierzchołek jest na początku swoim własnym",
            "weź kolejną krawędź z wejścia",
            "znajdź korzenie obu jej końców, skracając po drodze ścieżki",
            "gdy korzenie są równe, ta krawędź domyka cykl i jest szukaną odpowiedzią",
            "gdy są różne, podepnij jeden korzeń pod drugi",
            "przejdź do następnej krawędzi i powtarzaj aż do końca listy",
        ],
        deps=[[], [0], [1], [2], [2, 3], [4]],
        explanation=(
            "Struktura zbiorów rozłącznych odpowiada w czasie prawie stałym na pytanie, czy dwa "
            "wierzchołki są już połączone. Krawędź łącząca wierzchołki z tego samego zbioru jest "
            "dokładnie tą, która tworzy cykl."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="slowo-lamane-kroki",
        difficulty=3,
        spec=(
            "Sprawdź, czy napis da się rozłożyć na ciąg słów ze słownika, przy czym słów wolno "
            "używać wielokrotnie."
        ),
        steps=[
            "wrzuć słownik do zbioru haszującego, żeby sprawdzenie słowa było stałe",
            "utwórz tablicę logiczną o długości napisu plus jeden i ustaw prawdę na pozycji zerowej",
            "przechodź pozycje napisu od lewej do prawej",
            "pomiń pozycję, jeśli nie da się do niej dojść, czyli tablica ma tam fałsz",
            "dla osiągalnej pozycji sprawdź każdy fragment zaczynający się w niej",
            "gdy fragment należy do zbioru, ustaw prawdę na pozycji tuż za jego końcem",
        ],
        deps=CHAIN,
        explanation=(
            "Prawda na pozycji zerowej to warunek początkowy: pusty przedrostek zawsze da się "
            "rozłożyć. Bez niego żadna pozycja nie byłaby osiągalna i wynik zawsze wychodziłby "
            "fałszywy."
        ),
    ),
]
