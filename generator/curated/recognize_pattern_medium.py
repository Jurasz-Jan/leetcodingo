"""Kurowane `recognize-pattern` — poziom medium z listy NeetCode 150.

Druga partia, rozłączna z `recognize_pattern.py`. Ten sam identyfikator korpusu,
więc build scala obie w jeden plik.

Dobór jest celowy: każde zadanie uczy jednej rozstrzygającej różnicy, a nie samej
nazwy wzorca. Dlatego dystraktorem jest tu zwykle rozwiązanie, które **daje poprawny
wynik, ale łamie warunek z treści** (złożoność, pamięć, jedno przejście), albo takie,
które działa na typowych danych i wykłada się na przypadku granicznym.

Treści są własne. Lista NeetCode wyznacza dobór problemów, nie brzmienie zadań.
"""

CORPUS = {
    "id": "recognize-pattern",
    "name": "Rozpoznaj wzorzec",
}

EXERCISES = [
    # --- tablice i haszowanie ---
    dict(
        pattern="arrays-hashing",
        problem="najdluzszy-ciag-kolejnych",
        difficulty=3,
        spec=(
            "Nieuporządkowana tablica liczb całkowitych. Podaj długość najdłuższego ciągu "
            "kolejnych liczb, które w niej występują. Rozwiązanie ma działać w czasie liniowym."
        ),
        options=[
            "zbiór haszujący i liczenie tylko od początków ciągów",
            "sortowanie i jedno przejście",
            "okno przesuwne",
            "programowanie dynamiczne",
        ],
        answer="zbiór haszujący i liczenie tylko od początków ciągów",
        spec_ref="w czasie liniowym",
        explanation=(
            "Sortowanie daje poprawny wynik, ale kosztuje O(n log n), a treść wymaga czasu "
            "liniowego. Ze zbiorem sprawdzasz dla każdej liczby, czy nie ma poprzednika, i tylko "
            "wtedy liczysz w górę, dzięki czemu każdy element odwiedzasz raz."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="kodowanie-napisow",
        difficulty=2,
        spec=(
            "Zamień listę napisów na jeden napis i z powrotem. Napisy mogą zawierać dowolne "
            "znaki, także te, których chciałbyś użyć jako separatora."
        ),
        options=[
            "długość zapisana przed każdym napisem",
            "sklejenie rzadko używanym separatorem",
            "zbiór haszujący",
            "sortowanie napisów przed sklejeniem",
        ],
        answer="długość zapisana przed każdym napisem",
        spec_ref="których chciałbyś użyć jako separatora",
        explanation=(
            "Separator zawodzi zawsze, gdy trafi się w danych, a treść mówi wprost, że może. "
            "Długość przed napisem mówi dekoderowi, ile znaków przeczytać, i nie zależy od tego, "
            "co w nich jest."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="sudoku",
        difficulty=2,
        spec=(
            "Plansza dziewięć na dziewięć, częściowo wypełniona. Sprawdź, czy nie łamie zasad: "
            "cyfra nie może się powtórzyć w żadnym wierszu, żadnej kolumnie ani żadnym kwadracie "
            "trzy na trzy."
        ),
        options=[
            "trzy rodziny zbiorów: wiersze, kolumny, kwadraty",
            "sortowanie każdego wiersza i kolumny",
            "backtracking",
            "okno przesuwne po planszy",
        ],
        answer="trzy rodziny zbiorów: wiersze, kolumny, kwadraty",
        spec_ref="ani żadnym kwadracie",
        explanation=(
            "Jedno przejście po planszy aktualizuje trzy zbiory naraz, a indeks kwadratu wychodzi "
            "z podzielenia obu współrzędnych przez trzy. Backtracking służy do wypełniania sudoku, "
            "a nie do sprawdzania planszy już wypełnionej."
        ),
    ),
    # --- dwa wskaźniki ---
    dict(
        pattern="two-pointers",
        problem="trojka-do-zera",
        difficulty=3,
        spec=(
            "Tablica liczb. Znajdź wszystkie różne trójki sumujące się do zera. Ta sama trójka "
            "nie może pojawić się w wyniku dwa razy."
        ),
        options=[
            "sortowanie i dwa wskaźniki dla każdego ustalonego elementu",
            "słownik jak przy szukaniu pary o danej sumie",
            "backtracking po wszystkich trójkach",
            "okno przesuwne",
        ],
        answer="sortowanie i dwa wskaźniki dla każdego ustalonego elementu",
        spec_ref="nie może pojawić się w wyniku dwa razy",
        explanation=(
            "Sortowanie załatwia dwie rzeczy naraz: pozwala zwijać parę dwoma wskaźnikami i "
            "ustawia duplikaty obok siebie, więc pomija się je jednym warunkiem. Słownik znajdzie "
            "trójki, ale odsianie powtórzeń robi się wtedy osobnym, kłopotliwym problemem."
        ),
    ),
    # --- okno przesuwne ---
    dict(
        pattern="sliding-window",
        problem="zamiana-znakow",
        difficulty=3,
        spec=(
            "Napis i liczba k. Możesz zmienić najwyżej k znaków na dowolne inne. Podaj długość "
            "najdłuższego spójnego fragmentu złożonego z jednego powtarzającego się znaku."
        ),
        options=[
            "okno przesuwne z licznikiem najczęstszego znaku",
            "programowanie dynamiczne",
            "backtracking po zamianach",
            "dwa wskaźniki z obu końców",
        ],
        answer="okno przesuwne z licznikiem najczęstszego znaku",
        spec_ref="najwyżej k znaków",
        explanation=(
            "Okno jest dopuszczalne, dopóki jego długość minus liczba wystąpień najczęstszego "
            "znaku nie przekracza k, bo tyle znaków trzeba zmienić. Backtracking po zamianach "
            "rozważa wykładniczo wiele wariantów, choć wszystko rozstrzyga ten jeden warunek."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="permutacja-w-napisie",
        difficulty=2,
        spec=(
            "Dwa napisy. Sprawdź, czy drugi zawiera fragment będący permutacją pierwszego. "
            "Taki fragment ma dokładnie tyle znaków, ile pierwszy napis."
        ),
        options=[
            "okno stałej długości z licznikiem znaków",
            "okno o zmiennej długości",
            "backtracking po permutacjach",
            "sortowanie obu napisów",
        ],
        answer="okno stałej długości z licznikiem znaków",
        spec_ref="dokładnie tyle znaków",
        explanation=(
            "Długość jest z góry znana, więc okno się nie kurczy ani nie rośnie, tylko przesuwa: "
            "jeden znak wchodzi, jeden wychodzi. Generowanie permutacji jest wykładnicze i zbędne, "
            "bo permutację rozpoznaje się po samych licznikach znaków."
        ),
    ),
    # --- stos ---
    dict(
        pattern="stack",
        problem="stos-z-minimum",
        difficulty=2,
        spec=(
            "Zaprojektuj stos, który poza wkładaniem i zdejmowaniem podaje najmniejszy "
            "przechowywany element w czasie stałym."
        ),
        options=[
            "drugi stos z historią minimów",
            "przeliczanie minimum przy każdym pytaniu",
            "kopiec minimalny obok stosu",
            "lista utrzymywana w porządku rosnącym",
        ],
        answer="drugi stos z historią minimów",
        spec_ref="w czasie stałym",
        explanation=(
            "Równolegle z danymi rośnie stos minimów, więc zdjęcie elementu samo przywraca "
            "poprzednie minimum. Kopiec daje odczyt minimum w czasie stałym, ale usunięcie "
            "dowolnego elementu przy zdejmowaniu ze stosu kosztuje już O(n)."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="generowanie-nawiasow",
        difficulty=2,
        spec="Liczba n. Wypisz wszystkie poprawne sposoby ustawienia n par nawiasów.",
        prompt="Który wzorzec rozwiązuje to zadanie, mimo że dotyczy nawiasów?",
        options=["backtracking", "stos", "programowanie dynamiczne", "kolejka"],
        answer="backtracking",
        spec_ref="wszystkie poprawne sposoby",
        explanation=(
            "Stos sprawdza, czy gotowe nawiasowanie jest poprawne, ale tutaj nie ma czego "
            "sprawdzać: trzeba wygenerować każdy wariant. Budujesz napis znak po znaku, pilnując, "
            "żeby zamykających nigdy nie było więcej niż otwierających."
        ),
    ),
    # --- wyszukiwanie binarne ---
    dict(
        pattern="binary-search",
        problem="szukanie-w-obroconej",
        difficulty=3,
        spec=(
            "Tablica posortowana rosnąco, a potem obrócona, bez powtórzeń. Znajdź indeks zadanej "
            "wartości albo stwierdź, że jej nie ma."
        ),
        options=[
            "wyszukiwanie binarne z rozpoznaniem posortowanej połowy",
            "przejście liniowe",
            "dwa wskaźniki z obu końców",
            "słownik wartości na indeksy",
        ],
        answer="wyszukiwanie binarne z rozpoznaniem posortowanej połowy",
        spec_ref="a potem obrócona",
        explanation=(
            "Przy każdym podziale jedna połowa pozostaje posortowana i wystarczy sprawdzić, czy "
            "szukana wartość mieści się w jej zakresie, żeby odrzucić drugą. Słownik odpowie "
            "szybko, ale najpierw trzeba go zbudować w O(n) pamięci."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="magazyn-czasowy",
        difficulty=3,
        spec=(
            "Struktura zapisuje wartości pod kluczem wraz ze znacznikiem czasu, zawsze rosnącym. "
            "Zapytanie ma zwrócić wartość zapisaną w najpóźniejszej chwili nie późniejszej niż podana."
        ),
        options=[
            "słownik list i wyszukiwanie binarne po czasie",
            "sam słownik z kluczem złożonym z nazwy i czasu",
            "kopiec po znaczniku czasu",
            "okno przesuwne",
        ],
        answer="słownik list i wyszukiwanie binarne po czasie",
        spec_ref="nie późniejszej niż podana",
        explanation=(
            "Sam słownik odpowie tylko na pytanie o dokładny znacznik, a pytanie brzmi o "
            "najbliższy wcześniejszy. Skoro zapisy przychodzą w rosnącym czasie, lista pod kluczem "
            "jest już posortowana i szukanie sprowadza się do podziału połówkowego."
        ),
    ),
    # --- listy ---
    dict(
        pattern="linked-list",
        problem="n-ty-od-konca",
        difficulty=2,
        spec=(
            "Lista jednokierunkowa. Usuń n-ty węzeł licząc od końca, przechodząc listę tylko raz."
        ),
        options=[
            "dwa wskaźniki oddalone o n węzłów",
            "policzenie długości i drugie przejście",
            "stos wszystkich węzłów",
            "rekurencja z tablicą pomocniczą",
        ],
        answer="dwa wskaźniki oddalone o n węzłów",
        spec_ref="przechodząc listę tylko raz",
        explanation=(
            "Pierwszy wskaźnik wysuwa się o n węzłów, potem oba idą razem, więc gdy pierwszy "
            "dobiega końca, drugi stoi tuż przed szukanym. Policzenie długości daje ten sam wynik, "
            "ale wymaga drugiego przejścia, czego treść zabrania."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="lru",
        difficulty=3,
        spec=(
            "Zaprojektuj pamięć podręczną o ustalonej pojemności, która przy przepełnieniu usuwa "
            "element najdawniej używany. Odczyt i zapis mają działać w czasie stałym."
        ),
        options=[
            "słownik i lista dwukierunkowa",
            "sam słownik ze znacznikami ostatniego użycia",
            "kopiec uporządkowany czasem użycia",
            "zwykła kolejka",
        ],
        answer="słownik i lista dwukierunkowa",
        spec_ref="w czasie stałym",
        explanation=(
            "Słownik daje dostęp po kluczu, a lista dwukierunkowa pozwala wyjąć węzeł ze środka i "
            "przenieść na początek bez przechodzenia listy. Znaczniki czasu wymagałyby szukania "
            "najstarszego wpisu w O(n), a kopiec kosztuje O(log n), więc oba łamią warunek."
        ),
    ),
    # --- drzewa ---
    dict(
        pattern="trees",
        problem="lca-bst",
        difficulty=2,
        spec=(
            "Drzewo BST i dwa jego węzły. Znajdź ich najniższego wspólnego przodka, wykorzystując "
            "porządek wartości w drzewie."
        ),
        options=[
            "schodzenie w dół według porównania wartości",
            "przeszukiwanie w głąb całego drzewa",
            "zapamiętanie obu ścieżek od korzenia",
            "przeszukiwanie wszerz",
        ],
        answer="schodzenie w dół według porównania wartości",
        spec_ref="wykorzystując porządek wartości",
        explanation=(
            "Obie wartości mniejsze od bieżącej, więc w lewo; obie większe, więc w prawo; a gdy "
            "się rozchodzą, stoisz u przodka. Ogólny algorytm dla dowolnego drzewa binarnego też "
            "zadziała, ale odwiedzi całe drzewo zamiast jednej ścieżki."
        ),
    ),
    dict(
        pattern="trees",
        problem="widok-z-prawej",
        difficulty=2,
        spec=(
            "Drzewo binarne. Podaj wartości widoczne przy patrzeniu z prawej strony, czyli po "
            "jednym węźle z każdego poziomu."
        ),
        options=[
            "przeszukiwanie wszerz i ostatni węzeł poziomu",
            "schodzenie zawsze do prawego dziecka",
            "kopiec",
            "stos monotoniczny",
        ],
        answer="przeszukiwanie wszerz i ostatni węzeł poziomu",
        spec_ref="po jednym węźle z każdego poziomu",
        explanation=(
            "Kolejka podaje poziomy w całości, więc bierzesz z każdego ostatni węzeł. Schodzenie "
            "zawsze w prawo gubi poziomy, na których prawe poddrzewo już się skończyło, a lewe "
            "jeszcze sięga w dół."
        ),
    ),
    # --- drzewa trie ---
    dict(
        pattern="trie",
        problem="slowa-z-jokerem",
        difficulty=3,
        spec=(
            "Struktura przechowuje słowa i odpowiada na zapytania, w których kropka zastępuje "
            "dowolny pojedynczy znak."
        ),
        options=[
            "drzewo trie z przeszukiwaniem w głąb przy kropce",
            "drzewo trie ze schodzeniem jedną ścieżką",
            "zbiór haszujący pełnych słów",
            "dopasowanie wyrażeniem regularnym do każdego słowa",
        ],
        answer="drzewo trie z przeszukiwaniem w głąb przy kropce",
        spec_ref="kropka zastępuje dowolny pojedynczy znak",
        explanation=(
            "Kropka rozgałęzia poszukiwanie: trzeba spróbować wszystkich dzieci i cofnąć się, gdy "
            "gałąź zawiedzie. Schodzenie jedną ścieżką, jak przy zwykłym trie, obsłuży tylko "
            "zapytania bez kropki."
        ),
    ),
    # --- kopce ---
    dict(
        pattern="heap",
        problem="k-najblizszych-punktow",
        difficulty=2,
        spec=(
            "Punkty na płaszczyźnie i liczba k. Podaj k punktów leżących najbliżej początku "
            "układu współrzędnych."
        ),
        options=[
            "kopiec rozmiaru k",
            "sortowanie wszystkich punktów",
            "okno przesuwne",
            "wyszukiwanie binarne po odległości",
        ],
        answer="kopiec rozmiaru k",
        spec_ref="k punktów leżących najbliżej",
        explanation=(
            "Kopiec trzymający k najlepszych daje O(n log k). Sortowanie całości odpowie tak samo, "
            "ale kosztuje O(n log n) i wyznacza porządek, który poza pierwszą k-ką nikogo nie "
            "interesuje."
        ),
    ),
    # --- backtracking ---
    dict(
        pattern="backtracking",
        problem="suma-kombinacji",
        difficulty=2,
        spec=(
            "Zbiór różnych liczb dodatnich i wartość docelowa. Wypisz wszystkie kombinacje "
            "sumujące się do niej, przy czym każdej liczby wolno użyć dowolnie wiele razy."
        ),
        options=[
            "backtracking z możliwością powrotu do tego samego elementu",
            "programowanie dynamiczne",
            "algorytm zachłanny od największej liczby",
            "okno przesuwne",
        ],
        answer="backtracking z możliwością powrotu do tego samego elementu",
        spec_ref="Wypisz wszystkie kombinacje",
        explanation=(
            "Programowanie dynamiczne policzy, ile jest kombinacji albo która jest najkrótsza, ale "
            "nie wypisze każdej z osobna. Zachłanne branie największych potrafi w ogóle ominąć "
            "rozwiązanie."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="slowo-w-siatce",
        difficulty=3,
        spec=(
            "Siatka liter i słowo. Sprawdź, czy da się je ułożyć, przechodząc między sąsiednimi "
            "polami i nie używając tego samego pola dwa razy w jednym słowie."
        ),
        options=[
            "przeszukiwanie w głąb z cofaniem oznaczeń",
            "przeszukiwanie wszerz",
            "programowanie dynamiczne",
            "drzewo trie bez przeszukiwania siatki",
        ],
        answer="przeszukiwanie w głąb z cofaniem oznaczeń",
        spec_ref="nie używając tego samego pola dwa razy",
        explanation=(
            "Ten zakaz dotyczy jednej ścieżki, a nie całego przebiegu, więc oznaczenie pola trzeba "
            "zdjąć przy powrocie. Przeszukiwanie wszerz nie ma jak tego zrobić, bo nie pamięta, "
            "którą ścieżką dotarło do pola."
        ),
    ),
    # --- grafy ---
    dict(
        pattern="graphs",
        problem="klonowanie-grafu",
        difficulty=2,
        spec=(
            "Graf nieskierowany, podany przez dowolny węzeł, może zawierać cykle. Zbuduj jego "
            "pełną kopię, w której żaden węzeł nie jest współdzielony z oryginałem."
        ),
        options=[
            "przeszukiwanie z mapą: węzeł oryginału na węzeł kopii",
            "przeszukiwanie wszerz bez zapamiętywania kopii",
            "sortowanie topologiczne",
            "struktura zbiorów rozłącznych",
        ],
        answer="przeszukiwanie z mapą: węzeł oryginału na węzeł kopii",
        spec_ref="może zawierać cykle",
        explanation=(
            "Mapa pełni dwie role naraz: pamięta, co już skopiowano, i przerywa obieg po cyklu. "
            "Bez niej pierwszy cykl w grafie kończy się nieskończoną rekurencją."
        ),
    ),
    dict(
        pattern="graphs",
        problem="gnijace-owoce",
        difficulty=2,
        spec=(
            "Siatka, w której zepsute pola zarażają sąsiadów co minutę. Psucie zaczyna się "
            "jednocześnie od wszystkich pól już zepsutych. Podaj, po ilu minutach nie zostanie "
            "nic świeżego."
        ),
        options=[
            "przeszukiwanie wszerz z wieloma źródłami naraz",
            "przeszukiwanie wszerz osobno z każdego źródła",
            "przeszukiwanie w głąb",
            "programowanie dynamiczne",
        ],
        answer="przeszukiwanie wszerz z wieloma źródłami naraz",
        spec_ref="jednocześnie od wszystkich pól już zepsutych",
        explanation=(
            "Wszystkie zepsute pola trafiają do kolejki na starcie, więc fala rozchodzi się "
            "równolegle, a numer warstwy to wprost liczba minut. Puszczanie przeszukiwania osobno "
            "z każdego źródła policzy to samo, tylko wielokrotnie drożej."
        ),
    ),
    dict(
        pattern="graphs",
        problem="otoczone-obszary",
        difficulty=3,
        spec=(
            "Siatka pól dwóch rodzajów. Zamień na drugi rodzaj każdy obszar, który nie dotyka "
            "krawędzi planszy."
        ),
        prompt="Który wzorzec upraszcza to zadanie najbardziej?",
        options=[
            "przeszukiwanie od krawędzi i oznaczenie tego, co ma przetrwać",
            "przeszukiwanie każdego obszaru i sprawdzanie, czy dotyka krawędzi",
            "struktura zbiorów rozłącznych",
            "programowanie dynamiczne",
        ],
        answer="przeszukiwanie od krawędzi i oznaczenie tego, co ma przetrwać",
        spec_ref="nie dotyka krawędzi planszy",
        explanation=(
            "Zamiast dla każdego obszaru sprawdzać warunek, odwracasz problem: zaznaczasz to, co "
            "jest połączone z krawędzią, a cała reszta z definicji warunek spełnia. Jedno "
            "przejście zamiast osobnego sprawdzenia przy każdym obszarze."
        ),
    ),
    dict(
        pattern="advanced-graphs",
        problem="loty-z-limitem-przesiadek",
        difficulty=3,
        spec=(
            "Graf połączeń lotniczych z cenami. Znajdź najtańszą trasę z miasta startowego do "
            "docelowego, używając najwyżej k przesiadek."
        ),
        prompt="Który wzorzec radzi sobie z ograniczeniem podanym w treści?",
        options=[
            "algorytm Bellmana-Forda w k rundach",
            "algorytm Dijkstry",
            "przeszukiwanie wszerz",
            "sortowanie topologiczne",
        ],
        answer="algorytm Bellmana-Forda w k rundach",
        spec_ref="najwyżej k przesiadek",
        explanation=(
            "Dijkstra domyka wierzchołek, gdy znajdzie do niego najtańszą trasę, i przez to "
            "odrzuca trasę droższą, ale krótszą w przesiadkach, która jako jedyna mieści się w "
            "limicie. U Bellmana-Forda jedna runda to dokładnie jedna przesiadka, więc limit "
            "wchodzi wprost do algorytmu."
        ),
    ),
    # --- programowanie dynamiczne ---
    dict(
        pattern="dp-1d",
        problem="rabus",
        difficulty=2,
        spec=(
            "Ciąg wartości domów. Wybierz podzbiór o największej sumie, w którym żadne dwa "
            "wybrane domy nie sąsiadują."
        ),
        options=[
            "programowanie dynamiczne",
            "algorytm zachłanny od największej wartości",
            "backtracking bez zapamiętywania",
            "okno przesuwne",
        ],
        answer="programowanie dynamiczne",
        spec_ref="żadne dwa wybrane domy nie sąsiadują",
        explanation=(
            "Dla każdej pozycji wystarczy pamiętać najlepszy wynik z jej wzięciem i bez niej. "
            "Zachłanne branie największych wartości zawodzi, bo jedna duża potrafi zablokować dwie "
            "mniejsze, które razem dają więcej."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="najdluzszy-palindrom",
        difficulty=3,
        spec="Napis. Znajdź najdłuższy spójny fragment, który czyta się tak samo w obie strony.",
        options=[
            "rozszerzanie wokół każdego możliwego środka",
            "okno przesuwne",
            "sortowanie znaków",
            "zbiór haszujący fragmentów",
        ],
        answer="rozszerzanie wokół każdego możliwego środka",
        spec_ref="czyta się tak samo w obie strony",
        explanation=(
            "Palindrom jest jednoznacznie wyznaczony przez swój środek, a środków jest 2n minus "
            "jeden, licząc te między znakami. Okno przesuwne zawodzi, bo skrócenie fragmentu z "
            "lewej nie zachowuje własności bycia palindromem."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="reszta-monetami",
        difficulty=3,
        spec=(
            "Nominały monet, niekoniecznie takie jak w prawdziwej walucie, oraz kwota. Podaj "
            "najmniejszą liczbę monet, którą da się ją wydać, albo stwierdź, że się nie da. "
            "Nominałów można używać wielokrotnie."
        ),
        options=[
            "programowanie dynamiczne po kwotach",
            "algorytm zachłanny od największego nominału",
            "okno przesuwne",
            "wyszukiwanie binarne po liczbie monet",
        ],
        answer="programowanie dynamiczne po kwotach",
        spec_ref="niekoniecznie takie jak w prawdziwej walucie",
        explanation=(
            "Zachłanne branie największego nominału działa dla typowych walut i dlatego kusi, ale "
            "nie w ogólności: przy nominałach 1, 3 i 4 oraz kwocie 6 daje 4+1+1, czyli trzy monety, "
            "choć wystarczą dwie po 3."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="najwiekszy-iloczyn-fragmentu",
        difficulty=3,
        spec=(
            "Tablica, która może zawierać liczby ujemne. Podaj największy iloczyn spójnego, "
            "niepustego fragmentu."
        ),
        prompt="Który wzorzec tu zadziała?",
        options=[
            "jedno przejście pamiętające naraz największy i najmniejszy iloczyn",
            "jedno przejście pamiętające tylko największy iloczyn",
            "okno przesuwne",
            "sortowanie tablicy",
        ],
        answer="jedno przejście pamiętające naraz największy i najmniejszy iloczyn",
        spec_ref="może zawierać liczby ujemne",
        explanation=(
            "Mnożenie przez liczbę ujemną zamienia największy iloczyn w najmniejszy i odwrotnie, "
            "więc trzeba prowadzić oba naraz. Wersja pamiętająca samo maksimum, przeniesiona wprost "
            "z zadania o sumie, gubi przypadek dwóch liczb ujemnych dających duży iloczyn dodatni."
        ),
    ),
    dict(
        pattern="dp-2d",
        problem="unikalne-sciezki",
        difficulty=2,
        spec=(
            "Siatka o zadanych wymiarach. Policz, na ile sposobów da się przejść z lewego górnego "
            "rogu do prawego dolnego, ruszając się tylko w prawo albo w dół."
        ),
        options=[
            "programowanie dynamiczne po siatce",
            "przeszukiwanie wszerz",
            "backtracking wypisujący ścieżki",
            "algorytm zachłanny",
        ],
        answer="programowanie dynamiczne po siatce",
        spec_ref="Policz, na ile sposobów",
        explanation=(
            "Liczba dróg do pola to suma dróg do pola nad nim i po jego lewej. Backtracking "
            "wypisze każdą ścieżkę z osobna, a jest ich wykładniczo wiele, choć pytanie dotyczy "
            "tylko ich liczby."
        ),
    ),
    # --- zachłanne ---
    dict(
        pattern="greedy",
        problem="stacja-benzynowa",
        difficulty=3,
        spec=(
            "Stacje ustawione na okręgu, przy każdej ilość paliwa i koszt przejazdu do następnej. "
            "Wskaż stację, z której da się objechać pętlę, wiedząc, że rozwiązanie jest co "
            "najwyżej jedno."
        ),
        options=[
            "jedno przejście z przesuwaniem startu przy ujemnym bilansie",
            "sprawdzenie każdego możliwego startu po kolei",
            "programowanie dynamiczne",
            "kopiec po zapasie paliwa",
        ],
        answer="jedno przejście z przesuwaniem startu przy ujemnym bilansie",
        spec_ref="rozwiązanie jest co najwyżej jedno",
        explanation=(
            "Gdy bilans od bieżącego startu spadnie poniżej zera, żadna stacja po drodze też nie "
            "zadziała, więc start można przesunąć od razu za to miejsce. Sprawdzanie każdego "
            "startu daje ten sam wynik w czasie kwadratowym."
        ),
    ),
    # --- przedziały ---
    dict(
        pattern="intervals",
        problem="usun-najmniej-przedzialow",
        difficulty=3,
        spec="Lista przedziałów. Usuń jak najmniej z nich, żeby pozostałe nie nachodziły na siebie.",
        prompt="Który wybór zachłanny jest tu poprawny?",
        options=[
            "sortowanie po końcu przedziału",
            "sortowanie po początku przedziału",
            "sortowanie po długości przedziału",
            "sprawdzenie wszystkich podzbiorów",
        ],
        answer="sortowanie po końcu przedziału",
        spec_ref="Usuń jak najmniej",
        explanation=(
            "Zostawiając przedział kończący się najwcześniej, zostawiasz najwięcej miejsca na "
            "kolejne, i to prowadzi do wyniku optymalnego. Sortowanie po początku jest "
            "najczęstszym błędnym odruchem: jeden bardzo długi przedział zaczynający się wcześnie "
            "wypycha kilka krótkich, które zmieściłyby się razem."
        ),
    ),
]
