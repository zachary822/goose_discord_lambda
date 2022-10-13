from enum import Enum
from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field, constr, validator
from pydantic.generics import GenericModel

if TYPE_CHECKING:
    JsonStr = Any
else:
    JsonStr = str


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


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0].casefold() + "".join(word.capitalize() for word in words[1:])


class LambdaResponse(BaseModel):
    status_code: int
    body: JsonStr
    headers: Optional[dict]

    @validator("body", pre=True)
    def convert_json(cls, v):
        if isinstance(v, str):
            return v
        return cls.__config__.json_dumps(v, default=cls.__json_encoder__)

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel

    def dict(self, *, by_alias=True, exclude_none=True, **kwargs):
        return super().dict(by_alias=by_alias, exclude_none=exclude_none, **kwargs)


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
    value: Any


class SlashCommand(BaseModel):
    id: str
    type: int
    name: str
    options: Optional[list[Option]]


class Message(BaseModel):
    id: str
    content: str


class ResolvedData(BaseModel):
    messages: dict[str, Message]


class InteractionData(BaseModel):
    id: str
    name: str
    resolved: ResolvedData
    target_id: str
    type: int


T = TypeVar("T")


class Interaction(GenericModel, Generic[T]):
    application_id: str
    app_permissions: Optional[str]
    id: str
    channel_id: str
    guild_id: str
    token: str
    type: int
    data: Optional[T]
    user: Optional[User]
    member: Optional[Member]
    version: int
