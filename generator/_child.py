"""Uruchamia testy na (potencjalnie zepsutym) kodzie. Odpalany w podprocesie.

Wejscie: JSON na stdin. Wyjscie: jedna linia JSON na test, flushowana od razu -
dzieki temu rodzic po timeoucie wie, na ktorym tescie kod sie zapetlil.
"""

import json
import sys


def main():
    payload = json.load(sys.stdin)
    namespace = {}
    try:
        exec(compile(payload["source"], "<mutant>", "exec"), namespace)
        func = namespace[payload["func"]]
    except Exception as exc:  # noqa: BLE001 - mutant moze byc dowolnie zepsuty
        for i in range(len(payload["tests"])):
            print(json.dumps({"i": i, "status": "error", "detail": repr(exc)}), flush=True)
        return

    for i, test in enumerate(payload["tests"]):
        try:
            got = func(*test["args"])
            status = "pass" if got == test["expect"] else "fail"
            detail = repr(got)
        except Exception as exc:  # noqa: BLE001
            status = "error"
            detail = repr(exc)
        print(json.dumps({"i": i, "status": status, "detail": detail}), flush=True)


if __name__ == "__main__":
    main()
