"""
Определение оптимального порога бинаризации для соответствия номинальной пористости.
Фасадный интерфейс, делегирующий расчет классу ThresholdFinder.
"""

from typing import Optional
from config import STRUCTURES_DIR
from preprocessing.threshold import ThresholdFinder


def Opred_poroga(name: str, k_resize: float, structures_dir=STRUCTURES_DIR) -> int:
    """
    Находит порог яркости, минимизирующий отклонение
    расчетной пористости от номинальной пористости образца.
    """
    finder = ThresholdFinder(structures_dir=structures_dir)
    return finder.find_threshold_for_structure(name, k_resize=k_resize)


if __name__ == "__main__":
    val = Opred_poroga("Si12", 1.0)
    print(f"Оптимальный порог для Si12 (k=1.0): {val}")
