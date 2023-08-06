"""
Content coded 'edited or cropped content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'edited or cropped content': The video has been edited or rearranged. This category applies to time edits, including editing multiple videos together to alter the story being told or editing out large portions from a video.For an [[ImageObject]] to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[ImageObject]] with embedded text to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[AudioObject]] to be 'edited or cropped content': The audio has been edited or rearranged. This category applies to time edits, including editing multiple audio clips together to alter the story being told or editing out large portions from the recording.

https://schema.org/EditedOrCroppedContent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EditedOrCroppedContentInheritedProperties(TypedDict):
    """Content coded 'edited or cropped content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'edited or cropped content': The video has been edited or rearranged. This category applies to time edits, including editing multiple videos together to alter the story being told or editing out large portions from a video.For an [[ImageObject]] to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[ImageObject]] with embedded text to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[AudioObject]] to be 'edited or cropped content': The audio has been edited or rearranged. This category applies to time edits, including editing multiple audio clips together to alter the story being told or editing out large portions from the recording.

    References:
        https://schema.org/EditedOrCroppedContent
    Note:
        Model Depth 5
    Attributes:
    """

    


class EditedOrCroppedContentProperties(TypedDict):
    """Content coded 'edited or cropped content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'edited or cropped content': The video has been edited or rearranged. This category applies to time edits, including editing multiple videos together to alter the story being told or editing out large portions from a video.For an [[ImageObject]] to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[ImageObject]] with embedded text to be 'edited or cropped content': Presenting a part of an image from a larger whole to mislead the viewer.For an [[AudioObject]] to be 'edited or cropped content': The audio has been edited or rearranged. This category applies to time edits, including editing multiple audio clips together to alter the story being told or editing out large portions from the recording.

    References:
        https://schema.org/EditedOrCroppedContent
    Note:
        Model Depth 5
    Attributes:
    """

    

#EditedOrCroppedContentInheritedPropertiesTd = EditedOrCroppedContentInheritedProperties()
#EditedOrCroppedContentPropertiesTd = EditedOrCroppedContentProperties()


class AllProperties(EditedOrCroppedContentInheritedProperties , EditedOrCroppedContentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EditedOrCroppedContentProperties, EditedOrCroppedContentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EditedOrCroppedContent"
    return model
    

EditedOrCroppedContent = create_schema_org_model()