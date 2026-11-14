"""
Пакет синтетических геометрий и калибровочных бенчмарков.
"""

from synthetic.shapes import BaseSyntheticShape, SyntheticSphere, SyntheticCylinder
from synthetic.benchmark import CalibrationBenchmark

__all__ = [
    "BaseSyntheticShape",
    "SyntheticSphere",
    "SyntheticCylinder",
    "CalibrationBenchmark",
]
