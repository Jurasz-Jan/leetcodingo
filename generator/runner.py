"""Uruchamianie zestawu testow na mutancie.

Mutacja potrafi zapetlic kod (usuniete `left += 1` w petli while), wiec kazdy
przebieg idzie do podprocesu z twardym timeoutem. Podproces raportuje wyniki
strumieniowo, wiec po timeoucie wiemy dokladnie ktory test wisial.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_CHILD = Path(__file__).with_name("_child.py")

PASS = "pass"
FAIL = "fail"
ERROR = "error"
TIMEOUT = "timeout"


@dataclass(frozen=True)
class Outcome:
    """Wynik jednego przebiegu: status per test, w kolejnosci zestawu testow."""

    statuses: tuple
    details: tuple

    @property
    def failing(self) -> tuple:
        return tuple(i for i, s in enumerate(self.statuses) if s != PASS)

    @property
    def passing(self) -> tuple:
        return tuple(i for i, s in enumerate(self.statuses) if s == PASS)

    @property
    def all_pass(self) -> bool:
        return all(s == PASS for s in self.statuses)


def _parse_lines(raw: str) -> dict:
    out = {}
    for line in (raw or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        out[record["i"]] = (record["status"], record.get("detail", ""))
    return out


def run_tests(source: str, func: str, tests: list, timeout: float = 0.5) -> Outcome:
    """Statusy dla calego zestawu.

    Po zawieszeniu dobija pozostale testy kolejnym przebiegiem, zeby zapetlenie
    na tescie nr 3 nie oznaczylo testow 4-8 jako niezdanych. Kazda iteracja
    przesuwa sie za ostatni zawieszony test, wiec petla zawsze sie konczy.
    """
    statuses, details = _run_batch(source, func, tests, timeout)
    cursor = 0
    while True:
        hang = next((i for i in range(cursor, len(tests)) if statuses[i] == TIMEOUT), None)
        if hang is None or hang + 1 >= len(tests):
            break
        cursor = hang + 1
        rest_statuses, rest_details = _run_batch(source, func, tests[cursor:], timeout)
        statuses[cursor:] = rest_statuses
        details[cursor:] = rest_details
    return Outcome(statuses=tuple(statuses), details=tuple(details))


def _run_batch(source: str, func: str, tests: list, timeout: float):
    payload = json.dumps({"source": source, "func": func, "tests": tests})
    try:
        proc = subprocess.run(
            [sys.executable, str(_CHILD)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        raw = proc.stdout
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        timed_out = True

    seen = _parse_lines(raw)
    statuses = []
    details = []
    for i in range(len(tests)):
        if i in seen:
            status, detail = seen[i]
        elif timed_out:
            status, detail = TIMEOUT, "przekroczony limit czasu"
        else:
            status, detail = ERROR, "brak wyniku z podprocesu"
        statuses.append(status)
        details.append(detail)
    return statuses, details
