import requests
from ra_engine.core.app import RAEApp
from ra_engine.type_def.ml import TrainData, PredData, MLData
import pandas as pd
from ra_engine.ml.evaluator import Evaluator


base = "/api/v1/ml/regression"


class Linear(Evaluator):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/mlr",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class GradientBoosting(Evaluator):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/gradboost",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class RandomForest(Evaluator):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/randomforest",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class ANN(Evaluator):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/ann",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )


class Logistic(Evaluator):
    def __init__(
        self,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        super().__init__(
            f"{base}/logr",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )
