"""Operatory mutacji na AST.

Kazdy operator produkuje jednego mutanta na kazde pasujace miejsce w kodzie.
Trudnosc jest cecha operatora, nie doboru zadania: `>` -> `>=` jest subtelne,
zamiana `left`/`right` widoczna na pierwszy rzut oka.
"""

from __future__ import annotations

import ast
import copy
from dataclasses import dataclass

DIFFICULTY = {
    "swap_vars": 1,
    "op_swap": 2,
    "const_change": 2,
    "drop_stmt": 2,
    "cmp_swap": 3,
    "off_by_one": 3,
}

_CMP_SWAP = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
}

_CMP_LABEL = {
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Eq: "==",
    ast.NotEq: "!=",
}

_BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add}
_BIN_LABEL = {ast.Add: "+", ast.Sub: "-"}
_FUNC_SWAP = {"min": "max", "max": "min"}


@dataclass(frozen=True)
class Mutation:
    """Jeden mutant: pelne zrodlo funkcji plus opis czym rozni sie od oryginalu."""

    operator: str
    difficulty: int
    description: str
    source: str
    changed_lines: tuple
    original_lines: tuple
    mutated_lines: tuple


def normalize(source: str) -> str:
    """Kanoniczne formatowanie - mutanty i oryginal musza byc porownywalne linia w linie."""
    return ast.unparse(ast.parse(source))


def _nodes(tree):
    return list(ast.walk(tree))


def _mutate_nth(tree, index, transform):
    """Kopiuje drzewo i stosuje transform do i-tego wezla w kolejnosci ast.walk."""
    clone = copy.deepcopy(tree)
    transform(_nodes(clone)[index])
    return clone


def _replace_node(tree, old, new):
    for parent in ast.walk(tree):
        for field_name, value in ast.iter_fields(parent):
            if value is old:
                setattr(parent, field_name, new)
                return True
            if isinstance(value, list):
                for idx, item in enumerate(value):
                    if item is old:
                        value[idx] = new
                        return True
    return False


def _diff(original: str, mutated: str):
    a = original.splitlines()
    b = mutated.splitlines()
    if len(a) != len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return (i + 1,), (a[i],), (b[i],)
        return (len(b) + 1,), (a[len(b)],), ()
    lines = tuple(i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y)
    return lines, tuple(a[i - 1] for i in lines), tuple(b[i - 1] for i in lines)


def _make(operator, description, original, mutant_tree):
    mutated = ast.unparse(mutant_tree)
    if mutated == original:
        return None
    lines, orig_lines, mut_lines = _diff(original, mutated)
    return Mutation(
        operator=operator,
        difficulty=DIFFICULTY[operator],
        description=description,
        source=mutated,
        changed_lines=lines,
        original_lines=orig_lines,
        mutated_lines=mut_lines,
    )


def _cmp_swap(tree, original):
    for i, node in enumerate(_nodes(tree)):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1:
            continue
        op = type(node.ops[0])
        if op not in _CMP_SWAP:
            continue
        new = _CMP_SWAP[op]
        desc = "operator porównania {} zamieniony na {}".format(_CMP_LABEL[op], _CMP_LABEL[new])
        clone = _mutate_nth(tree, i, lambda n, new=new: n.ops.__setitem__(0, new()))
        yield _make("cmp_swap", desc, original, clone)


def _off_by_one(tree, original):
    for i, node in enumerate(_nodes(tree)):
        if not isinstance(node, ast.BinOp):
            continue
        if not isinstance(node.op, (ast.Add, ast.Sub)):
            continue
        if not (isinstance(node.right, ast.Constant) and node.right.value == 1):
            continue
        desc = "usunięte {} 1 w wyrażeniu `{}`".format(_BIN_LABEL[type(node.op)], ast.unparse(node))
        clone = copy.deepcopy(tree)
        target = _nodes(clone)[i]
        _replace_node(clone, target, target.left)
        yield _make("off_by_one", desc, original, clone)


def _const_change(tree, original):
    for i, node in enumerate(_nodes(tree)):
        if not isinstance(node, ast.Constant) or isinstance(node.value, bool):
            continue
        if not isinstance(node.value, int):
            continue
        for delta in (1, -1):
            new_value = node.value + delta
            desc = "stała {} zmieniona na {}".format(node.value, new_value)
            clone = _mutate_nth(tree, i, lambda n, v=new_value: setattr(n, "value", v))
            yield _make("const_change", desc, original, clone)


def _op_swap(tree, original):
    for i, node in enumerate(_nodes(tree)):
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_SWAP:
            old_op = type(node.op)
            new_op = _BIN_SWAP[old_op]
            desc = "operator {} zamieniony na {}".format(_BIN_LABEL[old_op], _BIN_LABEL[new_op])
            clone = _mutate_nth(tree, i, lambda n, new=new_op: setattr(n, "op", new()))
            yield _make("op_swap", desc, original, clone)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in _FUNC_SWAP:
                continue
            new_name = _FUNC_SWAP[node.func.id]
            desc = "{}() zamienione na {}()".format(node.func.id, new_name)
            clone = _mutate_nth(tree, i, lambda n, v=new_name: setattr(n.func, "id", v))
            yield _make("op_swap", desc, original, clone)


def _drop_stmt(tree, original):
    for i, node in enumerate(_nodes(tree)):
        for field_name in ("body", "orelse", "finalbody"):
            body = getattr(node, field_name, None)
            if not isinstance(body, list) or len(body) < 2:
                continue
            for j, stmt in enumerate(body):
                if isinstance(stmt, (ast.Return, ast.FunctionDef)):
                    continue
                head = ast.unparse(stmt).splitlines()[0]
                desc = "usunięta instrukcja `{}`".format(head)
                clone = copy.deepcopy(tree)
                getattr(_nodes(clone)[i], field_name).pop(j)
                yield _make("drop_stmt", desc, original, clone)


def _swap_vars(tree, original, pairs):
    """Zamiana zmiennych w obrebie JEDNEJ instrukcji.

    Zamiana wszystkich wystapien to zwykle przemianowanie - program rownowazny,
    zaden test tego nie wykryje. Bledem jest dopiero uzycie `right` tam, gdzie
    mialo byc `left`, w jednym miejscu.
    """
    for a, b in pairs:
        for i, node in enumerate(_nodes(tree)):
            if not isinstance(node, ast.stmt) or isinstance(node, (ast.FunctionDef, ast.For, ast.While)):
                continue
            names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            if not names & {a, b}:
                continue
            head = ast.unparse(node).splitlines()[0]
            desc = "w instrukcji `{}` zamienione `{}` i `{}`".format(head, a, b)
            clone = copy.deepcopy(tree)
            for inner in ast.walk(_nodes(clone)[i]):
                if isinstance(inner, ast.Name) and inner.id in (a, b):
                    inner.id = b if inner.id == a else a
            yield _make("swap_vars", desc, original, clone)


def generate(source: str, swappable_vars=()) -> list:
    """Wszystkie mutanty dla danego zrodla, zdeduplikowane po wynikowym kodzie."""
    original = normalize(source)
    tree = ast.parse(original)

    streams = [
        _cmp_swap(tree, original),
        _off_by_one(tree, original),
        _const_change(tree, original),
        _op_swap(tree, original),
        _drop_stmt(tree, original),
        _swap_vars(tree, original, swappable_vars),
    ]

    seen = {original}
    out = []
    for stream in streams:
        for mutation in stream:
            if mutation is None or mutation.source in seen:
                continue
            seen.add(mutation.source)
            out.append(mutation)
    return out
