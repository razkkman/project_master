"""
Расчет фактической объемной доли пористости (доли пустот) для всех исследуемых структур.
Фасадный интерфейс, использующий класс PorousStructure.
"""

from typing import Dict
from pathlib import Path
import pickle
from config import STRUCTURES_ALL, PROCESSED_DIR
from core.structure import PorousStructure


def compute_porosity_proportions(save_results: bool = True) -> Dict[str, float]:
    """
    Вычисляет долю пористости phi = 1 - N_solid / N_total для всех структур.
    """
    porosity_dict = {}
    print("=== РАСЧЕТ ДОЛИ ПОРИСТОСТИ СТРУКТУР ===")

    for name in STRUCTURES_ALL:
        struct = PorousStructure.load(name)
        phi = struct.porosity
        porosity_dict[name] = phi
        print(f"[{name:<14}] Пористость: {phi:.4f} (Всего: {struct.total_voxels}, Твердая фаза: {struct.solid_voxels})")

    if save_results:
        out_file = PROCESSED_DIR / "proportion_of_porosity_nominal.pickle"
        with open(out_file, "wb") as f:
            pickle.dump(porosity_dict, f)
        print(f"Результаты сохранены в {out_file}")

    return porosity_dict


if __name__ == "__main__":
    compute_porosity_proportions()
