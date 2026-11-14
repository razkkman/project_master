"""
Модуль доменной модели пористой структуры.
Инкапсулирует 3D воксельный массив, физические параметры,
масштабные коэффициенты (rescaling), кэширование и геометрические характеристики.
"""

from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image

from config import (
    SILICA_DENSITY,
    STRUCTURES_DIR,
    PROCESSED_DIR,
    parse_structure_name,
    get_voxel_size,
    get_nominal_bet,
    get_nominal_porosity,
)


class PorousStructure:
    """
    Класс, представляющий трехмерную дискретную модель пористой структуры.

    Атрибуты:
        name: Полное название структуры (например, 'Si12' или 'Si12-0.7')
        base_name: Базовый тип материала (например, 'Si12')
        scale_factor: Коэффициент масштабирования сетки (k in [0.7 .. 1.0])
        voxels: 3D массив вокселей (uint8, где 1 - твердая фаза / скелет, 0 - поры)
        voxel_size: Линейный физический размер ребра одного вокселя (метры)
        density: Физическая плотность твердой фазы (г/м^3, по умолчанию 2.12e6 для SiO2)
        nominal_ssa: Экспериментальное значение удельной площади (БЭТ, м^2/г)
        nominal_porosity: Справочная экспериментальная пористость образца
    """

    def __init__(
        self,
        name: str,
        voxels: np.ndarray,
        voxel_size: Optional[float] = None,
        density: float = SILICA_DENSITY,
        nominal_ssa: Optional[float] = None,
        nominal_porosity: Optional[float] = None,
        scale_factor: Optional[float] = None,
    ):
        self.name = name
        self.base_name, parsed_scale = parse_structure_name(name)
        self.scale_factor = scale_factor if scale_factor is not None else parsed_scale

        self.voxels = np.asarray(voxels, dtype=np.uint8)
        if self.voxels.ndim != 3:
            raise ValueError(f"Ожидается трехмерный массив, получена размерность {self.voxels.ndim}")

        # Физический размер вокселя (наследуется от базовой структуры)
        self.voxel_size = voxel_size if voxel_size is not None else get_voxel_size(self.name)
        self.density = density
        self.nominal_ssa = nominal_ssa if nominal_ssa is not None else get_nominal_bet(self.name)
        self.nominal_porosity = (
            nominal_porosity if nominal_porosity is not None else get_nominal_porosity(self.name)
        )

        self._cached_solid_count: Optional[int] = None

    @property
    def shape(self) -> Tuple[int, int, int]:
        """Размерность 3D массива (Z, Y, X)."""
        return self.voxels.shape

    @property
    def total_voxels(self) -> int:
        """Общее число вокселей в объеме."""
        return int(self.voxels.size)

    @property
    def solid_voxels(self) -> int:
        """Число вокселей твердой фазы (единиц)."""
        if self._cached_solid_count is None:
            self._cached_solid_count = int(np.count_nonzero(self.voxels))
        return self._cached_solid_count

    @property
    def pore_voxels(self) -> int:
        """Число вокселей порового пространства (нулей)."""
        return self.total_voxels - self.solid_voxels

    @property
    def porosity(self) -> float:
        """
        Расчетная пористость структуры phi = 1 - N_solid / N_total.
        """
        if self.total_voxels == 0:
            return 0.0
        return 1.0 - (self.solid_voxels / self.total_voxels)

    @property
    def solid_fraction(self) -> float:
        """Доля твердой фазы: 1.0 - porosity."""
        return 1.0 - self.porosity

    @property
    def solid_volume_m3(self) -> float:
        """Физический объем твердой фазы в м^3."""
        return self.solid_voxels * (self.voxel_size ** 3)

    @property
    def total_volume_m3(self) -> float:
        """Полный геометрический объем расчетной области в м^3."""
        return self.total_voxels * (self.voxel_size ** 3)

    @property
    def solid_mass_g(self) -> float:
        """Масса твердой фазы в граммах: V_solid * density."""
        return self.solid_volume_m3 * self.density

    def extract_subvolume(
        self,
        origin: Tuple[int, int, int] = (0, 0, 0),
        size: Tuple[int, int, int] = (100, 100, 100),
        sub_name: Optional[str] = None,
    ) -> "PorousStructure":
        """
        Извлекает прямоугольный подобъем (суб-воксельный массив).
        Полезно для 3D-визуализации и локального структурного анализа.
        """
        z0, y0, x0 = origin
        dz, dy, dx = size
        sub_voxels = self.voxels[z0 : z0 + dz, y0 : y0 + dy, x0 : x0 + dx].copy()
        name = sub_name or f"{self.name}_sub_{dz}x{dy}x{dx}"
        return PorousStructure(
            name=name,
            voxels=sub_voxels,
            voxel_size=self.voxel_size,
            density=self.density,
            nominal_ssa=self.nominal_ssa,
            nominal_porosity=self.nominal_porosity,
            scale_factor=self.scale_factor,
        )

    def save_cache(self, file_path: Union[str, Path]) -> Path:
        """Сохраняет воксельный массив в быстрый бинарный файл .npy."""
        target = Path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.suffix != ".npy":
            target = target.with_suffix(".npy")
        np.save(target, self.voxels)
        return target

    def export_slices(
        self,
        output_dir: Union[str, Path],
        prefix: Optional[str] = None,
        file_format: str = "png",
    ) -> int:
        """
        Экспортирует послойные 2D изображения (для 3D Viewer или ImageJ).
        Возвращает количество сохраненных срезов.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        pref = prefix or self.name

        count = 0
        for i in range(self.voxels.shape[0]):
            slice_data = (self.voxels[i, :, :] * 255).astype(np.uint8)
            img = Image.fromarray(slice_data)
            img.save(out_path / f"{pref}_{i:04d}.{file_format}")
            count += 1
        return count

    @classmethod
    def from_images(
        cls,
        folder_path: Union[str, Path],
        name: Optional[str] = None,
        threshold: int = 128,
        invert: bool = False,
        voxel_size: Optional[float] = None,
        density: float = SILICA_DENSITY,
        max_slices: Optional[int] = None,
        make_even: bool = True,
    ) -> "PorousStructure":
        """
        Загружает стек 2D изображений (TIFF/BMP/PNG) и бинаризует по порогу.
        Параметр make_even=True гарантирует четность размерностей по всем 3 осям,
        что строго необходимо для метода Marching Cubes (блоки 2x2x2) и совпадения
        с оригинальным алгоритмом автора FormirMass_v1.
        """
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError(f"Директория со срезами не найдена: {folder}")

        struct_name = name or folder.name
        valid_exts = {".tif", ".tiff", ".png", ".bmp", ".jpg", ".jpeg"}
        files = sorted([f for f in folder.iterdir() if f.suffix.lower() in valid_exts and not f.name.startswith(".")])

        if not files:
            raise FileNotFoundError(f"В директории {folder} не найдены графические файлы.")

        if max_slices:
            files = files[:max_slices]

        if make_even and len(files) % 2 != 0:
            files = files[: len(files) - 1]

        slices = []
        for f in files:
            with Image.open(f) as img:
                arr = np.array(img.convert("L"))
                if make_even:
                    ny = arr.shape[0] if arr.shape[0] % 2 == 0 else arr.shape[0] - 1
                    nx = arr.shape[1] if arr.shape[1] % 2 == 0 else arr.shape[1] - 1
                    arr = arr[:ny, :nx]
                binary_slice = (arr > threshold) if not invert else (arr <= threshold)
                slices.append(binary_slice)

        voxels = np.stack(slices, axis=0).astype(np.uint8)

        return cls(
            name=struct_name,
            voxels=voxels,
            voxel_size=voxel_size,
            density=density,
        )

    @classmethod
    def from_cache(
        cls,
        file_path: Union[str, Path],
        name: Optional[str] = None,
        voxel_size: Optional[float] = None,
        density: float = SILICA_DENSITY,
    ) -> "PorousStructure":
        """
        Загружает структуру из скомпилированного .npy или .pickle файла.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл кэша не найден: {path}")

        struct_name = name or path.stem.replace("_voxels", "")
        if path.suffix == ".npy":
            voxels = np.load(path)
        else:
            import pickle
            with open(path, "rb") as f:
                voxels = pickle.load(f)

        return cls(
            name=struct_name,
            voxels=voxels,
            voxel_size=voxel_size,
            density=density,
        )

    @classmethod
    def load(
        cls,
        name: str,
        structures_dir: Union[str, Path] = STRUCTURES_DIR,
        cache_dir: Union[str, Path] = PROCESSED_DIR,
        force_reload: bool = False,
        threshold: int = 128,
        invert: bool = False,
    ) -> "PorousStructure":
        """
        Универсальный фабричный метод:
        Сначала ищет скомпилированный кэш .npy в processed/, если нет —
        загружает стек изображений из data/structures/<name> и сохраняет кэш.
        Корректно работает как для базовых структур ('Si12'),
        так и для масштабированных серий ('Si12-0.7', 'Coreshell16-0.85').
        """
        cache_path = Path(cache_dir) / f"{name}.npy"
        if cache_path.exists() and not force_reload:
            return cls.from_cache(cache_path, name=name)

        struct_folder = Path(structures_dir) / name
        if not struct_folder.exists():
            # Попробуем найти среди поддиректорий без учета регистра
            for p in Path(structures_dir).iterdir():
                if p.is_dir() and p.name.lower() == name.lower():
                    struct_folder = p
                    break

        if not struct_folder.exists():
            raise FileNotFoundError(f"Структура {name} не найдена в {structures_dir}")

        structure = cls.from_images(
            folder_path=struct_folder,
            name=name,
            threshold=threshold,
            invert=invert,
        )
        try:
            structure.save_cache(cache_path)
        except Exception:
            pass

        return structure

    def __repr__(self) -> str:
        z, y, x = self.shape
        scale_str = f" (k={self.scale_factor})" if self.scale_factor < 1.0 else ""
        return (
            f"<PorousStructure '{self.name}'{scale_str}: {z}x{y}x{x} voxels, "
            f"phi={self.porosity:.3f}, voxel={self.voxel_size*1e9:.2f} nm>"
        )
