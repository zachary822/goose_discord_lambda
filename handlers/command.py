import json
import logging
from secrets import choice

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from pydantic import Json, SecretBytes, ValidationError, validator

from goose_discord.schemas import Interaction, LambdaResponse, SlashCommand
from goose_discord.settings import CustomBaseSettings

logger = logging.getLogger(__name__)


class Settings(CustomBaseSettings):
    PUBLIC_KEY: SecretBytes
    QUOTES: Json[list[str]]

    @validator("PUBLIC_KEY", pre=True)
    def convert_public_key(cls, v):
        return bytes.fromhex(v)

    class Config:
        parameter_path = "/discord"


settings = Settings()
verify_key = VerifyKey(settings.PUBLIC_KEY.get_secret_value())

events = boto3.client("events")


def handler(event, context):
    if logger.isEnabledFor(logging.INFO):
        logger.info(json.dumps(event))

    try:
        verify_key.verify(
            (event["headers"]["x-signature-timestamp"] + event["body"]).encode(),
            bytes.fromhex(event["headers"]["x-signature-ed25519"]),
        )
    except BadSignatureError:
        return {
            "statusCode": 401,
            "body": json.dumps("invalid request signature"),
            "headers": {
                "Content-Type": "application/json",
            },
        }

    events.put_events(
        Entries=[
            {
                "Source": "discord-lambda",
                "DetailType": "discord.interaction",
                "Detail": event["body"],
                "TraceHeader": event["headers"]["x-amzn-trace-id"],
            }
        ]
    )

    try:
        interaction: Interaction = Interaction.parse_raw(event["body"])

        match interaction:
            case Interaction(type=1):
                return LambdaResponse(
                    status_code=200,
                    body={
                        "type": 1,
                    },
                    headers={
                        "Content-Type": "application/json",
                    },
                ).dict()
            case Interaction(type=2, data=SlashCommand(name="fun")):
                return LambdaResponse(
                    status_code=200,
                    body={
                        "type": 4,
                        "data": {
                            "content": "Riveting content!",
                        },
                    },
                    headers={
                        "Content-Type": "application/json",
                    },
                ).dict()
            case Interaction(type=2, data=SlashCommand(name="quotes")):
                quote = choice(settings.QUOTES)
                logger.info("Quote: %s", quote)

                return LambdaResponse(
                    status_code=200,
                    body={
                        "type": 4,
                        "data": {
                            "content": f"> {quote}",
                        },
                    },
                    headers={
                        "Content-Type": "application/json",
                    },
                ).dict()
    except ValidationError:
        pass

    return {
        "statusCode": 400,
        "body": "",
    }
