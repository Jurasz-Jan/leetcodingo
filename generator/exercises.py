"""Budowanie cwiczen ze zwalidowanych mutantow.

Wejscie: modul wzorca (poprawna implementacja + spec + testy).
Wyjscie: lista cwiczen gotowych do zapisania w korpusie.

Zasada: cwiczenie powstaje wylacznie z mutanta, ktory OBLAL testy. Mutant
przechodzacy testy nie ma poprawnej odpowiedzi, wiec nie trafia do korpusu.
"""

from __future__ import annotations

import inspect
import random
from dataclasses import dataclass, field

import mutations
import runner

EST_SECONDS = {
    "find-bug": lambda d: 30 + 10 * d,
    "fill-gap": lambda d: 45,
    "order-steps": lambda d: 60,
    "complexity": lambda d: 25,
    "predict-output": lambda d: 15 + 15 * d,
}


@dataclass
class Exercise:
    id: str
    pattern: str
    problem: str
    type: str
    difficulty: int
    spec: str
    prompt: str
    code: str
    options: list
    answer: object
    explanation: str
    spec_ref: object
    est_seconds: int
    ui: str = "choice"
    source: str = "generated"
    reviewed: bool = True
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pattern": self.pattern,
            "problem": self.problem,
            "type": self.type,
            "ui": self.ui,
            "difficulty": self.difficulty,
            "spec": self.spec,
            "prompt": self.prompt,
            "code": self.code,
            "options": self.options,
            "answer": self.answer,
            "explanation": self.explanation,
            "spec_ref": self.spec_ref,
            "est_seconds": self.est_seconds,
            "source": self.source,
            "reviewed": self.reviewed,
            "tags": self.tags,
        }


@dataclass(frozen=True)
class Killed:
    """Mutant, ktory oblal przynajmniej jeden test."""

    mutation: mutations.Mutation
    outcome: runner.Outcome


TRIVIAL_ERRORS = ("UnboundLocalError", "NameError")


def _is_trivial(outcome) -> bool:
    """Mutant, ktory wywala sie na niezdefiniowanej nazwie, nie uczy niczego o wzorcu.

    Taki blad widac po tym, ze zmienna nie istnieje, a nie po zrozumieniu
    dzialania okna - do korpusu nie trafia, tak samo jak mutant przechodzacy testy.
    """
    failing = [outcome.details[i] for i in outcome.failing]
    return bool(failing) and all(
        any(marker in detail for marker in TRIVIAL_ERRORS) for detail in failing
    )


def evaluate(module, timeout: float = 0.5):
    """Zwraca (zrodlo, zabite mutanty, mutanty przechodzace testy, mutanty trywialne)."""
    source = mutations.normalize(inspect.getsource(module.solution))
    baseline = runner.run_tests(source, module.FUNC, module.TESTS, timeout)
    if not baseline.all_pass:
        raise AssertionError(
            "{}: implementacja referencyjna nie przechodzi wlasnych testow: {}".format(
                module.PROBLEM, baseline.statuses
            )
        )

    killed, survived, trivial = [], [], []
    for mutation in mutations.generate(source, getattr(module, "SWAPPABLE_VARS", ())):
        outcome = runner.run_tests(mutation.source, module.FUNC, module.TESTS, timeout)
        if outcome.all_pass:
            survived.append(mutation)
        elif _is_trivial(outcome):
            trivial.append(mutation)
        else:
            killed.append(Killed(mutation, outcome))
    return source, killed, survived, trivial


def test_label(module, test) -> str:
    params = list(inspect.signature(module.solution).parameters)
    return ", ".join("{}={!r}".format(p, v) for p, v in zip(params, test["args"]))


def _shuffled(options: list, answer_value, rng) -> tuple:
    shuffled = list(options)
    rng.shuffle(shuffled)
    return shuffled, shuffled.index(answer_value)


def _rng(key: str) -> random.Random:
    return random.Random(key)


def _slug(operator: str, index: int) -> str:
    return "{}-{:02d}".format(operator.replace("_", "-"), index)


def _spec_ref(module, mutation):
    """Fragment speca, ktory uzasadnia poprawna odpowiedz.

    Klucz to najpierw konkretna linia, a dopiero potem operator. Sam operator nie
    wystarcza: `const_change` na `else 0` uzasadnia zdanie o zwracaniu zera, ale
    ten sam operator na `left = 0` juz nie - a cytat, ktory niczego nie dowodzi,
    jest gorszy niz jego brak, bo walidator go przepuszcza.
    """
    by_line = getattr(module, "LINE_SPEC_REFS", {})
    if mutation is not None and mutation.original_lines:
        found = by_line.get(mutation.original_lines[0].strip())
        if found:
            return found
    operator = mutation.operator if mutation is not None else "drop_stmt"
    return getattr(module, "SPEC_REFS", {}).get(operator)


def _diversify(killed) -> list:
    """Przeplata mutanty wedlug operatora.

    Bez tego limit odcina cale klasy bledow: mutanty leca w kolejnosci operatorow,
    wiec pierwsze 10 to same `cmp_swap` i `const_change`, a `swap_vars` (trudnosc 1)
    nie trafia do korpusu w ogole. Indeks jest zachowany, zeby id cwiczen nie zalezalo
    od kolejnosci wyboru.
    """
    groups = {}
    for idx, item in enumerate(killed):
        groups.setdefault(item.mutation.operator, []).append((idx, item))
    order = sorted(groups, key=lambda key: mutations.DIFFICULTY[key])
    out = []
    round_index = 0
    while any(round_index < len(groups[key]) for key in order):
        for key in order:
            if round_index < len(groups[key]):
                out.append(groups[key][round_index])
        round_index += 1
    return out


def build_which_test(module, killed, limit: int) -> list:
    """`Ktory test wykryje blad?` - opcjami sa przypadki testowe.

    Wymaga mutanta z dokladnie jednym testem do wskazania i co najmniej trzema
    testami, ktore przechodza - inaczej poprawnych odpowiedzi byloby kilka.
    """
    out = []
    for i, item in _diversify(killed):
        if len(out) >= limit:
            break
        failing, passing = item.outcome.failing, item.outcome.passing
        if not failing or len(passing) < 3:
            continue
        answer_idx = failing[0]
        chosen = [answer_idx] + list(passing[:3])
        labels = [test_label(module, module.TESTS[j]) for j in chosen]
        answer_label = labels[0]
        options, answer = _shuffled(labels, answer_label, _rng("wt" + str(i)))

        expected = module.TESTS[answer_idx]["expect"]
        got = item.outcome.details[answer_idx]
        status = item.outcome.statuses[answer_idx]
        if status == runner.TIMEOUT:
            result = "kod się zapętla"
        elif status == runner.ERROR:
            result = "kod wyrzuca {}".format(got)
        else:
            result = "kod zwraca {}".format(got)

        out.append(
            Exercise(
                id="{}/{}/{}".format(module.PATTERN, module.PROBLEM, _slug(item.mutation.operator, i)),
                pattern=module.PATTERN,
                problem=module.PROBLEM,
                type="find-bug",
                difficulty=item.mutation.difficulty,
                spec=module.SPEC,
                prompt="Który test wykryje błąd?",
                code=item.mutation.source,
                options=options,
                answer=answer,
                explanation="Dla {} poprawną odpowiedzią jest {}, a {}. Przyczyna: {}.".format(
                    answer_label, expected, result, item.mutation.description
                ),
                spec_ref=_spec_ref(module, item.mutation),
                est_seconds=EST_SECONDS["find-bug"](item.mutation.difficulty),
                tags=["which-test", item.mutation.operator],
            )
        )
    return out


def build_which_line(module, source, killed, limit: int) -> list:
    """`W ktorej linii jest blad?` - opcjami sa linie kodu."""
    original_lines = source.splitlines()
    out = []
    for i, item in _diversify(killed):
        if len(out) >= limit:
            break
        mutation = item.mutation
        if len(mutation.changed_lines) != 1 or len(mutation.mutated_lines) != 1:
            continue
        mutant_lines = mutation.source.splitlines()
        if len(mutant_lines) != len(original_lines):
            continue  # usunieta linia - to material na fill-gap, nie na wskazanie linii

        answer_line = mutant_lines[mutation.changed_lines[0] - 1].strip()
        pool = [ln.strip() for ln in mutant_lines[1:] if ln.strip() and ln.strip() != answer_line]
        pool = list(dict.fromkeys(pool))
        if len(pool) < 3:
            continue
        rng = _rng("wl" + str(i))
        distractors = rng.sample(pool, 3)
        options, answer = _shuffled([answer_line] + distractors, answer_line, rng)

        failing = item.outcome.failing[0]
        out.append(
            Exercise(
                id="{}/{}/line-{}".format(module.PATTERN, module.PROBLEM, _slug(mutation.operator, i)),
                pattern=module.PATTERN,
                problem=module.PROBLEM,
                type="find-bug",
                difficulty=mutation.difficulty,
                spec=module.SPEC,
                prompt="W której linii jest błąd?",
                code=mutation.source,
                options=options,
                answer=answer,
                explanation="Powinno być `{}`. {}, przez co dla {} kod zwraca {} zamiast {}.".format(
                    mutation.original_lines[0].strip(),
                    mutation.description[0].upper() + mutation.description[1:],
                    test_label(module, module.TESTS[failing]),
                    item.outcome.details[failing],
                    module.TESTS[failing]["expect"],
                ),
                spec_ref=_spec_ref(module, mutation),
                est_seconds=EST_SECONDS["find-bug"](mutation.difficulty),
                tags=["which-line", mutation.operator],
            )
        )
    return out


def build_fill_gap(module, source, killed, limit: int) -> list:
    """`Czego brakuje w tej linii?` - luka po usunietej instrukcji.

    Luka jest zasadna tylko wtedy, gdy istnieje mutant `drop_stmt`, ktory oblal
    testy: to dowod, ze bez tej linii kod nie dziala. Dystraktory sa brane
    z innych zabitych mutantow tej samej linii, wiec kazdy z nich tez jest bledny.
    """
    original_lines = source.splitlines()
    by_line = {}
    for item in killed:
        m = item.mutation
        if len(m.changed_lines) == 1 and len(m.mutated_lines) == 1:
            if len(m.source.splitlines()) == len(original_lines):
                by_line.setdefault(m.changed_lines[0], []).append(item)

    out = []
    for item in killed:
        if len(out) >= limit:
            break
        m = item.mutation
        if m.operator != "drop_stmt" or not m.original_lines:
            continue
        line_no = m.changed_lines[0]
        if line_no > len(original_lines):
            continue
        correct = original_lines[line_no - 1]
        variants = [
            k.mutation.mutated_lines[0].strip()
            for k in by_line.get(line_no, [])
            if k.mutation.mutated_lines[0].strip() != correct.strip()
        ]
        variants = list(dict.fromkeys(variants))
        if len(variants) < 3:
            continue

        rng = _rng("fg" + str(line_no))
        indent = " " * (len(correct) - len(correct.lstrip()))
        gapped = list(original_lines)
        gapped[line_no - 1] = indent + "____"
        options, answer = _shuffled(
            [correct.strip()] + rng.sample(variants, 3), correct.strip(), rng
        )

        failing = item.outcome.failing[0]
        status = item.outcome.statuses[failing]
        effect = (
            "kod się zapętla"
            if status == runner.TIMEOUT
            else "kod zwraca {} zamiast {}".format(
                item.outcome.details[failing], module.TESTS[failing]["expect"]
            )
        )
        out.append(
            Exercise(
                id="{}/{}/gap-{:02d}".format(module.PATTERN, module.PROBLEM, line_no),
                pattern=module.PATTERN,
                problem=module.PROBLEM,
                type="fill-gap",
                difficulty=m.difficulty,
                spec=module.SPEC,
                prompt="Która linia powinna być w miejscu ____?",
                code="\n".join(gapped),
                options=options,
                answer=answer,
                explanation="Bez `{}` dla {} {}.".format(
                    correct.strip(), test_label(module, module.TESTS[failing]), effect
                ),
                spec_ref=_spec_ref(module, m),
                est_seconds=EST_SECONDS["fill-gap"](m.difficulty),
                tags=["fill-gap"],
            )
        )
    return out


def build_complexity(module, source) -> list:
    """Zlozonosc - odpowiedz pochodzi z metadanych wzorca, nie z mutacji."""
    meta = getattr(module, "COMPLEXITY", None)
    if not meta:
        return []
    out = []
    for kind, label in (("time", "czasowa"), ("space", "pamięciowa")):
        answer_value = meta.get(kind)
        distractors = meta.get(kind + "_distractors", [])
        if not answer_value or len(distractors) < 3:
            continue
        rng = _rng("cx" + kind + module.PROBLEM)
        options, answer = _shuffled([answer_value] + list(distractors[:3]), answer_value, rng)
        out.append(
            Exercise(
                id="{}/{}/complexity-{}".format(module.PATTERN, module.PROBLEM, kind),
                pattern=module.PATTERN,
                problem=module.PROBLEM,
                type="complexity",
                difficulty=2,
                spec=module.SPEC,
                prompt="Jaka jest złożoność {} tej implementacji?".format(label),
                code=source,
                options=options,
                answer=answer,
                explanation=meta.get(kind + "_explanation", ""),
                spec_ref=None,
                est_seconds=EST_SECONDS["complexity"](2),
                tags=["complexity", kind],
            )
        )
    return out


def build_order_steps(module, source) -> list:
    """Ulozenie krokow rozwiazania. Bloki sa opisane recznie w module wzorca."""
    blocks = getattr(module, "BLOCKS", None)
    if not blocks or len(blocks) < 3:
        return []
    rng = _rng("os" + module.PROBLEM)
    shuffled = list(blocks)
    while shuffled == list(blocks):
        rng.shuffle(shuffled)
    answer = [shuffled.index(b) for b in blocks]
    return [
        Exercise(
            id="{}/{}/order-steps".format(module.PATTERN, module.PROBLEM),
            pattern=module.PATTERN,
            problem=module.PROBLEM,
            type="order-steps",
            ui="ordering",
            difficulty=2,
            spec=module.SPEC,
            prompt="Ułóż kroki rozwiązania w kolejności.",
            code="",
            options=shuffled,
            answer=answer,
            explanation="Kolejność: " + " -> ".join(blocks),
            spec_ref=None,
            est_seconds=EST_SECONDS["order-steps"](2),
            source="handwritten",
            tags=["order-steps"],
        )
    ]


def _distance(value: str, reference: str):
    """Jak blisko siebie leza dwie odpowiedzi. Sluzy do wybrania kuszacych dystraktorow."""
    try:
        return abs(float(value) - float(reference))
    except (TypeError, ValueError):
        return float("inf")


def build_predict_output(module, source, killed, limit: int) -> list:
    """`Co zwroci ten kod?` - na ekranie stoi POPRAWNA implementacja.

    Dystraktory nie sa wymyslone: to sa wyniki, jakie zabite mutanty zwrocily na
    tym samym wejsciu. Kazdy jest wiec z definicji bledny i z definicji wiarygodny,
    bo powstal z realistycznej pomylki, a nie z fantazji autora.

    Odpowiedz nie potrzebuje `spec_ref`: uzasadnia ja uruchomienie kodu, a wartosc
    `expect` jest niezaleznie potwierdzona implementacja brute-force w testach
    pipeline'u. To mocniejszy dowod niz cytat ze specyfikacji.
    """
    out = []
    for i, test in enumerate(module.TESTS):
        if len(out) >= limit:
            break

        correct = repr(test["expect"])
        wrong_by_value = {}
        for item in killed:
            if item.outcome.statuses[i] != runner.FAIL:
                continue
            detail = item.outcome.details[i]
            if detail != correct:
                wrong_by_value.setdefault(detail, item.mutation.description)
        if len(wrong_by_value) < 3:
            continue

        # Najbardziej kuszace sa wyniki lezace blisko poprawnego; wynik odlegly
        # o rzad wielkosci odpada na pierwszy rzut oka i niczego nie sprawdza.
        ranked = sorted(wrong_by_value, key=lambda v: (_distance(v, correct), v))
        distractors = ranked[:3]
        closest = distractors[0]

        rng = _rng("po{}{}".format(module.PROBLEM, i))
        options, answer = _shuffled([correct] + distractors, correct, rng)

        difficulty = 3 if _distance(closest, correct) <= 1 else 2
        out.append(
            Exercise(
                id="{}/{}/predict-{:02d}".format(module.PATTERN, module.PROBLEM, i),
                pattern=module.PATTERN,
                problem=module.PROBLEM,
                type="predict-output",
                difficulty=difficulty,
                spec=module.SPEC,
                prompt="Co zwróci ten kod dla {}?".format(test_label(module, test)),
                code=source,
                options=options,
                answer=answer,
                explanation=(
                    "Kod jest poprawny, więc zwraca {}. Odpowiedź {} dostałbyś przy jednym "
                    "błędzie: {}.".format(correct, closest, wrong_by_value[closest])
                ),
                spec_ref=None,
                est_seconds=EST_SECONDS["predict-output"](difficulty),
                tags=["predict-output"],
            )
        )
    return out


LIMITS = {"which-test": 8, "which-line": 10, "fill-gap": 6, "predict-output": 5}


def build(module, limits=None) -> tuple:
    limits = limits or LIMITS
    source, killed, survived, trivial = evaluate(module)
    items = []
    items += build_which_test(module, killed, limits["which-test"])
    items += build_which_line(module, source, killed, limits["which-line"])
    items += build_fill_gap(module, source, killed, limits["fill-gap"])
    items += build_predict_output(module, source, killed, limits.get("predict-output", 5))
    items += build_complexity(module, source)
    items += build_order_steps(module, source)
    return items, killed, survived, trivial


# --------------------------------------------------------------------------
# Treści kurowane
# --------------------------------------------------------------------------

def forced_order(deps: list):
    """Kolejnosc wymuszona przez zaleznosci albo None, gdy nie jest jedyna.

    Zwraca (kolejnosc, gotowe_naraz). Sortowanie topologiczne daje dokladnie
    jedna poprawna kolejnosc wtedy i tylko wtedy, gdy na kazdym etapie gotowy
    do wziecia jest dokladnie jeden krok. Dwa gotowe naraz znacza, ze da sie je
    zamienic miejscami i obie odpowiedzi sa poprawne.
    """
    n = len(deps)
    indegree = [len(d) for d in deps]
    following = [[] for _ in range(n)]
    for index, sources in enumerate(deps):
        for source in sources:
            following[source].append(index)

    ready = [i for i in range(n) if indegree[i] == 0]
    order = []
    while ready:
        if len(ready) > 1:
            return None, sorted(ready)
        current = ready.pop()
        order.append(current)
        for nxt in following[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    if len(order) != n:
        return None, []
    return order, []


def check_forced_order(eid: str, steps: list, deps: list) -> None:
    """Pilnuje, ze zadeklarowana kolejnosc krokow jest jedyna mozliwa.

    To jest dla `order-steps` tym, czym filtr testowy dla mutantow: cwiczenie,
    w ktorym dwa kroki da sie zamienic miejscami, ma dwie poprawne odpowiedzi,
    czyli w praktyce nie ma zadnej.
    """
    if len(deps) != len(steps):
        raise AssertionError("{}: `deps` ma inna dlugosc niz `steps`".format(eid))
    for index, sources in enumerate(deps):
        for source in sources:
            if not 0 <= source < index:
                raise AssertionError(
                    "{}: krok {} zalezy od {}, a zaleznosc musi wskazywac krok wczesniejszy".format(
                        eid, index, source
                    )
                )

    order, tied = forced_order(deps)
    if order is None:
        raise AssertionError(
            "{}: kolejnosc nie jest jednoznaczna, bo kroki {} sa gotowe naraz: {}".format(
                eid,
                " i ".join(str(t) for t in tied),
                " ORAZ ".join(repr(steps[t]) for t in tied),
            )
        )
    if order != list(range(len(steps))):
        raise AssertionError(
            "{}: zaleznosci wymuszaja kolejnosc {}, a kroki podano w innej".format(eid, order)
        )


CURATED_DEFAULTS = {
    "recognize-pattern": {
        "prompt": "Który wzorzec rozwiązuje to zadanie?",
        "est_seconds": 20,
    },
    "key-insight": {
        "prompt": "Na jakiej obserwacji opiera się rozwiązanie?",
        "est_seconds": 25,
    },
    "edge-case": {
        "prompt": "Który przypadek łamie to podejście?",
        "est_seconds": 30,
    },
    "order-steps": {
        "prompt": "Ułóż kroki rozwiązania w kolejności.",
        "est_seconds": 60,
        "ui": "ordering",
    },
}


def build_curated(module) -> list:
    """Ćwiczenia pisane ręcznie, przede wszystkim `recognize-pattern`.

    Nie ma tu kodu do zmutowania, więc odpada jedyny automatyczny dowód
    poprawności, jaki ma reszta korpusu. Dlatego wszystkie wychodzą stąd z
    `reviewed=False` i build o nich przypomina, dopóki człowiek ich nie przejrzy.

    `answer` w danych jest tekstem opcji, nie indeksem: po przetasowaniu indeks
    liczy się sam, więc nie da się rozjechać odpowiedzi z opcjami.
    """
    corpus = module.CORPUS
    fallback_type = getattr(module, "DEFAULT_TYPE", "recognize-pattern")
    module_prompt = getattr(module, "DEFAULT_PROMPT", None)
    out = []

    for entry in module.EXERCISES:
        kind = entry.get("type", fallback_type)
        defaults = CURATED_DEFAULTS.get(kind)
        if defaults is None:
            raise AssertionError("{}: nieznany typ `{}`".format(entry["problem"], kind))

        eid = "{}/{}/{}".format(corpus["id"], entry["pattern"], entry["problem"])
        ui = defaults.get("ui", "choice")

        if ui == "ordering":
            # `steps` sa podane w kolejnosci poprawnej. Tasujemy je na opcje, a
            # odpowiedzia jest permutacja mowiaca, gdzie w potasowanej liscie
            # znalazl sie kolejny wlasciwy krok.
            steps = list(entry["steps"])
            if len(steps) != len(set(steps)):
                raise AssertionError("{}: powtorzony krok".format(eid))
            check_forced_order(eid, steps, entry["deps"])
            rng = _rng("cur" + eid)
            shuffled = list(steps)
            while shuffled == steps:
                rng.shuffle(shuffled)
            answer: object = [shuffled.index(step) for step in steps]
        else:
            options = list(entry["options"])
            answer_text = entry["answer"]
            if answer_text not in options:
                raise AssertionError(
                    "{}/{}: `answer` nie występuje wśród opcji".format(
                        entry["pattern"], entry["problem"]
                    )
                )
            shuffled, answer = _shuffled(options, answer_text, _rng("cur" + eid))

        out.append(
            Exercise(
                id=eid,
                pattern=entry["pattern"],
                problem=entry["problem"],
                type=kind,
                difficulty=entry["difficulty"],
                spec=entry["spec"],
                prompt=entry.get("prompt") or module_prompt or defaults["prompt"],
                code=entry.get("code", ""),
                options=shuffled,
                answer=answer,
                explanation=entry["explanation"],
                spec_ref=entry.get("spec_ref"),
                est_seconds=entry.get("est_seconds", defaults["est_seconds"]),
                ui=ui,
                source="curated",
                reviewed=False,
                tags=[kind, entry["pattern"]],
            )
        )
    return out
