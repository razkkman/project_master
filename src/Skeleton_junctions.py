"""
Расчет плотности тройных соединений ветвей скелетона (W_3p = n_3p / V_solid).
Фасадный интерфейс, делегирующий расчет классу SkeletonAnalyzer.
"""

from typing import Dict
from topology.skeleton_analyzer import SkeletonAnalyzer


def compute_triple_points_density(skeletons_dir=None) -> Dict[str, float]:
    """
    Вычисляет нормированную плотность тройных узлов W_3p = n_3p / V_solid.
    """
    if skeletons_dir is not None:
        analyzer = SkeletonAnalyzer(skeletons_dir=skeletons_dir)
    else:
        analyzer = SkeletonAnalyzer()

    return analyzer.calculate_all_triple_points_density()


if __name__ == "__main__":
    print("=== Расчет плотности тройных соединений W_3p ===")
    res = compute_triple_points_density()
    for name, val in res.items():
        print(f"[{name}] W_3p = {val:.4e} м^-3")
