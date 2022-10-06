import logging.config
from pathlib import Path

with (Path(__file__).resolve().parent.parent / "logging.conf").open("r") as f:
    logging.config.fileConfig(f)
