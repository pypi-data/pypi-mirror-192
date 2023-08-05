from __future__ import annotations

from semantha_sdk.api.boost_words import Boostword
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.api.boost_words import Boostwords
from semantha_sdk.api.synonyms import Synonyms
from semantha_sdk.rest.rest_client import RestClient


class DomainModel(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: attributes, backups, boostwords, classes, extractors,
            formatters, instances, metadata, namedentities, regexes, relations,
            rulefunctions, rules, synonyms
    """

    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__boostwords = Boostwords(session, self._endpoint)
        self.__synonyms = Synonyms(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def boostwords(self) -> Boostwords | Boostword:
        return self.__boostwords

    @property
    def synonyms(self):
        return self.__synonyms


class Domains(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def __call__(self, domain_name: str) -> DomainModel:
        # Returns a Domain object for the given domainname, throws error if id doesn't exist
        return DomainModel(self._session, self._endpoint, domain_name)
