from . import xmlwriter as xmlwriter

class RichValueStructure(xmlwriter.XMLwriter):
    has_embedded_descriptions: bool
    def __init__(self) -> None: ...
