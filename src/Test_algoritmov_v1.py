"""
Тестирование алгоритмов расчета удельной площади поверхности
на калибровочных аналитических геометрических объектах (сфера и цилиндр).
Фасадный интерфейс, делегирующий расчет классу CalibrationBenchmark.
"""

from typing import Tuple
import numpy as np
from synthetic.benchmark import CalibrationBenchmark


def test_spheres(d_min: int = 3, d_max: int = 30, step: int = 2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Тестирование на сферах различного диаметра."""
    benchmark = CalibrationBenchmark()
    df = benchmark.run_sphere_benchmark(d_min=d_min, d_max=d_max, step=step)
    return df["diameter"].values, df["error_mc_pct"].values, df["error_pm_pct"].values


def test_cylinders_fixed_h(h: int = 5, d_min: int = 3, d_max: int = 30, step: int = 2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Тестирование на цилиндрах фиксированной высоты h и переменного диаметра d."""
    benchmark = CalibrationBenchmark()
    df = benchmark.run_cylinder_benchmark(fixed_h=h, d_min=d_min, d_max=d_max, step=step)
    return df["diameter"].values, df["error_mc_pct"].values, df["error_pm_pct"].values


if __name__ == "__main__":
    print("=== ВЕРИФИКАЦИЯ НА СФЕРАХ РАЗЛИЧНОГО ДИАМЕТРА ===")
    d, emc, epm = test_spheres(3, 25, 4)
    for d_val, m, p in zip(d, emc, epm):
        print(f"d={d_val:2d} | MC error: {m:5.2f}% | PM error: {p:5.2f}%")
