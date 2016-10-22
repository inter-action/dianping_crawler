import os
from pathlib import Path

PROJECT_ROOT_PATH = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).resolve()

DATA_PATH = PROJECT_ROOT_PATH.joinpath("data")

LOG_PATH = PROJECT_ROOT_PATH.joinpath("log")

LOG_ENV_KEY = "LOGGER_LEVEL"




