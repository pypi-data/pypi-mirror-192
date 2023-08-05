from marshmallow import fields

from semantha_sdk.model.domain_settings import DomainSettings
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DomainSettingsSchema(SemanthaSchema, with_entity(DomainSettings)):
    similarity_model_id = fields.Str(
        data_key="similarityModelId",
        required=True
    )
    keep_numbers = fields.Bool(
        data_key="keepNumbers",
        required=True
    )
    min_tokens = fields.Int(
        data_key="minTokens",
        required=True
    )
    similarity_measure = fields.Str(
        data_key="similarityMeasure",
        required=True
    )
    context_weight = fields.Float(
        data_key="contextWeight",
        required=True
    )
    enable_string_comparison = fields.Bool(
        data_key="enableStringComparison",
        required=True
    )
    default_document_type = fields.Str(
        data_key="defaultDocumentType",
        required=True
    )
    enable_paragraph_sorting = fields.Bool(
        data_key="enableParagraphSorting",
        required=True
    )
    enable_paragraph_end_detection = fields.Bool(
        data_key="enableParagraphEndDetection",
        required=True
    )
    enable_paragraph_merging_based_on_formatting = fields.Bool(
        data_key="enableParagraphMergingBasedOnFormatting",
        required=True
    )
    enable_boost_word_filtering_for_input_documents = fields.Bool(
        data_key="enableBoostWordFilteringForInputDocuments",
        required=True
    )
    tagging_similarity_mode = fields.Str(
        data_key="taggingSimilarityMode",
        required=True
    )
    enable_updating_fingerprints_on_tag_updates = fields.Bool(
        data_key="enableUpdatingFingerprintsOnTagUpdates",
        required=True
    )
    similarity_matcher = fields.Str(
        data_key="similarityMatcher",
        required=True
    )
    similarity_max_deviation = fields.Int(
        data_key="similarityMaxDeviation",
        required=True
    )
    similarity_threshold = fields.Float(
        data_key="similarityThreshold",
        required=True
    )
    enable_tagging = fields.Bool(
        data_key="enableTagging",
        required=True
    )
    tagging_threshold = fields.Float(
        data_key="taggingThreshold",
        required=True
    )
    tagging_strategy = fields.Str(
        data_key="taggingStrategy",
        required=True
    )
    extraction_threshold = fields.Float(
        data_key="extractionThreshold",
        required=True
    )
    extraction_strategy = fields.Str(
        data_key="extractionStrategy",
        required=True
    )
    resize_paragraphs_on_extraction = fields.Bool(
        data_key="resizeParagraphsOnExtraction",
        required=True
    )
    use_creation_date_from_input_document = fields.Bool(
        data_key="useCreationDateFromInputDocument",
        required=True
    )
