"""
Ремасштабирование стеков микрофотографий пористых сред.
Фасадный интерфейс, делегирующий выполнение классу VolumeRescaler.
"""

from typing import Optional, Sequence
import numpy as np
from config import STRUCTURES_DIR, STRUCTURES_ALL
from preprocessing.rescale import VolumeRescaler


def rescale_all_structures(k_values: Optional[Sequence[float]] = None, structures_dir=STRUCTURES_DIR):
    """
    Масштабирует структуры с заданными коэффициентами сжатия k (по умолчанию 0.7 .. 0.95).
    """
    if k_values is None:
        k_values = np.around(np.arange(0.7, 1.0, 0.05), decimals=2)

    rescaler = VolumeRescaler(structures_dir=structures_dir)
    for name in STRUCTURES_ALL:
        try:
            print(f"Ремасштабирование структуры {name}...")
            rescaler.batch_rescale_structure(name, scale_factors=k_values)
        except Exception as e:
            print(f"Ошибка при масштабировании {name}: {e}")


if __name__ == "__main__":
    print("Запуск ремасштабирования...")
    # Пример вызова для проверки
