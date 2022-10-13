import json
import logging

import boto3
import requests

from goose_discord.schemas import Interaction, InteractionData, LambdaResponse

logger = logging.getLogger(__name__)

comprehend = boto3.client("comprehend")


def handler(event, context):
    if logger.isEnabledFor(logging.INFO):
        logger.info("Event: %s", json.dumps(event))

    interaction = Interaction[InteractionData](**event["detail"])

    message = interaction.data.resolved.messages[interaction.data.target_id]

    result = comprehend.detect_sentiment(Text=message.content, LanguageCode="en")

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": (
                    f"Sentiment: {result['Sentiment']}\n"
                    f"Scores:\n"
                    f"  Positive: {result['SentimentScore']['Positive']}\n"
                    f"  Negative: {result['SentimentScore']['Negative']}\n"
                    f"  Neutral: {result['SentimentScore']['Neutral']}\n"
                    f"  Mixed: {result['SentimentScore']['Mixed']}\n"
                    f"original: https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{message.id}"  # noqa: E501
                ),
                "flags": 1 << 6,
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=200,
        body="",
    ).dict()
