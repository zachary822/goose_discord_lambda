from pydantic import BaseModel, constr


class WebhookParams(BaseModel):
    content: constr(strip_whitespace=True, max_length=2000)
