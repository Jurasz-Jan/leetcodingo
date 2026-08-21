"""Najdłuższy spójny podciąg o co najwyżej k różnych znakach."""

PATTERN = "sliding-window"
PROBLEM = "longest-k-distinct"
FUNC = "solution"

SPEC = (
    "Zwraca długość najdłuższego spójnego podciągu zawierającego "
    "co najwyżej k różnych znaków. Dla k = 0 zwraca 0."
)

SPEC_REFS = {
    "cmp_swap": "co najwyżej k różnych znaków",
    "off_by_one": "długość najdłuższego spójnego podciągu",
    "const_change": "Dla k = 0 zwraca 0",
    "op_swap": "najdłuższego",
    "drop_stmt": "spójnego podciągu",
    "swap_vars": "spójnego podciągu",
}

LINE_SPEC_REFS = {
    "counts = {}": "co najwyżej k różnych znaków",
    "left = 0": "spójnego podciągu",
    "best = 0": "Dla k = 0 zwraca 0",
    "for right in range(len(s)):": "spójnego podciągu",
    "counts[s[right]] = counts.get(s[right], 0) + 1": "co najwyżej k różnych znaków",
    "while len(counts) > k:": "co najwyżej k różnych znaków",
    "counts[s[left]] -= 1": "co najwyżej k różnych znaków",
    "if counts[s[left]] == 0:": "co najwyżej k różnych znaków",
    "del counts[s[left]]": "co najwyżej k różnych znaków",
    "left += 1": "spójnego podciągu",
    "best = max(best, right - left + 1)": "najdłuższego",
    "return best": "Dla k = 0 zwraca 0",
}

COMPLEXITY = {
    "time": "O(n)",
    "time_distractors": ["O(n * k)", "O(n log n)", "O(n^2)"],
    "space": "O(k)",
    "space_distractors": ["O(1)", "O(n)", "O(n * k)"],
    "time_explanation": (
        "Każdy znak wchodzi do okna raz i wychodzi raz, a operacje na słowniku "
        "są stałe, więc liczba znaków w oknie nie wchodzi do złożoności czasowej."
    ),
    "space_explanation": (
        "Słownik trzyma liczniki tylko dla znaków obecnych w oknie, "
        "a tych z definicji nigdy nie jest więcej niż k + 1."
    ),
}

TESTS = [
    {"args": ["eceba", 2], "expect": 3},
    {"args": ["aa", 1], "expect": 2},
    {"args": ["", 2], "expect": 0},
    {"args": ["abc", 0], "expect": 0},
    {"args": ["aabbcc", 1], "expect": 2},
    {"args": ["aabbcc", 2], "expect": 4},
    {"args": ["abaccc", 2], "expect": 4},
    {"args": ["abcdef", 3], "expect": 3},
    {"args": ["aaabbb", 2], "expect": 6},
]

BLOCKS = [
    "pusty słownik liczników i wyzerowany wynik",
    "dopisanie znaku spod prawego brzegu do liczników",
    "zwężanie okna dopóki różnych znaków jest za dużo",
    "aktualizacja najlepszej długości",
]

SWAPPABLE_VARS = [("left", "right")]


def solution(s, k):
    counts = {}
    left = 0
    best = 0
    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
