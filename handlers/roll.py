import logging
import re
import secrets
from functools import cached_property

import requests
from pydantic import constr

from goose_discord.schemas import Interaction, LambdaResponse, Option, SlashCommand


class Die(Option):
    value: constr(regex=re.compile(r"^d\d+$", flags=re.I))  # type: ignore[valid-type]  # noqa: F722

    @cached_property
    def sides(self) -> int:
        return int(self.value[1:])

    class Config:
        frozen = True


logger = logging.getLogger(__name__)


def handler(event, context):
    interaction = Interaction[SlashCommand[tuple[Option[int], Die]]](**event["detail"])
    number, die = interaction.data.options

    if logger.isEnabledFor(logging.INFO):
        logger.info("Interaction: %s", interaction.json())

    random = secrets.SystemRandom()

    with requests.Session() as session:
        resp = session.patch(
            f"https://discord.com/api/webhooks/{interaction.application_id}/{interaction.token}/messages/@original",
            json={
                "content": f"dice rolls ({number}{die.value}): {' '.join(map(str, (random.randint(1, die.sides + 1) for _ in range(number))))}",  # noqa: E501
            },
        )
        logger.info("status: %s body: %s", resp.status_code, resp.text)

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
