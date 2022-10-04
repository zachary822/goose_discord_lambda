from goose_discord_webhook.settings import Settings

settings = Settings()


def handler(event, context):
    print(settings)

    return {
        "statusCode": 200,
        "body": ""
    }
