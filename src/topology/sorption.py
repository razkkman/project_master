"""
Анализ корреляций сорбционных изотерм, петли капиллярного гистерезиса
и топологических параметров скелетона (координационного числа Z и тройных соединений).
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import RESEARCH_DIR, FIGURES_DIR


class SorptionCorrelationAnalyzer:
    """
    Класс для исследования корреляций между петлей гистерезиса изотерм сорбции
    и изменениями удельной площади поверхности (SSA) и связности мезопор.

    Параметры:
        research_dir: Путь к директории с сорбционными данными (data/research)
        figures_dir: Путь для сохранения графиков (docs/figures)
    """

    def __init__(
        self,
        research_dir: Union[str, Path] = RESEARCH_DIR,
        figures_dir: Union[str, Path] = FIGURES_DIR,
    ):
        self.research_dir = Path(research_dir)
        self.figures_dir = Path(figures_dir)

    def analyze_hysteresis(
        self,
        filename: str = "two_graphs_from_paper.csv",
        save_plots: bool = True,
    ) -> Dict[str, Any]:
        """
        Анализирует ветви адсорбции и десорбции:
        нормирует кривые и вычисляет коэффициенты корреляции Пирсона между SSA и тройными узлами.
        """
        csv_path = self.research_dir / filename
        if not csv_path.exists():
            raise FileNotFoundError(f"Файл сорбционных данных не найден: {csv_path}")

        data = pd.read_csv(csv_path, sep=';')
        relpres_col = data.columns[3]

        # Фильтрация некорректных значений относительного давления
        data = data[(data[relpres_col] > 0) & (data[relpres_col] < 1)].copy()

        # Разделение на адсорбционную и десорбционную ветви
        data_ads = data[data['adsdes'] == 'ads'].copy().reset_index(drop=True)
        data_des = data[data['adsdes'] == 'des'].copy().reset_index(drop=True)

        # Нормировка
        for col in data_ads.columns[4:]:
            max_ads = data_ads[col].max()
            if max_ads > 0:
                data_ads[col] = data_ads[col] / max_ads

            max_des = data_des[col].max()
            if max_des > 0:
                data_des[col] = data_des[col] / max_des

        # Коэффициенты корреляции Пирсона
        cor_ads = float(np.corrcoef(data_ads['ssa'], data_ads['TriConnectivityDistr'])[0, 1])
        cor_des = float(np.corrcoef(data_des['ssa'], data_des['TriConnectivityDistr'])[0, 1])

        # Расчет ширины петли гистерезиса delta(p/p0) при 50% заполнении
        results = {
            "pearson_correlation_ads": cor_ads,
            "pearson_correlation_des": cor_des,
            "points_ads": len(data_ads),
            "points_des": len(data_des),
        }

        if save_plots:
            self.figures_dir.mkdir(parents=True, exist_ok=True)

            # 1. График SSA
            fig1, ax1 = plt.subplots(figsize=(7, 5), dpi=150)
            ax1.plot(data_ads[relpres_col], data_ads['ssa'], 'r-', lw=2, label='Адсорбция (SSA норм.)')
            ax1.plot(data_des[relpres_col], data_des['ssa'], 'r--', lw=2, label='Десорбция (SSA норм.)')
            if 'simulrhoavboundnorm' in data_ads.columns:
                ax1.plot(data_ads[relpres_col], data_ads['simulrhoavboundnorm'], color='gray', alpha=0.5, label='Флюид')
                ax1.plot(data_des[relpres_col], data_des['simulrhoavboundnorm'], color='gray', alpha=0.5, linestyle='--')
            ax1.set_xlabel('p / p0', fontsize=11)
            ax1.set_ylabel('SSA норм.', fontsize=11)
            ax1.set_title('Гистерезис удельной площади поверхности', fontsize=12)
            ax1.legend(loc='best')
            ax1.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            fig1.savefig(self.figures_dir / "Figure_hysteresis_SSA.png", dpi=170)
            plt.close(fig1)

            # 2. График Z / тройных узлов
            fig2, ax2 = plt.subplots(figsize=(7, 5), dpi=150)
            ax2.plot(data_ads[relpres_col], data_ads['TriConnectivityDistr'], 'b-', lw=2, label='Адсорбция (Z норм.)')
            ax2.plot(data_des[relpres_col], data_des['TriConnectivityDistr'], 'b--', lw=2, label='Десорбция (Z норм.)')
            if 'simulrhoavboundnorm' in data_ads.columns:
                ax2.plot(data_ads[relpres_col], data_ads['simulrhoavboundnorm'], color='gray', alpha=0.5, label='Флюид')
                ax2.plot(data_des[relpres_col], data_des['simulrhoavboundnorm'], color='gray', alpha=0.5, linestyle='--')
            ax2.set_xlabel('p / p0', fontsize=11)
            ax2.set_ylabel('Z норм.', fontsize=11)
            ax2.set_title('Гистерезис связности поровой сетки', fontsize=12)
            ax2.legend(loc='best')
            ax2.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            fig2.savefig(self.figures_dir / "Figure_hysteresis_Z.png", dpi=170)
            plt.close(fig2)

        return results
