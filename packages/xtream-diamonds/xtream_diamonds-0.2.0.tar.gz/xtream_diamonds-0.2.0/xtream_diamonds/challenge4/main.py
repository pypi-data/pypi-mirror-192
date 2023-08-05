from typing import Optional
from fastapi import FastAPI
from xgboost import XGBRegressor

from .parsing import parse_address
from .endpoints import prices_endpoint, root_endpoint
from .cli_arguments import read_cli_arguments
from .server import start_server
from .model import load_model
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from collections import defaultdict
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.include_router(prices_endpoint.router)
app.include_router(root_endpoint.router)


def main():
    model_path, server_address = read_cli_arguments()

    load_model(model_path)

    address, port = parse_address(server_address)

    start_server(app, address, port)


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    # https://stackoverflow.com/questions/58642528/displaying-of-fastapi-validation-errors-to-end-users
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )
