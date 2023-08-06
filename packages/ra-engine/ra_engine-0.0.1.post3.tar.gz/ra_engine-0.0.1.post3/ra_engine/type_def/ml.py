import pandas as pd

class TrainData:
   def __init__(self, data: pd.DataFrame, features:list, targets:list, config: dict=None):
      self.data: dict = data.to_dict()
      self.features: list = features
      self.targets: list = targets
      self.config: dict = config

   def as_dict(self):
      return {
         "data": self.data,
         "features": self.features,
         "targets": self.targets,
         "config": self.config
      }

class PredData:
   def __init__(self, data: pd.DataFrame, config: dict=None):
      self.data: dict = data.to_dict()
      self.config: dict = config

   def as_dict(self):
      return {
         "data": self.data,
         "config": self.config
      }

class MLData:
   def __init__(self, train: TrainData, predict: PredData):
      self.train: TrainData = train
      self.predict: PredData = predict

   def as_dict(self):
      return {
         "train": self.train.as_dict(),
         "predict": self.predict.as_dict()
      }