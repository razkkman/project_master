"""
Комплексный бенчмарк 6 передовых мировых методов расчета SSA на 7 пористых структурах.
Сопоставляет:
  1. Эксперимент БЭТ (номинал)
  2. Авторский Marching Cubes (2021)
  3. Enhanced MC v4 (Золотой дуэт White Box)
  4. Method 1: Crofton 13-Directions (Интегральная геометрия Коши-Крофтона)
  5. Method 2: QSDFT-Coupled Surface Model (Термодинамическая модель шероховатости)
  6. Method 3: Sub-Voxel Dual Porosity (Непрерывный градиент ТВ + корона микропор)
  7. Method 4: Dual Contouring Hermite QEF (Двойственное контурирование)
  8. Method 5: In-Silico GCMC Adsorption Simulation (Молекулярная адсорбция азота)
  9. Method 6: 3D Super-Resolution Roughness (Генеративная субсеточная наношероховатость)
"""

import sys
from pathlib import Path
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import STRUCTURES_ALL, SSA_FIS_NOMINAL, FIGURES_DIR
from core.structure import PorousStructure
from experimental_mc.enhanced_marching_cubes import EnhancedMarchingCubesCalculator
from experimental_mc.advanced_methods import (
    Crofton13Calculator,
    QSDFTSurfaceCalculator,
    SubVoxelDualPorosityCalculator,
    DualContouringCalculator,
    InSilicoGCMCCalculator,
    SuperResolutionRoughnessCalculator,
)


def run_advanced_benchmark(save_plot: bool = True) -> pd.DataFrame:
    """
    Запускает сравнительный анализ всех 6 передовых методов на 7 пористых структурах.
    """
    mc_auth = EnhancedMarchingCubesCalculator(mode="author")
    mc_v4 = EnhancedMarchingCubesCalculator(mode="fractal_v4")

    methods = [
        ("MC Автор (2021)", mc_auth),
        ("Enhanced MC v4", mc_v4),
        ("Crofton 13-Dir", Crofton13Calculator()),
        ("QSDFT-Coupled", QSDFTSurfaceCalculator()),
        ("Sub-Voxel DualPor", SubVoxelDualPorosityCalculator()),
        ("Dual Contouring", DualContouringCalculator()),
        ("In-Silico GCMC", InSilicoGCMCCalculator()),
        ("3D Super-Res", SuperResolutionRoughnessCalculator()),
    ]

    print("=" * 155)
    print("  СРАВНИТЕЛЬНЫЙ БЕНЧМАРК 6 ПЕРЕДОВЫХ МИРОВЫХ МЕТОДОВ РАСЧЕТА SSA (К ЭКСПЕРИМЕНТУ БЭТ)")
    print("=" * 155)
    header = f"{'Структура':<12} | {'БЭТ':<6} | " + " | ".join([f"{m_name:<14}" for m_name, _ in methods])
    print(header)
    print("-" * 155)

    records = []
    times = {m_name: [] for m_name, _ in methods}

    for name in STRUCTURES_ALL:
        bet = SSA_FIS_NOMINAL.get(name, 0.0)
        struct = PorousStructure.load(name)

        row_str = f"{name:<12} | {bet:<6.1f} | "
        rec = {"structure": name, "bet_exp": bet}

        for m_name, calc in methods:
            t0 = time.time()
            res = calc.calculate(struct)
            dt = time.time() - t0
            times[m_name].append(dt)

            err = abs(res.ssa_m2_g - bet) / bet * 100.0 if bet > 0 else 0.0
            row_str += f"{res.ssa_m2_g:5.1f} ({err:4.1f}%) | "
            rec[f"ssa_{m_name}"] = res.ssa_m2_g
            rec[f"err_{m_name}"] = err

        print(row_str)
        records.append(rec)

    df = pd.DataFrame(records)

    print("-" * 155)
    mean_row = f"{'СРЕДНЯЯ Δ_BET:':<12} | {'—':<6} | "
    for m_name, _ in methods:
        mean_err = df[f"err_{m_name}"].mean()
        mean_row += f"{mean_err:5.2f}%         | "
    print(mean_row)

    time_row = f"{'СРЕДНЕЕ ВРЕМЯ:':<12} | {'—':<6} | "
    for m_name, _ in methods:
        mean_t = np.mean(times[m_name])
        time_row += f"{mean_t:5.3f} с        | "
    print(time_row)
    print("=" * 155 + "\n")

    if save_plot:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.5), dpi=150)

        x = np.arange(len(df))
        n_m = len(methods)
        width = 0.85 / (n_m + 1)

        # График 1: Значения SSA
        ax1.bar(x - (n_m / 2) * width, df["bet_exp"], width=width, label="БЭТ (эксперимент)", color="#1b9e77", alpha=0.95)
        colors = ["#7570b3", "#d95f02", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666", "#1f78b4"]
        for idx, (m_name, _) in enumerate(methods):
            offset = x - (n_m / 2 - 1 - idx) * width
            ax1.bar(offset, df[f"ssa_{m_name}"], width=width, label=m_name, color=colors[idx % len(colors)], alpha=0.85)

        ax1.set_xticks(x)
        ax1.set_xticklabels(df["structure"], rotation=30, ha="right", fontsize=9)
        ax1.set_ylabel("Удельная площадь поверхности SSA, м²/г", fontsize=10)
        ax1.set_title("Сравнение расчетных SSA передовых методов с экспериментом БЭТ", fontsize=11, fontweight="bold")
        ax1.legend(fontsize=8, loc="upper left")
        ax1.grid(True, linestyle="--", alpha=0.5, axis="y")

        # График 2: Средние погрешности методов
        method_names = [m_name for m_name, _ in methods]
        mean_errors = [df[f"err_{m_name}"].mean() for m_name, _ in methods]

        bars = ax2.bar(range(len(method_names)), mean_errors, color=colors, alpha=0.85)
        ax2.set_xticks(range(len(method_names)))
        ax2.set_xticklabels(method_names, rotation=35, ha="right", fontsize=9)
        ax2.set_ylabel("Средняя погрешность к БЭТ (Δ_BET), %", fontsize=10)
        ax2.set_title("Средняя погрешность методов относительно БЭТ (%)", fontsize=11, fontweight="bold")
        ax2.grid(True, linestyle="--", alpha=0.5, axis="y")

        for bar, val in zip(bars, mean_errors):
            ax2.text(bar.get_x() + bar.get_width()/2, val + 0.4, f"{val:.2f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

        plt.tight_layout()
        out_path = FIGURES_DIR / "Figure_Advanced_Methods_Comparison.png"
        fig.savefig(out_path)
        plt.close(fig)
        print(f" График сравнительного бенчмарка сохранен в:\n {out_path}\n")

    return df


if __name__ == "__main__":
    run_advanced_benchmark(save_plot=True)
