"""
Пакетный расчет удельной площади поверхности (SSA) для всех 7 исследуемых мезопористых структур
методами Marching Cubes и Direct Method.
Фасадный интерфейс, делегирующий расчет классу SSAEvaluationPipeline.
"""

from typing import Dict, Tuple
from pipeline.ssa_pipeline import SSAEvaluationPipeline


def calculate_all_ssa(save_results: bool = True) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Выполняет быстрый расчет SSA пористых сред обоими методами
    и формирует аналитическую сводку погрешностей.
    """
    pipeline = SSAEvaluationPipeline()
    df = pipeline.run_all(verbose=True)

    if save_results:
        pipeline.save_results(df)

    mc_dict = dict(zip(df["structure"], df["ssa_mc_modified"]))
    pm_dict = dict(zip(df["structure"], df["ssa_direct_method"]))
    return mc_dict, pm_dict


if __name__ == "__main__":
    calculate_all_ssa()
