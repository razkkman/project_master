"""
Реализация прямого воксельного метода подсчета межфазных переходов и SSA.
Инкапсулирована в ООП класс DirectMethodCalculator.
"""

import time
from typing import Optional, Tuple, Dict, Any
import numpy as np

from config import SILICA_DENSITY
from methods.base import BaseSSACalculator, SSAResult


class DirectMethodCalculator(BaseSSACalculator):
    """
    Вычислитель удельной площади поверхности (SSA) прямым воксельным методом.
    Определяет число фазовых переходов 0 <-> 1 вдоль трех координатных осей.

    Формула:
        S = N_S * h^2
        V_solid = N_V * h^3
        SSA = N_S / (rho * h * N_V)
    """

    def __init__(self):
        super().__init__(name="Direct Method")

    @staticmethod
    def count_phase_transitions(voxels: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Векторизованно вычисляет число фазовых переходов вдоль осей Z, X, Y.

        Возвращает:
            (total_transitions, transitions_z, transitions_x, transitions_y)
        """
        if voxels is None or voxels.size == 0:
            return 0, 0, 0, 0

        # Срезы NumPy вдоль трех координатных осей
        pz = int(np.count_nonzero(voxels[:, :, :-1] != voxels[:, :, 1:]))
        px = int(np.count_nonzero(voxels[:-1, :, :] != voxels[1:, :, :]))
        py = int(np.count_nonzero(voxels[:, :-1, :] != voxels[:, 1:, :]))
        total = pz + px + py

        return total, pz, px, py

    def calculate(self, structure: Any) -> SSAResult:
        """
        Вычисляет SSA для объекта PorousStructure.
        """
        t0 = time.time()
        voxels = structure.voxels
        voxel_size = structure.voxel_size
        density = structure.density

        n_s, pz, px, py = self.count_phase_transitions(voxels)
        n_solid = structure.solid_voxels

        surface_area = n_s * (voxel_size ** 2)
        solid_volume = n_solid * (voxel_size ** 3)

        dt = time.time() - t0

        if n_solid <= 0 or voxel_size <= 0:
            ssa = 0.0
        elif density is None or density == 1.0:
            ssa = n_s / (n_solid * voxel_size)
        else:
            # SSA = N_S / (rho * h * N_solid)
            ssa = n_s / (density * voxel_size * n_solid)

        rel_error = None
        if structure.nominal_ssa and structure.nominal_ssa > 0:
            rel_error = ((ssa - structure.nominal_ssa) / structure.nominal_ssa) * 100.0

        details = {
            "phase_transitions_total": n_s,
            "transitions_z": pz,
            "transitions_x": px,
            "transitions_y": py,
            "solid_voxels": n_solid,
        }

        return SSAResult(
            structure_name=structure.name,
            method_name=self.name,
            ssa_m2_g=ssa,
            surface_area_m2=surface_area,
            solid_volume_m3=solid_volume,
            porosity=structure.porosity,
            voxel_size=voxel_size,
            execution_time_sec=dt,
            nominal_ssa=structure.nominal_ssa,
            relative_error_pct=rel_error,
            details=details,
        )

    def calculate_from_array(
        self,
        voxels: np.ndarray,
        voxel_size: float,
        density: float = SILICA_DENSITY,
        name: str = "custom_array",
        nominal_ssa: Optional[float] = None,
    ) -> SSAResult:
        """
        Вычисляет SSA напрямую для 3D NumPy массива.
        """
        from core.structure import PorousStructure

        struct = PorousStructure(
            name=name,
            voxels=voxels,
            voxel_size=voxel_size,
            density=density,
            nominal_ssa=nominal_ssa,
        )
        return self.calculate(struct)
