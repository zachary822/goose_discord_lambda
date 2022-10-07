from goose_discord.schemas import LambdaResponse


def handler(event, context):
    print(event)

    return LambdaResponse(
        status_code=200,
        body="",
    ).dict()
