"""
Базовый интерфейс и структуры данных для алгоритмов вычисления удельной площади поверхности.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import numpy as np

from config import SILICA_DENSITY


@dataclass
class SSAResult:
    """
    Результат расчета удельной площади поверхности (SSA).

    Атрибуты:
        structure_name: Название исследованной структуры
        method_name: Название использованного метода расчета
        ssa_m2_g: Удельная площадь поверхности (м^2/г)
        surface_area_m2: Абсолютная площадь поверхности (м^2)
        solid_volume_m3: Объем твердой фазы (м^3)
        porosity: Пористость объема
        voxel_size: Физический размер вокселя (метры)
        execution_time_sec: Время выполнения расчета (секунды)
        nominal_ssa: Экспериментальное значение (БЭТ, м^2/г), если известно
        relative_error_pct: Относительная погрешность относительно БЭТ (%), если известно
        details: Дополнительные диагностические параметры алгоритма
    """
    structure_name: str
    method_name: str
    ssa_m2_g: float
    surface_area_m2: float
    solid_volume_m3: float
    porosity: float
    voxel_size: float
    execution_time_sec: float
    nominal_ssa: Optional[float] = None
    relative_error_pct: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        """Форматированная сводная строка результата."""
        nominal_str = f", БЭТ: {self.nominal_ssa:.1f} м²/г" if self.nominal_ssa else ""
        err_str = f", Погрешность: {self.relative_error_pct:+.2f}%" if self.relative_error_pct is not None else ""
        return (
            f"[{self.method_name}] {self.structure_name} | "
            f"SSA: {self.ssa_m2_g:.2f} м²/г{nominal_str}{err_str} | "
            f"Время: {self.execution_time_sec:.3f} с"
        )


class BaseSSACalculator(ABC):
    """
    Абстрактный базовый класс для вычислителей удельной площади поверхности.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate(self, structure: Any) -> SSAResult:
        """
        Вычисляет SSA для переданного объекта PorousStructure.
        """
        pass

    @abstractmethod
    def calculate_from_array(
        self,
        voxels: np.ndarray,
        voxel_size: float,
        density: float = SILICA_DENSITY,
        name: str = "custom_array",
        nominal_ssa: Optional[float] = None,
    ) -> SSAResult:
        """
        Вычисляет SSA напрямую из 3D массива вокселей.
        """
        pass
