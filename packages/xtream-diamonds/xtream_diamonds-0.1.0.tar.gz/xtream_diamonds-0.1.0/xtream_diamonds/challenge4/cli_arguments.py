import argparse
from typing import Tuple


def read_cli_arguments() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(
        prog="xtream-assignments-diamond",
        description="REST API Server for pricing diamonds",
        epilog="",
    )

    parser.add_argument("-m", "--model", required=True)
    parser.add_argument("-a", "--address", required=True)
    args = vars(parser.parse_args())

    model_path = args["model"]
    server_address = args["address"]
    if not model_path or not server_address:
        raise Exception(
            "Please pass both model path and server address arguments as -a and -m"
        )

    return model_path, server_address
