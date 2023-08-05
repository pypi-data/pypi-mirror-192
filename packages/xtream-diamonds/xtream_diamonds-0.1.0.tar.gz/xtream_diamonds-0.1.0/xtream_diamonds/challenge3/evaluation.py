import pandas as pd
from xgboost import XGBRegressor


def evaluate(
    estimator: XGBRegressor, samples: pd.DataFrame, targets: pd.Series
) -> float:
    return estimator.score(samples, targets)
