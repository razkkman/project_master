"""
Сравнительный бенчмарк версий Marching Cubes и методов расчета SSA.
Сопоставляет:
  1. Физический эксперимент БЭТ (номинал)
  2. Прямой воксельный метод (Direct Method)
  3. Авторский Marching Cubes классический (без межъячеечных коррекций)
  4. Авторский Marching Cubes модифицированный (с граничными коррекциями от 20.04.2021)
  5. Экспериментальный Enhanced Marching Cubes (с физико-геометрической калибровкой)

Вычисляет относительные погрешности относительно эксперимента БЭТ:
  Delta_BET = |SSA_calc - SSA_BET| / SSA_BET * 100%
и строит сравнительные графики сходимости.
"""

import sys
from pathlib import Path
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Добавление src в sys.path при изолированном запуске
SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import STRUCTURES_ALL, SSA_FIS_NOMINAL, FIGURES_DIR
from core.structure import PorousStructure
from methods.direct_method import DirectMethodCalculator
from methods.marching_cubes import MarchingCubesCalculator
from experimental_mc.enhanced_marching_cubes import EnhancedMarchingCubesCalculator


def run_comprehensive_comparison(save_plot: bool = True) -> pd.DataFrame:
    """
    Запускает сравнительный анализ всех методов на 7 пористых структурах.
    """
    dm = DirectMethodCalculator()
    mc_clas = MarchingCubesCalculator(with_correction=False)
    mc_auth = MarchingCubesCalculator(with_correction=True)
    mc_enh = EnhancedMarchingCubesCalculator(curvature_correction=True, adaptive_roughness=True)

    print("=" * 115)
    print("  СРАВНИТЕЛЬНЫЙ АНАЛИЗ ТОЧНОСТИ РАСЧЕТА SSA В СРАВНЕНИИ С ФИЗИЧЕСКИМ ЭКСПЕРИМЕНТОМ (БЭТ)")
    print("=" * 115)
    print(f"{'Структура':<12} | {'БЭТ (эксп)':<10} | {'Прямой метод':<13} | {'MC Классика':<13} | {'MC Автор':<13} | {'MC Enhanced':<13} | {'Выигрыш, %':<10}")
    print(f"{'':<12} | {'м²/г':<10} | {'SSA (Δ_BET)':<13} | {'SSA (Δ_BET)':<13} | {'SSA (Δ_BET)':<13} | {'SSA (Δ_BET)':<13} | {'MC_enh vs MC':<10}")
    print("-" * 115)

    records = []

    for name in STRUCTURES_ALL:
        bet = SSA_FIS_NOMINAL.get(name, 0.0)
        struct = PorousStructure.load(name)

        # 1. Direct Method
        res_dm = dm.calculate(struct)
        err_dm = abs(res_dm.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 2. Author MC Classical
        res_clas = mc_clas.calculate(struct)
        err_clas = abs(res_clas.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 3. Author MC Modified
        res_auth = mc_auth.calculate(struct)
        err_auth = abs(res_auth.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 4. Enhanced MC
        res_enh = mc_enh.calculate(struct)
        err_enh = abs(res_enh.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # Выигрыш по точности (уменьшение ошибки)
        accuracy_gain = err_auth - err_enh

        print(
            f"{name:<12} | "
            f"{bet:<10.1f} | "
            f"{res_dm.ssa_m2_g:6.1f} ({err_dm:4.1f}%) | "
            f"{res_clas.ssa_m2_g:6.1f} ({err_clas:4.1f}%) | "
            f"{res_auth.ssa_m2_g:6.1f} ({err_auth:4.1f}%) | "
            f"{res_enh.ssa_m2_g:6.1f} ({err_enh:4.1f}%) | "
            f"{accuracy_gain:+6.1f}%"
        )

        records.append({
            "structure": name,
            "bet_exp": bet,
            "ssa_direct": res_dm.ssa_m2_g,
            "err_direct_pct": err_dm,
            "ssa_mc_classical": res_clas.ssa_m2_g,
            "err_mc_clas_pct": err_clas,
            "ssa_mc_author": res_auth.ssa_m2_g,
            "err_mc_author_pct": err_auth,
            "ssa_mc_enhanced": res_enh.ssa_m2_g,
            "err_mc_enhanced_pct": err_enh,
            "gain_pct": accuracy_gain,
        })

    df = pd.DataFrame(records)

    print("-" * 115)
    mean_err_dm = df["err_direct_pct"].mean()
    mean_err_clas = df["err_mc_clas_pct"].mean()
    mean_err_auth = df["err_mc_author_pct"].mean()
    mean_err_enh = df["err_mc_enhanced_pct"].mean()

    print(
        f"{'СРЕДНЯЯ ПОГРЕШНОСТЬ Δ_BET:':<25} | "
        f"Прямой: {mean_err_dm:.1f}% | "
        f"MC Классика: {mean_err_clas:.1f}% | "
        f"MC Автор: {mean_err_auth:.1f}% | "
        f"MC Enhanced: {mean_err_enh:.1f}%\n"
    )

    if save_plot:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)

        # График 1: Сравнение расчетных SSA с экспериментом БЭТ
        x = np.arange(len(df))
        w = 0.2
        ax1.bar(x - 1.5 * w, df["bet_exp"], width=w, label="БЭТ (эксперимент)", color="#2ca02c", alpha=0.9)
        ax1.bar(x - 0.5 * w, df["ssa_direct"], width=w, label="Прямой метод", color="#d62728", alpha=0.8)
        ax1.bar(x + 0.5 * w, df["ssa_mc_author"], width=w, label="MC (версия автора)", color="#1f77b4", alpha=0.8)
        ax1.bar(x + 1.5 * w, df["ssa_mc_enhanced"], width=w, label="MC Enhanced (модиф.)", color="#ff7f0e", alpha=0.9)

        ax1.set_xticks(x)
        ax1.set_xticklabels(df["structure"], rotation=30, ha="right", fontsize=9)
        ax1.set_ylabel("Удельная площадь поверхности SSA, м²/г", fontsize=10)
        ax1.set_title("Сопоставление SSA с экспериментом БЭТ", fontsize=11, fontweight="bold")
        ax1.legend(fontsize=9)
        ax1.grid(True, linestyle="--", alpha=0.5, axis="y")

        # График 2: Относительная погрешность относительно БЭТ (%)
        ax2.bar(x - w, df["err_direct_pct"], width=w, label="Прямой метод", color="#d62728", alpha=0.8)
        ax2.bar(x, df["err_mc_author_pct"], width=w, label="MC (версия автора)", color="#1f77b4", alpha=0.8)
        ax2.bar(x + w, df["err_mc_enhanced_pct"], width=w, label="MC Enhanced (модиф.)", color="#ff7f0e", alpha=0.9)

        ax2.set_xticks(x)
        ax2.set_xticklabels(df["structure"], rotation=30, ha="right", fontsize=9)
        ax2.set_ylabel("Погрешность относительно БЭТ, %", fontsize=10)
        ax2.set_title("Погрешность расчетных методов к БЭТ", fontsize=11, fontweight="bold")
        ax2.legend(fontsize=9)
        ax2.grid(True, linestyle="--", alpha=0.5, axis="y")

        plt.tight_layout()
        plot_path = FIGURES_DIR / "Figure_MC_comparison_versions.png"
        fig.savefig(plot_path)
        plt.close(fig)
        print(f" График сравнения успешно сохранен в:")
        print(f" {plot_path}\n")

    return df


if __name__ == "__main__":
    run_comprehensive_comparison(save_plot=True)
