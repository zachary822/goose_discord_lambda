import json
import logging

import boto3
import requests

from goose_discord.schemas import Interaction, LambdaResponse

logger = logging.getLogger(__name__)

comprehend = boto3.client("comprehend")


def handler(event, context):
    if logger.isEnabledFor(logging.INFO):
        logger.info("Event: %s", json.dumps(event))

    interaction = Interaction(**event["detail"])

    message = interaction.data.resolved.messages[interaction.data.target_id]

    result = comprehend.detect_sentiment(Text=message.content, LanguageCode="en")

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": (
                    f"Sentiment: {result['Sentiment']}\n"
                    + f"Scores: Positive: {result['SentimentScore']['Positive']} | "
                    + f"Negative: {result['SentimentScore']['Negative']} | "
                    + f"Neutral: {result['SentimentScore']['Neutral']} | "
                    + f"Mixed: {result['SentimentScore']['Mixed']}\n"
                    + f"original: https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{message.id}"  # noqa: E501
                ),
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=200,
        body="",
    ).dict()
