"""
Экспериментальная ветка разработки и тестирования модификаций метода Marching Cubes.
Изолирована в отдельный модуль для независимого сравнения с авторской реализацией
и повышения точности сопоставления с физическим экспериментом БЭТ.
"""

from .enhanced_marching_cubes import EnhancedMarchingCubesCalculator

__all__ = ["EnhancedMarchingCubesCalculator"]
