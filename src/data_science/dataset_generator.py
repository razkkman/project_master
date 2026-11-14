"""
Генератор табличного датасета признаков пористых материалов для машинного обучения.
Извлекает 3D суб-объемы и масштабированные варианты сеток, рассчитывает комплекс
геометрических, воксельных и топологических фичей, формируя датасет CSV/Excel.
"""

from pathlib import Path
import sys
import time
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd

# Добавление src в sys.path
SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import (
    STRUCTURES_ALL,
    STRUCTURES_ORDERED,
    STRUCTURES_DISORDERED,
    SSA_FIS_NOMINAL,
    POROSITY_NOMINAL,
    PROCESSED_DIR,
    get_voxel_size,
    parse_structure_name,
)
from core.structure import PorousStructure
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator
from topology.skeleton_analyzer import SkeletonAnalyzer


class DatasetGenerator:
    """
    Автоматический генератор датасета для задач Data Science / Machine Learning.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or PROCESSED_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.mc_mod = MarchingCubesCalculator(with_correction=True)
        self.mc_clas = MarchingCubesCalculator(with_correction=False)
        self.dm = DirectMethodCalculator()
        self.skel = SkeletonAnalyzer()

    def _get_morphology_type(self, base_name: str) -> str:
        """Определяет категорию морфологии материала."""
        if "Coreshell" in base_name:
            return "Core-Shell"
        elif base_name in STRUCTURES_ORDERED:
            return "Ordered Mesoporous"
        else:
            return "Stochastic Silica"

    def generate(
        self,
        subvolume_size: int = 100,
        subvolume_step: Optional[int] = None,
        max_samples_per_structure: int = 50,
        verbose: bool = True,
    ) -> pd.DataFrame:
        """
        Генерирует датасет, сканируя все доступные структуры и их кэшированные срезы.
        """
        step = subvolume_step or subvolume_size
        records: List[Dict[str, Any]] = []

        # 1. Сбор доступных файлов структур
        available_files = list(self.output_dir.glob("*.npy"))
        if verbose:
            print("=" * 80)
            print(f"  ГЕНЕРАЦИЯ ДАТАСЕТА МАШИННОГО ОБУЧЕНИЯ (Subvolume size: {subvolume_size}^3)")
            print("=" * 80)
            print(f"Найдено предобработанных 3D массивов: {len(available_files)}")

        # Топологические паспорта базовых структур
        topo_cache: Dict[str, Dict[str, float]] = {}
        for b in STRUCTURES_ALL:
            tau = self.skel.calculate_tortuosity(b) or 1.2
            coord = self.skel.calculate_coordination(b) or {"z": 3.2, "omega_3p": 0.8, "omega_4p": 0.15, "omega_other": 0.05}
            w3p = self.skel.calculate_triple_points_density(b) or 1.5e25
            topo_cache[b] = {
                "tau": tau,
                "z": coord["z"],
                "omega_3p": coord.get("omega_3p", 0.8),
                "omega_4p": coord.get("omega_4p", 0.15),
                "omega_other": coord.get("omega_other", 0.05),
                "w3p": w3p / 1e25,  # нормируем на 10^25
            }

        sample_idx = 0

        for npy_file in available_files:
            name = npy_file.stem
            base_name, scale = parse_structure_name(name)
            if base_name not in STRUCTURES_ALL:
                continue

            bet_nom = SSA_FIS_NOMINAL.get(base_name, 0.0)
            morph_type = self._get_morphology_type(base_name)
            topo = topo_cache.get(base_name, {})

            try:
                struct = PorousStructure.load(name)
            except Exception as e:
                continue

            vox = struct.voxels
            sz, sy, sx = vox.shape
            vsize_nm = struct.voxel_size * 1e9

            # Если объем меньше заданного размера суб-объема, берем его целиком
            if sz < subvolume_size or sy < subvolume_size or sx < subvolume_size:
                actual_sz = min(sz, subvolume_size)
                actual_sy = min(sy, subvolume_size)
                actual_sx = min(sx, subvolume_size)
                sub_cubes = [(0, 0, 0, actual_sz, actual_sy, actual_sx)]
            else:
                sub_cubes = []
                for z in range(0, sz - subvolume_size + 1, step):
                    for y in range(0, sy - subvolume_size + 1, step):
                        for x in range(0, sx - subvolume_size + 1, step):
                            sub_cubes.append((z, y, x, subvolume_size, subvolume_size, subvolume_size))
                            if len(sub_cubes) >= max_samples_per_structure:
                                break
                        if len(sub_cubes) >= max_samples_per_structure:
                            break
                    if len(sub_cubes) >= max_samples_per_structure:
                        break

            if verbose:
                print(f"[{name:<14}] Форма: {sz}x{sy}x{sx} | Суб-объемов: {len(sub_cubes):<3} | БЭТ: {bet_nom:.1f} м²/г")

            for (z, y, x, dz, dy, dx) in sub_cubes:
                sub_vox = vox[z:z+dz, y:y+dy, x:x+dx]
                n_solid = int(np.sum(sub_vox == 1))
                n_total = sub_vox.size
                if n_solid == 0 or n_solid == n_total:
                    continue  # Пропускаем однородные пустые/сплошные блоки

                porosity = 1.0 - (n_solid / n_total)
                solid_fraction = 1.0 - porosity

                sub_struct = PorousStructure(
                    name=f"{name}_sub_{sample_idx:04d}",
                    voxels=sub_vox,
                    voxel_size=struct.voxel_size,
                    density=struct.density,
                    nominal_ssa=bet_nom,
                )

                # Вычисление SSA методами
                res_mc_mod = self.mc_mod.calculate(sub_struct)
                res_mc_clas = self.mc_clas.calculate(sub_struct)
                res_dm = self.dm.calculate(sub_struct)

                ssa_mc = res_mc_mod.ssa_m2_g
                ssa_clas = res_mc_clas.ssa_m2_g
                ssa_dm = res_dm.ssa_m2_g

                if ssa_mc <= 0 or ssa_dm <= 0:
                    continue

                mc_dm_ratio = ssa_mc / ssa_dm if ssa_dm > 0 else 1.0
                clas_mod_ratio = ssa_clas / ssa_mc if ssa_mc > 0 else 1.0

                details = res_mc_mod.details
                s_total = details.get("s_total", 1.0)
                corr_z = details.get("corr_z", 0.0) / s_total if s_total > 0 else 0.0
                corr_y = details.get("corr_y", 0.0) / s_total if s_total > 0 else 0.0
                corr_x = details.get("corr_x", 0.0) / s_total if s_total > 0 else 0.0

                # Целевой коэффициент калибровки
                calib_factor = bet_nom / ssa_mc if ssa_mc > 0 else 1.0

                records.append({
                    "sample_id": f"{name}_{sample_idx:04d}",
                    "material": base_name,
                    "scale_k": scale,
                    "morphology_type": morph_type,
                    "voxel_size_nm": vsize_nm,
                    "sub_dim_z": dz,
                    "sub_dim_y": dy,
                    "sub_dim_x": dx,
                    "porosity": porosity,
                    "solid_fraction": solid_fraction,
                    "ssa_mc_modified": ssa_mc,
                    "ssa_mc_classical": ssa_clas,
                    "ssa_direct_method": ssa_dm,
                    "mc_direct_ratio": mc_dm_ratio,
                    "clas_mod_ratio": clas_mod_ratio,
                    "corr_share_z": corr_z,
                    "corr_share_y": corr_y,
                    "corr_share_x": corr_x,
                    "tortuosity_tau": topo.get("tau", 1.2),
                    "coordination_z": topo.get("z", 3.2),
                    "w3p_density_10e25": topo.get("w3p", 1.5),
                    "omega_3p": topo.get("omega_3p", 0.8),
                    "omega_4p": topo.get("omega_4p", 0.15),
                    "omega_other": topo.get("omega_other", 0.05),
                    "ssa_bet_target": bet_nom,
                    "calib_factor_target": calib_factor,
                })
                sample_idx += 1

        df = pd.DataFrame(records)

        # Сохранение в CSV и Excel
        csv_path = self.output_dir / "porous_materials_ml_dataset.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        if verbose:
            print("-" * 80)
            print(f" Сформирован датасет из {len(df)} строк и {len(df.columns)} колонок!")
            print(f" Файл сохранен: {csv_path}")

        return df


def main():
    generator = DatasetGenerator()
    df = generator.generate(subvolume_size=100, max_samples_per_structure=45, verbose=True)
    print("\nПервые 5 строк датасета:")
    print(df[["sample_id", "material", "porosity", "ssa_mc_modified", "ssa_direct_method", "ssa_bet_target"]].head())


if __name__ == "__main__":
    main()
