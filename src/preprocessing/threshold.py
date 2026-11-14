"""
Модуль подбора порогов бинаризации микрофотографий пористых сред.
Инкапсулирован в класс ThresholdFinder.
"""

from pathlib import Path
from typing import Union, List, Optional
import numpy as np
from PIL import Image

from config import STRUCTURES_DIR, POROSITY_NOMINAL


class ThresholdFinder:
    """
    Класс для автоматического определения оптимального порога бинаризации,
    обеспечивающего соответствие экспериментальной пористости образца
    (или алгоритмом Оцу).

    Параметры:
        structures_dir: Путь к директории со структурами (data/structures)
    """

    def __init__(self, structures_dir: Union[str, Path] = STRUCTURES_DIR):
        self.structures_dir = Path(structures_dir)

    def find_threshold_by_porosity(
        self,
        grayscale_stack: np.ndarray,
        target_porosity: float,
        val_range: range = range(50, 205),
    ) -> int:
        """
        Находит значение порога (0..255), минимизирующее расхождение
        рассчитанной пористости объема с целевым значением target_porosity.
        """
        if grayscale_stack.size == 0:
            return 128

        total_pixels = grayscale_stack.size
        best_threshold = 128
        min_error = float("inf")

        for val in val_range:
            # Твердая фаза > val, пустоты (поры) <= val
            voids = np.count_nonzero(grayscale_stack <= val)
            calc_porosity = voids / total_pixels
            error = abs(calc_porosity - target_porosity)
            if error < min_error:
                min_error = error
                best_threshold = val

        return best_threshold

    def find_threshold_for_structure(
        self,
        name: str,
        k_resize: float = 1.0,
        val_range: range = range(50, 205),
    ) -> int:
        """
        Находит оптимальный порог для конкретной структуры из папки structures_dir.
        """
        target_dir = self.structures_dir / name
        if not target_dir.exists():
            return 128

        target_porosity = POROSITY_NOMINAL.get(name, 0.5)
        valid_exts = {'.tif', '.tiff', '.png', '.bmp'}
        files = sorted([f for f in target_dir.iterdir() if f.suffix.lower() in valid_exts and not f.name.startswith('.')])

        if not files:
            return 128

        rescaled_images = []
        for fpath in files:
            with Image.open(fpath) as img:
                orig = img.convert('L')
                if abs(k_resize - 1.0) > 1e-4:
                    new_w = max(1, int(round(orig.width * k_resize)))
                    new_h = max(1, int(round(orig.height * k_resize)))
                    rescaled = orig.resize((new_w, new_h), Image.Resampling.BICUBIC)
                    rescaled_images.append(np.array(rescaled))
                else:
                    rescaled_images.append(np.array(orig))

        stack = np.stack(rescaled_images, axis=0)
        return self.find_threshold_by_porosity(stack, target_porosity, val_range)

    @staticmethod
    def otsu_threshold(grayscale_image: np.ndarray) -> int:
        """
        Классический алгоритм Оцу (Otsu's thresholding) для автоматической бинаризации.
        """
        hist, bin_edges = np.histogram(grayscale_image.ravel(), bins=256, range=(0, 256))
        total = grayscale_image.size
        current_max, threshold = 0.0, 0
        weight_bg, weight_fg = 0, 0
        sum_bg, sum_fg = 0.0, 0.0
        sum_all = np.dot(np.arange(256), hist)

        for i in range(256):
            weight_bg += hist[i]
            if weight_bg == 0:
                continue
            weight_fg = total - weight_bg
            if weight_fg == 0:
                break

            sum_bg += i * hist[i]
            sum_fg = sum_all - sum_bg

            mean_bg = sum_bg / weight_bg
            mean_fg = sum_fg / weight_fg

            var_between = float(weight_bg) * float(weight_fg) * ((mean_bg - mean_fg) ** 2)

            if var_between > current_max:
                current_max = var_between
                threshold = i

        return int(threshold)
