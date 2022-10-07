import logging

import requests

from goose_discord.schemas import Interaction, LambdaResponse

logger = logging.getLogger(__name__)


def handler(event, context):
    interaction = Interaction(**event["detail"])
    logging.info(interaction)

    with requests.Session() as session:
        resp = session.post(
            f"https://discord.com/api/v10/interactions/{interaction.id}/{interaction.token}/callback",
            json={
                "type": 4,
                "data": {
                    "content": "Riveting content!",
                },
            },
        )
        logging.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
