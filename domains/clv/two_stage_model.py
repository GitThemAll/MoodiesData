import os
import json
from datetime import datetime
from typing import Tuple, Dict
from lightgbm import LGBMClassifier, LGBMRegressor
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import joblib


class TwoStageCLVModel:
    """
    Two-stage CLV model with versioned persistence of models, metrics, and schema.
    """
    BASE_DIR: str = "clv_two_stage_models"
    VERSION_DIR: str = "versions"
    METRICS_FILE: str = "metrics.json"
    SCHEMA_FILE: str = "schema.json"

    target: str
    X_train: DataFrame
    X_test: DataFrame
    y_train: pd.Series
    y_test: pd.Series
    emails_train: pd.Series
    emails_test: pd.Series
    training_classifier: LGBMClassifier
    training_regressor: LGBMRegressor
    classifier: LGBMClassifier
    regressor: LGBMRegressor
    mae: float
    rmse: float
    r2: float
    version: str

    def __init__(self, training_data: DataFrame, target: str) -> None:
        self.target = target

        # Initialize training data holders
        self.X_train = DataFrame()
        self.X_test = DataFrame()
        self.y_train = pd.Series()
        self.y_test = pd.Series()

        # Initialize models with chosen hyperparameters
        self.training_classifier = LGBMClassifier(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.6,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        )
        self.training_regressor = LGBMRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.6,
            colsample_bytree=0.8,
            min_child_weight=5,
            random_state=42,
            n_jobs=-1,
        )

        # Metrics placeholders
        self.mae = 0.0
        self.rmse = 0.0
        self.r2 = 0.0

        # Perform train-test split
        self._split_data(training_data, target)

    def train(self) -> None:
        """
        Execute training, evaluation, and versioned saving of models, metrics, and schema.
        """
        self._fit()
        self._evaluate()
        self._save_models_and_metadata()
        # Load back latest version
        self.classifier, self.regressor = self._load_models(version=self.version)

    def _split_data(self, df: DataFrame, target: str) -> None:
        email_series = df["Email"]
        X = df.drop(columns=[target, "Email"])
        y = df[target]
        self.X_train, self.X_test, self.y_train, self.y_test, self.emails_train, self.emails_test = (
            train_test_split(X, y, email_series, test_size=0.2, random_state=42)
        )

    def _fit(self) -> None:
        # Stage 1: classification of spend > 0
        self.training_classifier.fit(self.X_train, self.y_train > 0)
        # Stage 2: regression on positive spenders
        mask = self.y_train > 0
        self.training_regressor.fit(self.X_train[mask], self.y_train[mask])

    def _evaluate(self) -> None:
        # Probabilities and amounts on test set
        y_prob = self.training_classifier.predict_proba(self.X_test)[:, 1]
        y_reg = self.training_regressor.predict(self.X_test)
        y_pred = y_prob * y_reg
        y_pred = y_pred.round()
        # Compute metrics
        self.mae = mean_absolute_error(self.y_test, y_pred)
        self.rmse = root_mean_squared_error(self.y_test, y_pred)
        self.r2 = r2_score(self.y_test, y_pred)

    def _save_models_and_metadata(self) -> None:
        # Create version identifier
        self.version = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        version_dir = os.path.join(self.BASE_DIR, self.VERSION_DIR, self.version)
        os.makedirs(version_dir, exist_ok=True, mode=0o755)

        # Save models
        clf_path = os.path.join(version_dir, 'classifier.pkl')
        reg_path = os.path.join(version_dir, 'regressor.pkl')
        joblib.dump(self.training_classifier, clf_path)
        joblib.dump(self.training_regressor, reg_path)

        # Save metrics
        metrics = self.get_metrics()
        with open(os.path.join(version_dir, self.METRICS_FILE), 'w') as f:
            json.dump(metrics, f)

        # Save schema: feature names and input shape
        schema = {
            'feature_names': list(self.X_train.columns),
            'input_shape': list(self.X_train.shape),
            'version': self.version
        }
        with open(os.path.join(version_dir, self.SCHEMA_FILE), 'w') as f:
            json.dump(schema, f)

    def get_metrics(self) -> Dict[str, float]:
        return {
            'mae': self.mae,
            'rmse': self.rmse,
            'r2': self.r2
        }

    def _load_models(self, version: str) -> Tuple[LGBMClassifier, LGBMRegressor]:
        version_dir = os.path.join(self.BASE_DIR, self.VERSION_DIR, version)
        clf = joblib.load(os.path.join(version_dir, 'classifier.pkl'))
        reg = joblib.load(os.path.join(version_dir, 'regressor.pkl'))
        return clf, reg

    def predict(self, customer_data: DataFrame) -> pd.DataFrame:
        emails = customer_data["Email"].reset_index(drop=True)
        features = customer_data.drop(columns=["Email"])
        prob_buy = self.classifier.predict_proba(features)[:, 1]
        expected_spend = self.regressor.predict(features)
        result = prob_buy * expected_spend
        result = result.round(2)
        return pd.DataFrame({
            "Email": emails,
            "Prediction": result
        })
