"""Testy pipeline'u.

Dwie rzeczy musza byc pewne, zanim korpus w ogole ma sens:
1. implementacje referencyjne sa poprawne (sprawdzane brute-force'em, nie same soba),
2. mutant przechodzacy testy nigdy nie trafia do korpusu.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import exercises  # noqa: E402
import mutations  # noqa: E402
import runner  # noqa: E402

PATTERNS = ROOT / "patterns"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def problem_modules():
    return [load(p) for p in sorted(PATTERNS.glob("*/[!_]*.py"))]


def ids(modules):
    return [m.PROBLEM for m in modules]


MODULES = problem_modules()


# --- niezalezne implementacje odniesienia (brute force, O(n^2)) ---------------


def brute_min_subarray(nums, target):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                length = j - i + 1
                if best == 0 or length < best:
                    best = length
                break
    return best


def brute_longest_k_distinct(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i : j + 1])) <= k:
                best = max(best, j - i + 1)
    return best


BRUTE = {
    "min-subarray": brute_min_subarray,
    "longest-k-distinct": brute_longest_k_distinct,
}


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_oczekiwane_wyniki_zgadzaja_sie_z_brute_force(module):
    """Wartosci `expect` w testach nie moga pochodzic z tej samej implementacji,
    ktora maja sprawdzac."""
    reference = BRUTE[module.PROBLEM]
    for test in module.TESTS:
        assert reference(*test["args"]) == test["expect"], test


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_implementacja_referencyjna_przechodzi_wlasne_testy(module):
    for test in module.TESTS:
        assert module.solution(*test["args"]) == test["expect"], test


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_kazde_cwiczenie_pochodzi_z_zabitego_mutanta(module):
    """Sedno filtra: mutant, ktory przeszedl testy, nie ma poprawnej odpowiedzi."""
    _, killed, survived, trivial = exercises.evaluate(module)
    assert killed, "brak zabitych mutantow - filtr albo generator nie dziala"
    for item in killed:
        assert not item.outcome.all_pass
    for mutation in survived:
        outcome = runner.run_tests(mutation.source, module.FUNC, module.TESTS)
        assert outcome.all_pass, "mutant odrzucony mimo ze oblewa testy"
    for item in killed:
        details = [item.outcome.details[i] for i in item.outcome.failing]
        assert not all(
            any(marker in d for marker in exercises.TRIVIAL_ERRORS) for d in details
        ), "cwiczenie z mutanta wywalajacego sie na niezdefiniowanej nazwie"


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_odpowiedz_wskazuje_na_wlasciwa_opcje(module):
    built, _, _, _ = exercises.build(module)
    assert built
    for item in (e.to_dict() for e in built):
        if item["ui"] == "choice":
            assert isinstance(item["answer"], int)
            assert 0 <= item["answer"] < len(item["options"])
        else:
            assert sorted(item["answer"]) == list(range(len(item["options"])))


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_which_test_ma_dokladnie_jedna_poprawna_odpowiedz(module):
    """W `ktory test wykryje blad` pozostale trzy opcje musza faktycznie przechodzic."""
    source, killed, _, _ = exercises.evaluate(module)
    by_label = {exercises.test_label(module, t): t for t in module.TESTS}
    for item in exercises.build_which_test(module, killed, limit=99):
        data = item.to_dict()
        wrong = [o for i, o in enumerate(data["options"]) if i != data["answer"]]
        mutant_source = data["code"]
        for label in wrong:
            test = by_label[label]
            outcome = runner.run_tests(mutant_source, module.FUNC, [test])
            assert outcome.all_pass, "dystraktor {} tez wykrywa blad w {}".format(label, data["id"])


@pytest.mark.parametrize("module", MODULES, ids=ids(MODULES))
def test_predict_output_zgadza_sie_z_uruchomieniem(module):
    """Zaznaczona odpowiedz musi byc tym, co kod faktycznie zwraca.

    Test uruchamia pokazany kod niezaleznie od generatora, wiec wykryje zarowno
    zla odpowiedz, jak i dystraktor, ktory przypadkiem rowna sie poprawnemu wynikowi.
    """
    source, killed, _, _ = exercises.evaluate(module)
    built = exercises.build_predict_output(module, source, killed, limit=99)
    assert built, "brak cwiczen predict-output dla {}".format(module.PROBLEM)

    for item in built:
        data = item.to_dict()
        index = int(data["id"].rsplit("-", 1)[1])
        outcome = runner.run_tests(data["code"], module.FUNC, [module.TESTS[index]])

        assert outcome.statuses[0] == runner.PASS, "kod w {} nie jest poprawny".format(data["id"])
        produced = outcome.details[0]
        assert data["options"][data["answer"]] == produced, (
            "zaznaczona opcja w {} to nie to, co kod zwraca".format(data["id"])
        )
        for position, option in enumerate(data["options"]):
            if position != data["answer"]:
                assert option != produced, (
                    "dystraktor w {} rowna sie poprawnemu wynikowi".format(data["id"])
                )


def test_mutacja_bez_zmiany_kodu_jest_odrzucana():
    source = "def solution(x):\n    return x\n"
    for mutation in mutations.generate(source):
        assert mutation.source != mutations.normalize(source)


def test_timeout_nie_zatruwa_pozostalych_testow():
    """Zapetlenie na jednym tescie nie moze oznaczyc kolejnych jako niezdanych."""
    source = "def solution(x):\n    while x == 1:\n        pass\n    return x\n"
    tests = [
        {"args": [0], "expect": 0},
        {"args": [1], "expect": 1},
        {"args": [2], "expect": 2},
    ]
    outcome = runner.run_tests(source, "solution", tests, timeout=0.5)
    assert outcome.statuses[0] == runner.PASS
    assert outcome.statuses[1] == runner.TIMEOUT
    assert outcome.statuses[2] == runner.PASS


def test_kolejnosc_jednoznaczna_jest_przyjmowana():
    """Lancuch zaleznosci wymusza dokladnie jedna kolejnosc."""
    order, tied = exercises.forced_order([[], [0], [1]])

    assert order == [0, 1, 2]
    assert tied == []


def test_dwa_kroki_gotowe_naraz_sa_odrzucane():
    """Dwie niezalezne inicjalizacje to dwie poprawne odpowiedzi, czyli zadna."""
    order, tied = exercises.forced_order([[], [], [0, 1]])

    assert order is None
    assert tied == [0, 1]


def test_check_forced_order_wskazuje_winne_kroki():
    steps = ["ustaw wskazniki", "zapamietaj maksima", "policz wynik"]

    with pytest.raises(AssertionError) as blad:
        exercises.check_forced_order("test/x", steps, [[], [], [0, 1]])

    assert "nie jest jednoznaczna" in str(blad.value)
    assert "ustaw wskazniki" in str(blad.value)


def test_zaleznosc_musi_wskazywac_krok_wczesniejszy():
    with pytest.raises(AssertionError) as blad:
        exercises.check_forced_order("test/x", ["a", "b"], [[1], []])

    assert "wczesniejszy" in str(blad.value)


def test_wszystkie_cwiczenia_order_steps_maja_wymuszona_kolejnosc():
    """Kazdy wpis w korpusie kurowanym przechodzi ten sam sprawdzian co w buildzie."""
    curated = ROOT / "curated"
    sprawdzone = 0

    for path in sorted(curated.glob("*.py")):
        if path.name.startswith("_"):
            continue
        module = load(path)
        domyslny = getattr(module, "DEFAULT_TYPE", "recognize-pattern")
        for entry in module.EXERCISES:
            if entry.get("type", domyslny) != "order-steps":
                continue
            assert "deps" in entry, "{}: brak deps".format(entry["problem"])
            exercises.check_forced_order(entry["problem"], entry["steps"], entry["deps"])
            sprawdzone += 1

    assert sprawdzone > 0, "nie znaleziono zadnego cwiczenia order-steps"
