"""Uzupełnienie kategorii stos i kopiec z NeetCode 150.

Obie kategorie mają na liście po siedem zadań. Ten moduł domyka luki, które
zostały po wcześniejszych partiach: odwrotna notacja polska, Design Twitter,
Last Stone Weight i quickselect nie miały ani jednego ćwiczenia, a kilka
pozostałych zadań miało tylko `recognize-pattern`.

Podział typów według natury zadania, a nie na chybił trafił:

* `order-steps` dostają algorytmy sekwencyjne, w których każdy krok zużywa
  wynik poprzedniego. Zadania projektowe, gdzie operacje są niezależne, dałyby
  kilka poprawnych ułożeń, więc trafiają do pozostałych typów.
* `key-insight` dostają zadania, w których jedna obserwacja decyduje o tym, czy
  rozwiązanie w ogóle jest poprawne albo czy mieści się w wymaganej złożoności.
* `edge-case` opisuje podejście prawie dobre i pyta, co je łamie.

Treści są własne. Lista NeetCode wyznacza dobór zadań, nie brzmienie opisów.
"""

CORPUS = {
    "id": "neetcode-150",
    "name": "NeetCode 150 — sedno",
}

DEFAULT_TYPE = "order-steps"

EXERCISES = [
    # ------------------------------------------------------------------ stos
    dict(
        pattern="stack",
        problem="onp-kroki",
        difficulty=2,
        spec=(
            "Policz wartość wyrażenia zapisanego w odwrotnej notacji polskiej, w której "
            "działanie stoi za swoimi argumentami."
        ),
        steps=[
            "przygotuj pusty stos na liczby",
            "czytaj kolejne symbole wyrażenia od lewej do prawej",
            "gdy symbol jest liczbą, odłóż ją na stos",
            "gdy symbol jest działaniem, zdejmij ze stosu dwie liczby",
            "potraktuj pierwszą zdjętą jako prawy argument, a drugą jako lewy",
            "odłóż wynik działania na stos, a po wyczerpaniu symboli zwróć jedyną pozostałą liczbę",
        ],
        explanation=(
            "Kolejność zdejmowania jest odwrotna do kolejności zapisu, więc pierwsza zdjęta "
            "liczba jest tą stojącą po prawej. Przy dodawaniu i mnożeniu nie ma to znaczenia, "
            "ale przy odejmowaniu i dzieleniu zamiana argumentów daje inny wynik."
        ),
    ),
    dict(
        pattern="stack",
        problem="cieplejszy-dzien-kroki",
        difficulty=2,
        spec=(
            "Temperatury w kolejnych dniach. Dla każdego dnia podaj, ile dni trzeba czekać na "
            "pierwszy cieplejszy, albo zero, gdy taki nie nadejdzie."
        ),
        steps=[
            "przygotuj tablicę wyników wypełnioną zerami",
            "przygotuj stos na indeksy dni, które wciąż czekają na cieplejszy",
            "przechodź dni od lewej do prawej",
            "dopóki bieżąca temperatura jest wyższa od temperatury dnia ze szczytu stosu, zdejmij ten szczyt",
            "dla każdego zdjętego dnia wpisz do wyniku różnicę między bieżącym indeksem a jego własnym",
            "dołóż bieżący indeks na stos i przejdź do następnego dnia",
        ],
        explanation=(
            "Dni zostające na stosie do końca mają w wyniku zero, bo tablica była nim wypełniona "
            "od początku. Dlatego nie trzeba osobno obsługiwać dni, dla których cieplejszy nigdy "
            "nie nadchodzi."
        ),
    ),
    dict(
        pattern="stack",
        problem="stos-z-minimum-kroki",
        difficulty=2,
        spec=(
            "Zaprojektuj stos, który poza wkładaniem i zdejmowaniem podaje najmniejszy "
            "przechowywany element w czasie stałym."
        ),
        steps=[
            "przygotuj stos na same wartości",
            "przygotuj drugi stos, na którym będzie leżeć minimum obowiązujące dla bieżącego stanu pierwszego",
            "przy wkładaniu odłóż wartość na stos wartości",
            "porównaj wkładaną wartość ze szczytem stosu minimów",
            "odłóż na stos minimów mniejszą z porównanych wartości",
            "przy zdejmowaniu usuń szczyt obu stosów naraz, dzięki czemu minimum samo wraca do poprzedniego",
        ],
        explanation=(
            "Na stosie minimów nie leżą kolejne coraz mniejsze wartości, tylko minimum osobno dla "
            "każdej wysokości stosu. Dlatego wysokości obu stosów muszą być zawsze równe i dlatego "
            "zdejmowanie musi dotyczyć obu naraz."
        ),
    ),
    dict(
        pattern="stack",
        problem="najwiekszy-prostokat-sedno",
        type="key-insight",
        difficulty=3,
        spec=(
            "Histogram słupków o jednostkowej szerokości. Znajdź pole największego prostokąta, "
            "jaki się w nim mieści, w czasie liniowym."
        ),
        options=[
            "w chwili zdejmowania słupka ze stosu znane są obie granice jego prostokąta naraz",
            "największy prostokąt zawsze opiera się na najwyższym słupku",
            "wystarczy sprawdzić wszystkie pary granic i wziąć najlepszą",
            "prostokąt zawsze zaczyna się przy pierwszym słupku histogramu",
        ],
        answer="w chwili zdejmowania słupka ze stosu znane są obie granice jego prostokąta naraz",
        spec_ref="w czasie liniowym",
        explanation=(
            "Prawą granicę wyznacza słupek, który wymusił zdjęcie, bo jest pierwszym niższym po "
            "prawej. Lewą wyznacza ten, który leży pod spodem, bo jest pierwszym niższym po lewej. "
            "Sprawdzanie wszystkich par jest poprawne, ale kwadratowe, a najwyższy słupek bywa tak "
            "wąski, że jego prostokąt jest maleńki."
        ),
    ),
    dict(
        pattern="stack",
        problem="cieplejszy-dzien-sedno",
        type="key-insight",
        difficulty=3,
        spec=(
            "Dla każdego dnia szukasz najbliższego cieplejszego, używając stosu z pętlą "
            "wewnętrzną. Rozwiązanie ma być liniowe."
        ),
        options=[
            "każdy indeks trafia na stos raz i schodzi z niego raz, więc pętla wewnętrzna nie psuje liniowości",
            "pętla wewnętrzna sprawia, że koszt jest kwadratowy",
            "stos trzeba przy każdym dniu przeglądać od dołu do góry",
            "liniowość wymaga ograniczenia rozmiaru stosu z góry",
        ],
        answer="każdy indeks trafia na stos raz i schodzi z niego raz, więc pętla wewnętrzna nie psuje liniowości",
        spec_ref="Rozwiązanie ma być liniowe",
        explanation=(
            "Zagnieżdżona pętla wygląda na kwadratową i to jest najczęstsza pomyłka przy szacowaniu "
            "kosztu tego rozwiązania. Liczy się jednak łączna liczba zdjęć, a ta nie może przekroczyć "
            "liczby włożeń, czyli n. To rozumowanie nazywa się analizą zamortyzowaną."
        ),
    ),
    dict(
        pattern="stack",
        problem="stos-z-minimum-sedno",
        type="key-insight",
        difficulty=3,
        spec=(
            "Stos ma podawać najmniejszy przechowywany element w czasie stałym, także po "
            "zdjęciu elementu."
        ),
        options=[
            "minimum trzeba zapamiętywać osobno dla każdej wysokości stosu, bo zdjęcie elementu potrafi je cofnąć do wcześniejszej wartości",
            "wystarczy jedna zmienna trzymająca bieżące minimum",
            "wystarczy przeliczyć minimum po każdym zdjęciu elementu",
            "wystarczy trzymać elementy w stosie w porządku rosnącym",
        ],
        answer="minimum trzeba zapamiętywać osobno dla każdej wysokości stosu, bo zdjęcie elementu potrafi je cofnąć do wcześniejszej wartości",
        spec_ref="także po zdjęciu elementu",
        explanation=(
            "Pojedyncza zmienna radzi sobie z wkładaniem, ale nie ze zdejmowaniem: gdy usuwany "
            "element był właśnie minimum, nie ma skąd odtworzyć poprzedniego. Przeliczanie po "
            "każdym zdjęciu daje poprawny wynik, ale kosztuje O(n), więc łamie warunek z treści."
        ),
    ),
    dict(
        pattern="stack",
        problem="onp-przypadek",
        type="edge-case",
        difficulty=2,
        spec=(
            "Liczysz wartość wyrażenia w odwrotnej notacji polskiej: liczby odkładasz na stos, "
            "a przy działaniu zdejmujesz dwie i odkładasz wynik. Jako lewy argument bierzesz "
            "pierwszą zdjętą liczbę."
        ),
        prompt="Które wyrażenie ujawni błąd w tym podejściu?",
        options=['"3 4 -"', '"3 4 +"', '"2 3 *"', '"5 5 -"'],
        answer='"3 4 -"',
        explanation=(
            "Poprawny wynik to trzy minus cztery, czyli minus jeden, a podejście policzy cztery "
            "minus trzy i zwróci jeden. Dodawanie i mnożenie są przemienne, więc na nich błąd się "
            "nie ujawni, a przy dwóch równych liczbach zamiana argumentów też niczego nie zmieni."
        ),
    ),
    dict(
        pattern="stack",
        problem="floty-przypadek",
        type="edge-case",
        difficulty=3,
        spec=(
            "Liczysz floty samochodów: idziesz od najbliższego mety i zaczynasz nową flotę, gdy "
            "czas dojazdu bieżącego samochodu jest ostro większy od czasu na szczycie stosu."
        ),
        prompt="Który przypadek trzeba tu rozstrzygnąć świadomie, a nie przez przypadek?",
        options=[
            "dwa samochody o dokładnie równym czasie dojazdu",
            "dwa samochody o równej prędkości",
            "samochód stojący dokładnie na mecie",
            "jeden samochód na całej drodze",
        ],
        answer="dwa samochody o dokładnie równym czasie dojazdu",
        explanation=(
            "Równy czas oznacza, że oba dojadą w tej samej chwili, więc tworzą jedną flotę, a nie "
            "dwie. Ostra nierówność załatwia to poprawnie, ale gdyby ktoś napisał nieostrą, wynik "
            "urósłby o jeden. To jest decyzja projektowa, którą trzeba zapisać, a nie odgadywać "
            "z implementacji."
        ),
    ),
    # ---------------------------------------------------------------- kopiec
    dict(
        pattern="heap",
        problem="k-najblizszych-kroki",
        difficulty=2,
        spec=(
            "Punkty na płaszczyźnie i liczba k. Podaj k punktów leżących najbliżej początku "
            "układu współrzędnych."
        ),
        steps=[
            "przygotuj kopiec maksymalny uporządkowany po odległości punktu od początku układu",
            "przechodź punkty po kolei",
            "policz dla punktu kwadrat odległości, bez pierwiastkowania",
            "wrzuć punkt na kopiec",
            "jeśli kopiec urósł ponad k elementów, zdejmij jego wierzchołek, czyli najdalszy z trzymanych punktów",
            "po przejściu wszystkich punktów zwróć zawartość kopca",
        ],
        explanation=(
            "Kopiec jest maksymalny, choć szukasz najbliższych: na wierzchołku ma leżeć najgorszy "
            "z trzymanych kandydatów, bo to jego wyrzucasz. Pierwiastek można pominąć, bo nie "
            "zmienia porządku, a kosztuje."
        ),
    ),
    dict(
        pattern="heap",
        problem="harmonogram-zadan-kroki",
        difficulty=3,
        spec=(
            "Zadania do wykonania i przerwa, która musi minąć między dwoma wykonaniami tego "
            "samego zadania. Odtwórz przebieg harmonogramu jednostka po jednostce."
        ),
        steps=[
            "policz, ile razy występuje każde zadanie",
            "wrzuć liczniki na kopiec maksymalny i przygotuj kolejkę na zadania odbywające przerwę",
            "na początku każdej jednostki czasu przenieś na kopiec te zadania z kolejki, którym przerwa już minęła",
            "zdejmij z kopca zadanie o największym pozostałym liczniku i wykonaj je",
            "zmniejsz jego licznik o jeden",
            "jeśli licznik jest wciąż dodatni, wstaw zadanie do kolejki wraz z chwilą, w której będzie mogło wrócić",
        ],
        explanation=(
            "Kopiec pilnuje, żeby zawsze schodziło zadanie najpilniejsze, a kolejka pilnuje przerwy. "
            "Przenoszenie z kolejki musi następować przed wyborem zadania, inaczej zadanie gotowe "
            "do powrotu przegapi swoją jednostkę."
        ),
    ),
    dict(
        pattern="heap",
        problem="k-ty-najwiekszy-kroki",
        difficulty=3,
        spec=(
            "Tablica liczb i wartość k. Podaj k-ty co do wielkości element, przestawiając "
            "elementy w miejscu zamiast używać dodatkowej struktury."
        ),
        steps=[
            "wybierz element rozdzielający spośród bieżącego zakresu",
            "przestaw elementy tak, żeby mniejsze od niego trafiły na lewo, a większe na prawo",
            "odczytaj pozycję, na której ostatecznie wylądował element rozdzielający",
            "jeśli to jest dokładnie szukane miejsce, zwróć stojącą tam wartość",
            "jeśli szukane miejsce leży na lewo od niej, powtórz całość wyłącznie dla lewej części",
            "w przeciwnym razie powtórz dla prawej części, zawężając zakres",
        ],
        explanation=(
            "To jest quickselect: jak sortowanie szybkie, ale schodzi tylko w tę połowę, w której "
            "leży odpowiedź. Stąd średni koszt liniowy zamiast n log n. Kopiec też rozwiąże zadanie, "
            "lecz wymaga dodatkowej pamięci, czego treść zabrania."
        ),
    ),
    dict(
        pattern="heap",
        problem="ostatni-kamien-kroki",
        difficulty=1,
        spec=(
            "Kamienie o podanych wagach. W każdym kroku zderzasz dwa najcięższe: lżejszy znika, "
            "a cięższy traci wagę lżejszego. Podaj wagę kamienia, który zostanie."
        ),
        steps=[
            "wrzuć wagi wszystkich kamieni na kopiec maksymalny",
            "dopóki na kopcu są co najmniej dwa kamienie, zdejmij najcięższy",
            "zdejmij drugi najcięższy",
            "policz różnicę ich wag",
            "jeśli różnica jest dodatnia, wrzuć ją na kopiec jako nowy kamień",
            "gdy zostanie najwyżej jeden kamień, zwróć jego wagę, a przy pustym kopcu zero",
        ],
        explanation=(
            "Zerowa różnica oznacza, że oba kamienie znikają, więc nie wraca nic. Kopiec maksymalny "
            "jest tu naturalny, bo po każdym zderzeniu skład zbioru się zmienia i najcięższy trzeba "
            "wyznaczać od nowa."
        ),
    ),
    dict(
        pattern="heap",
        problem="k-ty-najwiekszy-sedno",
        type="key-insight",
        difficulty=3,
        spec=(
            "Tablica n liczb i wartość k. Podaj k-ty co do wielkości element, przy czym n jest "
            "bardzo duże, a k małe."
        ),
        options=[
            "kopiec ma być minimalny i rozmiaru k, bo na wierzchołku leży wtedy najsłabszy z kandydatów i to jego wypycha lepszy element",
            "kopiec ma być maksymalny i rozmiaru k",
            "kopiec ma zawierać wszystkie n elementów, a odpowiedź zdejmuje się k razy",
            "trzeba posortować całą tablicę i odczytać element z pozycji k",
        ],
        answer="kopiec ma być minimalny i rozmiaru k, bo na wierzchołku leży wtedy najsłabszy z kandydatów i to jego wypycha lepszy element",
        spec_ref="n jest bardzo duże, a k małe",
        explanation=(
            "Rodzaj kopca jest tu odwrotny do intuicji: szukasz największych, więc kopiec jest "
            "minimalny, bo na wierzchołku ma stać ten do wyrzucenia. Kopiec ze wszystkich n "
            "elementów i sortowanie dają poprawny wynik, ale kosztują O(n log n), podczas gdy "
            "kopiec rozmiaru k daje O(n log k)."
        ),
    ),
    dict(
        pattern="heap",
        problem="twitter-sedno",
        type="key-insight",
        difficulty=3,
        spec=(
            "Serwis, w którym użytkownik obserwuje innych. Pokaż dziesięć najnowszych wpisów "
            "spośród obserwowanych, przy czym wpisów w całym serwisie jest bardzo dużo."
        ),
        options=[
            "wpisy każdego użytkownika są już uporządkowane w czasie, więc wystarczy scalić kopcem same ich najnowsze końce",
            "trzeba zebrać wpisy wszystkich obserwowanych i posortować je po czasie",
            "wystarczy wziąć dziesięć ostatnich wpisów w całym serwisie i odfiltrować obserwowanych",
            "trzeba trzymać osobną listę wpisów dla każdej pary obserwujący i obserwowany",
        ],
        answer="wpisy każdego użytkownika są już uporządkowane w czasie, więc wystarczy scalić kopcem same ich najnowsze końce",
        spec_ref="wpisów w całym serwisie jest bardzo dużo",
        explanation=(
            "To jest scalanie posortowanych list, tylko przebrane za serwis społecznościowy. "
            "Sortowanie wszystkich wpisów obserwowanych daje poprawny wynik, ale koszt rośnie z "
            "całą historią, a potrzeba tylko dziesięciu. Filtrowanie globalnych wpisów zawodzi, "
            "gdy obserwowani nie pisali od dawna."
        ),
    ),
    dict(
        pattern="heap",
        problem="kopiec-rozmiaru-k-przypadek",
        type="edge-case",
        difficulty=2,
        spec=(
            "Utrzymujesz k największych elementów: każdy nowy wrzucasz na kopiec, a gdy kopiec "
            "przekroczy rozmiar k, zdejmujesz jego wierzchołek. Użyłeś kopca maksymalnego."
        ),
        prompt="Co się przy tym psuje?",
        options=[
            "wyrzucany jest za każdym razem największy element, więc w kopcu zostają najmniejsze",
            "kopiec rośnie ponad rozmiar k",
            "koszt rośnie do O(n log n)",
            "nic, wynik jest poprawny, zmienia się tylko kolejność",
        ],
        answer="wyrzucany jest za każdym razem największy element, więc w kopcu zostają najmniejsze",
        explanation=(
            "Rozmiar pilnowany jest poprawnie i koszt też się zgadza, więc błąd nie objawia się ani "
            "wolniejszym działaniem, ani przepełnieniem. Wynik jest po prostu odwrotny do żądanego. "
            "Kopiec ma być minimalny: na wierzchołku stoi wtedy najsłabszy kandydat, czyli ten, "
            "którego należy wyrzucić."
        ),
    ),
]
