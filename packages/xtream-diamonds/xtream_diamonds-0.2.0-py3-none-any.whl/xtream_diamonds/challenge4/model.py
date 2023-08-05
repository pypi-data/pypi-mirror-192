#!/usr/bin/env python3

from typing import Optional
from xgboost import XGBRegressor


_model: Optional[XGBRegressor] = None


def load_model(path: str) -> None:
    global _model
    _model = XGBRegressor()
    _model.load_model(path)
    print(_model)


def get_model() -> Optional[XGBRegressor]:
    return _model
