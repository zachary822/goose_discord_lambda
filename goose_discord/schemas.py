from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, SecretStr, constr


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


class Token(BaseModel):
    access_token: SecretStr
    expires_in: int
    scope: str
    token_type: str


class User(BaseModel):
    id: str
    avatar: Optional[str]
    avatar_decoration: Optional[str]
    public_flags: int
    username: str
    discriminator: str


class Member(BaseModel):
    user: User


class Option(BaseModel):
    type: int
    name: str
    value: str


class SlashCommand(BaseModel):
    id: str
    type: int
    name: str
    options: Optional[list[Option]]


class Interaction(BaseModel):
    application_id: str
    app_permissions: Optional[str]
    id: str
    token: str
    type: int
    data: Optional[Union[SlashCommand, dict]]
    user: Optional[User]
    member: Optional[Member]
    version: int
