"""
An audiobook.

https://schema.org/Audiobook
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AudiobookInheritedProperties(TypedDict):
    """An audiobook.

    References:
        https://schema.org/Audiobook
    Note:
        Model Depth 4
    Attributes:
        caption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The caption for this object. For downloadable machine formats (closed caption, subtitles etc.) use MediaObject and indicate the [[encodingFormat]].
        embeddedTextCaption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.
        transcript: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): If this MediaObject is an AudioObject or VideoObject, the transcript of that object.
        abridged: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates whether the book is an abridged edition.
        bookFormat: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The format of the book.
        illustrator: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The illustrator of the book.
        bookEdition: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The edition of the book.
        numberOfPages: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of pages in the book.
        isbn: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The ISBN of the book.
    """

    caption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    embeddedTextCaption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    transcript: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    abridged: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    bookFormat: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    illustrator: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    bookEdition: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    numberOfPages: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    isbn: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class AudiobookProperties(TypedDict):
    """An audiobook.

    References:
        https://schema.org/Audiobook
    Note:
        Model Depth 4
    Attributes:
        duration: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).
        readBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A person who reads (performs) the audiobook.
    """

    duration: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    readBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#AudiobookInheritedPropertiesTd = AudiobookInheritedProperties()
#AudiobookPropertiesTd = AudiobookProperties()


class AllProperties(AudiobookInheritedProperties , AudiobookProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AudiobookProperties, AudiobookInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Audiobook"
    return model
    

Audiobook = create_schema_org_model()