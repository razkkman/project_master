"""
Синтетические калибровочные 3D-геометрии (сферы и цилиндры) с аналитическими решениями.
"""

from abc import ABC, abstractmethod
import math
from typing import Tuple, Optional
import numpy as np


class BaseSyntheticShape(ABC):
    """
    Абстрактный класс синтетического аналитического геометрического тела.
    """

    def __init__(self, voxel_size: float = 1.0, density: Optional[float] = None):
        self.voxel_size = voxel_size
        self.density = density

    @abstractmethod
    def generate(self) -> np.ndarray:
        """Генерирует бинарный 3D-массив формы."""
        pass

    @abstractmethod
    def analytical_surface_area(self) -> float:
        """Аналитическая площадь поверхности S."""
        pass

    @abstractmethod
    def analytical_volume(self) -> float:
        """Аналитический объем V."""
        pass

    def analytical_ssa(self) -> float:
        """
        Аналитическая удельная площадь поверхности:
        S / V (если density=None или 1.0) или S / (V * density).
        """
        v = self.analytical_volume()
        s = self.analytical_surface_area()
        if v <= 0:
            return 0.0
        if self.density is None or self.density == 1.0:
            return s / v
        return s / (v * self.density)


class SyntheticSphere(BaseSyntheticShape):
    """
    Дискретизированная сфера заданного диаметра.

    Параметры:
        diameter_voxels: Диаметр сферы в вокселях (D)
        voxel_size: Физический размер вокселя (метры)
        density: Физическая плотность
    """

    def __init__(
        self,
        diameter_voxels: int,
        voxel_size: float = 1.0,
        density: Optional[float] = None,
    ):
        super().__init__(voxel_size=voxel_size, density=density)
        self.diameter_voxels = diameter_voxels
        self.radius_voxels = diameter_voxels / 2.0

    def generate(self) -> np.ndarray:
        """
        Генерирует 3D массив дискретизированной сферы.
        Совместимо с Generator_sfer: смещение на 1 воксель.
        """
        n = self.diameter_voxels
        r = int(n / 2)
        o = int(n / 2)
        size = n + 3 if n % 2 != 0 else n + 2

        x, y, z = np.ogrid[:size, :size, :size]
        dist_sq = (x - o) ** 2 + (y - o) ** 2 + (z - o) ** 2
        mask = dist_sq <= r ** 2

        sfera = np.zeros((size, size, size), dtype=np.uint8)
        sfera[1:, 1:, 1:] = mask[:-1, :-1, :-1].astype(np.uint8)
        return sfera

    def analytical_surface_area(self) -> float:
        r = self.radius_voxels * self.voxel_size
        return 4.0 * math.pi * (r ** 2)

    def analytical_volume(self) -> float:
        r = self.radius_voxels * self.voxel_size
        return (4.0 / 3.0) * math.pi * (r ** 3)

    def analytical_ssa(self) -> float:
        r = self.radius_voxels * self.voxel_size
        if self.density is None or self.density == 1.0:
            return 3.0 / r
        return 3.0 / (r * self.density)


class SyntheticCylinder(BaseSyntheticShape):
    """
    Дискретизированный круговой цилиндр заданного диаметра и высоты.

    Параметры:
        diameter_voxels: Диаметр основания в вокселях (D)
        height_voxels: Высота цилиндра в вокселях (H)
        voxel_size: Физический размер вокселя
        density: Физическая плотность
    """

    def __init__(
        self,
        diameter_voxels: int,
        height_voxels: int,
        voxel_size: float = 1.0,
        density: Optional[float] = None,
    ):
        super().__init__(voxel_size=voxel_size, density=density)
        self.diameter_voxels = diameter_voxels
        self.height_voxels = height_voxels
        self.radius_voxels = diameter_voxels / 2.0

    def generate(self) -> np.ndarray:
        """
        Генерирует 3D массив дискретизированного цилиндра.
        Совместимо с Generator_cylinder: смещение на 1 воксель.
        """
        n = self.diameter_voxels
        h = self.height_voxels
        r = int(n / 2)
        o = int(n / 2)

        size_xy = n + 3 if n % 2 != 0 else n + 2
        size_z = h + 3 if h % 2 != 0 else h + 2

        x, y = np.ogrid[:size_xy, :size_xy]
        mask_2d = ((x - o) ** 2 + (y - o) ** 2) <= r ** 2

        cyl = np.zeros((size_xy, size_xy, size_z), dtype=np.uint8)
        cyl[1:, 1:, 1 : h + 1] = mask_2d[:-1, :-1, np.newaxis].astype(np.uint8)
        return cyl

    def analytical_surface_area(self) -> float:
        r = self.radius_voxels * self.voxel_size
        h = self.height_voxels * self.voxel_size
        # S = 2*pi*R^2 (основания) + 2*pi*R*H (боковая)
        return 2.0 * math.pi * (r ** 2) + 2.0 * math.pi * r * h

    def analytical_volume(self) -> float:
        r = self.radius_voxels * self.voxel_size
        h = self.height_voxels * self.voxel_size
        return math.pi * (r ** 2) * h

    def analytical_ssa(self) -> float:
        r = self.radius_voxels * self.voxel_size
        h = self.height_voxels * self.voxel_size
        geometric_ssa = (2.0 / r) + (2.0 / h)
        if self.density is None or self.density == 1.0:
            return geometric_ssa
        return geometric_ssa / self.density
