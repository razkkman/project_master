"""
Генерация дискретизированной 3D-модели сферы.
Фасадный интерфейс, делегирующий расчет классу SyntheticSphere.
"""

import numpy as np
from synthetic.shapes import SyntheticSphere


def Generator_sfer(N: int) -> np.ndarray:
    """
    Генерирует бинарный 3D-массив дискретизированной сферы диаметра N.
    """
    sphere = SyntheticSphere(diameter_voxels=int(N))
    return sphere.generate().astype(np.float64)


if __name__ == "__main__":
    arr = Generator_sfer(10)
    print(f"Сфера диаметра 10 создана, форма: {arr.shape}, единиц: {np.count_nonzero(arr)}")
