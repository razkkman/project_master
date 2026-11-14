"""
Вспомогательная функция усреднения значений в словаре по списку ключей.
"""

from typing import List, Dict, Any


def average_value(mass: List[Any], z_dict: Dict[Any, float]) -> Dict[Any, float]:
    """
    Усредняет значения z_dict для ключей из списка mass
    и присваивает среднее значение всем этим ключам.
    """
    if not mass:
        return z_dict

    total = sum(z_dict[k] for k in mass if k in z_dict)
    avg = total / len(mass)

    for k in mass:
        if k in z_dict:
            z_dict[k] = avg

    return z_dict
