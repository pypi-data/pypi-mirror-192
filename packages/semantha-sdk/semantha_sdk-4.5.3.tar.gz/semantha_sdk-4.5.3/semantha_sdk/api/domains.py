from __future__ import annotations

from semantha_sdk.api.document_annotations import DocumentAnnotations
from semantha_sdk.api.document_classes import DocumentClasses
from semantha_sdk.api.document_comparisons import DocumentComparisons
from semantha_sdk.api.documents import Documents
from semantha_sdk.api.reference_documents import ReferenceDocuments
from semantha_sdk.api.references import References
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.domain import Domain as DomainDTO
from semantha_sdk.model.domain_configuration import DomainConfiguration
from semantha_sdk.model.domain_settings import DomainSettings as DomainSettingsDTO, PatchDomainSettings
from semantha_sdk.model.schema.domain import DomainSchema
from semantha_sdk.model.schema.domain_configuration import DomainConfigurationSchema
from semantha_sdk.model.schema.domain_setting import DomainSettingsSchema
from semantha_sdk.rest.rest_client import RestClient


class DomainSettings(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/settings"

    def get(self) -> DomainSettingsDTO:
        """Get the domain settings"""
        return self._session.get(self._endpoint).execute().to(DomainSettingsSchema)

    def patch(
            self,
            domain_settings: PatchDomainSettings
    ) -> DomainSettings:
        """Patch one or more domain setting(s)"""
        #TODO: add Args description
        response = self._session.patch(
            self._endpoint,
            json=DomainSettingsSchema().dump(domain_settings)
        ).execute()
        return response.to(DomainSettingsSchema)


class DomainTags(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/tags"

    def get(self) -> list[str]:
        """Get all tags that are defined for the domain"""
        return self._session.get(self._endpoint).execute().as_list()


class Domain(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: documents, documentannotations, documentclasses, documentcomparisons,
            modelclasses, modelinstances, referencedocuments, references,
            settings, stopwords, similaritymatrix, tags and validation.
    """
    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__documents = Documents(session, self._endpoint)
        self.__document_annotations = DocumentAnnotations(session, self._endpoint)
        self.__document_classes = DocumentClasses(session, self._endpoint)
        self.__document_comparisons = DocumentComparisons(session, self._endpoint)
        self.__reference_documents = ReferenceDocuments(session, self._endpoint)
        self.__domain_settings = DomainSettings(session, self._endpoint)
        self.__references = References(session, self._endpoint)
        self.__tags = DomainTags(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def documents(self):
        return self.__documents

    @property
    def document_annotations(self):
        return self.__document_annotations

    @property
    def document_classes(self):
        return self.__document_classes

    @property
    def document_comparisons(self):
        return self.__document_comparisons

    @property
    def reference_documents(self) -> ReferenceDocuments:
        return self.__reference_documents

    @property
    def references(self) -> References:
        return self.__references

    @property
    def settings(self) -> DomainSettings:
        return self.__domain_settings

    @property
    def tags(self) -> DomainTags:
        return self.__tags

    def get(self) -> DomainConfiguration:
        """Get the domain configuration"""
        return self._session.get(self._endpoint).execute().to(DomainConfigurationSchema)


# TODO: Add docstrings, comments, type hints and error handling.
class Domains(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def get(self) -> list[DomainDTO]:
        """ Get all available domains """
        return self._session.get(self._endpoint).execute().to(DomainSchema)

    def __call__(self, domain_name: str):
        return Domain(self._session, self._endpoint, domain_name)
