import json
import logging

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from pydantic import SecretBytes, ValidationError, validator

from goose_discord.schemas import Interaction
from goose_discord.settings import CustomBaseSettings

logger = logging.getLogger(__name__)


class Settings(CustomBaseSettings):
    PUBLIC_KEY: SecretBytes

    @validator("PUBLIC_KEY", pre=True)
    def convert_public_key(cls, v):
        return bytes.fromhex(v)

    class Config:
        parameter_path = "/discord"


settings = Settings()
verify_key = VerifyKey(settings.PUBLIC_KEY.get_secret_value())


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

    try:
        interaction: Interaction = Interaction.parse_raw(event["body"])

        if interaction.type == 1:
            return {
                "statusCode": 200,
                "body": json.dumps({"type": 1}),
                "headers": {
                    "Content-Type": "application/json",
                },
            }
        elif interaction.type == 2:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "type": 4,
                        "data": {
                            "content": "Riveting content!",
                        },
                    }
                ),
                "headers": {
                    "Content-Type": "application/json",
                },
            }
    except ValidationError:
        pass

    return {
        "statusCode": 400,
        "body": "",
    }
