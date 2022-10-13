import logging

import boto3
import requests

from goose_discord.schemas import Interaction, LambdaResponse, Option, SlashCommand

logger = logging.getLogger(__name__)

kms = boto3.client("kms")


def handler(event, context):
    interaction = Interaction[SlashCommand[tuple[Option[int], Option[str]]]](**event["detail"])
    number, dice = interaction.data.options

    print(number, dice)

    if logger.isEnabledFor(logging.INFO):
        logger.info("Interaction: %s", interaction.json())

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": "dice roll!",
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
