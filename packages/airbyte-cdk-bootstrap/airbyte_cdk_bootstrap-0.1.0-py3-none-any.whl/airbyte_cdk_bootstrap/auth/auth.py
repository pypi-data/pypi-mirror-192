from typing import Any, Mapping

import requests
from airbyte_cdk.sources.streams.http.requests_native_auth import \
    TokenAuthenticator
from airbyte_cdk.sources.streams.http.requests_native_auth.abstract_token import \
    AbstractHeaderAuthenticator

from .exceptions import CredentialsCraftApiError
from abc import abstractmethod, ABC

class AbstractCredentialsCraftAuthenticator(AbstractHeaderAuthenticator, ABC):
    @property
    @abstractmethod
    def service_name_in_cc(self) -> str:
        pass

    def __init__(
        self,
        credentials_craft_host: str,
        credentials_craft_token: str,
        credentials_craft_token_id: int,
    ):
        self._cc_host = credentials_craft_host.rstrip("/")
        self._cc_token = credentials_craft_token
        self._cc_token_id = credentials_craft_token_id
        self._auth_header = "Bearer"
        self._auth_method = "Authorization"
        self._token: str | None = None

    @property
    def _url(self) -> str:
        return f"{self._cc_host}/api/v1/token/{self.service_name_in_cc}/{self._cc_token_id}/"

    @property
    def auth_header(self) -> str:
        return self._auth_header

    @property
    def token(self) -> str:
        response = requests.get(
            self._url,
            headers={"Authorization": f"Bearer {self._cc_token}"},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        access_token = data.get("access_token")
        if access_token:
            return access_token
        raise CredentialsCraftApiError(response.text)

    def get_auth_header(self) -> Mapping[str, Any]:
        if self.auth_header:
            auth_header = {self.auth_header: f"{self._auth_method} {self.token}"}
        else:
            auth_header = {}
        return auth_header

    def check_connection(self, raise_excepton: bool = False) -> tuple[bool, str | None]:
        error_msg = None
        try:
            requests.get(self._cc_host, timeout=15)
        except requests.exceptions.Timeout:
            error_msg = f"Connection to {self._cc_host} timed out"

        data: dict[str, Any] = requests.get(
            self._url,
            headers={"Authorization": f"Bearer {self._cc_token}"},
        ).json()

        if data.get("error"):
            error_msg = data.get('error')

        if error_msg:
            if raise_excepton:
                raise CredentialsCraftApiError(error_msg)
            return False, f'CredentialsCraft error: {error_msg}'

        return True, None
