"""
Конвейер комплексного сравнительного анализа удельной площади поверхности (SSA).
Объединяет загрузку, расчет методами Marching Cubes (классический и модифицированный)
и Direct Method, сопоставление с данными БЭТ и сеточный анализ сходимости по масштабам k.
"""

import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import (
    STRUCTURES_ALL,
    STRUCTURES_ORDERED,
    STRUCTURES_DISORDERED,
    VOXEL_SIZES,
    SSA_FIS_NOMINAL,
    POROSITY_NOMINAL,
    PROCESSED_DIR,
    FIGURES_DIR,
    SCALE_FACTORS,
    parse_structure_name,
    get_scale_series_names,
)
from core.structure import PorousStructure
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator
from methods.base import SSAResult


class SSAEvaluationPipeline:
    """
    Высокоуровневый пайплайн для пакетного расчета и сравнительного анализа
    всех исследуемых пористых сред (как базовых, так и масштабных серий k in [0.70 .. 1.00]).
    """

    def __init__(
        self,
        structures: Optional[List[str]] = None,
        cache_dir: Union[str, Path] = PROCESSED_DIR,
    ):
        self.structures = structures or STRUCTURES_ALL
        self.cache_dir = Path(cache_dir)
        self.mc_modified = MarchingCubesCalculator(with_correction=True, cube_step=2)
        self.mc_classical = MarchingCubesCalculator(with_correction=False, cube_step=2)
        self.direct_method = DirectMethodCalculator()

    def run_structure(self, name: str) -> Dict[str, Any]:
        """
        Выполняет расчет SSA для одной структуры всеми методами.
        Корректно обрабатывает как базовые структуры, так и масштабированные (например, 'Si12-0.7').
        """
        t0 = time.time()
        structure = PorousStructure.load(name, cache_dir=self.cache_dir)

        res_mc_mod = self.mc_modified.calculate(structure)
        res_mc_clas = self.mc_classical.calculate(structure)
        res_dm = self.direct_method.calculate(structure)
        total_time = time.time() - t0

        nominal_bet = structure.nominal_ssa or 0.0
        err_mc_mod = abs(res_mc_mod.ssa_m2_g - nominal_bet) * 100.0 / nominal_bet if nominal_bet else None
        err_mc_clas = abs(res_mc_clas.ssa_m2_g - nominal_bet) * 100.0 / nominal_bet if nominal_bet else None
        err_dm = abs(res_dm.ssa_m2_g - nominal_bet) * 100.0 / nominal_bet if nominal_bet else None

        best_method = "MC (модиф.)" if (err_mc_mod is not None and err_dm is not None and err_mc_mod < err_dm) else "Прямой метод"

        return {
            "structure": name,
            "base_structure": structure.base_name,
            "scale_factor": structure.scale_factor,
            "shape": f"{structure.shape[0]}x{structure.shape[1]}x{structure.shape[2]}",
            "nominal_bet": nominal_bet,
            "porosity": structure.porosity,
            "voxel_size_nm": structure.voxel_size * 1e9,
            "ssa_mc_modified": res_mc_mod.ssa_m2_g,
            "error_mc_mod_pct": err_mc_mod,
            "ssa_mc_classical": res_mc_clas.ssa_m2_g,
            "error_mc_clas_pct": err_mc_clas,
            "ssa_direct_method": res_dm.ssa_m2_g,
            "error_direct_pct": err_dm,
            "best_method": best_method,
            "time_sec": total_time,
        }

    def run_scale_series(self, base_name: str, verbose: bool = True, save_plot: bool = True) -> pd.DataFrame:
        """
        Исследует сеточную сходимость для структуры во всем диапазоне масштабов:
        k in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00].
        Формирует сравнительную таблицу погрешностей и строит график Delta(k).
        """
        scale_names = get_scale_series_names(base_name)
        nominal_bet = SSA_FIS_NOMINAL.get(base_name, 0.0)

        if verbose:
            print("\n" + "=" * 104)
            print(f"  ИССЛЕДОВАНИЕ СЕТОЧНОЙ СХОДИМОСТИ ДЛЯ {base_name} (k = 0.70 .. 1.00, БЭТ: {nominal_bet:.1f} м²/г)")
            print("=" * 104)
            print(f"{'Масштаб k':<10} | {'Сетка (Z,Y,X)':<14} | {'Пористость':<10} | {'MC Модиф':<10} | {'Δ_MC,%':<8} | {'Прямой':<10} | {'Δ_Прям,%':<9} | {'Преобл. метод':<14} | {'Время, с':<8}")
            print("-" * 104)

        records = []
        for name in scale_names:
            try:
                rec = self.run_structure(name)
                records.append(rec)
                if verbose:
                    err_mc = f"{rec['error_mc_mod_pct']:5.2f}%" if rec['error_mc_mod_pct'] is not None else "N/A"
                    err_dm = f"{rec['error_direct_pct']:5.2f}%" if rec['error_direct_pct'] is not None else "N/A"
                    print(
                        f"k = {rec['scale_factor']:<6.2f} | "
                        f"{rec['shape']:<14} | "
                        f"{rec['porosity']:<10.4f} | "
                        f"{rec['ssa_mc_modified']:<10.2f} | "
                        f"{err_mc:<8} | "
                        f"{rec['ssa_direct_method']:<10.2f} | "
                        f"{err_dm:<9} | "
                        f"{rec['best_method']:<14} | "
                        f"{rec['time_sec']:<8.2f}"
                    )
            except Exception as e:
                if verbose:
                    print(f"Ошибка при обработке {name}: {e}")

        df = pd.DataFrame(records)

        if verbose and not df.empty:
            print("-" * 104)
            print(f"Средняя погрешность в серии: MC (модиф) = {df['error_mc_mod_pct'].mean():.2f}%, Прямой = {df['error_direct_pct'].mean():.2f}%\n")

        if save_plot and not df.empty:
            FIGURES_DIR.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
            ax.plot(df['scale_factor'], df['error_mc_mod_pct'], 'b-o', lw=2, label='Marching Cubes (модиф.)')
            ax.plot(df['scale_factor'], df['error_direct_pct'], 'r-s', lw=2, label='Прямой воксельный метод')
            if 'error_mc_clas_pct' in df.columns:
                ax.plot(df['scale_factor'], df['error_mc_clas_pct'], 'g--^', lw=1.5, alpha=0.7, label='Marching Cubes (классич.)')
            ax.set_xlabel('Коэффициент масштабирования сетки k', fontsize=11)
            ax.set_ylabel('Погрешность относительно БЭТ Δ, %', fontsize=11)
            ax.set_title(f'Сеточная сходимость и погрешность SSA для {base_name}', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='best')
            plt.tight_layout()
            plot_path = FIGURES_DIR / f"Figure_scale_series_{base_name}.png"
            fig.savefig(plot_path, dpi=170)
            plt.close(fig)

        return df

    def run_all(self, verbose: bool = True) -> pd.DataFrame:
        """
        Выполняет пакетный расчет для базовых 7 структур.
        """
        if verbose:
            print("\n" + "=" * 94)
            print(f"{'Структура':<13} | {'БЭТ (м²/г)':<10} | {'MC Модиф':<10} | {'Δ_MC,%':<7} | {'Прямой':<10} | {'Δ_Прям,%':<8} | {'Время, с':<8}")
            print("=" * 94)

        records = []
        for name in self.structures:
            rec = self.run_structure(name)
            records.append(rec)
            if verbose:
                err_mc = f"{rec['error_mc_mod_pct']:5.1f}%" if rec['error_mc_mod_pct'] is not None else "N/A"
                err_dm = f"{rec['error_direct_pct']:5.1f}%" if rec['error_direct_pct'] is not None else "N/A"
                print(
                    f"{rec['structure']:<13} | "
                    f"{rec['nominal_bet']:<10.1f} | "
                    f"{rec['ssa_mc_modified']:<10.2f} | "
                    f"{err_mc:<7} | "
                    f"{rec['ssa_direct_method']:<10.2f} | "
                    f"{err_dm:<8} | "
                    f"{rec['time_sec']:<8.2f}"
                )

        df = pd.DataFrame(records)

        if verbose:
            print("-" * 94)
            mean_mc_err = df['error_mc_mod_pct'].mean()
            mean_dm_err = df['error_direct_pct'].mean()
            total_t = df['time_sec'].sum()
            print(f"Средняя погрешность: MC модиф = {mean_mc_err:.2f}%, Прямой = {mean_dm_err:.2f}% | Суммарное время: {total_t:.2f} с\n")

        return df

    def save_results(self, df: pd.DataFrame, output_dir: Optional[Union[str, Path]] = None, filename: str = "ssa_pipeline_results") -> Path:
        """
        Сохраняет итоговый DataFrame в CSV и pickle.
        """
        out_dir = Path(output_dir) if output_dir else self.cache_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = out_dir / f"{filename}.csv"
        pkl_path = out_dir / f"{filename}.pickle"

        df.to_csv(csv_path, index=False)
        df.to_pickle(pkl_path)
        return csv_path
