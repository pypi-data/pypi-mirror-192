"""
Categorization and other types related to a topic.

https://schema.org/TypesHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TypesHealthAspectInheritedProperties(TypedDict):
    """Categorization and other types related to a topic.

    References:
        https://schema.org/TypesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class TypesHealthAspectProperties(TypedDict):
    """Categorization and other types related to a topic.

    References:
        https://schema.org/TypesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#TypesHealthAspectInheritedPropertiesTd = TypesHealthAspectInheritedProperties()
#TypesHealthAspectPropertiesTd = TypesHealthAspectProperties()


class AllProperties(TypesHealthAspectInheritedProperties , TypesHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TypesHealthAspectProperties, TypesHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TypesHealthAspect"
    return model
    

TypesHealthAspect = create_schema_org_model()