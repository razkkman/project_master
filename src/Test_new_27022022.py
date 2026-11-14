"""
Скрипт расчета пористости структур (модернизирован с использованием PorousStructure).
"""

from config import STRUCTURES_ALL
from core.structure import PorousStructure


def calculate_sample_porosities(names=None):
    """Вычисляет пористость для списка образцов."""
    names = names or ['SBA15', 'KIT6', 'Si12']
    results = {}
    for name in names:
        try:
            struct = PorousStructure.load(name)
            phi = struct.porosity
            results[name] = phi
            print(f"[{name}] Пористость: {phi:.4f}")
        except Exception as e:
            print(f"[{name}] Ошибка: {e}")
    return results


if __name__ == "__main__":
    calculate_sample_porosities()
