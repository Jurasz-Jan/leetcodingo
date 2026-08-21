"""Najkrótszy spójny podciąg o sumie >= target."""

PATTERN = "sliding-window"
PROBLEM = "min-subarray"
FUNC = "solution"

SPEC = (
    "Zwraca długość najkrótszego spójnego podciągu o sumie >= target, "
    "albo 0 gdy taki nie istnieje. Tablica zawiera tylko liczby dodatnie."
)

SPEC_REFS = {
    "cmp_swap": "sumie >= target",
    "off_by_one": "długość najkrótszego spójnego podciągu",
    "const_change": "albo 0 gdy taki nie istnieje",
    "op_swap": "najkrótszego",
    "drop_stmt": "spójnego podciągu",
    "swap_vars": "spójnego podciągu",
}

LINE_SPEC_REFS = {
    "left = 0": "spójnego podciągu",
    "total = 0": "sumie >= target",
    "best = float('inf')": "albo 0 gdy taki nie istnieje",
    "for right in range(len(nums)):": "spójnego podciągu",
    "total += nums[right]": "sumie >= target",
    "while total >= target:": "sumie >= target",
    "best = min(best, right - left + 1)": "najkrótszego",
    "total -= nums[left]": "sumie >= target",
    "left += 1": "spójnego podciągu",
    "return best if best != float('inf') else 0": "albo 0 gdy taki nie istnieje",
}

COMPLEXITY = {
    "time": "O(n)",
    "time_distractors": ["O(n log n)", "O(n^2)", "O(1)"],
    "space": "O(1)",
    "space_distractors": ["O(n)", "O(log n)", "O(k)"],
    "space_explanation": (
        "Trzymamy tylko cztery liczniki niezależnie od długości tablicy; "
        "okno jest opisane dwoma indeksami, nie kopiowane."
    ),
    "time_explanation": (
        "Każdy indeks wchodzi do okna raz (right) i wychodzi raz (left), "
        "więc łącznie 2n operacji mimo zagnieżdżonej pętli while."
    ),
}

TESTS = [
    {"args": [[2, 3, 1, 2, 4, 3], 7], "expect": 2},
    {"args": [[1, 4, 4], 4], "expect": 1},
    {"args": [[1, 1, 1, 1, 1, 1, 1, 1], 11], "expect": 0},
    {"args": [[7], 7], "expect": 1},
    {"args": [[1, 2, 3, 4, 5], 11], "expect": 3},
    {"args": [[5, 1, 3], 9], "expect": 3},
    {"args": [[2, 2, 2, 2], 8], "expect": 4},
    {"args": [[10, 2, 3], 6], "expect": 1},
    # Łapie zawyżony licznik sumy: gdy total startuje z 1, warunek przepuszcza
    # podciągi o sumie target - 1, więc [2] wygląda tu na wystarczające.
    {"args": [[1, 2], 3], "expect": 2},
]

BLOCKS = [
    "inicjalizacja okna i wyniku",
    "rozszerzenie okna w prawo",
    "zwężanie okna dopóki warunek spełniony",
    "zwrócenie wyniku lub 0",
]

SWAPPABLE_VARS = [("left", "right"), ("total", "best")]


def solution(nums, target):
    left = 0
    total = 0
    best = float("inf")
    for right in range(len(nums)):
        total += nums[right]
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best != float("inf") else 0
