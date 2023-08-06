"""
Content coded 'as original media content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'original': No evidence the footage has been misleadingly altered or manipulated, though it may contain false or misleading claims.For an [[ImageObject]] to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[ImageObject]] with embedded text to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[AudioObject]] to be 'original': No evidence the audio has been misleadingly altered or manipulated, though it may contain false or misleading claims.

https://schema.org/OriginalMediaContent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OriginalMediaContentInheritedProperties(TypedDict):
    """Content coded 'as original media content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'original': No evidence the footage has been misleadingly altered or manipulated, though it may contain false or misleading claims.For an [[ImageObject]] to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[ImageObject]] with embedded text to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[AudioObject]] to be 'original': No evidence the audio has been misleadingly altered or manipulated, though it may contain false or misleading claims.

    References:
        https://schema.org/OriginalMediaContent
    Note:
        Model Depth 5
    Attributes:
    """

    


class OriginalMediaContentProperties(TypedDict):
    """Content coded 'as original media content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'original': No evidence the footage has been misleadingly altered or manipulated, though it may contain false or misleading claims.For an [[ImageObject]] to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[ImageObject]] with embedded text to be 'original': No evidence the image has been misleadingly altered or manipulated, though it may still contain false or misleading claims.For an [[AudioObject]] to be 'original': No evidence the audio has been misleadingly altered or manipulated, though it may contain false or misleading claims.

    References:
        https://schema.org/OriginalMediaContent
    Note:
        Model Depth 5
    Attributes:
    """

    

#OriginalMediaContentInheritedPropertiesTd = OriginalMediaContentInheritedProperties()
#OriginalMediaContentPropertiesTd = OriginalMediaContentProperties()


class AllProperties(OriginalMediaContentInheritedProperties , OriginalMediaContentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OriginalMediaContentProperties, OriginalMediaContentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OriginalMediaContent"
    return model
    

OriginalMediaContent = create_schema_org_model()