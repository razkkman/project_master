"""
Вспомогательный скрипт масштабирования отдельного среза структуры.
Использует Pillow вместо устаревшего skimage.
"""

from pathlib import Path
import numpy as np
from PIL import Image

from config import STRUCTURES_DIR


def preview_rescaled_slice(name: str = "SBA15", k_resize: float = 0.7):
    """Масштабирует первый срез структуры и возвращает массив."""
    folder = STRUCTURES_DIR / name
    if not folder.exists():
        print(f"Каталог не найден: {folder}")
        return None

    files = sorted([f for f in folder.iterdir() if f.suffix.lower() in ('.tif', '.tiff', '.png')])
    if not files:
        print(f"Нет файлов изображений в: {folder}")
        return None

    with Image.open(files[0]) as img:
        orig = img.convert('L')
        new_w = max(1, int(round(orig.width * k_resize)))
        new_h = max(1, int(round(orig.height * k_resize)))
        rescaled = orig.resize((new_w, new_h), Image.Resampling.BICUBIC)
        print(f"Срез масштабирован с {orig.size} до {rescaled.size} (k={k_resize})")
        return np.array(rescaled)


if __name__ == "__main__":
    preview_rescaled_slice()
