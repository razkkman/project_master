"""
Главный исполняемый модуль программного комплекса магистерской диссертации.
Предоставляет интерактивное меню выбора действий (TUI) и интерфейс командной строки (CLI).
"""

import sys
import time
from pathlib import Path
from typing import List, Optional

# Добавление src в sys.path для корректных импортов
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import (
    STRUCTURES_ALL,
    STRUCTURES_DIR,
    SKELETONS_DIR,
    RESEARCH_DIR,
    FIGURES_DIR,
    PROCESSED_DIR,
    VOXEL_SIZES,
    SSA_FIS_NOMINAL,
)
from core.structure import PorousStructure
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator
from pipeline.ssa_pipeline import SSAEvaluationPipeline
from topology.skeleton_analyzer import SkeletonAnalyzer
from topology.sorption import SorptionCorrelationAnalyzer
from synthetic.shapes import SyntheticSphere, SyntheticCylinder
from synthetic.benchmark import CalibrationBenchmark
from preprocessing.threshold import ThresholdFinder
from preprocessing.rescale import VolumeRescaler


# ============================================================================
# Вспомогательные функции форматирования и ввода
# ============================================================================

def print_header(title: str):
    """Выводит стилизованный заголовок раздела."""
    print("\n" + "═" * 84)
    print(f"  {title}")
    print("═" * 84)


def print_banner():
    """Главный баннер программного комплекса."""
    banner = r"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║   КОМПЛЕКС АНАЛИЗА МОРФОЛОГИИ ПОРИСТЫХ СРЕД И ВЫЧИСЛЕНИЯ УДЕЛЬНОЙ ПЛОЩАДИ (SSA)  ║
║   Магистерская диссертация Ю.Ю. Пилипенко (БГУ, РФКТ, САиКМ, 2021)               ║
╚══════════════════════════════════════════════════════════════════════════════════╝"""
    print(banner)


def pause():
    """Пауза перед возвратом в меню."""
    input("\n[Нажмите Enter для возврата в меню...]")


def choose_structure(prompt: str = "Выберите исследуемую структуру:", allow_scales: bool = True) -> Optional[str]:
    """Интерактивное меню выбора структуры (с поддержкой масштабных серий k in [0.70 .. 1.00])."""
    print(f"\n{prompt}")
    for idx, name in enumerate(STRUCTURES_ALL, 1):
        voxel_nm = VOXEL_SIZES[name] * 1e9
        bet = SSA_FIS_NOMINAL.get(name, 0.0)
        print(f"  [{idx}] {name:<12} (h = {voxel_nm:.2f} нм, BET = {bet:.1f} м²/г)")
    if allow_scales:
        print("  [s] Выбрать масштабированную структуру (k in [0.70 .. 0.95])")
    print("  [0] Отмена")

    while True:
        choice = input("\nВаш выбор: ").strip()
        if choice == "0":
            return None
        if allow_scales and choice.lower() == "s":
            print("\nВыберите базовую структуру для выбора масштаба:")
            for idx, name in enumerate(STRUCTURES_ALL, 1):
                print(f"  [{idx}] {name}")
            b_choice = input("Номер базовой структуры: ").strip()
            if b_choice.isdigit() and 1 <= int(b_choice) <= len(STRUCTURES_ALL):
                base = STRUCTURES_ALL[int(b_choice) - 1]
                series = get_scale_series_names(base)
                print(f"\nДоступные масштабированные сетки для {base}:")
                for s_idx, s_name in enumerate(series, 1):
                    _, k = parse_structure_name(s_name)
                    print(f"  [{s_idx}] {s_name:<16} (масштаб k = {k:.2f})")
                sc_choice = input("Выберите масштаб [1-7]: ").strip()
                if sc_choice.isdigit() and 1 <= int(sc_choice) <= len(series):
                    return series[int(sc_choice) - 1]
            print("Некорректный выбор.")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(STRUCTURES_ALL):
            return STRUCTURES_ALL[int(choice) - 1]
        print("Ошибка: введите номер от 1 до", len(STRUCTURES_ALL), "или 's'")


# ============================================================================
# Интерактивные сценарии действий
# ============================================================================

def menu_ssa():
    """Меню расчета SSA."""
    while True:
        print_header("📊 РАСЧЕТ УДЕЛЬНОЙ ПЛОЩАДИ ПОВЕРХНОСТИ (SSA)")
        print("  [1] Рассчитать SSA для структуры (базовой или масштабированной k)")
        print("  [2] Пакетный расчет базовых 7 структур (сравнение с БЭТ)")
        print("  [3] 🔬 Исследование сеточной сходимости по масштабам (k = 0.70 .. 1.00)")
        print("  [4] Детальная диагностика Marching Cubes (граничные поправки коллизий)")
        print("  [5] 🚀 Экспериментальная модификация Marching Cubes (Enhanced MC vs Авторский vs БЭТ)")
        print("  [6] Сохранить результаты последнего расчета в CSV / Pickle")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-6]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = choose_structure()
            if not name:
                continue

            print(f"\nЗагрузка и расчет структуры {name}...")
            struct = PorousStructure.load(name)
            pipeline = SSAEvaluationPipeline(structures=[name])
            res = pipeline.run_structure(name)

            scale_info = f" (k = {struct.scale_factor:.2f})" if struct.scale_factor < 1.0 else ""
            print_header(f"РЕЗУЛЬТАТЫ РАСЧЕТА ДЛЯ {name}{scale_info}")
            print(f"  Размерность объема:        {struct.shape[0]} x {struct.shape[1]} x {struct.shape[2]} вокселей")
            print(f"  Размер вокселя (h):        {res['voxel_size_nm']:.2f} нм")
            print(f"  Пористость объема (phi):   {res['porosity'] * 100:.2f}%")
            print(f"  Эксперимент БЭТ:           {res['nominal_bet']:.2f} м²/г")
            print("  " + "─" * 70)
            print(f"  Marching Cubes (модиф.):   {res['ssa_mc_modified']:.2f} м²/г (погрешность: {res['error_mc_mod_pct']:+.2f}%)")
            print(f"  Marching Cubes (классич.): {res['ssa_mc_classical']:.2f} м²/г (погрешность: {res['error_mc_clas_pct']:+.2f}%)")
            print(f"  Прямой воксельный метод:   {res['ssa_direct_method']:.2f} м²/г (погрешность: {res['error_direct_pct']:+.2f}%)")
            print(f"  Преобладающий метод:       {res['best_method']}")
            print(f"  Время вычисления:          {res['time_sec']:.3f} с")
            pause()

        elif choice == "2":
            print("\nЗапуск пакетного анализа всех пористых структур...")
            pipeline = SSAEvaluationPipeline()
            df = pipeline.run_all(verbose=True)
            save = input("Сохранить отчет в CSV? (y/n, по умолчанию y): ").strip().lower()
            if save != "n":
                p = pipeline.save_results(df)
                print(f"Сводка сохранена в: {p}")
            pause()

        elif choice == "3":
            base = choose_structure("Выберите базовую структуру для серии масштабирования k:", allow_scales=False)
            if not base:
                continue
            pipeline = SSAEvaluationPipeline()
            df = pipeline.run_scale_series(base, verbose=True, save_plot=True)
            print(f"График зависимости погрешности от разрешения сохранен:")
            print(f"  docs/figures/Figure_scale_series_{base}.png")
            pause()

        elif choice == "4":
            name = choose_structure("Выберите структуру для детальной диагностики:")
            if not name:
                continue
            struct = PorousStructure.load(name)
            mc = MarchingCubesCalculator(with_correction=True)
            res = mc.calculate(struct)
            d = res.details

            print_header(f"ДИАГНОСТИКА MARCHING CUBES ДЛЯ {name}")
            print(f"  Всего элементарных кубов:      {d.get('cubes_count', 0):,}")
            print(f"  Базовая площадь кубов (S_base):{d.get('s_base', 0):.4e} м²")
            print(f"  Поправка по оси Z (стыки 0-1): {d.get('corr_z', 0):.4e} м²")
            print(f"  Поправка по оси Y (стыки 0-1): {d.get('corr_y', 0):.4e} м²")
            print(f"  Поправка по оси X (стыки 0-1): {d.get('corr_x', 0):.4e} м²")
            print(f"  Итоговая площадь (S_total):    {d.get('s_total', 0):.4e} м²")
            print(f"  Объем твердой фазы (V_solid):  {d.get('v_solid', 0):.4e} м³")
            print(f"  Результирующая SSA:            {res.ssa_m2_g:.2f} м²/г")
            pause()

        elif choice == "5":
            print("\nЗапуск сравнительного анализа экспериментальной ветки Enhanced Marching Cubes...")
            from experimental_mc.compare_mc import run_comprehensive_comparison
            run_comprehensive_comparison(save_plot=True)
            pause()

        elif choice == "6":
            pipeline = SSAEvaluationPipeline()
            df = pipeline.run_all(verbose=False)
            p = pipeline.save_results(df)
            print(f"\nРезультаты сохранены в: {p}")
            pause()


def menu_skeleton():
    """Меню топологического анализа скелетонов."""
    analyzer = SkeletonAnalyzer(skeletons_dir=SKELETONS_DIR)

    while True:
        print_header("🧬 ТОПОЛОГИЧЕСКИЙ АНАЛИЗ СКЕЛЕТОНОВ (ImageJ Analyze Skeleton)")
        print("  [1] Расчет средней геометрической извилистости (тортуозность tau)")
        print("  [2] Расчет координационного числа ветвления Z и распределения узлов")
        print("  [3] Расчет нормированной объемной плотности тройных узлов (W_3p)")
        print("  [4] Сводный топологический паспорт для всех структур")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-4]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = choose_structure()
            if not name:
                continue
            tau = analyzer.calculate_tortuosity(name)
            if tau:
                print(f"\n[{name}] Тортуозность ветвей скелетона: tau = {tau:.6f}")
            else:
                print(f"\n[{name}] Не найдены данные скелетона в {SKELETONS_DIR}")
            pause()

        elif choice == "2":
            name = choose_structure()
            if not name:
                continue
            coord = analyzer.calculate_coordination(name)
            if coord:
                print_header(f"КООРДИНАЦИОННОЕ ЧИСЛО И УЗЛЫ ДЛЯ {name}")
                print(f"  Координационное число Z:   {coord['z']:.6f}")
                print(f"  Всего узлов ветвления:     {int(coord['junctions']):,}")
                print(f"  Тройных узлов (3p):        {int(coord['triple_points']):,} ({coord['omega_3p'] * 100:.1f}%)")
                print(f"  Четверных узлов (4p):      {int(coord['quadruple_points']):,} ({coord['omega_4p'] * 100:.1f}%)")
                print(f"  Узлов высшего порядка:     {int(coord['other_points']):,} ({coord['omega_other'] * 100:.1f}%)")
            else:
                print(f"\n[{name}] Данные скелетона отсутствуют.")
            pause()

        elif choice == "3":
            name = choose_structure()
            if not name:
                continue
            w3p = analyzer.calculate_triple_points_density(name)
            if w3p:
                print(f"\n[{name}] Объемная плотность тройных узлов: W_3p = {w3p:.4e} м^-3")
            else:
                print(f"\n[{name}] Ошибка при расчете W_3p.")
            pause()

        elif choice == "4":
            print("\nФормирование сводного топологического паспорта...")
            print("=" * 86)
            print(f"{'Структура':<13} | {'Извилистость τ':<16} | {'Число Z':<12} | {'Тройных узлов':<14} | {'W_3p, 10^25 м^-3':<18}")
            print("=" * 86)
            for name in STRUCTURES_ALL:
                p = analyzer.analyze_structure(name)
                tau_s = f"{p['tortuosity_tau']:.4f}" if p['tortuosity_tau'] else "-"
                z_s = f"{p['coordination_z']:.4f}" if p['coordination_z'] else "-"
                tp_s = f"{int(p['triple_points_count']):,}" if p['triple_points_count'] else "-"
                w3p_s = f"{p['triple_points_density_w3p'] / 1e25:.4f}" if p['triple_points_density_w3p'] else "-"
                print(f"{name:<13} | {tau_s:<16} | {z_s:<12} | {tp_s:<14} | {w3p_s:<18}")
            print("-" * 86)
            pause()


def menu_benchmark():
    """Меню калибровочных тестов на аналитических телах."""
    benchmark = CalibrationBenchmark()

    while True:
        print_header("🎯 КАЛИБРОВОЧНЫЕ ТЕСТЫ НА АНАЛИТИЧЕСКИХ ТЕЛАХ")
        print("  [1] Сеточный тест на сферах различного диаметра (D = 4 .. 24)")
        print("  [2] Сеточный тест на цилиндрах (H = 5 вокс., переменный диаметр D)")
        print("  [3] Полный калибровочный запуск с сохранением графиков погрешностей")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-3]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\nЗапуск калибровки на сферах...")
            df = benchmark.run_sphere_benchmark(d_min=4, d_max=24, step=4, save_plot=True)
            print("\n" + df.to_string(index=False))
            print("\nГрафик сохранен в docs/figures/Figure_sphere_error.png")
            pause()

        elif choice == "2":
            print("\nЗапуск калибровки на цилиндрах...")
            df = benchmark.run_cylinder_benchmark(fixed_h=5, d_min=4, d_max=24, step=4, save_plot=True)
            print("\n" + df.to_string(index=False))
            print("\nГрафик сохранен в docs/figures/Figure_cylinder_error.png")
            pause()

        elif choice == "3":
            print("\nВыполнение полного калибровочного бенчмарка...")
            df_s = benchmark.run_sphere_benchmark(save_plot=True)
            df_c = benchmark.run_cylinder_benchmark(save_plot=True)
            print("Сферы — средняя погрешность MC: {:.2f}%, Прямой метод: {:.2f}%".format(
                df_s["error_mc_pct"].mean(), df_s["error_pm_pct"].mean()
            ))
            print("Цилиндры — средняя погрешность MC: {:.2f}%, Прямой метод: {:.2f}%".format(
                df_c["error_mc_pct"].mean(), df_c["error_pm_pct"].mean()
            ))
            print("Все графики обновлены в каталоге docs/figures/")
            pause()


def menu_sorption():
    """Меню сорбционного анализа и гистерезиса."""
    analyzer = SorptionCorrelationAnalyzer()

    while True:
        print_header("📈 СОРБЦИОННЫЙ АНАЛИЗ И КОРРЕЛЯЦИЯ ГИСТЕРЕЗИСА")
        print("  [1] Анализ сорбционных изотерм и расчет корреляции Пирсона")
        print("  [2] Генерация графиков гистерезиса SSA и связности Z")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-2]: ").strip()

        if choice == "0":
            break
        elif choice in ("1", "2"):
            save = (choice == "2") or True
            res = analyzer.analyze_hysteresis(save_plots=save)
            print_header("РЕЗУЛЬТАТЫ КОРРЕЛЯЦИОННОГО АНАЛИЗА")
            print(f"  Корреляция Пирсона (ветвь адсорбции, SSA vs TriConnectivity): {res['pearson_correlation_ads']:.4f}")
            print(f"  Корреляция Пирсона (ветвь десорбции, SSA vs TriConnectivity): {res['pearson_correlation_des']:.4f}")
            print(f"  Количество экспериментальных точек: {res['points_ads']} (адс) / {res['points_des']} (дес)")
            print("\nГрафики гистерезиса сохранены:")
            print("  - docs/figures/Figure_hysteresis_SSA.png")
            print("  - docs/figures/Figure_hysteresis_Z.png")
            pause()


def menu_preprocessing():
    """Меню предобработки томографических данных."""
    finder = ThresholdFinder()
    rescaler = VolumeRescaler()

    while True:
        print_header("🔬 ПРЕДОБРАБОТКА ДАННЫХ И БИНАРИЗАЦИЯ")
        print("  [1] Подбор оптимального порога яркости по экспериментальной пористости")
        print("  [2] Автоматическая бинаризация среза алгоритмом Оцу")
        print("  [3] Пакетное ремасштабирование объема (исследование сеточной сходимости)")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-3]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = choose_structure()
            if not name:
                continue
            scale_str = input("Коэффициент масштабирования k (по умолчанию 1.0): ").strip()
            scale = float(scale_str) if scale_str else 1.0
            threshold = finder.find_threshold_for_structure(name, k_resize=scale)
            print(f"\nДля структуры {name} (масштаб k={scale}) оптимальный порог яркости: {threshold}")
            pause()

        elif choice == "2":
            name = choose_structure()
            if not name:
                continue
            struct = PorousStructure.load(name)
            slice_data = struct.voxels[struct.shape[0] // 2, :, :] * 255
            otsu_th = finder.otsu_threshold(slice_data)
            print(f"\nПорог Оцу для центрального среза структуры {name}: {otsu_th}")
            pause()

        elif choice == "3":
            name = choose_structure()
            if not name:
                continue
            confirm = input(f"Запустить ремасштабирование {name} для коэффициентов [0.70..0.95]? (y/n): ").strip().lower()
            if confirm == "y":
                created = rescaler.batch_rescale_structure(name)
                print(f"\nСоздано {len(created)} ремасштабированных наборов данных в папке:")
                print(f"{STRUCTURES_DIR}")
            pause()


def menu_subvolume():
    """Меню экспорта суб-объема для 3D просмотра."""
    while True:
        print_header("🧊 ЭКСПОРТ СУБ-ОБЪЕМА ДЛЯ 3D ВИЗУАЛИЗАЦИИ (ImageJ / 3D Viewer)")
        print("  [1] Экспорт октанта структуры (половина по каждой оси)")
        print("  [2] Экспорт кубического фрагмента заданного размера (например, 100x100x100)")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-2]: ").strip()

        if choice == "0":
            break
        elif choice in ("1", "2"):
            name = choose_structure()
            if not name:
                continue
            struct = PorousStructure.load(name)

            if choice == "1":
                hz, hy, hx = struct.shape[0] // 2, struct.shape[1] // 2, struct.shape[2] // 2
                sub = struct.extract_subvolume(origin=(hz, hy, hx), size=(hz, hy, hx), sub_name=f"{name}_octant")
            else:
                sz_str = input("Размер ребра куба в вокселях (по умолчанию 100): ").strip()
                sz = int(sz_str) if sz_str.isdigit() else 100
                sz = min(sz, min(struct.shape))
                sub = struct.extract_subvolume(origin=(0, 0, 0), size=(sz, sz, sz), sub_name=f"{name}_{sz}")

            out_dir = SRC_DIR.parent / "data" / "subvolumes" / sub.name
            count = sub.export_slices(output_dir=out_dir, file_format="tif")
            print(f"\nУспешно сохранено {count} срезов суб-объема {sub.shape} в:")
            print(f"{out_dir}")
            pause()


def run_selftest():
    """Автоматическое тестирование всех ключевых модулей комплекса."""
    print_header("🧪 АВТОМАТИЧЕСКАЯ САМОДИАГНОСТИКА КОМПЛЕКСА (SELF-TEST)")
    start_t = time.time()
    errors = []

    # 1. Тест загрузки структуры
    print("1. Тест загрузки и кэширования структуры Si12...", end=" ")
    try:
        struct = PorousStructure.load("Si12")
        assert struct.shape == (500, 650, 650), f"Неверная форма: {struct.shape}"
        assert abs(struct.porosity - 0.577) < 0.05, f"Неверная пористость: {struct.porosity}"
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"PorousStructure: {e}")

    # 2. Тест прямого метода (PM)
    print("2. Тест прямого воксельного метода...", end=" ")
    try:
        dm = DirectMethodCalculator()
        res_dm = dm.calculate(struct)
        assert res_dm.ssa_m2_g > 0, "SSA <= 0"
        print(f"OK (SSA = {res_dm.ssa_m2_g:.2f} м²/г)")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"DirectMethod: {e}")

    # 3. Тест Marching Cubes (модифицированный)
    print("3. Тест Marching Cubes с граничными поправками...", end=" ")
    try:
        mc = MarchingCubesCalculator(with_correction=True)
        res_mc = mc.calculate(struct)
        assert res_mc.ssa_m2_g > 0, "SSA <= 0"
        print(f"OK (SSA = {res_mc.ssa_m2_g:.2f} м²/г)")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"MarchingCubes: {e}")

    # 4. Тест скелетонов
    print("4. Тест анализа графов скелетонов...", end=" ")
    try:
        skel = SkeletonAnalyzer(skeletons_dir=SKELETONS_DIR)
        tau = skel.calculate_tortuosity("Si12")
        coord = skel.calculate_coordination("Si12")
        assert tau is not None and tau > 1.0, f"Некорректная тортуозность: {tau}"
        assert coord is not None and coord["z"] > 2.0, f"Некорректное Z: {coord}"
        print(f"OK (tau = {tau:.4f}, Z = {coord['z']:.4f})")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"SkeletonAnalyzer: {e}")

    # 5. Тест калибровочной сферы
    print("5. Тест аналитической геометрии (сфера)...", end=" ")
    try:
        sphere = SyntheticSphere(diameter_voxels=10, voxel_size=1.0, density=1.0)
        s_exact = sphere.analytical_surface_area()
        v_exact = sphere.analytical_volume()
        ssa_exact = sphere.analytical_ssa()
        assert abs(ssa_exact - 0.6) < 1e-6, f"Неверная аналитическая SSA: {ssa_exact}"
        print(f"OK (SSA_exact = {ssa_exact:.4f})")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"SyntheticSphere: {e}")

    # 6. Тест сорбционного анализа
    print("6. Тест корреляционного анализа гистерезиса...", end=" ")
    try:
        sorp = SorptionCorrelationAnalyzer()
        res_s = sorp.analyze_hysteresis(save_plots=False)
        assert res_s["pearson_correlation_ads"] > 0.9, "Слишком низкая корреляция"
        print(f"OK (r_ads = {res_s['pearson_correlation_ads']:.4f})")
    except Exception as e:
        print(f"FAIL: {e}")
        errors.append(f"SorptionAnalyzer: {e}")

    dt = time.time() - start_t
    print("─" * 84)
    if not errors:
        print(f" ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ за {dt:.2f} с! Комплекс полностью готов к работе.")
    else:
        print(f" ОБНАРУЖЕНО ОШИБОК: {len(errors)}")
        for err in errors:
            print(f"  - {err}")
    pause()


def menu_data_science():
    """Меню Data Science & Machine Learning пайплайна."""
    while True:
        print_header("🤖 DATA SCIENCE & MACHINE LEARNING ПАЙПЛАЙН (ФИНАЛЬНЫЙ ПРОЕКТ)")
        print("  [1] Сгенерировать / обновить датасет из 3D-томографии (CSV, 500+ строк)")
        print("  [2] Запустить полный цикл обучения и кросс-валидации моделей ML")
        print("  [3] Пересобрать интерактивный Jupyter Notebook (final_project_ds.ipynb)")
        print("  [4] Показать структуру и тезисы итоговой презентации проекта")
        print("  [0] Назад в главное меню")

        choice = input("\nВыберите действие [0-4]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\nЗапуск генератора датасета суб-объемов...")
            from data_science.dataset_generator import DatasetGenerator
            gen = DatasetGenerator()
            df = gen.generate(subvolume_size=100, max_samples_per_structure=45, verbose=True)
            print(f"\nДатасет обновлен: {len(df)} строк.")
            pause()
        elif choice == "2":
            print("\nЗапуск обучения моделей (Ridge, SVR, Random Forest, HistGBM, MLP)...")
            from data_science.model_trainer import run_full_pipeline
            run_full_pipeline()
            pause()
        elif choice == "3":
            print("\nСборка интерактивного Jupyter Notebook...")
            from data_science.notebook_generator import create_final_notebook
            p = create_final_notebook()
            print(f"\nНоутбук готов к запуску: {p}")
            pause()
        elif choice == "4":
            pres_file = SRC_DIR.parent / "docs" / "presentation" / "Data_Science_Final_Project_Presentation.md"
            if pres_file.exists():
                print_header("ТЕЗИСЫ И СТРУКТУРА ПРЕЗЕНТАЦИИ (docs/presentation)")
                lines = pres_file.read_text(encoding="utf-8").splitlines()
                for line in lines[:35]:
                    print(line)
                print(f"\n[Полный текст презентации доступен в файле: {pres_file}]")
            pause()


# ============================================================================
# Главное интерактивное меню
# ============================================================================

def interactive_main():
    """Запускает главное интерактивное меню."""
    while True:
        try:
            print_banner()
            print("\n  ГЛАВНОЕ МЕНЮ:")
            print("  ──────────────────────────────────────────────────────────────────────────")
            print("  [1] 📊 Расчет удельной площади поверхности (SSA: Marching Cubes & PM)")
            print("  [2] 🧬 Топологический анализ скелетонов (извилистость τ, узлы Z, W_3p)")
            print("  [3] 🎯 Калибровочные тесты на аналитических телах (сфера и цилиндр)")
            print("  [4] 📈 Сорбционный анализ и корреляция петель гистерезиса")
            print("  [5] 🔬 Предобработка томографических данных (порог пористости, Оцу, рескейл)")
            print("  [6] 🧊 Экспорт суб-объема для 3D визуализации (ImageJ 3D Viewer)")
            print("  [7] 🧪 Автоматическое самотестирование комплекса (Self-Test)")
            print("  [8] ⚖️  Сверка численной сходимости с архивными расчетами автора (2021)")
            print("  [9] 🤖 Data Science & Machine Learning пайплайн (Финальный проект)")
            print("  ──────────────────────────────────────────────────────────────────────────")
            print("  [0] 🚪 Выход из программы")

            choice = input("\nВыберите раздел [0-9]: ").strip()

            if choice == "0":
                print("\nРабота с программным комплексом завершена. До свидания!\n")
                break
            elif choice == "1":
                menu_ssa()
            elif choice == "2":
                menu_skeleton()
            elif choice == "3":
                menu_benchmark()
            elif choice == "4":
                menu_sorption()
            elif choice == "5":
                menu_preprocessing()
            elif choice == "6":
                menu_subvolume()
            elif choice == "7":
                run_selftest()
            elif choice == "8":
                from compare_results import compare_all
                compare_all()
                pause()
            elif choice == "9":
                menu_data_science()
            else:
                print("Некорректный ввод. Пожалуйста, введите цифру от 0 до 9.")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nПрерывание пользователем. Выход из программы.\n")
            break
        except Exception as e:
            print(f"\n[Ошибка выполнения]: {e}")
            pause()


# ============================================================================
# Точка входа в программу (CLI или Интерактивное Меню)
# ============================================================================

def main():
    """
    Единая точка входа:
    Если переданы аргументы командной строки — запускает CLI;
    Если аргументы отсутствуют — открывает интерактивное меню.
    """
    if len(sys.argv) > 1:
        # Импортируем CLI диспетчер
        from cli import main as cli_main
        cli_main()
    else:
        interactive_main()


if __name__ == "__main__":
    main()
