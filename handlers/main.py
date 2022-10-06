import logging

import requests
from pydantic import SecretStr

from goose_discord.schemas import WebhookParams
from goose_discord.settings import CustomBaseSettings

logger = logging.getLogger(__name__)


class Settings(CustomBaseSettings):
    WEBHOOK_URL: SecretStr
    MESSAGE: str

    class Config:
        parameter_path = "/discord"


settings = Settings()


def handler(event, context):
    data = WebhookParams(
        content=settings.MESSAGE,
    )

    resp = requests.post(
        settings.WEBHOOK_URL.get_secret_value(),
        data=data.json(exclude_none=True),
        headers={"content-type": "application/json"},
    )

    if logger.isEnabledFor(logging.INFO):
        logger.info("Status: %s | Post Body: %s | Response Body: %s", resp.status_code, data.json(), resp.text)

    return {"statusCode": 200, "body": ""}
