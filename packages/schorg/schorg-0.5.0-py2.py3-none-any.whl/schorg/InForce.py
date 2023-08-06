"""
Indicates that a legislation is in force.

https://schema.org/InForce
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InForceInheritedProperties(TypedDict):
    """Indicates that a legislation is in force.

    References:
        https://schema.org/InForce
    Note:
        Model Depth 6
    Attributes:
    """

    


class InForceProperties(TypedDict):
    """Indicates that a legislation is in force.

    References:
        https://schema.org/InForce
    Note:
        Model Depth 6
    Attributes:
    """

    

#InForceInheritedPropertiesTd = InForceInheritedProperties()
#InForcePropertiesTd = InForceProperties()


class AllProperties(InForceInheritedProperties , InForceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InForceProperties, InForceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InForce"
    return model
    

InForce = create_schema_org_model()