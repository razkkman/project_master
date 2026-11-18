"""
Сравнительный бенчмарк версий Marching Cubes и методов расчета SSA.
Сопоставляет:
  1. Физический эксперимент БЭТ (номинал)
  2. Прямой воксельный метод (Direct Method)
  3. Авторский Marching Cubes классический (без межъячеечных коррекций)
  4. Авторский Marching Cubes модифицированный (с граничными коррекциями от 20.04.2021)
  5. Enhanced MC v1 (со скалярной калибровкой сферы)
  6. Enhanced MC v2 (с локально-адаптивной тензорной кривизной и Numba)
  7. Enhanced MC v3 (с физическим зондом адсорбата азота Rolling Ball SASA)
  8. Enhanced MC v4 (Золотой дуэт White Box: Мандельброт-Пфайфер + микропористость)
  9. Hybrid Mesh-ML Corrector (MC + физико-нейросетевой остаточный корректор)

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
    mc_enh_v1 = EnhancedMarchingCubesCalculator(mode="scalar_v1")
    mc_enh_v2 = EnhancedMarchingCubesCalculator(mode="tensor_v2")
    mc_enh_v3 = EnhancedMarchingCubesCalculator(mode="sasa_v3")
    mc_enh_v4 = EnhancedMarchingCubesCalculator(mode="fractal_v4")
    mc_hybrid = EnhancedMarchingCubesCalculator(mode="hybrid_ml")

    print("=" * 145)
    print("  ПОЛНЫЙ СРАВНИТЕЛЬНЫЙ БЕНЧМАРК ЭВОЛЮЦИИ MARCHING CUBES В СРАВНЕНИИ С ЭКСПЕРИМЕНТОМ БЭТ")
    print("=" * 145)
    print(f"{'Структура':<12} | {'БЭТ':<6} | {'MC Автор':<12} | {'MC Enh v2':<12} | {'MC Enh v3':<12} | {'MC Enh v4 (WB)':<14} | {'Hybrid ML':<12} | {'Выигрыш v4':<10}")
    print(f"{'':<12} | {'м²/г':<6} | {'SSA (Δ_BET)':<12} | {'SSA (Δ_BET)':<12} | {'SASA (Δ_BET)':<12} | {'SSA (Δ_BET)':<14} | {'SSA (Δ_BET)':<12} | {'к Автору':<10}")
    print("-" * 145)

    records = []

    for name in STRUCTURES_ALL:
        bet = SSA_FIS_NOMINAL.get(name, 0.0)
        struct = PorousStructure.load(name)

        # 1. Direct Method
        res_dm = dm.calculate(struct)
        err_dm = abs(res_dm.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 2. MC Classical
        res_clas = mc_clas.calculate(struct)
        err_clas = abs(res_clas.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 3. MC Author Modified
        res_auth = mc_auth.calculate(struct)
        err_auth = abs(res_auth.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 4. Enhanced MC v1
        res_v1 = mc_enh_v1.calculate(struct)
        err_v1 = abs(res_v1.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 5. Enhanced MC v2 (Tensor)
        res_v2 = mc_enh_v2.calculate(struct)
        err_v2 = abs(res_v2.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 6. Enhanced MC v3 (SASA)
        res_v3 = mc_enh_v3.calculate(struct)
        err_v3 = abs(res_v3.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 7. Enhanced MC v4 (Fractal-Pfeifer White Box)
        res_v4 = mc_enh_v4.calculate(struct)
        err_v4 = abs(res_v4.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        # 8. Hybrid Mesh-ML
        res_ml = mc_hybrid.calculate(struct)
        err_ml = abs(res_ml.ssa_m2_g - bet) / bet * 100 if bet > 0 else 0

        gain_v4 = err_auth - err_v4

        print(
            f"{name:<12} | "
            f"{bet:<6.1f} | "
            f"{res_auth.ssa_m2_g:5.1f} ({err_auth:4.1f}%) | "
            f"{res_v2.ssa_m2_g:5.1f} ({err_v2:4.1f}%) | "
            f"{res_v3.ssa_m2_g:5.1f} ({err_v3:4.1f}%) | "
            f"{res_v4.ssa_m2_g:5.1f} ({err_v4:4.1f}%) | "
            f"{res_ml.ssa_m2_g:5.1f} ({err_ml:4.2f}%) | "
            f"{gain_v4:+6.1f}%"
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
            "ssa_mc_v1": res_v1.ssa_m2_g,
            "err_mc_v1_pct": err_v1,
            "ssa_mc_v2": res_v2.ssa_m2_g,
            "err_mc_v2_pct": err_v2,
            "ssa_mc_v3": res_v3.ssa_m2_g,
            "err_mc_v3_pct": err_v3,
            "ssa_mc_v4": res_v4.ssa_m2_g,
            "err_mc_v4_pct": err_v4,
            "ssa_hybrid_ml": res_ml.ssa_m2_g,
            "err_hybrid_ml_pct": err_ml,
            "gain_v4_pct": gain_v4,
        })

    df = pd.DataFrame(records)

    print("-" * 145)
    mean_err_clas = df["err_mc_clas_pct"].mean()
    mean_err_auth = df["err_mc_author_pct"].mean()
    mean_err_v1 = df["err_mc_v1_pct"].mean()
    mean_err_v2 = df["err_mc_v2_pct"].mean()
    mean_err_v3 = df["err_mc_v3_pct"].mean()
    mean_err_v4 = df["err_mc_v4_pct"].mean()
    mean_err_ml = df["err_hybrid_ml_pct"].mean()

    print(
        f"{'СРЕДНЯЯ ПОГРЕШНОСТЬ Δ_BET:':<25} | "
        f"MC Классика: {mean_err_clas:.1f}% | "
        f"MC Автор: {mean_err_auth:.1f}% | "
        f"MC Enh v2 (Tensor): {mean_err_v2:.1f}% | "
        f"MC Enh v3 (SASA): {mean_err_v3:.1f}% | "
        f"MC Enh v4 (White Box): {mean_err_v4:.2f}% | "
        f"Hybrid Mesh-ML: {mean_err_ml:.2f}%\n"
    )

    if save_plot:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 6), dpi=150)

        # График 1: Сравнение расчетных SSA с экспериментом БЭТ
        x = np.arange(len(df))
        w = 0.13
        ax1.bar(x - 2.5 * w, df["bet_exp"], width=w, label="БЭТ (эксперимент)", color="#2ca02c", alpha=0.95)
        ax1.bar(x - 1.5 * w, df["ssa_mc_author"], width=w, label="MC Авторский", color="#1f77b4", alpha=0.8)
        ax1.bar(x - 0.5 * w, df["ssa_mc_v2"], width=w, label="MC Enh v2 (Tensor)", color="#9467bd", alpha=0.85)
        ax1.bar(x + 0.5 * w, df["ssa_mc_v3"], width=w, label="MC Enh v3 (SASA зонд)", color="#ff7f0e", alpha=0.85)
        ax1.bar(x + 1.5 * w, df["ssa_mc_v4"], width=w, label=f"MC Enh v4 White Box ({mean_err_v4:.1f}%)", color="#008080", alpha=0.95)
        ax1.bar(x + 2.5 * w, df["ssa_hybrid_ml"], width=w, label=f"Hybrid Mesh-ML ({mean_err_ml:.1f}%)", color="#d62728", alpha=0.90)

        ax1.set_xticks(x)
        ax1.set_xticklabels(df["structure"], rotation=30, ha="right", fontsize=9)
        ax1.set_ylabel("Удельная площадь поверхности SSA, м²/г", fontsize=10)
        ax1.set_title("Сходимость SSA методов к физическому эксперименту БЭТ", fontsize=11, fontweight="bold")
        ax1.legend(fontsize=8)
        ax1.grid(True, linestyle="--", alpha=0.5, axis="y")

        # График 2: Эволюция погрешности к БЭТ (%)
        ax2.bar(x - 2.5 * w, df["err_mc_clas_pct"], width=w, label=f"MC Классика ({mean_err_clas:.1f}%)", color="#7f7f7f", alpha=0.5)
        ax2.bar(x - 1.5 * w, df["err_mc_author_pct"], width=w, label=f"MC Автор ({mean_err_auth:.1f}%)", color="#1f77b4", alpha=0.8)
        ax2.bar(x - 0.5 * w, df["err_mc_v2_pct"], width=w, label=f"MC Enh v2 Tensor ({mean_err_v2:.1f}%)", color="#9467bd", alpha=0.85)
        ax2.bar(x + 0.5 * w, df["err_mc_v3_pct"], width=w, label=f"MC Enh v3 SASA ({mean_err_v3:.1f}%)", color="#ff7f0e", alpha=0.85)
        ax2.bar(x + 1.5 * w, df["err_mc_v4_pct"], width=w, label=f"MC Enh v4 White Box ({mean_err_v4:.2f}%)", color="#008080", alpha=0.95)
        ax2.bar(x + 2.5 * w, df["err_hybrid_ml_pct"], width=w, label=f"Hybrid Mesh-ML ({mean_err_ml:.2f}%)", color="#2ca02c", alpha=0.95)

        ax2.set_xticks(x)
        ax2.set_xticklabels(df["structure"], rotation=30, ha="right", fontsize=9)
        ax2.set_ylabel("Относительная погрешность к БЭТ (Δ_BET), %", fontsize=10)
        ax2.set_title("Эволюция снижения погрешности модификаций MC", fontsize=11, fontweight="bold")
        ax2.legend(fontsize=8)
        ax2.grid(True, linestyle="--", alpha=0.5, axis="y")

        plt.tight_layout()
        plot_path = FIGURES_DIR / "Figure_MC_comparison_versions.png"
        fig.savefig(plot_path)
        plt.close(fig)
        print(f" График сравнения успешно обновлен и сохранен в:")
        print(f" {plot_path}\n")

    return df


if __name__ == "__main__":
    run_comprehensive_comparison(save_plot=True)


if __name__ == "__main__":
    run_comprehensive_comparison(save_plot=True)
