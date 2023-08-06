"""
The item contains sexually oriented content such as nudity, suggestive or explicit material, or related online services, or is intended to enhance sexual activity. Examples: Erotic videos or magazine, sexual enhancement devices, sex toys.

https://schema.org/SexualContentConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SexualContentConsiderationInheritedProperties(TypedDict):
    """The item contains sexually oriented content such as nudity, suggestive or explicit material, or related online services, or is intended to enhance sexual activity. Examples: Erotic videos or magazine, sexual enhancement devices, sex toys.

    References:
        https://schema.org/SexualContentConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class SexualContentConsiderationProperties(TypedDict):
    """The item contains sexually oriented content such as nudity, suggestive or explicit material, or related online services, or is intended to enhance sexual activity. Examples: Erotic videos or magazine, sexual enhancement devices, sex toys.

    References:
        https://schema.org/SexualContentConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#SexualContentConsiderationInheritedPropertiesTd = SexualContentConsiderationInheritedProperties()
#SexualContentConsiderationPropertiesTd = SexualContentConsiderationProperties()


class AllProperties(SexualContentConsiderationInheritedProperties , SexualContentConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SexualContentConsiderationProperties, SexualContentConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SexualContentConsideration"
    return model
    

SexualContentConsideration = create_schema_org_model()