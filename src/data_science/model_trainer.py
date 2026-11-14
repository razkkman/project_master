"""
Пайплайн машинного обучения для предсказания удельной площади поверхности (SSA_BET).
Реализует полный цикл Data Science:
  1. Загрузка данных и исследовательский анализ (EDA)
  2. Предобработка, масштабирование (StandardScaler) и PCA
  3. Обучение линейных, ансамблевых моделей и нейронной сети (MLP)
  4. Кросс-валидация и подбор гиперпараметров
  5. Сравнение метрик (R², MAE, RMSE, MAPE)
  6. Анализ важности признаков (Feature Importance)
  7. Анализ ошибок и остатков (Residual Analysis)
  8. Экспорт лучшей модели и визуализаций для отчета/презентации
"""

from pathlib import Path
import sys
import time
import json
import pickle
from typing import Dict, Any, Tuple, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, KFold, cross_validate, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

# Пути
SRC_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SRC_DIR.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "porous_materials_ml_dataset.csv"
FIG_ML_DIR = PROJECT_ROOT / "docs" / "figures" / "ml"
MODEL_SAVE_DIR = PROJECT_ROOT / "data" / "models"


class MLModelTrainer:
    """Оркестратор машинного обучения для прогнозирования свойств пористых сред."""

    def __init__(self, data_path: Path = DATA_PATH):
        self.data_path = data_path
        FIG_ML_DIR.mkdir(parents=True, exist_ok=True)
        MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)
        self.feature_cols = [
            "porosity",
            "solid_fraction",
            "voxel_size_nm",
            "ssa_mc_modified",
            "ssa_mc_classical",
            "ssa_direct_method",
            "mc_direct_ratio",
            "clas_mod_ratio",
            "corr_share_z",
            "corr_share_y",
            "corr_share_x",
            "tortuosity_tau",
            "coordination_z",
            "w3p_density_10e25",
            "omega_3p",
            "omega_4p",
            "omega_other",
        ]
        self.target_col = "ssa_bet_target"
        self.scaler = StandardScaler()
        self.models: Dict[str, Any] = {}
        self.results: Dict[str, Dict[str, float]] = {}
        self.best_model_name: str = ""
        self.best_model: Any = None

    def load_and_preprocess(self) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Загрузка, аудит и разбиение данных на Train / Test."""
        print("=" * 80)
        print("  1. ЗАГРУЗКА И ПРЕДОБРАБОТКА ДАННЫХ (DATA PREPROCESSING)")
        print("=" * 80)
        df = pd.read_csv(self.data_path)
        print(f"Размер датасета: {df.shape[0]} строк, {df.shape[1]} признаков.")
        print(f"Пропущенных значений (NaN): {df.isna().sum().sum()}")
        print(f"Дубликатов: {df.duplicated().sum()}")
        print(f"Уникальных материалов: {df['material'].nunique()} ({list(df['material'].unique())})")

        X = df[self.feature_cols].copy()
        y = df[self.target_col].values

        # 80/20 train/test split
        X_train_raw, X_test_raw, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, shuffle=True
        )

        # Масштабирование признаков
        X_train = self.scaler.fit_transform(X_train_raw)
        X_test = self.scaler.transform(X_test_raw)

        print(f"Обучающая выборка (Train): {X_train.shape[0]} объектов")
        print(f"Тестовая выборка (Test):   {X_test.shape[0]} объектов")

        self.df = df
        self.X_train_raw = X_train_raw
        self.X_test_raw = X_test_raw
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        return df, X_train, X_test, y_train, y_test

    def generate_eda_visualizations(self):
        """Формирование визуализаций исследовательского анализа данных (EDA)."""
        print("\n" + "=" * 80)
        print("  2. ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ ДАННЫХ (EDA VISUALIZATIONS)")
        print("=" * 80)
        df = self.df

        # 1. Корреляционная матрица (Heatmap)
        plt.figure(figsize=(12, 10), dpi=150)
        corr_cols = self.feature_cols[:12] + [self.target_col]
        corr = df[corr_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
        plt.title("Корреляционная матрица признаков и целевой переменной (SSA BET)", fontsize=12, fontweight="bold", pad=14)
        plt.tight_layout()
        corr_path = FIG_ML_DIR / "eda_correlation_matrix.png"
        plt.savefig(corr_path, bbox_inches="tight")
        plt.close()
        print(f" [EDA 1/4] Корреляционная матрица сохранена: {corr_path.name}")

        # 2. Распределение пористости и SSA по материалам
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)
        sns.boxplot(data=df, x="material", y="porosity", hue="material", palette="Set2", ax=axes[0], legend=False)
        axes[0].set_title("Вариация пористости суб-объемов по материалам", fontsize=11, fontweight="bold", pad=10)
        axes[0].tick_params(axis="x", rotation=30)
        axes[0].grid(True, linestyle="--", alpha=0.5)

        sns.boxplot(data=df, x="material", y="ssa_mc_modified", hue="material", palette="Set3", ax=axes[1], legend=False)
        axes[1].set_title("Распределение удельной площади Marching Cubes", fontsize=11, fontweight="bold", pad=10)
        axes[1].tick_params(axis="x", rotation=30)
        axes[1].grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        dist_path = FIG_ML_DIR / "eda_distributions.png"
        plt.savefig(dist_path, bbox_inches="tight")
        plt.close()
        print(f" [EDA 2/4] Распределения по материалам сохранены: {dist_path.name}")

        # 3. PCA проекция (снижение размерности до 2 главнейших компонент)
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(self.scaler.transform(df[self.feature_cols]))
        df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
        df_pca["morphology"] = df["morphology_type"].values

        plt.figure(figsize=(9, 6), dpi=150)
        sns.scatterplot(
            data=df_pca, x="PC1", y="PC2", hue="morphology",
            style="morphology", s=70, alpha=0.85, palette="tab10"
        )
        plt.title(
            f"PCA-проекция пористых сред (Объясненная дисперсия: {pca.explained_variance_ratio_.sum() * 100:.1f}%)",
            fontsize=12, fontweight="bold", pad=14
        )
        plt.xlabel(f"Главная компонента 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)", fontsize=11)
        plt.ylabel(f"Главная компонента 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        pca_path = FIG_ML_DIR / "eda_pca_clusters.png"
        plt.savefig(pca_path, bbox_inches="tight")
        plt.close()
        print(f" [EDA 3/4] Проекция PCA сохранена: {pca_path.name}")

        # 4. Сопоставление Marching Cubes vs Физ. эксперимент БЭТ
        plt.figure(figsize=(9, 6), dpi=150)
        sns.scatterplot(
            data=df, x="ssa_mc_modified", y="ssa_bet_target", hue="material",
            s=65, alpha=0.85, palette="tab10"
        )
        max_val = max(df["ssa_mc_modified"].max(), df["ssa_bet_target"].max()) * 1.05
        plt.plot([0, max_val], [0, max_val], "k--", lw=1.5, label="Идеальное совпадение (y = x)")
        plt.title("Расчет Marching Cubes против физического эксперимента БЭТ", fontsize=12, fontweight="bold", pad=14)
        plt.xlabel("Расчетное значение SSA Marching Cubes (м²/г)", fontsize=11, labelpad=8)
        plt.ylabel("Истинное физическое значение БЭТ (м²/г)", fontsize=11, labelpad=8)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        scatter_path = FIG_ML_DIR / "eda_bet_vs_mc.png"
        plt.savefig(scatter_path, bbox_inches="tight")
        plt.close()
        print(f" [EDA 4/4] График MC vs БЭТ сохранен: {scatter_path.name}")

    def train_and_evaluate_models(self) -> pd.DataFrame:
        """Обучение и сравнительная оценка моделей машинного обучения."""
        print("\n" + "=" * 80)
        print("  3. ОБУЧЕНИЕ И КРОСС-ВАЛИДАЦИЯ МОДЕЛЕЙ (MODEL TRAINING)")
        print("=" * 80)

        model_candidates = {
            "Линейная регрессия (Ridge)": Ridge(alpha=1.0, random_state=42),
            "Метод опорных векторов (SVR)": SVR(C=10.0, epsilon=0.1),
            "Случайный лес (Random Forest)": RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1),
            "Градиентный бустинг (HistGBM)": HistGradientBoostingRegressor(max_iter=150, max_depth=6, random_state=42),
            "Нейросеть (MLP Regressor)": MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42, early_stopping=True),
        }

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        records = []

        print(f"{'Модель':<30} | {'CV R² (mean)':<14} | {'Test R²':<10} | {'Test MAE':<10} | {'Test MAPE':<11} | {'Время, с':<8}")
        print("-" * 95)

        for name, model in model_candidates.items():
            t0 = time.time()
            # 5-Fold Cross Validation
            cv_scores = cross_validate(model, self.X_train, self.y_train, cv=kf, scoring="r2", n_jobs=-1)
            cv_r2_mean = float(np.mean(cv_scores["test_score"]))

            # Финальное обучение на train и оценка на отложенном test
            model.fit(self.X_train, self.y_train)
            dt = time.time() - t0

            y_pred = model.predict(self.X_test)
            r2 = float(r2_score(self.y_test, y_pred))
            mae = float(mean_absolute_error(self.y_test, y_pred))
            rmse = float(np.sqrt(mean_squared_error(self.y_test, y_pred)))
            mape = float(mean_absolute_percentage_error(self.y_test, y_pred) * 100.0)

            self.models[name] = model
            self.results[name] = {
                "cv_r2_mean": cv_r2_mean,
                "test_r2": r2,
                "test_mae": mae,
                "test_rmse": rmse,
                "test_mape": mape,
                "time_sec": dt,
            }

            records.append({
                "model": name,
                "cv_r2_mean": cv_r2_mean,
                "test_r2": r2,
                "test_mae": mae,
                "test_rmse": rmse,
                "test_mape": mape,
                "time_sec": dt,
            })

            print(
                f"{name:<30} | "
                f"{cv_r2_mean:<14.4f} | "
                f"{r2:<10.4f} | "
                f"{mae:<10.2f} | "
                f"{mape:<10.2f}% | "
                f"{dt:<8.2f}"
            )

        # Добавим для сравнения базовую точность чистого Marching Cubes (без ML)
        mc_pred = self.X_test_raw["ssa_mc_modified"].values
        mc_r2 = r2_score(self.y_test, mc_pred)
        mc_mae = mean_absolute_error(self.y_test, mc_pred)
        mc_mape = mean_absolute_percentage_error(self.y_test, mc_pred) * 100.0
        print("-" * 95)
        print(f"{'[BASELINE] Marching Cubes (чистый)':<30} | {'—':<14} | {mc_r2:<10.4f} | {mc_mae:<10.2f} | {mc_mape:<10.2f}% | {'0.00':<8}")

        df_res = pd.DataFrame(records)

        # Выбор лучшей модели по Test R²
        best_row = df_res.sort_values(by="test_r2", ascending=False).iloc[0]
        self.best_model_name = best_row["model"]
        self.best_model = self.models[self.best_model_name]

        print(f"\n ЛУЧШАЯ МОДЕЛЬ: {self.best_model_name} (R² = {best_row['test_r2']:.4f}, MAPE = {best_row['test_mape']:.2f}%)")

        # Сохранение лучшей модели
        model_file = MODEL_SAVE_DIR / "best_ssa_regressor.pkl"
        with open(model_file, "wb") as f:
            pickle.dump({
                "model": self.best_model,
                "scaler": self.scaler,
                "feature_cols": self.feature_cols,
                "best_model_name": self.best_model_name,
                "metrics": self.results[self.best_model_name],
            }, f)
        print(f" Модель сохранена в: {model_file.name}")

        return df_res

    def analyze_feature_importance_and_residuals(self):
        """Анализ важности признаков и остатков (Residual Analysis)."""
        print("\n" + "=" * 80)
        print("  4. ИНТЕРПРЕТАЦИЯ И АНАЛИЗ ОШИБОК (INTERPRETATION & RESIDUALS)")
        print("=" * 80)

        # 1. Feature Importance для Random Forest
        rf = self.models.get("Случайный лес (Random Forest)")
        if rf and hasattr(rf, "feature_importances_"):
            importances = rf.feature_importances_
            feat_df = pd.DataFrame({
                "feature": self.feature_cols,
                "importance": importances,
            }).sort_values(by="importance", ascending=True)

            plt.figure(figsize=(10, 7), dpi=150)
            plt.barh(feat_df["feature"], feat_df["importance"], color="#1f77b4", alpha=0.85)
            plt.title("Важность признаков (Random Forest Feature Importance - MDI)", fontsize=12, fontweight="bold", pad=12)
            plt.xlabel("Относительная важность признака", fontsize=11, labelpad=8)
            plt.grid(True, linestyle="--", alpha=0.5, axis="x")
            plt.tight_layout()
            feat_path = FIG_ML_DIR / "feature_importance.png"
            plt.savefig(feat_path, bbox_inches="tight")
            plt.close()
            print(f" [Интерпретация 1/2] График важности признаков сохранен: {feat_path.name}")

            top3 = feat_df.tail(3)["feature"].tolist()
            print(f" Топ-3 ключевых фактора для прогнозирования SSA: {top3[::-1]}")

        # 2. График фактических и предсказанных значений + распределение остатков
        best_pred = self.best_model.predict(self.X_test)
        residuals = self.y_test - best_pred

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

        # А. Predicted vs Actual
        ax1.scatter(self.y_test, best_pred, color="#2ca02c", alpha=0.7, edgecolors="k", s=50)
        min_v = min(self.y_test.min(), best_pred.min()) * 0.9
        max_v = max(self.y_test.max(), best_pred.max()) * 1.05
        ax1.plot([min_v, max_v], [min_v, max_v], "r--", lw=2, label="Идеальный прогноз (y = x)")
        ax1.set_title(f"Фактическое vs Предсказанное SSA ({self.best_model_name})", fontsize=11, fontweight="bold", pad=10)
        ax1.set_xlabel("Фактическое значение БЭТ (м²/г)", fontsize=10, labelpad=6)
        ax1.set_ylabel("Предсказание модели (м²/г)", fontsize=10, labelpad=6)
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.5)

        # Б. Residuals Histogram
        sns.histplot(residuals, kde=True, color="#1f77b4", ax=ax2, bins=25)
        ax2.axvline(0, color="r", linestyle="--", lw=2)
        ax2.set_title("Распределение остатков модели (y_true - y_pred)", fontsize=11, fontweight="bold", pad=10)
        ax2.set_xlabel("Ошибка прогноза (м²/г)", fontsize=10, labelpad=6)
        ax2.set_ylabel("Плотность", fontsize=10, labelpad=6)
        ax2.grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        res_path = FIG_ML_DIR / "residuals_analysis.png"
        plt.savefig(res_path, bbox_inches="tight")
        plt.close()
        print(f" [Интерпретация 2/2] График анализа ошибок сохранен: {res_path.name}\n")


def run_full_pipeline():
    trainer = MLModelTrainer()
    trainer.load_and_preprocess()
    trainer.generate_eda_visualizations()
    df_metrics = trainer.train_and_evaluate_models()
    trainer.analyze_feature_importance_and_residuals()
    return trainer, df_metrics


if __name__ == "__main__":
    run_full_pipeline()
