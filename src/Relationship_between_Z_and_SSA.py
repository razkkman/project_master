"""
Анализ корреляции гистерезисов адсорбции/десорбции удельной площади поверхности (SSA)
и количества тройных соединений ветвей скелетона (TriConnectivityDistr).
Фасадный интерфейс, делегирующий расчет классу SorptionCorrelationAnalyzer.
"""

from typing import Tuple, Optional
from topology.sorption import SorptionCorrelationAnalyzer


def analyze_hysteresis_correlations(csv_path: Optional[str] = None, save_plots: bool = True) -> Tuple[float, float]:
    """
    Разделяет данные на ветви адсорбции и десорбции,
    вычисляет нормированные кривые и коэффициенты корреляции.
    """
    analyzer = SorptionCorrelationAnalyzer()
    filename = "two_graphs_from_paper.csv"
    if csv_path:
        from pathlib import Path
        filename = Path(csv_path).name

    res = analyzer.analyze_hysteresis(filename=filename, save_plots=save_plots)
    print("=== РЕЗУЛЬТАТЫ КОРРЕЛЯЦИОННОГО АНАЛИЗА ГИСТЕРЕЗИСОВ ===")
    print(f"Коэффициент корреляции для адсорбции (SSA vs TriConnectivity): {res['pearson_correlation_ads']:.4f}")
    print(f"Коэффициент корреляции для десорбции (SSA vs TriConnectivity): {res['pearson_correlation_des']:.4f}")
    return res['pearson_correlation_ads'], res['pearson_correlation_des']


if __name__ == "__main__":
    analyze_hysteresis_correlations()
