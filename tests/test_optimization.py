"""
Тесты корректности и производительности оптимизации.

Проверяют, что:
1. Оригинальный slow_code выдаёт корректный результат (smoke test).
2. optimized_run возвращает тот же результат, что и оригинал.
3. optimized_run работает минимум в 5 раз быстрее оригинала.
4. accelerated_run возвращает тот же результат, что и оригинал.
5. accelerated_run работает быстрее, чем optimized_run.
"""

from __future__ import annotations

import math
import time

import pytest

from src.slow_code import VARIANTS
from tests.conftest import _read_student_name, get_variant

# ---------------------------------------------------------------------------
# Helpers for comparing results across different variant return types
# ---------------------------------------------------------------------------

FLOAT_ABS_TOL = 1e-6
FLOAT_REL_TOL = 1e-4


def _approx_equal(a: float, b: float) -> bool:
    """Check two floats are approximately equal."""
    if math.isinf(a) and math.isinf(b):
        return (a > 0) == (b > 0)
    if math.isnan(a) and math.isnan(b):
        return True
    if abs(a) < FLOAT_ABS_TOL and abs(b) < FLOAT_ABS_TOL:
        return True
    return abs(a - b) <= max(FLOAT_ABS_TOL, FLOAT_REL_TOL * max(abs(a), abs(b)))


def _compare_matrix(original: list[list[float]], optimized: list[list[float]]) -> None:
    """Compare two 2D float matrices (variants 0 and 2)."""
    assert len(original) == len(optimized), (
        f"Row count mismatch: {len(original)} vs {len(optimized)}"
    )
    for i, (row_a, row_b) in enumerate(zip(original, optimized)):
        assert len(row_a) == len(row_b), (
            f"Column count mismatch in row {i}: {len(row_a)} vs {len(row_b)}"
        )
        for j, (va, vb) in enumerate(zip(row_a, row_b)):
            assert _approx_equal(va, vb), f"Mismatch at [{i}][{j}]: original={va}, optimized={vb}"


def _compare_csv_result(original: dict, optimized: dict) -> None:
    """Compare CSV aggregation results (variant 1)."""
    assert set(original.keys()) == set(optimized.keys()), (
        f"Category keys differ: {set(original.keys())} vs {set(optimized.keys())}"
    )
    for cat in original:
        orig_cat = original[cat]
        opt_cat = optimized[cat]
        for key in orig_cat:
            assert key in opt_cat, f"Missing key '{key}' for category '{cat}'"
            if isinstance(orig_cat[key], float):
                assert _approx_equal(orig_cat[key], opt_cat[key]), (
                    f"{key} mismatch for '{cat}': {orig_cat[key]} vs {opt_cat[key]}"
                )
            else:
                assert orig_cat[key] == opt_cat[key], (
                    f"{key} mismatch for '{cat}': {orig_cat[key]} vs {opt_cat[key]}"
                )


def _compare_text_result(original: dict, optimized: dict) -> None:
    """Compare text parsing results (variant 3)."""
    assert set(original.keys()) == set(optimized.keys()), (
        f"Pattern keys differ: {set(original.keys())} vs {set(optimized.keys())}"
    )
    for pattern in original:
        orig_p = original[pattern]
        opt_p = optimized[pattern]
        assert orig_p["count"] == opt_p["count"], (
            f"Count mismatch for '{pattern}': {orig_p['count']} vs {opt_p['count']}"
        )
        # positions_sample can differ in implementation detail,
        # but count must match exactly
        assert isinstance(opt_p.get("positions_sample"), list), (
            f"positions_sample for '{pattern}' must be a list"
        )


def compare_results(variant: int, original, optimized) -> None:
    """Dispatch to the right comparison function based on variant."""
    if variant == 0:
        _compare_matrix(original, optimized)
    elif variant == 1:
        _compare_csv_result(original, optimized)
    elif variant == 2:
        _compare_matrix(original, optimized)
    elif variant == 3:
        _compare_text_result(original, optimized)
    else:
        raise ValueError(f"Unknown variant: {variant}")


# ---------------------------------------------------------------------------
# Timing helper
# ---------------------------------------------------------------------------


def _time_call(func, *args, **kwargs) -> tuple:
    """Run func and return (result, elapsed_seconds)."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


# ---------------------------------------------------------------------------
# Session-scoped fixtures (run slow code only once)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def variant_number():
    """Session-scoped variant calculation."""
    name = _read_student_name()
    return get_variant(name, n_variants=4)


@pytest.fixture(scope="session")
def original_benchmark(variant_number):
    """Run slow code once, cache result and timing."""
    func = VARIANTS[variant_number]
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    return {"result": result, "time": elapsed}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestOriginalSmoke:
    """Smoke test: original slow code runs and returns something sensible."""

    def test_original_runs(self, original_benchmark) -> None:
        assert original_benchmark["result"] is not None


class TestOptimized:
    """Tests for hw06/optimized.py."""

    def test_optimized_correctness(self, variant_number, original_benchmark) -> None:
        """Optimized version produces the same result as the original."""
        from hw06.optimized import optimized_run

        optimized_result = optimized_run(variant_number)

        compare_results(variant_number, original_benchmark["result"], optimized_result)

    def test_optimized_speedup(self, variant_number, original_benchmark) -> None:
        """Optimized version is at least 5x faster than the original."""
        from hw06.optimized import optimized_run

        _, optimized_time = _time_call(optimized_run, variant_number)

        original_time = original_benchmark["time"]
        speedup = original_time / optimized_time
        assert speedup >= 5.0, (
            f"Insufficient speedup: {speedup:.1f}x "
            f"(original={original_time:.2f}s, optimized={optimized_time:.2f}s, "
            f"required >= 5.0x)"
        )


class TestAccelerated:
    """Tests for hw06/accelerated.py."""

    def test_accelerated_correctness(self, variant_number, original_benchmark) -> None:
        """Accelerated version produces the same result as the original."""
        from hw06.accelerated import accelerated_run

        accelerated_result = accelerated_run(variant_number)

        compare_results(variant_number, original_benchmark["result"], accelerated_result)

    def test_accelerated_faster_than_optimized(self, variant_number) -> None:
        """Accelerated version is faster than the pure-Python optimized version."""
        from hw06.accelerated import accelerated_run
        from hw06.optimized import optimized_run

        _, optimized_time = _time_call(optimized_run, variant_number)
        _, accelerated_time = _time_call(accelerated_run, variant_number)

        assert accelerated_time < optimized_time, (
            f"Accelerated ({accelerated_time:.2f}s) is not faster "
            f"than optimized ({optimized_time:.2f}s)"
        )
