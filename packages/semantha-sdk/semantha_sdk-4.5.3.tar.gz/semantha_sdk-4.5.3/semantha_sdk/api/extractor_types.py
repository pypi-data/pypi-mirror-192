from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class ExtractorTypes(SemanthaAPIEndpoint):
    """ api/model/extractortypes endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/extractortypes"

    def get_extractortypes(self):
        pass