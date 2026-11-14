"""
Модуль формирования 3D массива из стека 2D изображений TIFF.
Фасадный интерфейс для сохранения 100% обратной совместимости,
делегирующий загрузку доменному классу PorousStructure.
"""

from pathlib import Path
from typing import Optional
import numpy as np

from config import STRUCTURES_DIR, PROCESSED_DIR
from core.structure import PorousStructure


def FormirMass_v1(name: str, path: Optional[str] = None, folder: Optional[str] = None) -> np.ndarray:
    """
    Загружает стек 2D срезов в 3D массив NumPy (значения 0 и 1).
    Фасадная функция для совместимости с оригинальными скриптами.
    """
    # Если передан нестандартный путь
    if path is not None:
        target_dir = Path(path)
        if folder is not None:
            target_dir = target_dir / folder / name
        else:
            target_dir = target_dir / name
        structure = PorousStructure.from_images(target_dir, name=name)
        return structure.voxels

    # Стандартный путь через PorousStructure.load с автокэшированием
    structure = PorousStructure.load(name, structures_dir=STRUCTURES_DIR, cache_dir=PROCESSED_DIR)
    return structure.voxels


if __name__ == "__main__":
    import time
    print("Тестирование быстрой загрузки массива...")
    t0 = time.time()
    arr = FormirMass_v1("Si12")
    dt = time.time() - t0
    print(f"Структура Si12 загружена: форма {arr.shape}, единиц: {np.count_nonzero(arr)}, время: {dt:.2f} с")
