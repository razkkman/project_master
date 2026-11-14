"""
Модуль изменения масштаба (rescaling) 3D-томографических объемов
для исследования влияния пространственного разрешения на удельную площадь поверхности.
"""

from pathlib import Path
from typing import Union, List, Optional, Sequence
import numpy as np
from PIL import Image

from config import STRUCTURES_DIR, STRUCTURES_ALL
from preprocessing.threshold import ThresholdFinder


class VolumeRescaler:
    """
    Класс для изменения масштаба (сжатия/растяжения) стеков микрофотографий.

    Параметры:
        structures_dir: Путь к директории с исходными структурами
    """

    def __init__(self, structures_dir: Union[str, Path] = STRUCTURES_DIR):
        self.structures_dir = Path(structures_dir)
        self.threshold_finder = ThresholdFinder(structures_dir)

    def rescale_and_binarize_stack(
        self,
        folder_path: Union[str, Path],
        scale_factor: float,
        threshold: Optional[int] = None,
        max_slices: Optional[int] = None,
    ) -> np.ndarray:
        """
        Масштабирует изображения из папки с коэффициентом scale_factor и бинаризует.
        """
        folder = Path(folder_path)
        valid_exts = {'.tif', '.tiff', '.png', '.bmp'}
        files = sorted([f for f in folder.iterdir() if f.suffix.lower() in valid_exts and not f.name.startswith('.')])

        if not files:
            raise FileNotFoundError(f"В папке {folder} нет подходящих файлов.")

        if max_slices:
            files = files[:max_slices]

        if threshold is None:
            threshold = 128

        rescaled_slices = []
        for fpath in files:
            with Image.open(fpath) as img:
                orig = img.convert('L')
                new_w = max(1, int(round(orig.width * scale_factor)))
                new_h = max(1, int(round(orig.height * scale_factor)))
                rescaled = orig.resize((new_w, new_h), Image.Resampling.BICUBIC)
                arr = np.array(rescaled)
                rescaled_slices.append(arr > threshold)

        return np.stack(rescaled_slices, axis=0).astype(np.uint8)

    def batch_rescale_structure(
        self,
        name: str,
        scale_factors: Sequence[float] = (0.7, 0.75, 0.8, 0.85, 0.9, 0.95),
        output_parent_dir: Optional[Union[str, Path]] = None,
    ) -> List[Path]:
        """
        Пакетно ремасштабирует указанную структуру для сетки масштабных коэффициентов.
        """
        src_folder = self.structures_dir / name
        if not src_folder.exists():
            raise FileNotFoundError(f"Структура {name} не найдена в {self.structures_dir}")

        out_parent = Path(output_parent_dir) if output_parent_dir else self.structures_dir
        valid_exts = {'.tif', '.tiff', '.png', '.bmp'}
        files = sorted([f for f in src_folder.iterdir() if f.suffix.lower() in valid_exts and not f.name.startswith('.')])

        created_folders = []
        for k in scale_factors:
            k_val = round(float(k), 2)
            dst_folder = out_parent / f"{name}-{k_val}"
            dst_folder.mkdir(parents=True, exist_ok=True)

            val = self.threshold_finder.find_threshold_for_structure(name, k_resize=k_val)

            for fpath in files:
                with Image.open(fpath) as img:
                    orig = img.convert('L')
                    new_w = max(1, int(round(orig.width * k_val)))
                    new_h = max(1, int(round(orig.height * k_val)))
                    rescaled = orig.resize((new_w, new_h), Image.Resampling.BICUBIC)
                    arr = np.array(rescaled)
                    bin_slice = ((arr > val) * 255).astype(np.uint8)
                    out_img = Image.fromarray(bin_slice)
                    out_img.save(dst_folder / fpath.name)

            created_folders.append(dst_folder)

        return created_folders
