import logging
from secrets import choice

import requests
from pydantic import Json

from goose_discord.schemas import Interaction, LambdaResponse
from goose_discord.settings import CustomBaseSettings

logger = logging.getLogger(__name__)


class Settings(CustomBaseSettings):
    QUOTES: Json[list[str]]

    class Config:
        parameter_path = "/discord"


settings = Settings()


def handler(event, context):
    interaction = Interaction(**event["detail"])

    if logger.isEnabledFor(logging.INFO):
        logger.info("Interaction: %s", interaction.json())

    quote = choice(settings.QUOTES)
    logger.info("Quote: %s", quote)

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": f"> {quote}",
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
