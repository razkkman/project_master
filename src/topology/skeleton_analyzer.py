"""
Анализ топологических характеристик порового пространства и скелетона.
Включает расчет геометрической извилистости (тортуозности), координационного числа Z
и объемной плотности тройных узлов ветвления W_3p.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import numpy as np
import pandas as pd

from config import (
    SKELETONS_DIR,
    PROCESSED_DIR,
    STRUCTURES_ALL,
    VOXEL_SIZES,
)


class SkeletonAnalyzer:
    """
    Класс для комплексного топологического анализа графов скелетонов
    (полученных из плагина ImageJ Analyze Skeleton).

    Параметры:
        skeletons_dir: Директория с CSV-файлами скелетонов (data/skeletons)
    """

    def __init__(self, skeletons_dir: Union[str, Path] = SKELETONS_DIR):
        self.skeletons_dir = Path(skeletons_dir)

    def calculate_tortuosity(
        self,
        structure_name: str,
        min_branches: int = 500,
    ) -> Optional[float]:
        """
        Вычисляет среднюю геометрическую извилистость (тортуозность) ветвей скелетона:
        tau = mean(Branch length / Euclidean distance).

        Фильтрует мелкие изолированные артефакты скелетонизации (компоненты с <= min_branches).
        """
        csv_file = self.skeletons_dir / f"{structure_name}_Branch_info.csv"
        if not csv_file.exists():
            return None

        data = pd.read_csv(csv_file)
        counts = data['Skeleton ID'].value_counts()
        valid_ids = counts[counts > min_branches].index
        filt = data[data['Skeleton ID'].isin(valid_ids) & (data['Euclidean distance'] > 0)]

        if len(filt) == 0:
            return None

        tau_mean = float((filt['Branch length'] / filt['Euclidean distance']).mean())
        return tau_mean

    def calculate_all_tortuosity(self, min_branches: int = 500) -> Dict[str, float]:
        """
        Вычисляет тортуозность для всех исследуемых структур.
        """
        results = {}
        for name in STRUCTURES_ALL:
            tau = self.calculate_tortuosity(name, min_branches=min_branches)
            if tau is not None:
                results[name] = tau
        return results

    def calculate_coordination(self, structure_name: str) -> Optional[Dict[str, float]]:
        """
        Вычисляет координационное число ветвления Z и доли узлов:
        Z = 3*(tp/junc) + 4*(qp/junc) + 5*(other/junc).
        """
        csv_file = self.skeletons_dir / f"{structure_name}_Results.csv"
        if not csv_file.exists():
            return None

        data = pd.read_csv(csv_file)
        if data.empty or '# Junctions' not in data.columns:
            return None

        row = data.loc[np.argmax(data['# Junctions'])]
        junc = float(row['# Junctions'])
        if junc <= 0:
            return None

        tp = float(row.get('# Triple points', 0))
        qp = float(row.get('# Quadruple points', 0))
        other = max(0.0, junc - tp - qp)

        z = 3.0 * (tp / junc) + 4.0 * (qp / junc) + 5.0 * (other / junc)

        return {
            "z": z,
            "junctions": junc,
            "triple_points": tp,
            "quadruple_points": qp,
            "other_points": other,
            "omega_3p": tp / junc,
            "omega_4p": qp / junc,
            "omega_other": other / junc,
        }

    def calculate_all_coordination(self) -> Dict[str, float]:
        """
        Вычисляет координационное число Z для всех структур.
        """
        results = {}
        for name in STRUCTURES_ALL:
            res = self.calculate_coordination(name)
            if res is not None:
                results[name] = res["z"]
        return results

    def calculate_triple_points_density(
        self,
        structure_name: str,
        solid_volume_m3: Optional[float] = None,
    ) -> Optional[float]:
        """
        Вычисляет объемную плотность тройных узлов:
        W_3p = n_3p / V_solid [м^-3].
        Если объем solid_volume_m3 не передан, вычисляется через MarchingCubesCalculator.
        """
        coord = self.calculate_coordination(structure_name)
        if coord is None:
            return None

        n_3p = coord["triple_points"]

        if solid_volume_m3 is None or solid_volume_m3 <= 0:
            from core.structure import PorousStructure
            from methods.marching_cubes import MarchingCubesCalculator

            struct = PorousStructure.load(structure_name)
            mc = MarchingCubesCalculator()
            res = mc.calculate(struct)
            solid_volume_m3 = res.solid_volume_m3

        if solid_volume_m3 <= 0:
            return None

        return float(n_3p / solid_volume_m3)

    def calculate_all_triple_points_density(self) -> Dict[str, float]:
        """
        Вычисляет плотность тройных узлов W_3p для всех структур.
        """
        results = {}
        for name in STRUCTURES_ALL:
            w = self.calculate_triple_points_density(name)
            if w is not None:
                results[name] = w
        return results

    def analyze_structure(self, structure_name: str) -> Dict[str, Any]:
        """
        Полный топологический паспорт пористой структуры:
        тортуозность tau, координационное число Z, плотность узлов W_3p.
        """
        tau = self.calculate_tortuosity(structure_name)
        coord = self.calculate_coordination(structure_name)
        w_3p = self.calculate_triple_points_density(structure_name)

        return {
            "structure": structure_name,
            "tortuosity_tau": tau,
            "coordination_z": coord["z"] if coord else None,
            "triple_points_count": coord["triple_points"] if coord else None,
            "triple_points_density_w3p": w_3p,
        }
