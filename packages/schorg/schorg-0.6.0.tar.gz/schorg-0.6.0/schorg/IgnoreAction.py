"""
The act of intentionally disregarding the object. An agent ignores an object.

https://schema.org/IgnoreAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class IgnoreActionInheritedProperties(TypedDict):
    """The act of intentionally disregarding the object. An agent ignores an object.

    References:
        https://schema.org/IgnoreAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class IgnoreActionProperties(TypedDict):
    """The act of intentionally disregarding the object. An agent ignores an object.

    References:
        https://schema.org/IgnoreAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#IgnoreActionInheritedPropertiesTd = IgnoreActionInheritedProperties()
#IgnoreActionPropertiesTd = IgnoreActionProperties()


class AllProperties(IgnoreActionInheritedProperties , IgnoreActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[IgnoreActionProperties, IgnoreActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "IgnoreAction"
    return model
    

IgnoreAction = create_schema_org_model()