"""Sedno zadań z NeetCode 150 — typ `key-insight`.

`recognize-pattern` pyta, **który** wzorzec. Ten typ pyta o coś innego i trudniejszego:
o tę jedną obserwację, bez której wzorzec i tak nie zadziała albo zadziała za wolno.

Wiele zadań z listy sprowadza się do jednego zdania. Bez „licz tylko od liczby bez
poprzednika” najdłuższy ciąg kolejnych jest kwadratowy, a nie liniowy, mimo że zbiór
haszujący jest na miejscu. Wzorzec rozpoznany, zadanie niezrobione. To właśnie ta
różnica jest tu trenowana.

Reguły treści:

* Poprawna odpowiedź to obserwacja **rozstrzygająca**, a nie prawdziwa uwaga na temat.
* Dystraktory są trzech rodzajów: prawdziwe, ale niewystarczające; brzmiące sensownie,
  a fałszywe; oraz właściwy pomysł z jednym zepsutym szczegółem.
* `spec_ref` musi być tym fragmentem treści, na którym obserwacja się zawiesza.
  Zwykle to warunek o złożoności, pamięci albo o dopuszczalnym wejściu.
* Treści są własne. Lista NeetCode wyznacza dobór zadań, nie brzmienie opisów.
"""

CORPUS = {
    "id": "neetcode-150",
    "name": "NeetCode 150 — sedno",
}

DEFAULT_TYPE = "key-insight"

EXERCISES = [
    dict(
        pattern="arrays-hashing",
        problem="najdluzszy-ciag-sedno",
        difficulty=3,
        spec=(
            "Nieuporządkowana tablica liczb. Podaj długość najdłuższego ciągu kolejnych liczb. "
            "Masz do dyspozycji zbiór haszujący, a rozwiązanie ma być liniowe."
        ),
        options=[
            "liczenie w górę zaczyna się wyłącznie od liczby, która nie ma poprzednika w zbiorze",
            "dla każdej liczby liczy się w górę, dopóki następnik jest w zbiorze",
            "liczby trzeba najpierw posortować",
            "zbiór trzeba przeglądać w kolejności rosnącej",
        ],
        answer="liczenie w górę zaczyna się wyłącznie od liczby, która nie ma poprzednika w zbiorze",
        spec_ref="rozwiązanie ma być liniowe",
        explanation=(
            "Bez warunku o braku poprzednika ten sam ciąg jest przechodzony od każdego swojego "
            "elementu i całość robi się kwadratowa. Ten jeden warunek sprawia, że każdy element "
            "bierze udział w liczeniu dokładnie raz, i dopiero on daje obiecaną liniowość."
        ),
    ),
    dict(
        pattern="arrays-hashing",
        problem="k-najczestszych-sedno",
        difficulty=3,
        spec=(
            "Tablica n liczb i wartość k. Podaj k wartości występujących najczęściej. "
            "Rozwiązanie ma działać w czasie liniowym."
        ),
        options=[
            "częstotliwość nigdy nie przekracza n, więc sama może służyć za indeks kubełka",
            "wystarczy posortować liczniki malejąco",
            "kopiec rozmiaru k daje czas liniowy",
            "liczniki trzeba trzymać w strukturze uporządkowanej",
        ],
        answer="częstotliwość nigdy nie przekracza n, więc sama może służyć za indeks kubełka",
        spec_ref="w czasie liniowym",
        explanation=(
            "Sortowanie liczników kosztuje O(n log n), a kopiec O(n log k). Oba są dobrymi "
            "rozwiązaniami, ale żadne nie jest liniowe. Liniowość bierze się z tego, że "
            "częstotliwość mieści się w zakresie od 1 do n, więc można ją potraktować jak indeks."
        ),
    ),
    dict(
        pattern="two-pointers",
        problem="najwieksze-pole-sedno",
        difficulty=3,
        spec=(
            "Wysokości pionowych linii. Wybierz dwie, które razem z osią poziomą dają największe "
            "pole. Zaczynasz od pary najbardziej oddalonej."
        ),
        options=[
            "przesunięcie wyższej linii nigdy nie zwiększy pola, więc przesuwa się niższą",
            "zawsze przesuwa się lewy wskaźnik, bo prawy wyznacza szerokość",
            "wystarczy znaleźć dwie najwyższe linie",
            "pary trzeba przejrzeć wszystkie, tylko w kolejności malejącej szerokości",
        ],
        answer="przesunięcie wyższej linii nigdy nie zwiększy pola, więc przesuwa się niższą",
        spec_ref="Zaczynasz od pary najbardziej oddalonej",
        explanation=(
            "Pole to szerokość razy niższa z dwóch linii. Każdy ruch zmniejsza szerokość, więc "
            "jedyną szansą na wzrost jest podniesienie tej niższej — przesuwanie wyższej gwarantuje "
            "wynik nie lepszy. Dwie najwyższe linie mogą stać obok siebie i dawać maleńkie pole."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="zamiana-znakow-sedno",
        difficulty=3,
        spec=(
            "Napis i liczba k. Możesz zmienić najwyżej k znaków na dowolne inne. Podaj długość "
            "najdłuższego fragmentu złożonego z jednego powtarzającego się znaku."
        ),
        options=[
            "okno jest dopuszczalne, gdy jego długość minus liczba wystąpień najczęstszego znaku nie przekracza k",
            "okno jest dopuszczalne, gdy zawiera najwyżej k różnych znaków",
            "okno jest dopuszczalne, gdy k jest większe od połowy jego długości",
            "okno trzeba sprawdzić osobno dla każdego znaku alfabetu",
        ],
        answer="okno jest dopuszczalne, gdy jego długość minus liczba wystąpień najczęstszego znaku nie przekracza k",
        spec_ref="najwyżej k znaków",
        explanation=(
            "Koszt naprawy okna to dokładnie jego długość minus liczba wystąpień znaku, którego "
            "jest w nim najwięcej, bo najtaniej zmienić wszystko na ten znak. Liczba różnych znaków "
            "nie mówi o koszcie nic: okno z dwoma znakami może wymagać jednej zmiany albo stu."
        ),
    ),
    dict(
        pattern="sliding-window",
        problem="minimalne-okno-sedno",
        difficulty=3,
        spec=(
            "Napis i wzorzec. Znajdź najkrótszy fragment zawierający wszystkie znaki wzorca wraz "
            "z powtórzeniami. Sprawdzenie warunku ma być stałe, niezależnie od długości wzorca."
        ),
        options=[
            "wystarczy jeden licznik brakujących znaków, poprawiany przy każdym ruchu krawędzi okna",
            "po każdym ruchu trzeba porównać słownik okna ze słownikiem wzorca",
            "wystarczy porównywać sumy liczników obu słowników",
            "okno można zwężać dopiero po dojściu do końca napisu",
        ],
        answer="wystarczy jeden licznik brakujących znaków, poprawiany przy każdym ruchu krawędzi okna",
        spec_ref="Sprawdzenie warunku ma być stałe",
        explanation=(
            "Porównywanie słowników jest poprawne, ale kosztuje tyle, ile jest różnych znaków, i "
            "robi się przy każdym kroku. Jedna liczba mówiąca, ilu znaków jeszcze brakuje, zmienia "
            "się o jeden przy wejściu i wyjściu znaku, więc warunek sprawdza się porównaniem z zerem."
        ),
    ),
    dict(
        pattern="stack",
        problem="floty-samochodow-sedno",
        difficulty=3,
        spec=(
            "Samochody na jednopasmowej drodze, każdy z pozycją i prędkością, nikt nikogo nie "
            "wyprzedza. Policz, ile odrębnych flot dotrze do mety."
        ),
        options=[
            "idąc od samochodu najbliższego mety, kolejny dołącza do floty przed sobą, gdy jego czas dojazdu nie jest większy",
            "flota powstaje wtedy, gdy samochód z tyłu jest szybszy od tego z przodu",
            "wystarczy posortować samochody po prędkości",
            "trzeba symulować ruch wszystkich samochodów krok po kroku",
        ],
        answer="idąc od samochodu najbliższego mety, kolejny dołącza do floty przed sobą, gdy jego czas dojazdu nie jest większy",
        spec_ref="nikt nikogo nie wyprzedza",
        explanation=(
            "Zakaz wyprzedzania zamienia zadanie w porównywanie czasów dojazdu. Sama większa "
            "prędkość nie wystarcza: liczy się, czy szybszy zdąży dogonić tego z przodu przed metą, "
            "a to widać po czasach, nie po prędkościach. Kolejność od mety sprawia, że flota z "
            "przodu jest już rozstrzygnięta."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="szukanie-po-odpowiedzi-sedno",
        difficulty=3,
        spec=(
            "Szukasz najmniejszej wartości parametru, przy której zadanie się udaje. Sprawdzenie "
            "jednej wartości jest tanie, a jeśli jakaś wartość wystarcza, to każda większa też."
        ),
        options=[
            "monotoniczność warunku pozwala szukać granicy połowieniem, choć wejście nie jest posortowane",
            "dane wejściowe trzeba najpierw posortować",
            "granicę znajduje się, sprawdzając wartości od najmniejszej po kolei",
            "wystarczy sprawdzić wartość średnią z danych wejściowych",
        ],
        answer="monotoniczność warunku pozwala szukać granicy połowieniem, choć wejście nie jest posortowane",
        spec_ref="jeśli jakaś wartość wystarcza, to każda większa też",
        explanation=(
            "To zdanie jest całym uzasadnieniem. Wyszukiwanie binarne nie potrzebuje posortowanej "
            "tablicy, tylko warunku, który raz spełniony pozostaje spełniony. Szuka się wtedy w "
            "przestrzeni odpowiedzi, a nie w danych."
        ),
    ),
    dict(
        pattern="binary-search",
        problem="minimum-w-obroconej-sedno",
        difficulty=3,
        spec=(
            "Tablica posortowana rosnąco i obrócona, bez powtórzeń. Znajdź najmniejszy element, "
            "porównując wyłącznie elementy tablicy między sobą."
        ),
        options=[
            "element środkowy porównuje się z prawym skrajnym, bo porównanie z lewym nie rozstrzyga dla tablicy nieobróconej",
            "element środkowy wystarczy porównać z lewym skrajnym",
            "wystarczy sprawdzić, czy pierwszy element jest większy od ostatniego",
            "punkt obrotu trzeba najpierw znaleźć przejściem liniowym",
        ],
        answer="element środkowy porównuje się z prawym skrajnym, bo porównanie z lewym nie rozstrzyga dla tablicy nieobróconej",
        spec_ref="porównując wyłącznie elementy tablicy między sobą",
        explanation=(
            "Przy porównaniu z lewym skrajnym tablica obrócona o zero wygląda tak samo jak taka, "
            "w której minimum leży po prawej, i trzeba dokładać osobny warunek brzegowy. "
            "Porównanie z prawym rozstrzyga jednoznacznie: środek większy od prawego oznacza, że "
            "minimum jest po prawej stronie."
        ),
    ),
    dict(
        pattern="linked-list",
        problem="powtorzona-liczba-sedno",
        difficulty=3,
        spec=(
            "Tablica n plus jeden liczb z zakresu od 1 do n. Dokładnie jedna wartość się powtarza, "
            "ale może wystąpić więcej niż dwa razy. Znajdź ją bez modyfikowania tablicy i w stałej pamięci."
        ),
        options=[
            "tablica zadaje funkcję z indeksu na wartość, więc powtórzenie jest wejściem do cyklu i znajdują je dwa wskaźniki",
            "wystarczy zbiór widzianych wartości",
            "wystarczy posortować tablicę i poszukać sąsiadów o równych wartościach",
            "wystarczy odjąć od sumy elementów sumę ciągu od 1 do n",
        ],
        answer="tablica zadaje funkcję z indeksu na wartość, więc powtórzenie jest wejściem do cyklu i znajdują je dwa wskaźniki",
        spec_ref="bez modyfikowania tablicy i w stałej pamięci",
        explanation=(
            "Zbiór łamie warunek pamięci, sortowanie łamie zakaz modyfikacji, a różnica sum "
            "zadziała tylko wtedy, gdy wartość powtarza się dokładnie dwa razy — treść na to nie "
            "pozwala liczyć. Potraktowanie tablicy jak funkcji sprowadza zadanie do wykrywania "
            "cyklu, które spełnia oba warunki naraz."
        ),
    ),
    dict(
        pattern="trees",
        problem="srednica-sedno",
        difficulty=3,
        spec=(
            "Drzewo binarne. Podaj długość najdłuższej ścieżki między dowolnymi dwoma węzłami. "
            "Ścieżka nie musi przechodzić przez korzeń."
        ),
        options=[
            "rekurencja zwraca wysokość poddrzewa, a najdłuższą ścieżkę aktualizuje po drodze jako sumę wysokości obu poddrzew węzła",
            "wynik to suma wysokości lewego i prawego poddrzewa korzenia",
            "najdłuższa ścieżka zawsze łączy dwa najgłębsze liście",
            "trzeba policzyć odległość między każdą parą węzłów",
        ],
        answer="rekurencja zwraca wysokość poddrzewa, a najdłuższą ścieżkę aktualizuje po drodze jako sumę wysokości obu poddrzew węzła",
        spec_ref="nie musi przechodzić przez korzeń",
        explanation=(
            "Ten warunek wyklucza liczenie czegokolwiek wyłącznie w korzeniu. Sztuczka polega na "
            "tym, że funkcja zwraca jedno (wysokość), a po drodze odkłada co innego (najlepszy "
            "wynik), dzięki czemu każdy węzeł jest rozpatrywany jako szczyt ścieżki w jednym przejściu."
        ),
    ),
    dict(
        pattern="trees",
        problem="odtworzenie-drzewa-sedno",
        difficulty=3,
        spec=(
            "Dane są dwa porządki obchodzenia drzewa binarnego, preorder i inorder, "
            "bez powtórzonych wartości. Odtwórz drzewo."
        ),
        options=[
            "pierwszy element preorder to korzeń, a jego pozycja w inorder dzieli resztę na lewe i prawe poddrzewo",
            "sam inorder wystarcza, bo zawiera wszystkie wartości we właściwej kolejności",
            "korzeniem jest ostatni element preorder",
            "trzeba wypróbować każdy element w roli korzenia",
        ],
        answer="pierwszy element preorder to korzeń, a jego pozycja w inorder dzieli resztę na lewe i prawe poddrzewo",
        spec_ref="bez powtórzonych wartości",
        explanation=(
            "Brak powtórzeń nie jest tu ozdobnikiem, tylko warunkiem koniecznym: pozycja korzenia "
            "w inorder musi być jednoznaczna. Sam inorder nie wystarcza, bo pasuje do wielu różnych "
            "drzew — dopiero drugi porządek mówi, który element jest korzeniem."
        ),
    ),
    dict(
        pattern="heap",
        problem="harmonogram-zadan-sedno",
        difficulty=3,
        spec=(
            "Zadania do wykonania i przerwa n, która musi minąć między dwoma wykonaniami tego "
            "samego zadania. Podaj najkrótszy łączny czas."
        ),
        options=[
            "czas wyznacza zadanie najczęstsze: jego wystąpienia tworzą szkielet przerw, który pozostałe zadania wypełniają",
            "czas zależy przede wszystkim od liczby różnych zadań",
            "wystarczy pomnożyć liczbę zadań przez długość przerwy",
            "kolejność nie ma znaczenia, więc czas to zawsze liczba zadań",
        ],
        answer="czas wyznacza zadanie najczęstsze: jego wystąpienia tworzą szkielet przerw, który pozostałe zadania wypełniają",
        spec_ref="przerwa n, która musi minąć między dwoma wykonaniami tego samego zadania",
        explanation=(
            "Ograniczenie dotyczy powtórzeń jednego zadania, więc to zadanie o największej liczbie "
            "wystąpień narzuca kształt harmonogramu. Reszta albo mieści się w jego przerwach i nic "
            "nie zmienia, albo jest jej tyle, że przerwy znikają i wynikiem jest po prostu liczba zadań."
        ),
    ),
    dict(
        pattern="backtracking",
        problem="hetmany-sedno",
        difficulty=3,
        spec=(
            "Szachownica n na n i n hetmanów, z których żaden nie może atakować innego. "
            "Stawiasz dokładnie jednego w każdym wierszu."
        ),
        options=[
            "obie przekątne adresuje się liczbami wiersz plus kolumna oraz wiersz minus kolumna, więc kolizję sprawdza się w czasie stałym",
            "przy każdym ustawieniu trzeba przejść całą szachownicę i sprawdzić pola atakowane",
            "wystarczy pilnować kolumn, bo wiersze są z definicji różne",
            "hetmany trzeba stawiać od środka planszy ku brzegom",
        ],
        answer="obie przekątne adresuje się liczbami wiersz plus kolumna oraz wiersz minus kolumna, więc kolizję sprawdza się w czasie stałym",
        spec_ref="Stawiasz dokładnie jednego w każdym wierszu",
        explanation=(
            "Założenie z treści usuwa wiersze z równania, zostają kolumny i dwie przekątne. "
            "Wszystkie pola jednej przekątnej mają tę samą sumę współrzędnych, a drugiej tę samą "
            "różnicę, więc trzy zbiory liczb zastępują przeglądanie planszy."
        ),
    ),
    dict(
        pattern="trie",
        problem="szukanie-wielu-slow-sedno",
        difficulty=3,
        spec="Siatka liter i lista wielu słów. Znajdź te słowa, które da się w siatce ułożyć.",
        options=[
            "wszystkie słowa wkłada się do jednego drzewa trie, żeby jedno przejście po siatce sprawdzało je naraz i urywało się na nieistniejącym przedrostku",
            "dla każdego słowa uruchamia się osobne przeszukiwanie siatki",
            "wystarczy sprawdzić, czy wszystkie litery słowa w ogóle występują w siatce",
            "słowa trzeba posortować i szukać ich binarnie",
        ],
        answer="wszystkie słowa wkłada się do jednego drzewa trie, żeby jedno przejście po siatce sprawdzało je naraz i urywało się na nieistniejącym przedrostku",
        spec_ref="lista wielu słów",
        explanation=(
            "Osobne przeszukiwanie dla każdego słowa jest poprawne, ale powtarza tę samą pracę "
            "tyle razy, ile jest słów o wspólnym początku. Trie odwraca zależność: przechodzisz "
            "siatkę raz, a zejście kończysz w chwili, gdy zbudowany przedrostek nie pasuje do żadnego słowa."
        ),
    ),
    dict(
        pattern="graphs",
        problem="splyw-do-dwoch-mors-sedno",
        difficulty=3,
        spec=(
            "Siatka wysokości, woda spływa do sąsiadów nie wyższych. Znajdź pola, z których "
            "woda dopłynie zarówno do górnej, jak i do dolnej krawędzi planszy."
        ),
        options=[
            "zamiast śledzić spływ z każdego pola, puszcza się przeszukiwanie od krawędzi pod górę i przecina oba otrzymane zbiory",
            "dla każdego pola trzeba prześledzić spływ w dół do obu krawędzi",
            "wystarczy sprawdzić pola o największej wysokości",
            "wystarczy jedno przeszukiwanie zaczęte od najwyższego pola",
        ],
        answer="zamiast śledzić spływ z każdego pola, puszcza się przeszukiwanie od krawędzi pod górę i przecina oba otrzymane zbiory",
        spec_ref="zarówno do górnej, jak i do dolnej krawędzi",
        explanation=(
            "Warunek „do obu” podpowiada przecięcie dwóch zbiorów, a odwrócenie kierunku zamienia "
            "sprawdzanie każdego pola z osobna na dwa przejścia po całej siatce. Relacja „spływa do” "
            "odwrócona daje „może przyjąć wodę od”, więc od krawędzi idzie się ku polom nie niższym."
        ),
    ),
    dict(
        pattern="graphs",
        problem="drabina-slow-sedno",
        difficulty=3,
        spec=(
            "Słowo początkowe, końcowe i słownik dozwolonych słów. W jednym kroku zmieniasz jedną "
            "literę, a wynik musi należeć do słownika. Podaj najmniejszą liczbę kroków."
        ),
        options=[
            "słowa są wierzchołkami, sąsiadów generuje się w locie podmieniając każdą literę, a najkrótszą drogę daje przeszukiwanie wszerz",
            "graf trzeba zbudować z góry, porównując każdą parę słów ze słownika",
            "wystarczy zachłannie zmieniać litery na te ze słowa końcowego",
            "to zadanie na programowanie dynamiczne po pozycjach liter",
        ],
        answer="słowa są wierzchołkami, sąsiadów generuje się w locie podmieniając każdą literę, a najkrótszą drogę daje przeszukiwanie wszerz",
        spec_ref="najmniejszą liczbę kroków",
        explanation=(
            "Zachłanne dopasowywanie liter zawodzi, bo słowo pośrednie może nie istnieć w słowniku "
            "i trzeba nadłożyć drogi. Budowanie pełnego grafu przez porównanie każdej pary jest "
            "poprawne, ale kwadratowe względem liczby słów; generowanie sąsiadów w locie kosztuje "
            "tyle, ile długość słowa razy alfabet."
        ),
    ),
    dict(
        pattern="graphs",
        problem="czy-graf-jest-drzewem-sedno",
        difficulty=3,
        spec="Graf nieskierowany o n wierzchołkach i lista krawędzi. Sprawdź, czy graf jest drzewem.",
        options=[
            "graf jest drzewem dokładnie wtedy, gdy jest spójny i ma dokładnie n minus jeden krawędzi",
            "wystarczy sprawdzić spójność",
            "wystarczy sprawdzić brak cykli",
            "wystarczy policzyć krawędzie",
        ],
        answer="graf jest drzewem dokładnie wtedy, gdy jest spójny i ma dokładnie n minus jeden krawędzi",
        spec_ref="Sprawdź, czy graf jest drzewem",
        explanation=(
            "Każdy z warunków osobno przepuszcza kontrprzykład: spójny graf z cyklem, las bez cykli, "
            "albo n minus jeden krawędzi ułożonych tak, że powstaje cykl i osobny wierzchołek. "
            "Dopiero para warunków jest równoważna byciu drzewem, i to jest cała treść tego zadania."
        ),
    ),
    dict(
        pattern="advanced-graphs",
        problem="spiecie-punktow-sedno",
        difficulty=3,
        spec=(
            "Punkty na płaszczyźnie, koszt połączenia dwóch to ich odległość. Połącz wszystkie "
            "punkty w jedną całość jak najtaniej."
        ),
        options=[
            "to jest minimalne drzewo rozpinające: dokłada się zachłannie najtańszą krawędź wychodzącą poza już spięty zbiór",
            "trzeba znaleźć najkrótszą trasę odwiedzającą wszystkie punkty",
            "wystarczy połączyć każdy punkt z jego najbliższym sąsiadem",
            "trzeba policzyć najkrótsze ścieżki algorytmem Dijkstry z dowolnego punktu",
        ],
        answer="to jest minimalne drzewo rozpinające: dokłada się zachłannie najtańszą krawędź wychodzącą poza już spięty zbiór",
        spec_ref="Połącz wszystkie punkty w jedną całość jak najtaniej",
        explanation=(
            "Łączenie każdego z najbliższym sąsiadem potrafi zostawić kilka rozłącznych grup. "
            "Najkrótsza trasa odwiedzająca wszystkie punkty to zupełnie inny, znacznie trudniejszy "
            "problem. Dijkstra liczy odległości od jednego źródła, a tutaj nie ma źródła — liczy się "
            "koszt spięcia całości."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="rabus-na-okregu-sedno",
        difficulty=3,
        spec=(
            "Domy ustawione na okręgu, więc pierwszy sąsiaduje z ostatnim. Wybierz podzbiór o "
            "największej sumie, w którym żadne dwa wybrane domy nie sąsiadują."
        ),
        options=[
            "wystarczy dwa razy rozwiązać wersję liniową, raz bez ostatniego domu i raz bez pierwszego, a potem wziąć lepszy wynik",
            "wystarczy rozwiązać wersję liniową i odjąć mniejszy z dwóch domów skrajnych",
            "trzeba rozważyć wszystkie podzbiory domów",
            "wystarczy zawsze pominąć pierwszy dom",
        ],
        answer="wystarczy dwa razy rozwiązać wersję liniową, raz bez ostatniego domu i raz bez pierwszego, a potem wziąć lepszy wynik",
        spec_ref="pierwszy sąsiaduje z ostatnim",
        explanation=(
            "Jedyna nowa trudność to para skrajnych domów, których nie można wziąć razem. "
            "Wystarczy więc rozbić zadanie na dwa przypadki, w których ten konflikt znika, i "
            "w każdym użyć rozwiązania z wersji liniowej bez żadnej zmiany."
        ),
    ),
    dict(
        pattern="dp-2d",
        problem="liczba-sposobow-wydania-sedno",
        difficulty=3,
        spec=(
            "Nominały monet i kwota. Policz, na ile sposobów da się ją wydać. Dwa sposoby "
            "różniące się tylko kolejnością monet uznajemy za ten sam sposób."
        ),
        options=[
            "pętla po nominałach musi być zewnętrzna, bo przy odwrotnym zagnieżdżeniu zliczane są permutacje, a nie kombinacje",
            "kolejność pętli nie ma znaczenia, liczy się tylko rozmiar tablicy stanów",
            "nominały trzeba posortować malejąco",
            "wystarczy policzyć najmniejszą liczbę monet i podnieść ją do potęgi",
        ],
        answer="pętla po nominałach musi być zewnętrzna, bo przy odwrotnym zagnieżdżeniu zliczane są permutacje, a nie kombinacje",
        spec_ref="różniące się tylko kolejnością monet uznajemy za ten sam sposób",
        explanation=(
            "To jeden z niewielu przypadków, w których kolejność zagnieżdżenia pętli zmienia wynik, "
            "a nie tylko szybkość. Nominał na zewnątrz sprawia, że każda kombinacja powstaje w "
            "jednym ustalonym porządku, więc jest liczona raz. Odwrotne zagnieżdżenie policzy "
            "1+2 i 2+1 jako dwa różne sposoby."
        ),
    ),
    dict(
        pattern="greedy",
        problem="skoki-minimalna-liczba-sedno",
        difficulty=3,
        spec=(
            "Tablica, w której wartość pola mówi, jak daleko najwyżej można z niego skoczyć. "
            "Podaj najmniejszą liczbę skoków potrzebną, by dojść na ostatnie pole."
        ),
        options=[
            "tablicę przechodzi się warstwami: bieżący zasięg zamyka jeden skok, a najdalszy widziany punkt otwiera następny",
            "zawsze opłaca się skoczyć tak daleko, jak to możliwe",
            "zawsze opłaca się skoczyć na pole o największej wartości w zasięgu",
            "trzeba sprawdzić wszystkie możliwe ciągi skoków",
        ],
        answer="tablicę przechodzi się warstwami: bieżący zasięg zamyka jeden skok, a najdalszy widziany punkt otwiera następny",
        spec_ref="najmniejszą liczbę skoków",
        explanation=(
            "Skok najdalszy bywa gorszy od krótszego, który ląduje na polu otwierającym większy "
            "zasięg — i tak samo zawodzi wybór pola o największej wartości, bo liczy się suma "
            "pozycji i wartości, nie sama wartość. Warstwy odpowiadają wprost liczbie skoków."
        ),
    ),
    dict(
        pattern="greedy",
        problem="etykiety-sedno",
        difficulty=2,
        spec=(
            "Napis. Podziel go na jak najwięcej fragmentów tak, żeby żadna litera nie pojawiła się "
            "w dwóch różnych fragmentach."
        ),
        options=[
            "granicę fragmentu wyznacza najdalsze ostatnie wystąpienie spośród liter widzianych do tej pory",
            "granicę wyznacza pierwsza litera, która nie powtarza się dalej",
            "wystarczy ciąć po każdej literze występującej tylko raz",
            "trzeba sprawdzić wszystkie możliwe podziały",
        ],
        answer="granicę fragmentu wyznacza najdalsze ostatnie wystąpienie spośród liter widzianych do tej pory",
        spec_ref="żadna litera nie pojawiła się w dwóch różnych fragmentach",
        explanation=(
            "Fragment można zamknąć dopiero wtedy, gdy każda litera, która się w nim pojawiła, "
            "już się dalej nie powtórzy. Wystarczy więc jedno wcześniejsze przejście zapisujące "
            "ostatnie wystąpienie każdej litery, a potem przesuwanie granicy w miarę czytania."
        ),
    ),
    dict(
        pattern="intervals",
        problem="wstawienie-przedzialu-sedno",
        difficulty=2,
        spec=(
            "Rozłączne przedziały posortowane po początku oraz nowy przedział. Wstaw go, scalając "
            "wszystko, co się z nim nachodzi, w jednym przejściu."
        ),
        options=[
            "przedziały rozpadają się na trzy grupy: kończące się przed nowym, nachodzące na niego i zaczynające się za nim",
            "trzeba dorzucić nowy przedział i posortować całość od nowa",
            "wystarczy porównać nowy przedział z pierwszym i ostatnim",
            "trzeba scalać sąsiednie pary od lewej, aż nic się nie zmieni",
        ],
        answer="przedziały rozpadają się na trzy grupy: kończące się przed nowym, nachodzące na niego i zaczynające się za nim",
        spec_ref="w jednym przejściu",
        explanation=(
            "Wejście jest już posortowane, więc trzy grupy występują dokładnie w tej kolejności i "
            "wystarczy je przepisać po kolei, a środkową zwinąć w jeden przedział. Ponowne "
            "sortowanie marnuje daną z treści i psuje obiecany jeden przebieg."
        ),
    ),
    dict(
        pattern="math",
        problem="zerowanie-macierzy-sedno",
        difficulty=3,
        spec=(
            "Macierz. Jeśli komórka zawiera zero, wyzeruj cały jej wiersz i całą jej kolumnę. "
            "Zrób to bez dodatkowej pamięci rosnącej wraz z rozmiarem macierzy."
        ),
        options=[
            "pierwszy wiersz i pierwsza kolumna służą za znaczniki, a to, czy same mają być wyzerowane, trzeba zapamiętać osobno",
            "wystarczy zerować wiersz i kolumnę od razu po napotkaniu zera",
            "wystarczy zapamiętać listę współrzędnych wszystkich zer",
            "macierz trzeba przejść od prawego dolnego rogu ku lewemu górnemu",
        ],
        answer="pierwszy wiersz i pierwsza kolumna służą za znaczniki, a to, czy same mają być wyzerowane, trzeba zapamiętać osobno",
        spec_ref="bez dodatkowej pamięci rosnącej wraz z rozmiarem macierzy",
        explanation=(
            "Zerowanie w locie zamazuje informację: świeżo wpisane zero jest nieodróżnialne od "
            "pierwotnego i lawinowo zeruje całą macierz. Lista współrzędnych jest poprawna, ale "
            "łamie warunek pamięci. Znaczniki w pierwszym wierszu i kolumnie mieszczą się w stałej "
            "pamięci, pod warunkiem że ich własny los rozstrzygnie się osobno, przed nadpisaniem."
        ),
    ),
    dict(
        pattern="math",
        problem="szybkie-potegowanie-sedno",
        difficulty=2,
        spec="Policz x podniesione do całkowitej potęgi n, w czasie logarytmicznym względem n.",
        options=[
            "x do potęgi n to kwadrat x do potęgi n przez dwa, a przy nieparzystym n dochodzi jeszcze jedno mnożenie przez x",
            "wystarczy pomnożyć x przez siebie n razy",
            "wystarczy policzyć eksponentę z iloczynu logarytmu i n",
            "każdy wynik da się zapisać jako iloczyn potęg dwójki",
        ],
        answer="x do potęgi n to kwadrat x do potęgi n przez dwa, a przy nieparzystym n dochodzi jeszcze jedno mnożenie przez x",
        spec_ref="w czasie logarytmicznym",
        explanation=(
            "Każde podniesienie do kwadratu podwaja wykładnik, więc liczba kroków to liczba bitów "
            "n. Mnożenie n razy jest poprawne, ale liniowe, a droga przez logarytm i eksponentę "
            "traci dokładność i nie działa dla ujemnych podstaw."
        ),
    ),
    dict(
        pattern="bit-manipulation",
        problem="liczenie-bitow-sedno",
        difficulty=3,
        spec=(
            "Liczba n. Dla każdej liczby od zera do n podaj, ile jedynek ma w zapisie binarnym. "
            "Łączny czas ma być liniowy względem n."
        ),
        options=[
            "liczba jedynek w i to liczba jedynek w i przesuniętym o jeden bit w prawo, powiększona o najmłodszy bit i",
            "dla każdej liczby trzeba przejść wszystkie jej bity",
            "liczba jedynek rośnie o jeden przy każdej kolejnej liczbie",
            "wystarczy policzyć jedynki w n i odejmować",
        ],
        answer="liczba jedynek w i to liczba jedynek w i przesuniętym o jeden bit w prawo, powiększona o najmłodszy bit i",
        spec_ref="Łączny czas ma być liniowy",
        explanation=(
            "Przesunięcie w prawo daje liczbę mniejszą, więc jej wynik jest już policzony. To "
            "zamienia liczenie bitów w programowanie dynamiczne o stałym koszcie na liczbę. "
            "Przechodzenie wszystkich bitów każdej liczby daje O(n log n), czyli za wolno."
        ),
    ),
    dict(
        pattern="bit-manipulation",
        problem="suma-bez-plusa-sedno",
        difficulty=3,
        spec="Dodaj dwie liczby całkowite, nie używając operatora dodawania ani odejmowania.",
        options=[
            "XOR daje sumę bez przeniesień, a AND przesunięty o bit w lewo daje same przeniesienia, więc powtarza się to, aż przeniesień zabraknie",
            "wystarczy XOR obu liczb",
            "wystarczy OR obu liczb",
            "trzeba zamienić liczby na napisy i dodać je cyfra po cyfrze",
        ],
        answer="XOR daje sumę bez przeniesień, a AND przesunięty o bit w lewo daje same przeniesienia, więc powtarza się to, aż przeniesień zabraknie",
        spec_ref="nie używając operatora dodawania ani odejmowania",
        explanation=(
            "Sam XOR jest dodawaniem tylko wtedy, gdy żadna pozycja nie generuje przeniesienia. "
            "Rozbicie na dwie części, sumę bez przeniesień i same przeniesienia, i powtarzanie tego "
            "aż do wyzerowania przeniesień, odtwarza dokładnie działanie sumatora sprzętowego."
        ),
    ),
    dict(
        pattern="dp-1d",
        problem="dekodowanie-sedno",
        difficulty=3,
        spec=(
            "Napis cyfr, w którym 1 oznacza A, a 26 oznacza Z. Policz, na ile sposobów da się go "
            "odczytać. Zero samo w sobie nie koduje żadnej litery."
        ),
        options=[
            "wynik dla pozycji to suma dwóch poprzednich wyników, ale każdy z nich dokłada się tylko wtedy, gdy odpowiadający mu kod jest dopuszczalny",
            "wynik dla pozycji to zawsze suma dwóch poprzednich, jak w ciągu Fibonacciego",
            "wystarczy policzyć, ile jest w napisie liczb dwucyfrowych nie większych niż 26",
            "wynik to dwa podniesione do potęgi równej długości napisu",
        ],
        answer="wynik dla pozycji to suma dwóch poprzednich wyników, ale każdy z nich dokłada się tylko wtedy, gdy odpowiadający mu kod jest dopuszczalny",
        spec_ref="Zero samo w sobie nie koduje żadnej litery",
        explanation=(
            "Bez warunku dopuszczalności wychodzi Fibonacci, który ignoruje zera i liczby powyżej "
            "26. Cała trudność tego zadania siedzi w tym jednym sprawdzeniu, a zera są jego "
            "najczęściej przeoczanym przypadkiem."
        ),
    ),
]
