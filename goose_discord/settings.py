from pathlib import PurePosixPath as Path
from typing import Any

import boto3
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable

client = boto3.client("ssm")


def parameter_store_settings(settings: BaseSettings) -> dict[str, Any]:
    try:
        prefix = Path(settings.__config__.parameter_path)  # type: ignore[attr-defined]
        names = [str(prefix / n) for n in settings.__fields__.keys()]
    except TypeError:
        prefix = None
        names = list(settings.__fields__.keys())

    response = client.get_parameters(
        Names=names,
        WithDecryption=True,
    )

    result = {}

    for param in response["Parameters"]:
        if prefix is not None:
            key = str(Path(param["Name"]).relative_to(prefix))
        else:
            key = param["Name"]
        result[key] = param["Value"]

    return result


class CustomBaseSettings(BaseSettings):
    class Config:
        parameter_path = None

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                parameter_store_settings,
                file_secret_settings,
            )
