from __future__ import annotations

from io import IOBase
from typing import Optional

from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.cluster import DocumentCluster as DocumentClusterDTO
from semantha_sdk.model.document import Document
from semantha_sdk.model.named_entity import NamedEntities as NamedEntitiesDTO
from semantha_sdk.model.paragraph import Paragraph
from semantha_sdk.model.reference_document import ReferenceDocuments as ReferenceDocumentsDTO, \
    DocumentInformation, Statistic
from semantha_sdk.model.schema.cluster import DocumentClusterSchema
from semantha_sdk.model.schema.document import DocumentSchema
from semantha_sdk.model.schema.document_information import DocumentInformationSchema
from semantha_sdk.model.schema.named_entity import NamedEntitySchema
from semantha_sdk.model.schema.paragraph import ParagraphSchema
from semantha_sdk.model.schema.reference_document import ReferenceDocumentsSchema
from semantha_sdk.model.schema.sentence import SentenceSchema
from semantha_sdk.model.schema.statistic import StatisticSchema
from semantha_sdk.model.sentence import Sentence

from semantha_sdk.model.paragraph import PatchParagraph


class Statistics(SemanthaAPIEndpoint):
    """ Access role(s) information about the currently logged-in user. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/statistic"

    def get(self) -> Statistic:
        return self._session.get(self._endpoint).execute().to(StatisticSchema)


class DocumentCluster(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/clusters"

    def get(
            self,
            min_cluster_size: str = None,
            clustering_structure: str = None
    ) -> list[DocumentClusterDTO]:
        """ Get document clusters, i.e. a semantic clustering of the documents in the library. Clusters are named and
        have an integer ID. Note that a special cluster with ID '-1' is reserved for outliers, i.e. documents that could
        not have been assigned to a cluster.
        Args:
            min_cluster_size: choose whether to require only a few documents to form a cluster or more. Choose from
                                     either 'LOW', 'MEDIUM' or 'HIGH'.
            clustering_structure: the strategy the clustering algorithm uses to create the clustering space. Choose from
                                  either 'LOCAL', 'BALANCED' or 'GLOBAL' (default 'BALANCED') where LOCAL means that the
                                  model is able to better represent dense structure and GLOBAL means that more
                                  datapoints are considered and the model better represents the overall structure of the
                                  data but lacks details.

        Compatibility note: In future releases more parameters will be added to alter the clustering.
        """
        q_params = {}
        if min_cluster_size is not None:
            q_params["minclustersize"] = min_cluster_size
        if clustering_structure is not None:
            q_params["clusteringstructure"] = clustering_structure
        return self._session.get(
            self._endpoint,
            q_params=q_params
        ).execute().to(DocumentClusterSchema)


class NamedEntities(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/namedentities"

    def get(self) -> Optional[NamedEntitiesDTO]:
        """ Get all named entities (aka custom entities) that were extracted from the reference documents.
        Note: Might be None iff no named entities have been extracted.
        """
        res = self._session.get(self._endpoint).execute()
        if res.content_is_empty():
            return None
        return self._session.get(self._endpoint).execute().to(NamedEntitySchema)


class ReferenceDocument(SemanthaAPIEndpoint):
    class ReferenceDocumentParagraphs(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/paragraphs"

        def __call__(self, id: str):
            return ReferenceDocument.ReferenceDocumentParagraphs.ReferenceDocumentParagraph(self._session, self._endpoint, id)

        class ReferenceDocumentParagraph(SemanthaAPIEndpoint):

            def __init__(self, session: RestClient, parent_endpoint: str, id: str):
                super().__init__(session, parent_endpoint)
                self._id = id

            @property
            def _endpoint(self):
                return self._parent_endpoint + f"/{self._id}"

            def get(self) -> Paragraph:
                """ Get the paragraph of the reference document """
                return self._session.get(self._endpoint).execute().to(ParagraphSchema)

            def delete(self):
                """ Delete the paragraph of the reference document """
                self._session.delete(self._endpoint).execute()

            def patch(self, update: PatchParagraph) -> Paragraph:
                """Update the paragraph of the reference document
                Args:
                    update (Paragraph): (partial) paragraph information that should be updated. Please provide an
                                        instance of Paragraph (semantha_sdk.model.Paragraphs.Paragraph). E.g. to alter
                                        (only) the text of the paragraph you can use something like
                                        Paragraph({"text": "updated text"}).
                """
                return self._session.patch(
                    url=self._endpoint,
                    json=ParagraphSchema().dump(update)
                ).execute().to(ParagraphSchema)

    class ReferenceDocumentSentences(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/sentences"

        def __call__(self, id: str):
            return ReferenceDocument.ReferenceDocumentSentences.ReferenceDocumentSentence(self._session, self._endpoint, id)

        class ReferenceDocumentSentence(SemanthaAPIEndpoint):

            def __init__(self, session: RestClient, parent_endpoint: str, id: str):
                super().__init__(session, parent_endpoint)
                self._id = id

            @property
            def _endpoint(self):
                return self._parent_endpoint + f"/{self._id}"

            def get(self) -> Sentence:
                """ Get the paragraph of the reference document """
                return self._session.get(self._endpoint).execute().to(SentenceSchema)

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id
        self.__child_reference_document_paragraphs = ReferenceDocument.ReferenceDocumentParagraphs(session, self._endpoint)
        self.__child_reference_document_sentences = ReferenceDocument.ReferenceDocumentSentences(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._id}"

    @property
    def paragraphs(self):
        return self.__child_reference_document_paragraphs

    @property
    def sentences(self):
        return self.__child_reference_document_sentences

    def get(self) -> Document:
        """ Get the reference document """
        return self._session.get(self._endpoint).execute().to(DocumentSchema)

    def delete(self):
        """ Delete the reference document """
        self._session.delete(self._endpoint).execute()

    def patch(
            self,
            update: DocumentInformation,
    ) -> DocumentInformation:
        """ Update the document information of the reference document

        Args:
            update (DocumentInformation): (partial) document information that should be updated. Please provide an
                                          instance of DocumentInformation (semantha_sdk.model.ReferenceDocuments.
                                          DocumentInformation). E.g. to alter (only) the name of the document you can
                                          use something like Document({"name": "new name"}).
        """
        return self._session.patch(
            url=self._endpoint,
            json=DocumentSchema().dump(update)
        ).execute().to(DocumentInformationSchema)


class ReferenceDocuments(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__statistics = Statistics(session, self._endpoint)
        self.__named_entities = NamedEntities(session, self._endpoint)
        self.__document_clusters = DocumentCluster(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/referencedocuments"

    @property
    def statistic(self):
        return self.__statistics

    @property
    def named_entities(self):
        return self.__named_entities

    @property
    def clusters(self):
        return self.__document_clusters

    def get(self,
            offset: int = None,
            limit: int = None,
            filter_tags: str = None,
            filter_document_class_ids: str = None,
            filter_name: str = None,
            filter_created_before: int = None,
            filter_created_after: int = None,
            filter_metadata: str = None,
            filter_comment: str = None,
            sort_by: str = None,
            return_fields: str = None) -> ReferenceDocumentsDTO:
        """ Get reference documents (library documents)

        If no parameters are set all reference documents are returned.
        However, the result set can be filtered (filter_*), sorted (sort_by), sliced (offset AND limit) and the returned
        attributes/fields can be manipulated (return_fields) to reduce the size of the response.
        Note that some filters and sorting can only be used iff slicing is used (offset and limit).

        Args:
            offset (int): the start index (inclusive) of the returned slice of reference documents
            limit (int): the end index (exclusive) of the returned slice of reference documents
            filter_tags (str): the tags to filter by: comma separated lists are interpreted as OR and + is interpreted
                               as AND. E.g. 'a+b,c+d' means a AND b OR c AND d. The tag filter can be used without
                               slicing.
            filter_document_class_ids (str): the class ids to filter by. Filtering by class ids can be done without
                                             slicing.
            filter_name (str): filter by (document) name. Can only be used with slicing (offset and limit).
            filter_created_before (int): filter by creation date before. Can only be used with slicing (offset and
                                         limit).
            filter_created_after (int): filter by creation date after. Can only be used with slicing (offset and
                                        limit).
            filter_metadata (str): filter by metadata. Can only be used with slicing (offset and limit).
            filter_comment (str): filter by comment. Can only be used with slicing (offset and limit).
            sort_by (str): (lexically) sort the result by one or more criteria: "name", "filename", "metadata",
                           "created", "updated", "color", "comment", "derivedcolor", "derivedcomment", "documentclass".
                           If a value is prefixed by a '-', the sorting is inverted. Can only be used with slicing
                           (offset and limit). Note that sorting is performed before slicing.
            return_fields (str): limit the returned fields to the defined (instead of a full response): "id", "name",
                                 "tags", "derivedtags", "metadata", "filename", "created", "processed", "lang",
                                 "updated", "color", "derivedcolor", "comment", "derivedcomment", "documentclass",
                                 "contentpreview"
        """
        if (offset is None and limit is not None) or (limit is None and offset is not None):
            raise ValueError("'limit' and 'offset' must be set together.")
        if offset is None and limit is None:
            if filter_name is not None:
                raise ValueError("filter by name can only be used if 'limit' and 'offset' are set")
            if filter_created_before is not None:
                raise ValueError("filter by 'created before' can only be used if 'limit' and 'offset' are set")
            if filter_created_after is not None:
                raise ValueError("filter by 'created after' can only be used if 'limit' and 'offset' are set")
            if filter_metadata is not None:
                raise ValueError("filter by metadata can only be used if 'limit' and 'offset' are set")
            if filter_comment is not None:
                raise ValueError("filter by comment can only be used if 'limit' and 'offset' are set")
            if sort_by is not None:
                raise ValueError("sorting can only activated if 'limit' and 'offset' are set")

        q_params = {}
        if filter_tags is not None:
            q_params["tags"] = filter_tags
        if filter_document_class_ids is not None:
            q_params["documentclassids"] = filter_document_class_ids
        if return_fields is not None:
            q_params["fields"] = return_fields
        if offset is not None and limit is not None:
            q_params["offset"] = offset
            q_params["limit"] = limit
            if filter_name is not None:
                q_params["name"] = filter_name
            if filter_created_before is not None:
                q_params["createdbefore"] = filter_created_before
            if filter_created_after is not None:
                q_params["createdafter"] = filter_created_after
            if filter_metadata is not None:
                q_params["metadata"] = filter_metadata
            if filter_comment is not None:
                q_params["comment"] = filter_comment
            if sort_by is not None:
                q_params["sort"] = sort_by

        return self._session.get(self._endpoint, q_params=q_params).execute().to(ReferenceDocumentsSchema)

    def delete(self):
        """ Delete all reference documents """
        self._session.delete(self._endpoint).execute()

    def post(
            self,
            name: str = None,
            tags: str = None,
            metadata: str = None,
            file: IOBase = None,
            text: str = None,
            document_type: str = None,
            color: str = None,
            comment: str = None,
            detect_language: bool = False,
            add_paragraphs_as_documents: bool = False
    ) -> list[DocumentInformation]:
        """ Upload a reference document

        Args:
            name (str): The document name in your library (in contrast to the file name being used during upload).
            tags (str): List of tags to filter the reference library.
                You can combine the tags using a comma (OR) and using a plus sign (AND).
            metadata (str): Filter by metadata
            file (str): Input document (left document).
            text (str): Plain text input (left document). If set, the parameter file will be ignored.
            document_type (str): Specifies the document type that is to be used when reading the uploaded PDF document. 
            color (str): Use this parameter to specify the color for your reference document.
                Possible values are RED, MAGENTA, AQUA, ORANGE, GREY, or LAVENDER.
            comment (str): Use this parameter to add a comment to your reference document.
            detect_language (bool): Auto-detect the language of the document (only available if configured for the domain).
            add_paragraphs_as_documents (bool): If true a library item for every paragraph in this document is added.
        """
        return self._session.post(
            self._endpoint,
            body={
                "name": name,
                "tags": tags,
                "metadata": metadata,
                "file": file,
                "text": text,
                "documenttype": document_type,
                "color": color,
                "comment": comment,
                "addparagraphsasdocuments": add_paragraphs_as_documents
            },
            q_params={
                "detectlanguage": str(detect_language)
            }
        ).execute().to(DocumentInformationSchema)

    def __call__(self, id: str):
        return ReferenceDocument(self._session, self._endpoint, id)
