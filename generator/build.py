"""CLI: patterns/ -> corpus/*.json

    python generator/build.py            # buduje wszystkie wzorce
    python generator/build.py sliding-window
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import exercises  # noqa: E402

PATTERNS_DIR = ROOT / "patterns"
CURATED_DIR = ROOT / "curated"
CORPUS_DIR = ROOT.parent / "corpus"

REQUIRE_SPEC_REF = {"find-bug", "fill-gap", "recognize-pattern", "key-insight"}


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(items: list) -> list:
    """Walidator jakosci korpusu. Zwraca liste problemow."""
    problems = []
    seen = set()
    for item in items:
        eid = item["id"]
        if eid in seen:
            problems.append("duplikat id: {}".format(eid))
        seen.add(eid)

        if item["type"] in REQUIRE_SPEC_REF and not item.get("spec_ref"):
            problems.append("{}: brak spec_ref (odpowiedzi nie da się uzasadnić specem)".format(eid))
        if item.get("spec_ref") and item["spec_ref"] not in item["spec"]:
            problems.append("{}: spec_ref nie występuje dosłownie w spec".format(eid))
        if not item.get("spec"):
            problems.append("{}: brak spec".format(eid))
        if not item.get("explanation"):
            problems.append("{}: brak wyjaśnienia".format(eid))

        options = item["options"]
        if len(options) != len(set(map(str, options))):
            problems.append("{}: powtórzone opcje".format(eid))
        if item["ui"] == "choice":
            if len(options) < 2:
                problems.append("{}: mniej niż dwie opcje".format(eid))
            if not isinstance(item["answer"], int) or not 0 <= item["answer"] < len(options):
                problems.append("{}: answer poza zakresem opcji".format(eid))
        elif item["ui"] == "ordering":
            if sorted(item["answer"]) != list(range(len(options))):
                problems.append("{}: answer nie jest permutacją opcji".format(eid))
    return problems


def build_pattern(pattern_dir: Path) -> dict:
    meta_path = pattern_dir / "_pattern.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"id": pattern_dir.name}

    items, stats = [], []
    for problem_path in sorted(pattern_dir.glob("*.py")):
        if problem_path.name.startswith("_"):
            continue
        module = _load_module(problem_path)
        built, killed, survived, trivial = exercises.build(module)
        items += [e.to_dict() for e in built]
        stats.append((module.PROBLEM, len(killed), len(survived) + len(trivial), len(built)))

    return {"meta": meta, "items": items, "stats": stats}


def build_curated_group(paths: list) -> dict:
    """Moduły dzielące identyfikator korpusu trafiają do jednego pliku.

    Dzięki temu treść można dzielić na pliki tematycznie, a mimo to renderer
    dostaje jeden spójny korpus. Powtórzone `id` wyłapie walidator.
    """
    meta, items = None, []
    for path in paths:
        module = _load_module(path)
        meta = meta or module.CORPUS
        items += [e.to_dict() for e in exercises.build_curated(module)]
    return {"meta": meta, "items": items, "stats": []}


def main(argv: list) -> int:
    wanted = argv[1:]
    CORPUS_DIR.mkdir(exist_ok=True)
    total_problems = 0
    exit_code = 0

    sources = [("pattern", [d]) for d in sorted(x for x in PATTERNS_DIR.iterdir() if x.is_dir())]
    if CURATED_DIR.exists():
        groups = {}
        for f in sorted(CURATED_DIR.glob("*.py")):
            if f.name.startswith("_"):
                continue
            groups.setdefault(_load_module(f).CORPUS["id"], []).append(f)
        sources += [("curated", paths) for paths in groups.values()]

    unreviewed = 0
    for kind, paths in sources:
        result = build_curated_group(paths) if kind == "curated" else build_pattern(paths[0])
        if wanted and result["meta"]["id"] not in wanted:
            continue
        items = result["items"]
        problems = validate(items)

        out_path = CORPUS_DIR / "{}.json".format(result["meta"]["id"])
        payload = {"pattern": result["meta"], "exercises": items}
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        print("== {}".format(result["meta"]["id"]))
        for problem, killed, survived, built in result["stats"]:
            print(
                "   {:<20} mutanty: {} zabite / {} odrzucone -> {} ćwiczeń".format(
                    problem, killed, survived, built
                )
            )
        by_type = Counter("{} / {}".format(i["type"], i["tags"][0] if i["tags"] else "-") for i in items)
        for key, count in sorted(by_type.items()):
            print("   {:<28} {}".format(key, count))
        print("   RAZEM: {} ćwiczeń -> {}".format(len(items), out_path.relative_to(CORPUS_DIR.parent)))

        pending = [i for i in items if not i.get("reviewed", True)]
        if pending:
            unreviewed += len(pending)
            print("   DO PRZEJRZENIA: {} ćwiczeń bez weryfikacji człowieka".format(len(pending)))

        if problems:
            exit_code = 1
            print("   PROBLEMY WALIDACJI:")
            for problem in problems:
                print("     - {}".format(problem))
                total_problems += 1

    if unreviewed:
        print(
            "\nuwaga: {} ćwiczeń kurowanych czeka na przegląd (pole `reviewed`), "
            "bo żaden test ich nie sprawdza".format(unreviewed)
        )
    if total_problems:
        print("\nkorpus niepoprawny: {} problemów".format(total_problems))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
