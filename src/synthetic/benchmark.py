"""
Калибровочные тесты алгоритмов на синтетических телах (сферах и цилиндрах).
Инкапсулированы в класс CalibrationBenchmark.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import FIGURES_DIR
from synthetic.shapes import SyntheticSphere, SyntheticCylinder
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator


class CalibrationBenchmark:
    """
    Класс для сравнительного тестирования вычислительных алгоритмов SSA
    на дискретизированных калибровочных геометрических телах с точным аналитическим решением.

    Параметры:
        figures_dir: Путь для сохранения графиков верификации
    """

    def __init__(self, figures_dir: Union[str, Path] = FIGURES_DIR):
        self.figures_dir = Path(figures_dir)
        self.mc_mod = MarchingCubesCalculator(with_correction=True, cube_step=2)
        self.mc_clas = MarchingCubesCalculator(with_correction=False, cube_step=2)
        self.pm = DirectMethodCalculator()

    def run_sphere_benchmark(
        self,
        d_min: int = 3,
        d_max: int = 30,
        step: int = 2,
        voxel_size: float = 1.0,
        save_plot: bool = True,
    ) -> pd.DataFrame:
        """
        Проводит серию расчетов для сфер с диаметром от d_min до d_max.
        Сравнивает аналитическое решение с Marching Cubes и Direct Method.
        """
        diameters = np.arange(d_min, d_max, step)
        records = []

        for d in diameters:
            sphere = SyntheticSphere(diameter_voxels=int(d), voxel_size=voxel_size, density=1.0)
            voxels = sphere.generate()
            exact_ssa = sphere.analytical_ssa()

            # Marching Cubes (модифицированный)
            res_mc = self.mc_mod.calculate_from_array(voxels, voxel_size=voxel_size, density=1.0)
            err_mc = abs(res_mc.ssa_m2_g - exact_ssa) * 100.0 / exact_ssa

            # Прямой воксельный метод
            res_pm = self.pm.calculate_from_array(voxels, voxel_size=voxel_size, density=1.0)
            err_pm = abs(res_pm.ssa_m2_g - exact_ssa) * 100.0 / exact_ssa

            records.append({
                "diameter": int(d),
                "ssa_exact": exact_ssa,
                "ssa_mc": res_mc.ssa_m2_g,
                "error_mc_pct": err_mc,
                "ssa_pm": res_pm.ssa_m2_g,
                "error_pm_pct": err_pm,
            })

        df = pd.DataFrame(records)

        if save_plot:
            self.figures_dir.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
            ax.plot(df["diameter"], df["error_mc_pct"], 'b-o', label='Marching Cubes (модиф.)', lw=2)
            ax.plot(df["diameter"], df["error_pm_pct"], 'r-s', label='Прямой воксельный метод', lw=2)
            ax.set_xlabel('Диаметр сферы d (в вокселях)', fontsize=11)
            ax.set_ylabel('Погрешность Δ, %', fontsize=11)
            ax.set_title('Зависимость погрешности расчета SSA от диаметра сферы', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            fig.savefig(self.figures_dir / "Figure_sphere_error.png", dpi=170)
            plt.close(fig)

        return df

    def run_cylinder_benchmark(
        self,
        fixed_h: int = 5,
        d_min: int = 3,
        d_max: int = 30,
        step: int = 2,
        voxel_size: float = 1.0,
        save_plot: bool = True,
    ) -> pd.DataFrame:
        """
        Проводит серию расчетов для цилиндров фиксированной высоты и переменного диаметра.
        """
        diameters = np.arange(d_min, d_max, step)
        records = []

        for d in diameters:
            cyl = SyntheticCylinder(
                diameter_voxels=int(d),
                height_voxels=fixed_h,
                voxel_size=voxel_size,
                density=1.0,
            )
            voxels = cyl.generate()
            exact_ssa = cyl.analytical_ssa()

            res_mc = self.mc_mod.calculate_from_array(voxels, voxel_size=voxel_size, density=1.0)
            err_mc = abs(res_mc.ssa_m2_g - exact_ssa) * 100.0 / exact_ssa

            res_pm = self.pm.calculate_from_array(voxels, voxel_size=voxel_size, density=1.0)
            err_pm = abs(res_pm.ssa_m2_g - exact_ssa) * 100.0 / exact_ssa

            records.append({
                "diameter": int(d),
                "height": fixed_h,
                "ssa_exact": exact_ssa,
                "ssa_mc": res_mc.ssa_m2_g,
                "error_mc_pct": err_mc,
                "ssa_pm": res_pm.ssa_m2_g,
                "error_pm_pct": err_pm,
            })

        df = pd.DataFrame(records)

        if save_plot:
            self.figures_dir.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
            ax.plot(df["diameter"], df["error_mc_pct"], 'b-o', label='Marching Cubes (модиф.)', lw=2)
            ax.plot(df["diameter"], df["error_pm_pct"], 'r-s', label='Прямой воксельный метод', lw=2)
            ax.set_xlabel('Диаметр цилиндра d (в вокселях, H=const)', fontsize=11)
            ax.set_ylabel('Погрешность Δ, %', fontsize=11)
            ax.set_title(f'Погрешность расчета цилиндра (высота H={fixed_h} вокс.)', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            fig.savefig(self.figures_dir / "Figure_cylinder_error.png", dpi=170)
            plt.close(fig)

        return df
