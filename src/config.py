"""
Модуль централизованной конфигурации и констант проекта.
Обеспечивает переносимость между ОС (Windows, Linux, macOS)
без жестко закодированных абсолютных путей.
"""

from pathlib import Path
from typing import Tuple, List, Optional

# Определение путей репозитория
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"

# Поддиректории данных
STRUCTURES_DIR = DATA_DIR / "structures"
SKELETONS_DIR = DATA_DIR / "skeletons"
MODELS_DIR = DATA_DIR / "models"
RESEARCH_DIR = DATA_DIR / "research"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = DOCS_DIR / "figures"

# Физические константы
SILICA_DENSITY = 2.12e6  # плотность аморфного кремнезема в г/м^3 (2.12 г/см^3)

# Номинальные значения удельной площади поверхности (BET, м^2/г)
SSA_FIS_NOMINAL = {
    'Coreshell16': 78.0,
    'Coreshell9': 111.0,
    'Si26': 129.0,
    'Si21': 173.0,
    'Si12': 315.0,
    'SBA15': 554.0,
    'KIT6': 614.0,
}

# Размер вокселя для каждой структуры (метры)
# Базовый размер вокселя умножается на 2 при формировании кубов Marching Cubes
VOXEL_SIZES = {
    'Coreshell16': 0.46e-9,
    'Coreshell9': 0.46e-9,
    'Si26': 0.50e-9,
    'Si21': 0.50e-9,
    'Si12': 0.35e-9,
    'SBA15': 0.46e-9,
    'KIT6': 0.46e-9,
}

# Номинальная пористость образцов
POROSITY_NOMINAL = {
    'Coreshell16': 0.370,
    'Coreshell9': 0.302,
    'Si26': 0.702,
    'Si21': 0.649,
    'Si12': 0.577,
    'SBA15': 0.487,
    'KIT6': 0.649,
}

# Базовые исследуемые структуры
STRUCTURES_ALL = ['Coreshell16', 'Coreshell9', 'Si26', 'Si21', 'Si12', 'SBA15', 'KIT6']
STRUCTURES_ORDERED = ['SBA15', 'KIT6']
STRUCTURES_DISORDERED = ['Coreshell16', 'Coreshell9', 'Si26', 'Si21', 'Si12']

# Коэффициенты масштабирования сетки (rescaling) для анализа сеточной сходимости
# Шаг дискретизации 0.05 от 0.70 до 1.00
SCALE_FACTORS = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]


def parse_structure_name(name: str) -> Tuple[str, float]:
    """
    Разбирает имя структуры на базовое имя и масштабный коэффициент.
    Например, 'Si12-0.7' -> ('Si12', 0.7), а 'Si12' -> ('Si12', 1.0).
    """
    if "-" in name:
        parts = name.rsplit("-", 1)
        try:
            scale = float(parts[1])
            return parts[0], scale
        except ValueError:
            return name, 1.0
    return name, 1.0


def get_voxel_size(name: str) -> float:
    """Возвращает физический размер вокселя с учетом базовой структуры."""
    base, _ = parse_structure_name(name)
    return VOXEL_SIZES.get(base, 1.0)


def get_nominal_bet(name: str) -> float:
    """Возвращает номинальное БЭТ значение для структуры."""
    base, _ = parse_structure_name(name)
    return SSA_FIS_NOMINAL.get(base, 0.0)


def get_nominal_porosity(name: str) -> float:
    """Возвращает номинальную пористость образца."""
    base, _ = parse_structure_name(name)
    return POROSITY_NOMINAL.get(base, 0.5)


def get_scale_series_names(base_name: str) -> List[str]:
    """
    Возвращает список имен папок для всей масштабной серии структуры:
    [f'{base_name}-0.7', ..., base_name].
    """
    return [f"{base_name}-{k:g}" if k < 1.0 else base_name for k in SCALE_FACTORS]


def get_all_structures_with_scales() -> List[str]:
    """Возвращает полный список всех 49 вариантов структур (базовые + масштабированные)."""
    all_names = []
    for base in STRUCTURES_ALL:
        all_names.extend(get_scale_series_names(base))
    return all_names
