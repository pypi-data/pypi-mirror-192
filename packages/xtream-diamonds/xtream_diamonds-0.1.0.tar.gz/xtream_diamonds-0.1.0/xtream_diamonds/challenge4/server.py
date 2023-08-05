#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn


def start_server(
    app: FastAPI, host_address: str, port: int, log_level: str = "info"
) -> None:
    uvicorn.run(app, host=host_address, port=port, log_level=log_level)
