from __future__ import annotations

from semantha_sdk.api.current_user import CurrentUser
from semantha_sdk.api.diff import Diff
from semantha_sdk.api.domains import Domains, Domain
from semantha_sdk.api.model import Model
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient


class SemanthaAPI(SemanthaAPIEndpoint):
    """ Entry point to the Semantha API.

        References the /currentuser, /domains and /diff endpoints.

        Note:
            The __init__ method is not meant to be invoked directly
            use `semantha_sdk.login()` with your credentials instead.
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__current_user = CurrentUser(session, self._endpoint)
        self.__diff = Diff(session, self._endpoint)
        self.__domains = Domains(session, self._endpoint)
        self.__model = Model(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint

    @property
    def current_user(self) -> CurrentUser:
        return self.__current_user

    @property
    def domains(self) -> Domain | Domains:
        return self.__domains

    @property
    def diff(self) -> Diff:
        return self.__diff

    @property
    def model(self) -> Model:
        return self.__model
