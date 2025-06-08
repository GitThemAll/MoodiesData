from typing import Tuple, Dict
from lightgbm import LGBMClassifier, LGBMRegressor
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import joblib

class TwoStageCLVModel:
    # Class constants for model save paths
    CLASSIFIER_PATH: str = "clv_2_stage_classifier.pkl"
    REGRESSOR_PATH: str = "clv_2_stage_regressor.pkl"

    # Class-level variable declarations (for type hinting & clarity)
    target: str
    X_train: DataFrame
    X_test: DataFrame
    y_train: pd.Series
    y_test: pd.Series
    emails_train: pd.Series
    emails_test:  pd.Series
    classifier: LGBMClassifier
    regressor: LGBMRegressor
    mae: float
    rmse: float
    r2: float

    def __init__(self, training_data: DataFrame, target: str) -> None:
        self.target = target

        self.X_train = DataFrame()
        self.X_test = DataFrame()
        self.y_train = DataFrame()
        self.y_test = DataFrame()

        self.classifier = LGBMClassifier(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.6,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        )
        self.regressor = LGBMRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.6,
            colsample_bytree=0.8,
            min_child_weight=5,
            random_state=42,
            n_jobs=-1,
        )

        self.mae = 0.0
        self.rmse = 0.0
        self.r2 = 0.0

        self._split_data(training_data, target)

    def train(self) -> Tuple[str, str]:
        self._fit()
        self._evaluate()
        self._save_models()
        return self.CLASSIFIER_PATH, self.REGRESSOR_PATH

    def _split_data(self, df: DataFrame, target: str) -> None:
        email_series = df["Email"]
        X = df.drop(columns=[target, "Email"])
        y = df[target]

        self.X_train, self.X_test, self.y_train, self.y_test, self.emails_train, self.emails_test = train_test_split(
            X, y, email_series, test_size=0.2, random_state=42
        )

    def _fit(self) -> None:
        self.classifier.fit(self.X_train, self.y_train > 0)
        self.regressor.fit(self.X_train[self.y_train > 0], self.y_train[self.y_train > 0])

    def _evaluate(self) -> None:
        y_prob: np.ndarray = self.classifier.predict_proba(self.X_test)[:, 1]
        y_reg: np.ndarray = self.regressor.predict(self.X_test)
        y_pred: np.ndarray = y_prob * y_reg

        self.mae = mean_absolute_error(self.y_test, y_pred)
        self.rmse = root_mean_squared_error(self.y_test, y_pred)
        self.r2 = r2_score(self.y_test, y_pred)

    def _save_models(self) -> None:
        joblib.dump(self.classifier, self.CLASSIFIER_PATH)
        joblib.dump(self.regressor, self.REGRESSOR_PATH)

    def get_metrics(self) -> Dict[str, float]:
        return {
            "mae": self.mae,
            "rmse": self.rmse,
            "r2": self.r2
        }

    @classmethod
    def load_models(cls) -> Tuple[LGBMClassifier, LGBMRegressor]:
        clf: LGBMClassifier = joblib.load(cls.CLASSIFIER_PATH)
        reg: LGBMRegressor = joblib.load(cls.REGRESSOR_PATH)
        return clf, reg