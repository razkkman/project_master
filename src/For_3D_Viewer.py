"""
Подготовка усеченной области 3D структуры для трехмерной визуализации (3D Viewer).
Фасадный интерфейс, использующий методы класса PorousStructure.
"""

from pathlib import Path
from typing import Optional
import numpy as np

from config import STRUCTURES_DIR
from core.structure import PorousStructure


def prepare_subvolume_for_viewer(name: str = 'Coreshell9', output_dir: Optional[str] = None):
    """
    Вырезает октант структуры и сохраняет стеком TIFF для 3D-просмотра в ImageJ / 3D Viewer.
    """
    struct = PorousStructure.load(name)
    hz, hy, hx = struct.shape[0] // 2, struct.shape[1] // 2, struct.shape[2] // 2
    sub = struct.extract_subvolume(origin=(hz, hy, hx), size=(hz, hy, hx), sub_name=f"{name}_octant")

    out_path = Path(output_dir) if output_dir else STRUCTURES_DIR / f"{name}-3D_Viewer"
    count = sub.export_slices(output_dir=out_path, prefix="IMG", file_format="tif")
    print(f"Октант сохранен в {out_path} (форма: {sub.shape}, срезов: {count})")
    return sub.voxels


if __name__ == "__main__":
    prepare_subvolume_for_viewer('Coreshell9')
