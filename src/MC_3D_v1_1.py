"""
Высокопроизводительная реализация адаптированного метода Marching Cubes
для расчета удельной площади поверхности (SSA) и объема пористых структур.
Фасадный интерфейс обратной совместимости к методам класса MarchingCubesCalculator.
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np

from config import SILICA_DENSITY
from methods.tables.mc_tables import (
    CORRECTION_M0,
    CORRECTION_M1,
    CORRECTION_M2,
    get_lookup_table_raw,
    build_table_arrays,
)
from methods.marching_cubes import MarchingCubesCalculator

_DEFAULT_MC_CALC = MarchingCubesCalculator(with_correction=True, cube_step=2)


def MakeTable_v1_1(cub: np.ndarray) -> np.ndarray:
    """
    Преобразует 3D массив вокселей в двумерный массив кубов формы (N_cubes, 8).
    Делегирует вызов в MarchingCubesCalculator.
    """
    return _DEFAULT_MC_CALC.make_cubes_table(cub)


def LookupTable_v1_1(A: float = 1.0) -> Dict[str, Tuple[float, float]]:
    """
    Оригинальная таблица поиска Marching Cubes для 256 конфигураций.
    """
    return get_lookup_table_raw(A)


def ChTypeAndReturnSSA_v1_1(
    cubes: np.ndarray,
    Table: Optional[Dict[str, Tuple[float, float]]] = None,
    A: float = 1.0,
    Shape: Optional[Tuple[int, int, int]] = None,
    density: Optional[float] = SILICA_DENSITY,
) -> float:
    """
    Вычисляет удельную площадь поверхности (SSA) методом Marching Cubes
    с авторской модификацией учета межъячеечных потерь.
    """
    if cubes is None or len(cubes) == 0:
        return 0.0

    shape = Shape or (100, 100, 100)
    s_total, v_solid, _ = _DEFAULT_MC_CALC.compute_surface_and_volume(
        cubes=cubes,
        shape=shape,
        cube_edge=A,
    )

    if v_solid <= 0:
        return 0.0
    if density is None or density == 1.0:
        return s_total / v_solid
    return s_total / (v_solid * density)


def ChTypeAndReturnV_v1_1(
    cubes: np.ndarray,
    Table: Optional[Dict[str, Tuple[float, float]]] = None,
) -> float:
    """
    Вычисляет нормированный объем твердой фазы по кубам (без умножения на A^3).
    """
    if cubes is None or len(cubes) == 0:
        return 0.0

    _, v_solid, _ = _DEFAULT_MC_CALC.compute_surface_and_volume(
        cubes=cubes,
        shape=(100, 100, 100),
        cube_edge=1.0,
    )
    return v_solid
