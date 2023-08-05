from pydantic import Field

from ..models import OneOfConfigAbstractChildBase


class AuthConfigBase(OneOfConfigAbstractChildBase):
    const_field_name = "auth_type"


class AccessTokenAuthConfig(AuthConfigBase):
    auth_type: str = Field(default="access_token_auth", const=True)
    access_token: str = Field(
        title="Access Token",
        description="Long-term access token used for authorization",
        airbyte_secret=True,
    )


class CredentialsCraftAuthConfig(AuthConfigBase):
    auth_type: str = Field(default="credentials_craft_auth", const=True)
    credentials_craft_host: str = Field(
        title="CredentialsCraft Host",
        description="CredentialsCraft Host",
        regex="https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
    )
    credentials_craft_token: str = Field(
        title="CredentialsCraft Token",
        description="Long-term CredentialsCraft Access Token",
        airbyte_secret=True,
    )
    credentials_craft_token_id: int = Field(
        title="Token ID In CredentialsCraft",
        description="Token ID in CredentialsCraft",
        examples=[123],
        minimum=0,
    )
