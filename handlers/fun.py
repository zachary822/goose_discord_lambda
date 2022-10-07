import logging

import requests

from goose_discord.schemas import Interaction, LambdaResponse

logger = logging.getLogger(__name__)


def handler(event, context):
    interaction = Interaction(**event["detail"])

    if logger.isEnabledFor(logging.INFO):
        logger.info("Interaction: %s", interaction.json())

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": "Riveting content!",
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
