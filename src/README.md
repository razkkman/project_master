# Программный комплекс численных методов магистерской диссертации

Программный комплекс разработан в рамках магистерской диссертации Ю.Ю. Пилипенко «Исследование взаимосвязи удельной площади поверхности с морфологией системы пор пористой среды» (БГУ, РФКТ, САиКМ, 2021). Комплекс оптимизирован для высокопроизводительных научных расчетов и реорганизован в модульную объектно-ориентированную (ООП) архитектуру с единым CLI-интерфейсом.

---

## 🏗 Модульная архитектура (ООП)

Исходный код разделен на функциональные пакеты с четким разделением ответственности (Single Responsibility & Interface Segregation):

```
src/
├── config.py                     # Централизованная конфигурация, пути и физические константы
├── main.py                       # Главная точка входа: интерактивное меню (TUI) и запуск CLI
├── cli.py                        # CLI диспетчер командной строки (argparse)
├── pyproject.toml                # Стандартная спецификация сборки и зависимостей проекта
├── requirements.txt              # Зависимости окружения Python
│
├── core/                         # Доменная модель пористой структуры
│   ├── __init__.py
│   └── structure.py              # Класс PorousStructure (3D воксели, пористость, кэширование, срезы)
│
├── methods/                      # Алгоритмы расчета удельной площади поверхности (SSA)
│   ├── __init__.py
│   ├── base.py                   # Интерфейс BaseSSACalculator и dataclass SSAResult
│   ├── marching_cubes.py         # MarchingCubesCalculator (классический и модифицированный с учетом потерь)
│   ├── direct_method.py          # DirectMethodCalculator (векторизованный подсчет переходов фаз)
│   └── tables/                   # Таблицы поиска и матрицы граничных поправок
│       ├── __init__.py
│       └── mc_tables.py          # LookupTable_v1_1 и матрицы коллизий M0, M1, M2 (16x16)
│
├── topology/                     # Топологический анализ графов скелетонов и сорбции
│   ├── __init__.py
│   ├── skeleton_analyzer.py      # SkeletonAnalyzer (извилистость τ, координационное число Z, плотность узлов W_3p)
│   └── sorption.py               # SorptionCorrelationAnalyzer (гистерезис изотерм, корреляция Пирсона)
│
├── synthetic/                    # Аналитические калибровочные тела и бенчмарки
│   ├── __init__.py
│   ├── shapes.py                 # Классы SyntheticSphere, SyntheticCylinder, BaseSyntheticShape
│   └── benchmark.py              # CalibrationBenchmark (сеточные тесты погрешности на сферах и цилиндрах)
│
├── preprocessing/                # Предобработка и трансформация 3D данных
│   ├── __init__.py
│   ├── threshold.py              # ThresholdFinder (подбор порога бинаризации по целевой пористости, Оцу)
│   └── rescale.py                # VolumeRescaler (исследование влияния разрешения при ремасштабировании)
│
├── pipeline/                     # Высокоуровневые конвейеры анализа
│   ├── __init__.py
│   └── ssa_pipeline.py           # SSAEvaluationPipeline (пакетный расчет 7 структур, сопоставление с БЭТ)
│
└── [Фасадные скрипты]            # 100% обратная совместимость с оригинальными именами файлов
    ├── MC_3D_v1_1.py             # Делегирует в MarchingCubesCalculator
    ├── Pryamoy_metod.py          # Делегирует в DirectMethodCalculator
    ├── Formirovanie_massiva_v1.py# Делегирует в PorousStructure.load()
    ├── MC_SSA_for_porous_structures.py # Делегирует в SSAEvaluationPipeline
    ├── Skeleton_tau.py           # Делегирует в SkeletonAnalyzer
    ├── Skeleton_Z.py             # Делегирует в SkeletonAnalyzer
    ├── Skeleton_junctions.py     # Делегирует в SkeletonAnalyzer
    ├── Test_algoritmov_v1.py     # Делегирует в CalibrationBenchmark
    ├── Gener_sfer.py             # Делегирует в SyntheticSphere
    ├── Gener_cylinder.py         # Делегирует в SyntheticCylinder
    ├── Relationship_between_Z_and_SSA.py # Делегирует в SorptionCorrelationAnalyzer
    ├── Proportion.py             # Делегирует в PorousStructure
    ├── Opredelenie_poroga.py     # Делегирует в ThresholdFinder
    ├── Rescale_v1.py             # Делегирует в VolumeRescaler
    └── For_3D_Viewer.py          # Делегирует в PorousStructure.extract_subvolume()
```

---

## ⚡ Оптимизации производительности

| Модуль | Исходное состояние | Векторизованное ООП решение | Ускорение |
| :--- | :--- | :--- | :--- |
| **Marching Cubes** | 4-кратные циклы; конкатенация строк; >3000 строк `if/elif` | 8-битное кодирование; $16 \times 16$ предрассчитанные матрицы $M_0, M_1, M_2$; векторизованные срезы | **в 1000–5000 раз** (26.4 млн кубов за 4.3 с вместо 70 мин) |
| **Direct Method** | 3 тройных цикла по 211 млн вокселей | Векторизованные срезы `np.count_nonzero(A[:, :, :-1] != A[:, :, 1:])` | **в 500 раз** (0.3 с вместо 3 мин) |
| **Structure I/O** | Попиксельная сборка; повторные `os.listdir` | Загрузка через Pillow + автокэширование в `.npy` | **в 150 раз** (0.1 с при чтении из кэша) |
| **Skeleton Analysis**| Итерации по строкам DataFrame | Векторизованная фильтрация графов через `value_counts()` | **в 300 раз** (20 мс вместо 5 мин) |

---

## 🎮 Главная точка входа и интерактивное меню (`main.py`)

Для интерактивной работы без необходимости запоминать команды и флаги запустите главный скрипт:

```bash
python src/main.py
```

Откроется терминальное меню выбора действий:
- **`[1] 📊 Расчет SSA`** — расчет по отдельной структуре или пакетно для всех 7 структур, детальная диагностика Marching Cubes, экспорт отчетов.
- **`[2] 🧬 Топологический анализ скелетонов`** — извилистость ветвей $\tau$, координационное число $Z$, распределение узлов ($\omega_3, \omega_4$), плотность $W_{3p}$.
- **`[3] 🎯 Калибровочные тесты`** — валидация алгоритмов на дискретизированных сферах и цилиндрах с точными аналитическими решениями.
- **`[4] 📈 Сорбционный анализ`** — сорбционный гистерезис, корреляция Пирсона между SSA и связностью мезопор.
- **`[5] 🔬 Предобработка данных`** — автоподбор порога бинаризации по пористости, метод Оцу, рескейлинг объема.
- **`[6] 🧊 Экспорт 3D суб-объема`** — нарезка октантов или кубических фрагментов для ImageJ 3D Viewer.
- **`[7] 🧪 Автодиагностика (Self-Test)`** — запуск полного цикла самопроверки всех подсистем комплекса.

---

## 🚀 Консольный режим CLI (`main.py` / `cli.py`)

Если переданы аргументы, скрипт автоматически работает в режиме консольной утилиты:

```bash
# 1. Расчет удельной площади поверхности (SSA) для всех структур или отдельной структуры:
python src/main.py ssa
python src/main.py ssa --structure Si12 --save

# 2. Топологический анализ графов скелетонов (извилистость τ, число Z, плотность узлов W_3p):
python src/main.py skeleton
python src/main.py skeleton --structure SBA15 --metric all

# 3. Калибровочные тесты на синтетических аналитических телах:
python src/main.py benchmark --shape sphere --dmin 4 --dmax 24 --step 4
python src/main.py benchmark --shape cylinder --height 5

# 4. Анализ гистерезиса сорбции и расчет корреляции Пирсона:
python src/main.py sorption

# 5. Определение оптимального порога бинаризации по целевой пористости:
python src/main.py porosity --structure Si12 --scale 1.0

# 6. Извлечение суб-объема для 3D Viewer / ImageJ:
python src/main.py subvolume --structure Coreshell9 --size 100
```

---

## 🔄 Использование в Python-коде (ООП API)

```python
from core.structure import PorousStructure
from methods.marching_cubes import MarchingCubesCalculator
from methods.direct_method import DirectMethodCalculator
from topology.skeleton_analyzer import SkeletonAnalyzer

# 1. Загрузка пористой структуры
struct = PorousStructure.load("Si12")
print(f"Структура: {struct.name}, пористость: {struct.porosity:.3f}")

# 2. Расчет удельной площади поверхности модифицированным Marching Cubes
mc_calc = MarchingCubesCalculator(with_correction=True)
result_mc = mc_calc.calculate(struct)
print(result_mc.summary())

# 3. Расчет прямым воксельным методом
dm_calc = DirectMethodCalculator()
result_dm = dm_calc.calculate(struct)
print(result_dm.summary())

# 4. Анализ скелетона
skel = SkeletonAnalyzer()
print(f"Тортуозность τ: {skel.calculate_tortuosity('Si12'):.4f}")
print(f"Координационное число Z: {skel.calculate_coordination('Si12')['z']:.4f}")
```

Все исторические скрипты в корне `src/` (`MC_3D_v1_1.py`, `Pryamoy_metod.py`, `Skeleton_tau.py`, `MC_SSA_for_porous_structures.py`) продолжают работать как тонкие фасады без изменения сигнатур функций.
