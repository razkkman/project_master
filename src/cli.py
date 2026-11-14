"""
Единая консольная точка входа (CLI) для исследовательского комплекса
анализа пористых сред и расчета удельной площади поверхности (SSA).
"""

import sys
import argparse
from pathlib import Path

# Обеспечиваем доступность модулей из src
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import STRUCTURES_ALL, STRUCTURES_DIR, SKELETONS_DIR, RESEARCH_DIR
from core.structure import PorousStructure
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator
from pipeline.ssa_pipeline import SSAEvaluationPipeline
from topology.skeleton_analyzer import SkeletonAnalyzer
from topology.sorption import SorptionCorrelationAnalyzer
from synthetic.benchmark import CalibrationBenchmark
from preprocessing.threshold import ThresholdFinder


def cmd_ssa(args):
    """Расчет SSA методами Marching Cubes и Direct Method."""
    pipeline = SSAEvaluationPipeline()
    if args.scale_series:
        base = args.structure or "Si12"
        df = pipeline.run_scale_series(base, verbose=True, save_plot=True)
        if args.save:
            saved_path = pipeline.save_results(df, filename=f"scale_series_{base}")
            print(f"Результаты серии сохранены в: {saved_path}")
        return

    structs = [args.structure] if args.structure else STRUCTURES_ALL
    pipeline.structures = structs
    df = pipeline.run_all(verbose=True)

    if args.save:
        saved_path = pipeline.save_results(df)
        print(f"Результаты успешно сохранены в: {saved_path}")


def cmd_skeleton(args):
    """Анализ топологии скелетона: тортуозность, координационные числа, тройные узлы."""
    analyzer = SkeletonAnalyzer(skeletons_dir=SKELETONS_DIR)
    structs = [args.structure] if args.structure else STRUCTURES_ALL

    print("\n" + "=" * 80)
    print(f"{'Структура':<14} | {'Тортуозность τ':<16} | {'Коорд. число Z':<16} | {'W_3p, 10^25 м^-3':<18}")
    print("=" * 80)

    for name in structs:
        tau = analyzer.calculate_tortuosity(name) if args.metric in ("all", "tau") else None
        coord = analyzer.calculate_coordination(name) if args.metric in ("all", "z") else None
        w3p = analyzer.calculate_triple_points_density(name) if args.metric in ("all", "w3p") else None

        tau_str = f"{tau:.6f}" if tau is not None else "-"
        z_str = f"{coord['z']:.6f}" if coord is not None else "-"
        w3p_str = f"{w3p / 1e25:.4f}" if w3p is not None else "-"

        print(f"{name:<14} | {tau_str:<16} | {z_str:<16} | {w3p_str:<18}")

    print("-" * 80 + "\n")


def cmd_benchmark(args):
    """Калибровочные тесты алгоритмов на синтетических сферах и цилиндрах."""
    benchmark = CalibrationBenchmark()
    if args.shape in ("all", "sphere"):
        print("\n--- Запуск калибровочного теста на сферах ---")
        df_sphere = benchmark.run_sphere_benchmark(d_min=args.dmin, d_max=args.dmax, step=args.step)
        print(df_sphere.to_string(index=False))

    if args.shape in ("all", "cylinder"):
        print(f"\n--- Запуск калибровочного теста на цилиндрах (H={args.height}) ---")
        df_cyl = benchmark.run_cylinder_benchmark(fixed_h=args.height, d_min=args.dmin, d_max=args.dmax, step=args.step)
        print(df_cyl.to_string(index=False))


def cmd_sorption(args):
    """Анализ гистерезиса изотерм сорбции и корреляций со связностью."""
    analyzer = SorptionCorrelationAnalyzer()
    res = analyzer.analyze_hysteresis(save_plots=not args.no_plots)
    print("\n=== Результаты анализа сорбционного гистерезиса ===")
    print(f"Коэффициент корреляции Пирсона (адсорбция): {res['pearson_correlation_ads']:.4f}")
    print(f"Коэффициент корреляции Пирсона (десорбция): {res['pearson_correlation_des']:.4f}")
    print(f"Точек на ветви адсорбции: {res['points_ads']}, десорбции: {res['points_des']}")
    if not args.no_plots:
        print("Графики сохранены в docs/figures/\n")


def cmd_porosity(args):
    """Определение порога бинаризации для соответствия номинальной пористости."""
    finder = ThresholdFinder()
    struct_name = args.structure
    scale = args.scale
    threshold = finder.find_threshold_for_structure(struct_name, k_resize=scale)
    print(f"\nСтруктура: {struct_name}")
    print(f"Масштабный фактор: {scale}")
    print(f"Подобранный оптимальный порог яркости: {threshold}\n")


def cmd_subvolume(args):
    """Извлечение и экспорт суб-объема для 3D Viewer."""
    struct = PorousStructure.load(args.structure)
    size = args.size
    sub = struct.extract_subvolume(origin=(0, 0, 0), size=(size, size, size))
    out_dir = Path(args.output) if args.output else SRC_DIR.parent / "data" / "subvolumes" / f"{args.structure}_{size}"
    count = sub.export_slices(output_dir=out_dir)
    print(f"\nУспешно экспортировано {count} срезов суб-объема {size}x{size}x{size} в папку:")
    print(f"{out_dir}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Комплекс анализа морфологии мезопористых структур и расчета удельной площади поверхности (SSA)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    # 1. ssa
    p_ssa = subparsers.add_parser("ssa", help="Расчет SSA методами Marching Cubes и Direct Method")
    p_ssa.add_argument("--structure", "-s", type=str, help="Имя структуры (базовой 'Si12' или масштабированной 'Si12-0.7')")
    p_ssa.add_argument("--scale-series", action="store_true", help="Исследовать сеточную сходимость по масштабам k in [0.70 .. 1.00]")
    p_ssa.add_argument("--save", action="store_true", help="Сохранить результаты в CSV/pickle")
    p_ssa.set_defaults(func=cmd_ssa)

    # 2. skeleton
    p_skel = subparsers.add_parser("skeleton", help="Топологический анализ скелетонов графов")
    p_skel.add_argument("--structure", "-s", type=str, choices=STRUCTURES_ALL, help="Имя структуры")
    p_skel.add_argument("--metric", "-m", choices=["all", "tau", "z", "w3p"], default="all", help="Анализируемая метрика")
    p_skel.set_defaults(func=cmd_skeleton)

    # 3. benchmark
    p_bm = subparsers.add_parser("benchmark", help="Калибровка на аналитических сферах и цилиндрах")
    p_bm.add_argument("--shape", choices=["all", "sphere", "cylinder"], default="all", help="Геометрическое тело")
    p_bm.add_argument("--dmin", type=int, default=4, help="Минимальный диаметр")
    p_bm.add_argument("--dmax", type=int, default=24, help="Максимальный диаметр")
    p_bm.add_argument("--step", type=int, default=4, help="Шаг диаметра")
    p_bm.add_argument("--height", type=int, default=5, help="Высота цилиндра")
    p_bm.set_defaults(func=cmd_benchmark)

    # 4. sorption
    p_sorp = subparsers.add_parser("sorption", help="Анализ сорбционного гистерезиса и корреляций")
    p_sorp.add_argument("--no-plots", action="store_true", help="Не генерировать графики")
    p_sorp.set_defaults(func=cmd_sorption)

    # 5. porosity
    p_poro = subparsers.add_parser("porosity", help="Подбор порога бинаризации по номинальной пористости")
    p_poro.add_argument("--structure", "-s", required=True, choices=STRUCTURES_ALL, help="Имя структуры")
    p_poro.add_argument("--scale", "-k", type=float, default=1.0, help="Масштабный фактор")
    p_poro.set_defaults(func=cmd_porosity)

    # 6. subvolume
    p_sub = subparsers.add_parser("subvolume", help="Извлечение суб-объема для 3D Viewer")
    p_sub.add_argument("--structure", "-s", required=True, choices=STRUCTURES_ALL, help="Имя структуры")
    p_sub.add_argument("--size", type=int, default=100, help="Размер кубического среза (по умолчанию 100)")
    p_sub.add_argument("--output", "-o", type=str, help="Путь сохранения срезов")
    p_sub.set_defaults(func=cmd_subvolume)

    if len(sys.argv) == 1:
        from main import interactive_main
        interactive_main()
        return

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
