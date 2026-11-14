"""
Пакет Data Science & Machine Learning для проекта анализа нанопористых сред.
Включает генератор обучающего датасета, пайплайн обучения моделей,
интерпретацию (Feature Importance) и экспорт Jupyter Notebook.
"""

from .dataset_generator import DatasetGenerator
from .model_trainer import MLModelTrainer

__all__ = ["DatasetGenerator", "MLModelTrainer"]
