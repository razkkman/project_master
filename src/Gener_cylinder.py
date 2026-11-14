"""
Генерация дискретизированной 3D-модели цилиндра.
Фасадный интерфейс, делегирующий расчет классу SyntheticCylinder.
"""

import numpy as np
from synthetic.shapes import SyntheticCylinder


def Generator_cylinder(N: int, h: int) -> np.ndarray:
    """
    Генерирует бинарный 3D-массив дискретизированного цилиндра диаметра N и высоты h.
    """
    cyl = SyntheticCylinder(diameter_voxels=int(N), height_voxels=int(h))
    return cyl.generate().astype(np.float64)


if __name__ == "__main__":
    arr = Generator_cylinder(10, 5)
    print(f"Цилиндр диаметра 10 и высоты 5 создан, форма: {arr.shape}, единиц: {np.count_nonzero(arr)}")
