"""
A specific and exact (byte-for-byte) version of an [[ImageObject]]. Two byte-for-byte identical files, for the purposes of this type, considered identical. If they have different embedded metadata (e.g. XMP, EXIF) the files will differ. Different external facts about the files, e.g. creator or dateCreated that aren't represented in their actual content, do not affect this notion of identity.

https://schema.org/ImageObjectSnapshot
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ImageObjectSnapshotInheritedProperties(TypedDict):
    """A specific and exact (byte-for-byte) version of an [[ImageObject]]. Two byte-for-byte identical files, for the purposes of this type, considered identical. If they have different embedded metadata (e.g. XMP, EXIF) the files will differ. Different external facts about the files, e.g. creator or dateCreated that aren't represented in their actual content, do not affect this notion of identity.

    References:
        https://schema.org/ImageObjectSnapshot
    Note:
        Model Depth 5
    Attributes:
        caption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The caption for this object. For downloadable machine formats (closed caption, subtitles etc.) use MediaObject and indicate the [[encodingFormat]].
        thumbnail: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Thumbnail image for an image or video.
        exifData: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): exif data for this object.
        embeddedTextCaption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.
        representativeOfPage: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates whether this image is representative of the content of the page.
    """

    caption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    thumbnail: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exifData: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    embeddedTextCaption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    representativeOfPage: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    


class ImageObjectSnapshotProperties(TypedDict):
    """A specific and exact (byte-for-byte) version of an [[ImageObject]]. Two byte-for-byte identical files, for the purposes of this type, considered identical. If they have different embedded metadata (e.g. XMP, EXIF) the files will differ. Different external facts about the files, e.g. creator or dateCreated that aren't represented in their actual content, do not affect this notion of identity.

    References:
        https://schema.org/ImageObjectSnapshot
    Note:
        Model Depth 5
    Attributes:
    """

    

#ImageObjectSnapshotInheritedPropertiesTd = ImageObjectSnapshotInheritedProperties()
#ImageObjectSnapshotPropertiesTd = ImageObjectSnapshotProperties()


class AllProperties(ImageObjectSnapshotInheritedProperties , ImageObjectSnapshotProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ImageObjectSnapshotProperties, ImageObjectSnapshotInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ImageObjectSnapshot"
    return model
    

ImageObjectSnapshot = create_schema_org_model()