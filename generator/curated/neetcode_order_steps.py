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
            "gdy prefiksy są już w wyniku, zawiąż zmienną na iloczyn prawej strony i ustaw ją na jeden",
            "przejdź wejście jeszcze raz, tym razem od prawej do lewej",
            "pomnóż wartość w wyniku przez bieżący iloczyn prawej strony",
            "dopiero potem wmnóż element wejścia do iloczynu prawej strony",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "ustaw wskaźniki na obu końcach tablicy, a oba zapamiętane maksima na zero",
            "porównaj zapamiętane maksima i wybierz stronę, po której maksimum jest niższe",
            "zaktualizuj maksimum wybranej strony bieżącym słupkiem",
            "dolicz do wyniku różnicę między tym maksimum a wysokością bieżącego słupka",
            "przesuń wskaźnik wybranej strony o jeden do środka",
            "powtarzaj, dopóki wskaźniki się nie miną, i zwróć zsumowaną wodę",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "ustaw licznik brakujących znaków na sumę tych zliczeń",
            "rozszerzaj okno w prawo, zmniejszając licznik, gdy znak był jeszcze potrzebny",
            "gdy licznik brakujących spadnie do zera, zapamiętaj okno, jeśli jest krótsze od najlepszego",
            "zwężaj okno z lewej, dopóki pokrycie się utrzymuje, po każdym skróceniu ponawiając zapis",
            "gdy zwężenie zabierze znak potrzebny do pokrycia, zwiększ licznik i wróć do rozszerzania",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "weź kolejny element wejścia",
            "oczyść kolejkę: z przodu wyrzuć indeks spoza okna, z tyłu wszystkie o wartościach nie większych od bieżącej",
            "dopisz bieżący indeks na koniec kolejki",
            "gdy okno osiągnęło pełną długość, odczytaj maksimum z przodu kolejki",
            "dopisz odczytaną wartość do wyniku i przejdź do następnego elementu",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "przygotuj stos na indeksy słupków i przechodź słupki od lewej do prawej",
            "dopóki bieżący słupek jest niższy od tego na szczycie stosu, zdejmij szczyt",
            "dla zdjętego słupka prawą granicą jest bieżąca pozycja, a lewą nowy szczyt stosu",
            "policz pole zdjętego prostokąta i zaktualizuj najlepszy wynik",
            "gdy zdejmowanie się skończy, dołóż bieżący indeks na stos",
            "po przejściu całego histogramu opróżnij stos, przyjmując jako prawą granicę jego koniec",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "posortuj samochody po pozycji malejąco i przygotuj pusty stos na czasy dojazdu czół flot",
            "weź kolejny samochód z tej kolejności",
            "policz jego czas dojazdu do mety jako dystans podzielony przez prędkość",
            "porównaj ten czas z czasem leżącym na szczycie stosu",
            "gdy jest większy, samochód zakłada nową flotę i jego czas ląduje na stosie",
            "gdy nie jest większy, samochód dogoni flotę przed sobą i stos zostaje bez zmian",
        ],
        deps=[[], [0], [1], [2], [3], [3, 4]],
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
            "ustal przedział: dolną granicę na wartość na pewno za małą, górną na na pewno wystarczającą",
            "weź środek przedziału i sprawdź go przygotowaną funkcją",
            "gdy wartość wystarcza, zapamiętaj ją jako najlepszą dotychczasową",
            "wtedy przenieś górną granicę tuż pod środek, a w przeciwnym razie dolną tuż nad środek",
            "powtarzaj, aż granice się zejdą, i zwróć zapamiętaną wartość",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "utwórz listę dwukierunkową z wartownikami na obu końcach oraz słownik z klucza na węzeł",
            "przy odczycie znajdź węzeł w słowniku",
            "wypnij go z jego bieżącego miejsca na liście",
            "wepnij go tuż przy wartowniku oznaczającym stronę najświeższych",
            "przy zapisie dołóż nowy węzeł po tej samej stronie i dopisz go do słownika",
            "gdy rozmiar przekroczy pojemność, wypnij węzeł przy przeciwnym wartowniku i usuń jego klucz",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "przygotuj kopiec porządkowany wartościami węzłów i wrzuć pierwszy węzeł z każdej niepustej listy",
            "gdy kopiec jest pusty, zwróć pustą listę, a w przeciwnym razie utwórz węzeł wartowniczy",
            "zdejmij z kopca najmniejszy węzeł",
            "dopnij go na koniec budowanego wyniku",
            "jeśli zdjęty węzeł miał następnika, wrzuć następnika do kopca",
            "powtarzaj, aż kopiec opustoszeje, i zwróć listę za wartownikiem",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "zawiąż zmienną na najlepszy wynik i ustaw ją na minus nieskończoność",
            "zejdź rekurencyjnie i policz wkład lewego oraz prawego poddrzewa",
            "ujemny wkład potraktuj jak zero, bo takiej gałęzi lepiej nie brać wcale",
            "policz sumę wartości węzła i obu poprawionych wkładów",
            "zaktualizuj tą sumą najlepszy dotychczasowy wynik",
            "zwróć w górę wartość węzła powiększoną o większy z dwóch wkładów",
        ],
        deps=[[], [0], [1], [2], [3], [2, 4]],
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
            "wstaw wszystkie szukane słowa do jednego drzewa trie, oznaczając węzły kończące słowo",
            "uruchom przeszukiwanie w głąb z każdego pola siatki, startując od korzenia trie",
            "przy wejściu na pole zejdź do dziecka trie dla jego litery, a gdy go nie ma, przerwij gałąź",
            "oznacz pole jako zajęte, żeby ta sama ścieżka nie użyła go dwa razy",
            "gdy bieżący węzeł trie kończy słowo, dopisz je do wyniku i odznacz, żeby nie trafiło tam ponownie",
            "po powrocie z sąsiadów cofnij oznaczenie pola",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "gdy kopiec większej połowy urósł ponad rozmiar mniejszej, przełóż jego wierzchołek z powrotem",
            "porównaj rozmiary obu kopców",
            "przy nierównych medianą jest wierzchołek większego kopca, a przy równych średnia obu wierzchołków",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "w przeciwnym razie rozważ każdy możliwy koniec fragmentu zaczynającego się w tej pozycji",
            "sprawdź, czy tak wycięty fragment jest palindromem, i pomiń go, jeśli nie jest",
            "dopisz fragment do podziału, zejdź głębiej, a po powrocie zdejmij go z powrotem",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "zbuduj listy sąsiedztwa i policz dla każdego kursu liczbę wymagań",
            "wrzuć do kolejki wszystkie kursy o zerowej liczbie wymagań",
            "zdejmij kurs z kolejki i dopisz go do wynikowej kolejności",
            "zmniejsz licznik wymagań u każdego z jego następników",
            "następnika, którego licznik spadł do zera, dołóż do kolejki",
            "gdy kolejka opustoszeje, porównaj długość wyniku z liczbą kursów, żeby wykryć cykl",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "przygotuj dwa osobne zbiory odwiedzonych pól, po jednym dla każdej krawędzi",
            "wrzuć do pierwszego zbioru wszystkie pola leżące przy górnej krawędzi",
            "rozszerzaj ten zbiór, wchodząc tylko na sąsiadów o wysokości nie mniejszej niż bieżąca",
            "zrób to samo dla dolnej krawędzi, zapełniając drugi zbiór",
            "przetnij oba zbiory",
            "zwróć współrzędne pól należących do przecięcia",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "zawiąż pomocniczą tablicę na najmniejsze zakończenia podciągów kolejnych długości",
            "weź kolejny element wejścia",
            "poszukaj binarnie pierwszej pozycji w tablicy pomocniczej o wartości nie mniejszej od niego",
            "gdy taka pozycja istnieje, nadpisz ją tym elementem, a gdy nie, dopisz go na koniec tablicy",
            "przejdź do następnego elementu wejścia i powtórz",
            "po wyczerpaniu wejścia zwróć długość tablicy pomocniczej",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
            "przechodź pozostałe komórki wierszami, od lewej do prawej",
            "porównaj znaki odpowiadające bieżącej komórce",
            "przy znakach równych przepisz wartość po przekątnej, a przy różnych weź najmniejszą z trzech sąsiadek i dodaj jeden",
            "po wypełnieniu całej tablicy odczytaj wynik z prawego dolnego rogu",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
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
        deps=[[], [0], [1], [2], [3], [4]],
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
            "posortuj spotkania po godzinie rozpoczęcia i przygotuj pusty kopiec na godziny zakończenia",
            "weź kolejne spotkanie z posortowanej listy",
            "sprawdź, czy na wierzchołku kopca leży godzina nie późniejsza niż jego początek",
            "jeśli tak, zdejmij ją, bo tamta sala właśnie się zwolniła",
            "wrzuć na kopiec godzinę zakończenia bieżącego spotkania",
            "zapamiętaj największy rozmiar kopca, jaki wystąpił, i zwróć go jako wynik",
        ],
        deps=[[], [0], [1], [2], [3], [4]],
        explanation=(
            "Kopiec trzyma tylko godziny zakończeń, bo o zwolnieniu sali decyduje wyłącznie ta "
            "wartość. Rozmiar kopca w szczycie to liczba spotkań nakładających się w jednej chwili, "
            "czyli dokładnie liczba potrzebnych sal."
        ),
    ),
]
