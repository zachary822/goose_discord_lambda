import logging.config
from pathlib import Path

import requests

from goose_discord_webhook.schemas import WebhookParams
from goose_discord_webhook.settings import Settings

with (Path(__file__).resolve().parent / "logging.conf").open("r") as f:
    logging.config.fileConfig(f)

logger = logging.getLogger(__name__)

settings = Settings()


def handler(event, context):
    resp = requests.post(
        settings.WEBHOOK_URL.get_secret_value(),
        data=WebhookParams(content="Riveting content!").json(),
        headers={"content-type": "application/json"},
    )
    logger.info("Status: %s Body: %s", resp.status_code, resp.text)

    return {"statusCode": 200, "body": ""}
