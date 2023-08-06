import requests
from ra_engine.core.app import RAEApp
from ra_engine.type_def.ml import TrainData, PredData, MLData
import pandas as pd


class BaseRegression:
    base_url = "/api/v1/ml/time-series/"

    def __init__(
        self,
        model: str,
        app: RAEApp,
        train_df: pd.DataFrame,
        pred_df: pd.DataFrame,
        features: list,
        targets: list,
        train_config: dict = None,
        pred_config: dict = None,
    ):
        self.rae_app: RAEApp = app
        self.ml_data = MLData(
            TrainData(train_df, features, targets, train_config),
            PredData(pred_df, pred_config),
        )
        self._app = app.app()
        self._json = None
        self.model = model
        if self._app is None:
            raise ValueError("RAEApp is not initialized. Please run app.init() first.")
        if self._app.result is None:
            raise ValueError(
                "Provided RAEApp is not authenticated properly. Please check your credentials."
            )
        self.run()

    def run(self):
        response = requests.get(
            self.rae_app.credentials.host + self.base_url + self.model,
            json=self.ml_data.as_dict(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._app.result['jwt']}",
            },
        )
        self.response = response
        if response.status_code == 200:
            self._json = response.json()
        return response

    def inputs(self):
        return self.ml_data.as_dict()

    def result(self):
        return self._json

    def predictions(self, as_df=False):
        res = self._json.get("result", None)
        if res is not None and as_df:
            return pd.DataFrame(res)
        return res

    def scores(self):
        return self._json.get("score", None)

    def status_code(self):
        return self.response.status_code


class ARIMA(BaseRegression):
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
            "arima",
            app,
            train_df,
            pred_df,
            features,
            targets,
            train_config,
            pred_config,
        )
