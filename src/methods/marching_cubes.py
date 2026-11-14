"""
Реализация алгоритма Marching Cubes с модификацией учета межъячеечных потерь.
Инкапсулирована в ООП класс MarchingCubesCalculator.
"""

import time
from typing import Optional, Tuple, Dict, Any
import numpy as np

from config import SILICA_DENSITY
from methods.base import BaseSSACalculator, SSAResult
from methods.tables.mc_tables import (
    CORRECTION_M0,
    CORRECTION_M1,
    CORRECTION_M2,
    BASE_TABLE_S,
    BASE_TABLE_V,
)


class MarchingCubesCalculator(BaseSSACalculator):
    """
    Вычислитель удельной площади поверхности (SSA) и объема
    методом Marching Cubes с авторской модификацией учета потерь.

    Параметры:
        with_correction: Учитывать ли межъячеечные граничные коррекции (авторская модификация).
                         Если False, выполняется расчет классическим методом Marching Cubes.
        cube_step: Шаг дискретизации кубов (по умолчанию 2 вокселя, как в диссертации).
    """

    def __init__(self, with_correction: bool = True, cube_step: int = 2):
        method_name = "Marching Cubes (Modified)" if with_correction else "Marching Cubes (Classical)"
        super().__init__(name=method_name)
        self.with_correction = with_correction
        self.cube_step = cube_step

    def make_cubes_table(self, voxels: np.ndarray) -> np.ndarray:
        """
        Преобразует 3D массив вокселей в двумерный массив кубов формы (N_cubes, 8).
        Срезы берутся с шагом self.cube_step.
        """
        shape = voxels.shape
        nx = shape[0] if shape[0] % 2 == 0 else shape[0] - 1
        ny = shape[1] if shape[1] % 2 == 0 else shape[1] - 1
        nz = shape[2] if shape[2] % 2 == 0 else shape[2] - 1
        c = voxels[:nx, :ny, :nz]

        # 8 вершин куба в порядке обхода алгоритма
        v0 = c[0::2, 0::2, 0::2].ravel()
        v1 = c[0::2, 0::2, 1::2].ravel()
        v2 = c[0::2, 1::2, 1::2].ravel()
        v3 = c[0::2, 1::2, 0::2].ravel()
        v4 = c[1::2, 0::2, 0::2].ravel()
        v5 = c[1::2, 0::2, 1::2].ravel()
        v6 = c[1::2, 1::2, 1::2].ravel()
        v7 = c[1::2, 1::2, 0::2].ravel()

        return np.column_stack([v0, v1, v2, v3, v4, v5, v6, v7])

    def compute_surface_and_volume(
        self,
        cubes: np.ndarray,
        shape: Tuple[int, int, int],
        cube_edge: float,
    ) -> Tuple[float, float, Dict[str, float]]:
        """
        Вычисляет абсолютную площадь поверхности (м^2) и объем твердой фазы (м^3).

        Параметры:
            cubes: (N_cubes, 8) массив вершин
            shape: (Z, Y, X) исходного массива вокселей
            cube_edge: линейный размер ребра элементарного куба A (в метрах)

        Возвращает:
            (surface_area_m2, solid_volume_m3, diagnostics_dict)
        """
        if cubes is None or len(cubes) == 0:
            return 0.0, 0.0, {}

        v0 = cubes[:, 0].astype(np.int32)
        v1 = cubes[:, 1].astype(np.int32)
        v2 = cubes[:, 2].astype(np.int32)
        v3 = cubes[:, 3].astype(np.int32)
        v4 = cubes[:, 4].astype(np.int32)
        v5 = cubes[:, 5].astype(np.int32)
        v6 = cubes[:, 6].astype(np.int32)
        v7 = cubes[:, 7].astype(np.int32)

        # 8-битный код топологии каждого куба (0..255)
        codes = (v0 << 7) | (v1 << 6) | (v2 << 5) | (v3 << 4) | (v4 << 3) | (v5 << 2) | (v6 << 1) | v7

        # Базовая площадь и объем ячеек
        s_unit = float(np.sum(BASE_TABLE_S[codes]))
        v_unit = float(np.sum(BASE_TABLE_V[codes]))

        s_base = s_unit * (cube_edge ** 2)
        v_base = v_unit * (cube_edge ** 3)

        corr0, corr1, corr2 = 0.0, 0.0, 0.0
        if self.with_correction and v_base > 0:
            # Смежные грани по трем осям:
            # Ось Z:
            fn0 = (v0 << 3) | (v3 << 2) | (v4 << 1) | v7
            fc0 = (v1 << 3) | (v2 << 2) | (v5 << 1) | v6

            # Ось Y:
            fn1 = (v0 << 3) | (v1 << 2) | (v4 << 1) | v5
            fc1 = (v2 << 3) | (v3 << 2) | (v6 << 1) | v7

            # Ось X:
            fn2 = (v0 << 3) | (v1 << 2) | (v2 << 1) | v3
            fc2 = (v4 << 3) | (v5 << 2) | (v6 << 1) | v7

            step0 = 1
            step1 = int((shape[2] * 4 * 2) / (8 * 2))
            step2 = int((4 * shape[1] * shape[2]) / (2 * 8))

            n_cubes = len(codes)
            if step0 < n_cubes:
                corr0 = float(np.sum(CORRECTION_M0[fn0[step0:], fc0[:-step0]])) * (cube_edge ** 2)
            if step1 < n_cubes:
                corr1 = float(np.sum(CORRECTION_M1[fn1[step1:], fc1[:-step1]])) * (cube_edge ** 2)
            if step2 < n_cubes:
                corr2 = float(np.sum(CORRECTION_M2[fn2[step2:], fc2[:-step2]])) * (cube_edge ** 2)

        s_total = s_base + corr0 + corr1 + corr2

        details = {
            "s_base": s_base,
            "corr_z": corr0,
            "corr_y": corr1,
            "corr_x": corr2,
            "s_total": s_total,
            "v_solid": v_base,
            "cubes_count": len(codes),
        }

        return s_total, v_base, details

    def calculate(self, structure: Any) -> SSAResult:
        """
        Вычисляет SSA для объекта PorousStructure.
        """
        t0 = time.time()
        # Линейный размер куба Marching Cubes: A = cube_step * voxel_size
        cube_edge = structure.voxel_size * self.cube_step

        cubes = self.make_cubes_table(structure.voxels)
        s_total, v_solid, details = self.compute_surface_and_volume(
            cubes=cubes,
            shape=structure.shape,
            cube_edge=cube_edge,
        )

        dt = time.time() - t0

        if v_solid <= 0:
            ssa = 0.0
        elif structure.density is None or structure.density == 1.0:
            ssa = s_total / v_solid
        else:
            # SSA = S / (V_solid * density)
            ssa = s_total / (v_solid * structure.density)

        rel_error = None
        if structure.nominal_ssa and structure.nominal_ssa > 0:
            rel_error = ((ssa - structure.nominal_ssa) / structure.nominal_ssa) * 100.0

        return SSAResult(
            structure_name=structure.name,
            method_name=self.name,
            ssa_m2_g=ssa,
            surface_area_m2=s_total,
            solid_volume_m3=v_solid,
            porosity=structure.porosity,
            voxel_size=structure.voxel_size,
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
