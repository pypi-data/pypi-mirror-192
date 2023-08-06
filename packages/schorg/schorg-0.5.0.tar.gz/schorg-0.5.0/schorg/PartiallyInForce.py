"""
Indicates that parts of the legislation are in force, and parts are not.

https://schema.org/PartiallyInForce
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PartiallyInForceInheritedProperties(TypedDict):
    """Indicates that parts of the legislation are in force, and parts are not.

    References:
        https://schema.org/PartiallyInForce
    Note:
        Model Depth 6
    Attributes:
    """

    


class PartiallyInForceProperties(TypedDict):
    """Indicates that parts of the legislation are in force, and parts are not.

    References:
        https://schema.org/PartiallyInForce
    Note:
        Model Depth 6
    Attributes:
    """

    

#PartiallyInForceInheritedPropertiesTd = PartiallyInForceInheritedProperties()
#PartiallyInForcePropertiesTd = PartiallyInForceProperties()


class AllProperties(PartiallyInForceInheritedProperties , PartiallyInForceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PartiallyInForceProperties, PartiallyInForceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PartiallyInForce"
    return model
    

PartiallyInForce = create_schema_org_model()