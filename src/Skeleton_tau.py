"""
Расчет средней геометрической кривизны (тортуозности) ветвей скелетона.
Фасадный интерфейс, делегирующий расчет классу SkeletonAnalyzer.
"""

from typing import Dict
from topology.skeleton_analyzer import SkeletonAnalyzer


def compute_tau_all(skeletons_dir=None, min_branches: int = 500) -> Dict[str, float]:
    """
    Вычисляет среднюю геометрическую кривизну ветвей скелетона для всех структур.
    """
    if skeletons_dir is not None:
        analyzer = SkeletonAnalyzer(skeletons_dir=skeletons_dir)
    else:
        analyzer = SkeletonAnalyzer()

    return analyzer.calculate_all_tortuosity(min_branches=min_branches)


if __name__ == "__main__":
    print("=== Расчет геометрической извилистости (тортуозности) tau ===")
    res = compute_tau_all()
    for name, val in res.items():
        print(f"[{name}] tau = {val:.6f}")
