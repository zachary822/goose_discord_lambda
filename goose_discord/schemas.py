from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, constr


class MentionType(str, Enum):
    roles = "roles"
    users = "users"
    everyone = "everyone"


class AllowedMentions(BaseModel):
    parse: list[MentionType]
    users: list[str] = Field(default_factory=list)


class WebhookParams(BaseModel):
    content: constr(strip_whitespace=True, max_length=2000)  # type: ignore[valid-type]
    allowed_mentions: Optional[AllowedMentions]
