import requests

from goose_discord.schemas import Interaction, LambdaResponse


def handler(event, context):
    interaction = Interaction(**event["detail"])

    with requests.Session() as session:
        resp = session.post(
            f"https://discord.com/api/v10/interactions/{interaction.id}/{interaction.token}/callback",
            json={
                "type": 4,
                "content": "Riveting content!",
            },
        )

    return LambdaResponse(
        status_code=resp.status_code,
        body=resp.text,
    ).dict()
