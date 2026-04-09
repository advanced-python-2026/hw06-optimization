"""
Ускоренная версия с использованием Numba (@jit) или Cython.

Реализуйте функцию accelerated_run(variant: int), которая
возвращает тот же результат, что и src/slow_code.VARIANTS[variant](),
используя Numba JIT-компиляцию или Cython для критичных участков.
"""


def accelerated_run(variant: int):
    """
    Запускает ускоренную (Numba/Cython) версию алгоритма для данного варианта.

    Должна возвращать результат, идентичный src/slow_code.VARIANTS[variant]().
    """
    raise NotImplementedError("Реализуй ускоренную версию с Numba или Cython")
