"""
Other prominent or relevant topics tied to the main topic.

https://schema.org/RelatedTopicsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RelatedTopicsHealthAspectInheritedProperties(TypedDict):
    """Other prominent or relevant topics tied to the main topic.

    References:
        https://schema.org/RelatedTopicsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class RelatedTopicsHealthAspectProperties(TypedDict):
    """Other prominent or relevant topics tied to the main topic.

    References:
        https://schema.org/RelatedTopicsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#RelatedTopicsHealthAspectInheritedPropertiesTd = RelatedTopicsHealthAspectInheritedProperties()
#RelatedTopicsHealthAspectPropertiesTd = RelatedTopicsHealthAspectProperties()


class AllProperties(RelatedTopicsHealthAspectInheritedProperties , RelatedTopicsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RelatedTopicsHealthAspectProperties, RelatedTopicsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RelatedTopicsHealthAspect"
    return model
    

RelatedTopicsHealthAspect = create_schema_org_model()