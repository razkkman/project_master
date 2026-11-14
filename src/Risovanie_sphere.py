"""
Генерация и послойное сохранение стека изображений сферы.
Использует Pillow и SyntheticSphere.
"""

from pathlib import Path
import numpy as np
from PIL import Image

from config import DATA_DIR
from synthetic.shapes import SyntheticSphere


def export_sphere_stack(diameter: int = 10, output_dir: Path = None):
    """Генерирует сферу и сохраняет стек изображений TIFF."""
    if output_dir is None:
        output_dir = DATA_DIR / "synthetic" / f"Sphere_{diameter}"

    output_dir.mkdir(parents=True, exist_ok=True)
    sphere = SyntheticSphere(diameter_voxels=diameter)
    arr = sphere.generate()

    # Инвертирование для формата TIFF: 0 - твердая фаза (черный), 255 - фон (белый)
    stack = np.where(arr == 1, 0, 255).astype(np.uint8)

    for i in range(stack.shape[0]):
        img = Image.fromarray(stack[i, :, :])
        img.save(output_dir / f"slice_{i:04d}.tif")

    print(f"Сфера диаметра {diameter} сохранена в {output_dir} (срезов: {stack.shape[0]})")


if __name__ == "__main__":
    export_sphere_stack(10)
