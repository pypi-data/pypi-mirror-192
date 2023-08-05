from xgboost import XGBRegressor


def save(model: XGBRegressor, path: str) -> None:
    model.save_model(path)
