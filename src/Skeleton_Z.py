"""
Расчет среднего координационного числа ветвления (Z).
Фасадный интерфейс, делегирующий расчет классу SkeletonAnalyzer.
"""

from typing import Dict
from topology.skeleton_analyzer import SkeletonAnalyzer


def compute_z_all(skeletons_dir=None) -> Dict[str, float]:
    """
    Вычисляет среднее координационное число Z для всех структур.
    """
    if skeletons_dir is not None:
        analyzer = SkeletonAnalyzer(skeletons_dir=skeletons_dir)
    else:
        analyzer = SkeletonAnalyzer()

    return analyzer.calculate_all_coordination()


if __name__ == "__main__":
    print("=== Расчет координационного числа Z ===")
    res = compute_z_all()
    for name, val in res.items():
        print(f"[{name}] Z = {val:.6f}")
