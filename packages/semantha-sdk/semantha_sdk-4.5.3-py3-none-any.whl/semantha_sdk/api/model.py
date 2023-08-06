from semantha_sdk.api.domain_model import Domains
from semantha_sdk.api.extractor_types import ExtractorTypes
from semantha_sdk.api.metadata_types import MetadataTypes
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient


class Model(SemanthaAPIEndpoint):
    """
        api/model endpoint

        References: datatypes, domains, exctractortypes, metadatatypes
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__model_domains = Domains(session, self._endpoint)
        self.__extractor_types = ExtractorTypes(session, self._endpoint)
        self.__metadata_types = MetadataTypes(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/model"

    @property
    def domains(self):
        return self.__model_domains

    @property
    def extractor_types(self):
        return self.__extractor_types

    @property
    def metadata_types(self):
        return self.__metadata_types
