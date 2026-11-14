"""
Оптимизированный прямой воксельный метод расчета переходов и удельной площади поверхности.
Фасадный интерфейс обратной совместимости к методам класса DirectMethodCalculator.
"""

from typing import Optional
import numpy as np

from config import SILICA_DENSITY
from methods.direct_method import DirectMethodCalculator

_DEFAULT_DM_CALC = DirectMethodCalculator()


def PerehodiStrucure(A: np.ndarray, a: Optional[int] = None, b: Optional[int] = None, c: Optional[int] = None) -> int:
    """
    Вычисляет суммарное количество фазовых переходов 0 <-> 1
    вдоль трех декартовых осей координат (Z, X, Y).
    """
    total, _, _, _ = _DEFAULT_DM_CALC.count_phase_transitions(A)
    return total


def FullSSA(cubes: int, A: float, perehodi: int, density: Optional[float] = SILICA_DENSITY) -> float:
    """
    Вычисляет удельную площадь поверхности (SSA, м^2/г):
    SSA = N_S / (N_V * a * rho).
    """
    if cubes == 0 or A == 0:
        return 0.0
    if density is None or density == 1.0:
        return perehodi / (cubes * A)
    return perehodi / (cubes * A * density)
