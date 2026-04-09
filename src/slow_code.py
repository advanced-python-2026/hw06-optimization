"""
Намеренно медленные реализации для профилирования и оптимизации.
Каждая функция корректна, но неэффективна.
Ваш вариант определяет, какую функцию нужно оптимизировать.
"""

import math
import random

# === Вариант 0: Алгоритм на графах ===


def slow_shortest_paths(n: int = 200) -> list[list[float]]:
    """
    Наивная реализация Floyd-Warshall O(n^3) с дополнительными
    неэффективностями: создание промежуточных списков, лишние проверки.
    """
    INF = float("inf")
    # Generate random weighted graph as adjacency matrix
    random.seed(42)
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for _ in range(n * 3):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        w = random.uniform(1.0, 100.0)
        if w < dist[u][v]:
            dist[u][v] = w

    # Deliberately slow: extra list copies and redundant operations
    for k in range(n):
        new_dist = [row[:] for row in dist]  # unnecessary full copy each iteration
        for i in range(n):
            for j in range(n):
                candidate = dist[i][k] + dist[k][j]
                if candidate < dist[i][j]:
                    new_dist[i][j] = candidate
                # Redundant: recompute min even when not needed
                new_dist[i][j] = min(new_dist[i][j], dist[i][j])
        dist = new_dist
    return dist


# === Вариант 1: Обработка CSV ===


def slow_csv_processing(n_rows: int = 200_000) -> dict:
    """
    Наивная агрегация данных без pandas: повторное сканирование,
    конкатенация строк, пересоздание списков.
    """
    random.seed(42)
    categories = ["electronics", "clothing", "food", "books", "toys"]

    # Generate data as list of dicts (simulating CSV rows)
    rows = []
    for i in range(n_rows):
        rows.append(
            {
                "id": i,
                "category": categories[i % len(categories)],
                "price": round(random.uniform(1.0, 1000.0), 2),
                "quantity": random.randint(1, 100),
            }
        )

    # Deliberately slow aggregation — multiple redundant passes
    result = {}
    for cat in categories:
        # Filter by scanning entire list each time
        cat_rows = []
        for row in rows:
            if row["category"] == cat:
                cat_rows.append(row)

        # Sum prices by iterating again
        total_price = 0.0
        for row in cat_rows:
            total_price = total_price + row["price"]

        # Count by iterating again
        count = 0
        for row in cat_rows:
            count = count + 1

        # Average using string formatting and parsing (deliberately bad)
        avg_str = f"{total_price / count:.10f}"
        avg = float(avg_str)

        # Max price by sorting (O(n log n) instead of O(n))
        sorted_rows = sorted(cat_rows, key=lambda r: r["price"], reverse=True)
        max_price = sorted_rows[0]["price"]

        # Deliberately wasteful: recompute total_quantity by scanning ALL rows again
        total_qty = 0
        for row in rows:
            if row["category"] == cat:
                total_qty += row["quantity"]

        # Deliberately wasteful: build a price list via string conversion and back
        price_strings = []
        for row in cat_rows:
            price_strings.append(f"{row['price']:.10f}")
        parsed_prices = [float(s) for s in price_strings]
        _verify_total = sum(parsed_prices)

        # Deliberately wasteful: find min price by sorting again
        sorted_asc = sorted(cat_rows, key=lambda r: r["price"])
        min_price = sorted_asc[0]["price"]

        # Deliberately wasteful: compute median by sorting yet again
        price_list = sorted([row["price"] for row in cat_rows])
        mid = len(price_list) // 2
        median = price_list[mid]

        result[cat] = {
            "count": count,
            "total": total_price,
            "average": avg,
            "max_price": max_price,
            "min_price": min_price,
            "median": median,
            "total_quantity": total_qty,
        }

    return result


# === Вариант 2: Числовые вычисления ===


def slow_numerical(n: int = 300) -> list[list[float]]:
    """
    Матричные операции с вложенными циклами: умножение матриц,
    вычисление нормы, всё на чистом Python без numpy.
    """
    random.seed(42)

    # Create two random matrices
    A = [[random.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
    B = [[random.uniform(-10, 10) for _ in range(n)] for _ in range(n)]

    # Matrix multiplication O(n^3) — pure Python
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s

    # Normalize each row (recompute norm per element — deliberately wasteful)
    result = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            # Recompute row norm for every element (should compute once per row)
            norm = 0.0
            for k in range(n):
                norm += C[i][k] ** 2
            norm = math.sqrt(norm)
            if norm > 0:
                result[i][j] = C[i][j] / norm

    return result


# === Вариант 3: Парсинг текста ===


def slow_text_parsing(text_size: int = 500_000) -> dict:
    """
    Наивный поиск паттернов в тексте: посимвольный проход,
    конкатенация строк, регулярки в цикле.
    """

    random.seed(42)

    # Generate large text with patterns
    words = [
        "error",
        "warning",
        "info",
        "debug",
        "critical",
        "connection",
        "timeout",
        "success",
        "failure",
        "retry",
        "the",
        "a",
        "is",
        "was",
        "to",
        "from",
        "at",
        "by",
    ]
    text = " ".join(random.choice(words) for _ in range(text_size))

    # Deliberately slow pattern search
    patterns = ["error", "warning", "critical", "timeout", "failure"]
    result = {}

    for pattern in patterns:
        # Method 1: Character-by-character search (deliberately naive)
        count = 0
        for i in range(len(text) - len(pattern) + 1):
            match = True
            for j in range(len(pattern)):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                count += 1

        # Method 2: Also find positions using string concatenation (slow)
        positions = []
        current = ""
        pos = 0
        for char in text:
            current += char  # string concatenation in loop!
            if len(current) > 1000:
                # Search in accumulated chunk
                idx = 0
                while True:
                    found = current.find(pattern, idx)
                    if found == -1:
                        break
                    positions.append(pos - len(current) + found)
                    idx = found + 1
                current = current[-len(pattern) :]  # keep overlap
            pos += 1

        result[pattern] = {"count": count, "positions_sample": positions[:10]}

    return result


# Dispatch table for running the right variant
VARIANTS = {
    0: slow_shortest_paths,
    1: slow_csv_processing,
    2: slow_numerical,
    3: slow_text_parsing,
}


def run_variant(variant: int):
    """Run the slow code for the given variant."""
    func = VARIANTS[variant]
    return func()
