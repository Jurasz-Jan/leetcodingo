"""Szkielety rozwiązań z NeetCode 150 — typ `order-steps`.

Sześć kroków do ułożenia w kolejności. Ten typ sprawdza co innego niż pozostałe:
nie „który wzorzec” i nie „jaka obserwacja”, tylko czy potrafisz odtworzyć **kształt
rozwiązania** od początku do końca. Na rozmowie to jest moment, w którym wiadomo,
czy ktoś rozumie algorytm, czy pamięta o nim anegdotę.

Zasada, bez której ten typ się psuje: **kolejność musi być jednoznaczna**. Każdy krok
zużywa coś, co powstało w którymś z wcześniejszych, więc istnieje dokładnie jedno
poprawne ułożenie. Dwa kroki niezależne od siebie dałyby dwie poprawne odpowiedzi,
czyli ćwiczenie bez poprawnej odpowiedzi — ten sam błąd, co mutant przechodzący testy.

Dobór: poziom medium i hard, bo przy zadaniach łatwych szkielet jest zwykle
trzykrokowy i nie ma czego układać.

Treści są własne. Lista NeetCode wyznacza dobór zadań, nie brzmienie opisów.
"""

CORPUS = {
    "id": "neetcode-150",
    "name": "NeetCode 150 — sedno",
}

DEFAULT_TYPE = "order-steps"

EXERCISES = [
    dict(
        pattern="arrays-hashing",
        problem="iloczyn-pozostalych-kroki",
        difficulty=2,
        spec=(
            "Dla każdej pozycji tablicy podaj iloczyn wszystkich pozostałych elementów, "
            "bez dzielenia i w jednej dodatkowej tablicy wynikowej."
        ),
        steps=[
            "utwórz tablicę wynikową tej samej długości co wejście",
            "przejdź wejście od lewej, wpisując do wyniku iloczyn wszystkiego, co leży na lewo od pozycji",
            "zapamiętaj osobną zmienną na iloczyn tego, co leży na prawo, i ustaw ją na jeden",
            "przejdź wejście od prawej do lewej",
            "pomnóż wartość w wyniku przez bieżący iloczyn prawej strony",
            "dopiero potem wmnóż element wejścia do iloczynu prawej strony",
        ],
        explanation=(
            "Kolejność dwóch ostatnich kroków jest tu całą trudnością. Najpierw mnożysz wynik "
            "przez iloczyn prawej strony, a dopiero potem dokładasz do niego bieżący element — "
            "gdyby odwrotnie, element wszedłby do iloczynu własnej pozycji."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="trojka-do-zera-kroki",
        difficulty=3,
        spec="Znajdź wszystkie różne trójki sumujące się do zera, bez powtórzeń w wyniku.",
        steps=[
            "posortuj tablicę rosnąco",
            "ustalaj pierwszy element trójki, idąc po kolejnych pozycjach",
            "pomiń ustaloną pozycję, jeśli ma tę samą wartość co poprzednia",
            "ustaw dwa wskaźniki: tuż za ustalonym elementem oraz na końcu tablicy",
            "zwężaj parę zależnie od znaku sumy, zapisując trójki sumujące się do zera",
            "po zapisaniu trójki przesuń lewy wskaźnik za wszystkie powtórzenia jego wartości",
        ],
        explanation=(
            "Sortowanie robi dwie rzeczy naraz: pozwala zwijać parę wskaźnikami i ustawia "
            "duplikaty obok siebie. Dlatego oba pomijania powtórzeń, zewnętrzne i wewnętrzne, "
            "są tanie i sprowadzają się do porównania z sąsiadem."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="woda-deszczowa-kroki",
        difficulty=3,
        spec=(
            "Tablica wysokości słupków. Policz, ile wody zatrzyma się między nimi po deszczu, "
            "w stałej pamięci."
        ),
        steps=[
            "ustaw wskaźniki na obu końcach tablicy",
            "zapamiętaj najwyższy słupek widziany od lewej i najwyższy widziany od prawej",
            "wybierz tę stronę, po której zapamiętane maksimum jest niższe",
            "zaktualizuj maksimum tej strony bieżącym słupkiem",
            "dolicz do wyniku różnicę między maksimum tej strony a wysokością bieżącego słupka",
            "przesuń wskaźnik wybranej strony do środka i powtarzaj, aż się miną",
        ],
        explanation=(
            "Woda nad słupkiem to niższe z dwóch maksimów minus jego wysokość. Ruch po niższej "
            "stronie jest bezpieczny, bo o wyniku decyduje właśnie ta strona, a druga jest już "
            "gwarantowanym ograniczeniem z góry."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="minimalne-okno-kroki",
        difficulty=3,
        spec=(
            "Znajdź najkrótszy fragment napisu zawierający wszystkie znaki wzorca wraz "
            "z powtórzeniami."
        ),
        steps=[
            "policz, ile razy każdy znak występuje we wzorcu",
            "ustaw licznik brakujących znaków na długość wzorca",
            "rozszerzaj okno w prawo, zmniejszając licznik brakujących, gdy znak był jeszcze potrzebny",
            "gdy licznik brakujących spadnie do zera, zapamiętaj okno, jeśli jest krótsze od dotychczas najlepszego",
            "zwężaj okno z lewej, dopóki pokrycie się utrzymuje, po każdym skróceniu ponawiając zapis wyniku",
            "gdy zwężenie zabierze znak potrzebny do pokrycia, zwiększ licznik brakujących i wróć do rozszerzania",
        ],
        explanation=(
            "Klucz to jeden licznik zamiast porównywania słowników: zmienia się o jeden przy "
            "wejściu i wyjściu znaku, więc warunek pokrycia sprawdza się porównaniem z zerem."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="maksimum-w-oknie-kroki",
        difficulty=3,
        spec="Dla każdego okna o stałej długości k podaj największy element, w czasie liniowym.",
        steps=[
            "przygotuj kolejkę dwustronną, w której będziesz trzymać indeksy, nie wartości",
            "dla kolejnego elementu usuń z przodu kolejki indeks, który wypadł już poza okno",
            "usuwaj z tyłu kolejki wszystkie indeksy o wartościach nie większych od bieżącej",
            "dopisz bieżący indeks na koniec kolejki",
            "gdy okno osiągnie pełną długość, odczytaj maksimum z przodu kolejki",
            "dopisz odczytaną wartość do wyniku i przesuń się o jeden element dalej",
        ],
        explanation=(
            "Kolejka pozostaje malejąca, więc jej przód to zawsze maksimum bieżącego okna. "
            "Trzymanie indeksów zamiast wartości jest konieczne, żeby dało się rozpoznać moment, "
            "w którym element wypada poza okno."
        ),
    ),
    dict(
        pattern="stack",
        problem="najwiekszy-prostokat-kroki",
        difficulty=3,
        spec=(
            "Histogram słupków o jednostkowej szerokości. Znajdź pole największego prostokąta, "
            "jaki się w nim mieści."
        ),
        steps=[
            "przygotuj stos, na którym będą leżeć indeksy słupków o rosnących wysokościach",
            "przechodź słupki od lewej do prawej",
            "dopóki bieżący słupek jest niższy od tego na szczycie stosu, zdejmij szczyt",
            "dla zdjętego słupka przyjmij, że jego prostokąt sięga w prawo do bieżącej pozycji",
            "lewą granicę odczytaj z nowego szczytu stosu, bo to pierwszy niższy słupek po lewej",
            "policz pole i zaktualizuj najlepszy wynik, a na koniec dołóż bieżący indeks na stos",
        ],
        explanation=(
            "Zdejmowanie ze stosu jest momentem, w którym znane są obie granice prostokąta naraz: "
            "prawą wyznacza słupek, który wymusił zdjęcie, a lewą ten, który leży pod spodem."
        ),
    ),
    dict(
        pattern="stack",
        problem="floty-kroki",
        difficulty=2,
        spec=(
            "Samochody z pozycją i prędkością jadą do wspólnej mety, nikt nie wyprzedza. "
            "Policz liczbę flot, które dojadą."
        ),
        steps=[
            "połącz pozycję i prędkość każdego samochodu w jedną parę",
            "posortuj samochody po pozycji malejąco, czyli od najbliższego mety",
            "policz dla każdego samochodu czas dojazdu do mety",
            "przechodź samochody w tej kolejności, trzymając na stosie czasy dojazdu czół flot",
            "jeśli czas bieżącego samochodu jest większy od czasu na szczycie stosu, zacznij nową flotę",
            "w przeciwnym razie samochód dogoni flotę przed sobą i nie zwiększa wyniku",
        ],
        explanation=(
            "Liczba flot to po prostu rozmiar stosu na końcu. Kolejność od mety jest konieczna, "
            "bo flota z przodu musi być rozstrzygnięta, zanim rozpatrzy się tę za nią."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="szukanie-po-odpowiedzi-kroki",
        difficulty=2,
        spec=(
            "Znajdź najmniejszą wartość parametru, przy której zadanie zdąży się wykonać "
            "w limicie."
        ),
        steps=[
            "napisz funkcję sprawdzającą, czy pojedyncza wartość parametru wystarcza",
            "ustal dolną granicę przedziału na najmniejszą wartość, która w ogóle ma sens",
            "ustal górną granicę na wartość, przy której zadanie na pewno się udaje",
            "weź środek przedziału i sprawdź go przygotowaną funkcją",
            "gdy wartość wystarcza, zapamiętaj ją i przenieś górną granicę tuż pod środek",
            "gdy nie wystarcza, przenieś dolną granicę tuż nad środek i powtarzaj aż do zejścia się granic",
        ],
        explanation=(
            "Kolejność pierwszych trzech kroków nie jest kosmetyczna: bez funkcji sprawdzającej "
            "nie wiadomo, co znaczy „wystarcza”, a bez niej nie da się dobrać granic tak, żeby "
            "jedna spełniała warunek, a druga nie."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="mediana-dwoch-tablic-kroki",
        difficulty=3,
        spec=(
            "Dwie posortowane tablice. Podaj medianę ich połączenia w czasie logarytmicznym "
            "względem krótszej z nich."
        ),
        steps=[
            "zamień tablice miejscami tak, żeby pierwsza była tą krótszą",
            "szukaj binarnie, ile elementów krótszej tablicy trafia do lewej połowy",
            "dolicz resztę do pełnej połowy z drugiej tablicy, co wyznacza jej podział",
            "odczytaj cztery wartości graniczne: po dwie tuż przed i tuż za każdym cięciem",
            "sprawdź, czy każdy element lewej strony nie przekracza każdego elementu prawej",
            "gdy warunek zawodzi, przesuń zakres szukania i powtórz, a gdy zachodzi, złóż medianę z wartości granicznych",
        ],
        explanation=(
            "Szukasz nie wartości, tylko miejsca cięcia. Ograniczenie się do krótszej tablicy "
            "daje logarytm od mniejszego rozmiaru i pilnuje, żeby indeksy w drugiej tablicy nie "
            "wyszły poza zakres."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="przeplot-listy-kroki",
        difficulty=2,
        spec=(
            "Przeplot listy jednokierunkowej: pierwszy element, ostatni, drugi, przedostatni "
            "i tak dalej, w miejscu."
        ),
        steps=[
            "znajdź środek listy wskaźnikiem wolnym i szybkim",
            "przetnij listę na środku, żeby powstały dwie osobne części",
            "odwróć drugą część, przepinając wskaźniki",
            "ustaw po jednym wskaźniku na początku każdej z części",
            "wpinaj na przemian po jednym węźle z pierwszej i z drugiej części",
            "zakończ, gdy druga część się wyczerpie",
        ],
        explanation=(
            "Trzy znane operacje na listach złożone w jedną. Przecięcie na środku musi nastąpić "
            "przed odwracaniem, inaczej odwrócenie zawróci również pierwszą połowę i powstanie cykl."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="lru-kroki",
        difficulty=3,
        spec=(
            "Pamięć podręczna o ustalonej pojemności, usuwająca element najdawniej używany. "
            "Odczyt i zapis w czasie stałym."
        ),
        steps=[
            "utwórz listę dwukierunkową z wartownikami na obu końcach",
            "utwórz słownik odwzorowujący klucz na węzeł tej listy",
            "przy odczycie znajdź węzeł w słowniku i wypnij go z jego miejsca na liście",
            "wepnij ten węzeł tuż przy wartowniku oznaczającym stronę najświeższych",
            "przy zapisie dołóż nowy węzeł po tej samej stronie i dopisz go do słownika",
            "gdy rozmiar przekroczy pojemność, wypnij węzeł przy przeciwnym wartowniku i usuń jego klucz ze słownika",
        ],
        explanation=(
            "Wartownicy na obu końcach usuwają wszystkie przypadki brzegowe z wypinania i wpinania: "
            "każdy prawdziwy węzeł ma zawsze poprzednika i następnika, więc nie ma gałęzi na pustą "
            "listę ani na jedyny element."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="scal-k-list-kroki",
        difficulty=3,
        spec="Scal k posortowanych list jednokierunkowych w jedną posortowaną listę.",
        steps=[
            "wrzuć do kopca pierwszy węzeł z każdej niepustej listy",
            "porządkuj kopiec po wartościach węzłów",
            "utwórz węzeł wartowniczy, który będzie początkiem wyniku",
            "zdejmij z kopca najmniejszy węzeł i dopnij go na koniec wyniku",
            "jeśli zdjęty węzeł miał następnika, wrzuć następnika do kopca",
            "powtarzaj, aż kopiec opustoszeje, i zwróć listę za wartownikiem",
        ],
        explanation=(
            "Kopiec ma rozmiar k, a nie n, bo w każdej chwili leży w nim najwyżej jeden węzeł "
            "z każdej listy. Stąd koszt n log k zamiast n log n za scalanie wszystkiego naraz."
        ),
    ),
    dict(
        pattern="trees",
        problem="odtworzenie-drzewa-kroki",
        difficulty=2,
        spec="Odtwórz drzewo binarne z porządków preorder i inorder, bez powtórzonych wartości.",
        steps=[
            "zbuduj słownik odwzorowujący wartość na jej pozycję w inorder",
            "weź kolejną wartość z preorder i utwórz z niej węzeł",
            "odczytaj ze słownika pozycję tej wartości w inorder",
            "wszystko na lewo od tej pozycji należy do lewego poddrzewa, wszystko na prawo do prawego",
            "zbuduj rekurencyjnie lewe poddrzewo, zużywając kolejne wartości preorder",
            "zbuduj prawe poddrzewo z tego, co z preorder zostało",
        ],
        explanation=(
            "Słownik zamienia szukanie korzenia w inorder z liniowego na stałe, co ściąga całość "
            "z kwadratu do liniowości. Lewe poddrzewo musi powstać przed prawym, bo obie gałęzie "
            "czerpią z tego samego, wspólnego strumienia preorder."
        ),
    ),
    dict(
        pattern="trees",
        problem="maksymalna-sciezka-kroki",
        difficulty=3,
        spec=(
            "Drzewo binarne z wartościami mogącymi być ujemnymi. Podaj największą sumę wartości "
            "na ścieżce między dowolnymi dwoma węzłami."
        ),
        steps=[
            "zawiąż zmienną na najlepszy dotychczasowy wynik i ustaw ją na minus nieskończoność",
            "policz rekurencyjnie najlepszy wkład lewego poddrzewa",
            "policz tak samo wkład prawego poddrzewa",
            "ujemny wkład potraktuj jak zero, bo lepiej takiej gałęzi nie brać wcale",
            "zaktualizuj najlepszy wynik sumą wartości węzła i obu wkładów",
            "zwróć w górę wartość węzła powiększoną o większy z dwóch wkładów",
        ],
        explanation=(
            "Funkcja zwraca co innego, niż aktualizuje. W górę idzie ścieżka schodząca tylko jedną "
            "gałęzią, bo tylko taka da się przedłużyć u rodzica, a w wyniku odkłada się ścieżka "
            "przechodząca przez węzeł obiema gałęziami."
        ),
    ),
    dict(
        pattern="trie",
        problem="szukanie-wielu-slow-kroki",
        difficulty=3,
        spec="Siatka liter i lista słów. Znajdź te słowa, które da się w siatce ułożyć.",
        steps=[
            "wstaw wszystkie szukane słowa do jednego drzewa trie",
            "oznacz w trie węzły kończące słowo",
            "uruchom przeszukiwanie w głąb z każdego pola siatki, startując od korzenia trie",
            "przy wejściu na pole zejdź do dziecka trie odpowiadającego jego literze, a gdy go nie ma, przerwij gałąź",
            "gdy trafisz na węzeł kończący słowo, dopisz to słowo do wyniku i odznacz je, żeby nie trafiło tam drugi raz",
            "oznacz pole jako zajęte na czas schodzenia w głąb i cofnij to oznaczenie przy powrocie",
        ],
        explanation=(
            "Trie odwraca zależność: zamiast szukać każdego słowa osobno, przechodzisz siatkę raz, "
            "a gałąź urywa się w chwili, gdy zbudowany przedrostek nie pasuje do żadnego słowa."
        ),
    ),
    dict(
        pattern="heap",
        problem="mediana-strumienia-kroki",
        difficulty=3,
        spec="Po każdej nowej liczbie w strumieniu podaj medianę wszystkich dotychczasowych.",
        steps=[
            "przygotuj kopiec maksymalny na mniejszą połowę i minimalny na większą",
            "wstaw nową liczbę do kopca mniejszej połowy",
            "przełóż wierzchołek mniejszej połowy do kopca większej",
            "jeśli kopiec większej połowy urósł ponad rozmiar mniejszej, przełóż jego wierzchołek z powrotem",
            "przy nieparzystej liczbie elementów odczytaj medianę z wierzchołka większego kopca",
            "przy parzystej uśrednij wierzchołki obu kopców",
        ],
        explanation=(
            "Bezwarunkowe przełożenie w trzecim kroku wygląda na zbędne, ale to ono gwarantuje "
            "podział na właściwe połowy. Samo wyrównywanie rozmiarów nie wystarcza: element "
            "wstawiony do mniejszej połowy może być większy od wszystkiego w większej."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="hetmany-kroki",
        difficulty=3,
        spec="Ustaw n hetmanów na szachownicy n na n tak, żeby żadne dwa się nie atakowały.",
        steps=[
            "przygotuj trzy zbiory: zajęte kolumny oraz obie rodziny przekątnych",
            "schodź rekurencyjnie wiersz po wierszu",
            "dla bieżącego wiersza przejrzyj wszystkie kolumny",
            "pomiń kolumnę, jeśli ona sama albo któraś z jej przekątnych jest już zajęta",
            "wpisz hetmana i dopisz jego kolumnę oraz obie przekątne do zbiorów",
            "po powrocie z rekurencji usuń te trzy wpisy, żeby odblokować pole dla innych ustawień",
        ],
        explanation=(
            "Przekątne adresuje się sumą i różnicą współrzędnych, więc kolizja sprawdza się w "
            "czasie stałym. Ostatni krok jest istotą nawrotów: bez cofnięcia wpisów kolejne "
            "gałęzie widziałyby planszę zabrudzoną poprzednią próbą."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="podzial-na-palindromy-kroki",
        difficulty=2,
        spec="Podziel napis na wszystkie możliwe sposoby tak, żeby każdy fragment był palindromem.",
        steps=[
            "zawiąż listę na bieżący podział i listę na wynik",
            "wejdź rekurencyjnie z pozycją, od której zaczyna się kolejny fragment",
            "gdy pozycja dobiegnie końca napisu, dopisz kopię bieżącego podziału do wyniku",
            "rozważ każdy możliwy koniec fragmentu zaczynającego się w tej pozycji",
            "sprawdź, czy tak wycięty fragment jest palindromem, i pomiń go, jeśli nie jest",
            "dopisz fragment do podziału, zejdź głębiej, a po powrocie zdejmij go z powrotem",
        ],
        explanation=(
            "Sprawdzenie palindromu przed zejściem w głąb odcina gałąź od razu, zamiast budować "
            "cały podział i odrzucać go na końcu. Kopia podziału przy zapisie jest konieczna, bo "
            "sama lista jest dalej modyfikowana przy nawrotach."
        ),
    ),
    dict(
        pattern="graphs",
        problem="kolejnosc-kursow-kroki",
        difficulty=2,
        spec=(
            "Kursy i pary mówiące, że jeden trzeba zaliczyć przed drugim. Podaj dopuszczalną "
            "kolejność zaliczania albo stwierdź, że nie istnieje."
        ),
        steps=[
            "zbuduj listy sąsiedztwa: dla każdego kursu te, które go wymagają",
            "policz dla każdego kursu, ile kursów trzeba zaliczyć przed nim",
            "wrzuć do kolejki wszystkie kursy o zerowej liczbie wymagań",
            "zdejmij kurs z kolejki i dopisz go do wynikowej kolejności",
            "zmniejsz licznik wymagań u każdego z jego następników",
            "następnika, którego licznik spadł do zera, dołóż do kolejki",
        ],
        explanation=(
            "Jeśli na końcu wynikowa kolejność jest krótsza niż liczba kursów, to znaczy, że w "
            "grafie został cykl i zaliczenie wszystkiego jest niemożliwe. Sprawdzenie cyklu wychodzi "
            "więc za darmo, przy okazji budowania kolejności."
        ),
    ),
    dict(
        pattern="graphs",
        problem="splyw-do-dwoch-mors-kroki",
        difficulty=2,
        spec=(
            "Siatka wysokości, woda spływa do sąsiadów nie wyższych. Znajdź pola, z których "
            "dopłynie i do górnej, i do dolnej krawędzi."
        ),
        steps=[
            "przygotuj dwa osobne zbiory pól, po jednym dla każdej krawędzi",
            "odwróć kierunek myślenia: zamiast spływu w dół rozważaj wchodzenie pod górę",
            "uruchom przeszukiwanie z wszystkich pól przy górnej krawędzi, dopisując odwiedzone do pierwszego zbioru",
            "wchodź tylko na sąsiadów o wysokości nie mniejszej niż bieżąca",
            "powtórz to samo przeszukiwanie od dolnej krawędzi, zapełniając drugi zbiór",
            "zwróć przecięcie obu zbiorów",
        ],
        explanation=(
            "Odwrócenie relacji zamienia sprawdzanie każdego pola z osobna na dwa przejścia po "
            "całej siatce. Warunek „do obu krawędzi” przekłada się wprost na przecięcie zbiorów."
        ),
    ),
    dict(
        pattern="advanced-graphs",
        problem="najtansze-loty-kroki",
        difficulty=3,
        spec=(
            "Graf lotów z cenami. Znajdź najtańszą trasę z miasta startowego do docelowego, "
            "używając najwyżej k przesiadek."
        ),
        steps=[
            "przygotuj tablicę najtańszych znanych kosztów dojazdu do każdego miasta",
            "ustaw koszt miasta startowego na zero, a pozostałych na nieskończoność",
            "powtórz całą rundę dokładnie k plus jeden razy",
            "na początku rundy zrób kopię tablicy kosztów z poprzedniej rundy",
            "dla każdego połączenia policz koszt dojścia, czytając wyłącznie z kopii",
            "zapisz poprawiony koszt do tablicy bieżącej i przejdź do następnej rundy",
        ],
        explanation=(
            "Czytanie z kopii jest tu warunkiem poprawności, a nie ostrożnością: bez niego trasa "
            "poprawiona w tej samej rundzie zostałaby użyta ponownie i przemyciła dodatkową "
            "przesiadkę ponad limit. Jedna runda to dokładnie jeden przelot."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="najdluzszy-rosnacy-kroki",
        difficulty=3,
        spec=(
            "Podaj długość najdłuższego rosnącego podciągu, niekoniecznie spójnego, "
            "w czasie n log n."
        ),
        steps=[
            "zawiąż pomocniczą tablicę na najmniejsze możliwe zakończenia podciągów kolejnych długości",
            "przechodź elementy wejścia po kolei",
            "poszukaj binarnie pierwszej pozycji w tablicy pomocniczej o wartości nie mniejszej od bieżącego elementu",
            "gdy taka pozycja istnieje, nadpisz ją bieżącym elementem",
            "gdy nie istnieje, dopisz element na koniec tablicy pomocniczej",
            "po przejściu całego wejścia zwróć długość tablicy pomocniczej",
        ],
        explanation=(
            "Tablica pomocnicza nie jest żadnym konkretnym podciągiem i próba odczytania jej jako "
            "wyniku jest najczęstszym nieporozumieniem przy tym zadaniu. Prawdziwa jest tylko jej "
            "długość: na pozycji i leży najmniejsze znane zakończenie podciągu długości i plus jeden."
        ),
    ),
    dict(
        pattern="dp-2d",
        problem="odleglosc-edycyjna-kroki",
        difficulty=3,
        spec=(
            "Podaj najmniejszą liczbę wstawień, usunięć i zamian znaku, która zamienia pierwszy "
            "napis w drugi."
        ),
        steps=[
            "utwórz tablicę o wymiarach o jeden większych niż długości obu napisów",
            "wypełnij pierwszy wiersz i pierwszą kolumnę kolejnymi liczbami, bo to koszt zamiany na napis pusty",
            "przechodź komórki wierszami, od lewej do prawej",
            "gdy odpowiadające sobie znaki są równe, przepisz wartość z komórki po przekątnej",
            "gdy się różnią, weź najmniejszą z trzech sąsiadek: z góry, z lewej i po przekątnej",
            "dodaj jeden do wybranej wartości i zapisz wynik w komórce",
        ],
        explanation=(
            "Trzy sąsiadki to trzy dozwolone operacje: z góry usunięcie, z lewej wstawienie, "
            "po przekątnej zamiana. Wypełnienie brzegów przed pętlą nie jest formalnością, tylko "
            "warunkiem początkowym, bez którego pierwsza komórka nie ma się o co oprzeć."
        ),
    ),
    dict(
        pattern="greedy",
        problem="stacja-benzynowa-kroki",
        difficulty=2,
        spec=(
            "Stacje na okręgu z ilością paliwa i kosztem przejazdu do następnej. Wskaż stację, "
            "z której da się objechać pętlę."
        ),
        steps=[
            "policz sumę różnic między paliwem a kosztem na wszystkich stacjach",
            "gdy suma wyszła ujemna, zakończ: żadna stacja nie pozwoli objechać pętli",
            "ustaw kandydata na start na pierwszą stację i wyzeruj bieżący bilans",
            "przechodź stacje po kolei, dodając do bilansu różnicę paliwa i kosztu",
            "gdy bilans zejdzie poniżej zera, przesuń kandydata na stację następną po bieżącej",
            "wyzeruj bilans i idź dalej, a po przejściu wszystkich stacji zwróć kandydata",
        ],
        explanation=(
            "Sprawdzenie sumy na początku rozstrzyga istnienie odpowiedzi, więc reszta może już "
            "tylko szukać właściwej stacji. Skok kandydata za miejsce awarii jest poprawny, bo "
            "żadna stacja po drodze też by nie zadziałała."
        ),
    ),
    dict(
        pattern="intervals",
        problem="sale-kroki",
        difficulty=2,
        spec=(
            "Lista spotkań z godziną początku i końca. Podaj najmniejszą liczbę sal potrzebną, "
            "żeby żadne dwa nie kolidowały."
        ),
        steps=[
            "posortuj spotkania po godzinie rozpoczęcia",
            "przygotuj kopiec minimalny na godziny zakończenia zajętych sal",
            "weź kolejne spotkanie z posortowanej listy",
            "jeśli na wierzchołku kopca leży godzina nie późniejsza niż jego początek, zdejmij ją i zwolnij tę salę",
            "wrzuć na kopiec godzinę zakończenia bieżącego spotkania",
            "zapamiętaj największy rozmiar kopca, jaki wystąpił, i zwróć go jako wynik",
        ],
        explanation=(
            "Kopiec trzyma tylko godziny zakończeń, bo o zwolnieniu sali decyduje wyłącznie ta "
            "wartość. Rozmiar kopca w szczycie to liczba spotkań nakładających się w jednej chwili, "
            "czyli dokładnie liczba potrzebnych sal."
        ),
    ),
]
