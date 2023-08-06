"""
Indicates that a legislation is currently not in force.

https://schema.org/NotInForce
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NotInForceInheritedProperties(TypedDict):
    """Indicates that a legislation is currently not in force.

    References:
        https://schema.org/NotInForce
    Note:
        Model Depth 6
    Attributes:
    """

    


class NotInForceProperties(TypedDict):
    """Indicates that a legislation is currently not in force.

    References:
        https://schema.org/NotInForce
    Note:
        Model Depth 6
    Attributes:
    """

    

#NotInForceInheritedPropertiesTd = NotInForceInheritedProperties()
#NotInForcePropertiesTd = NotInForceProperties()


class AllProperties(NotInForceInheritedProperties , NotInForceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NotInForceProperties, NotInForceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NotInForce"
    return model
    

NotInForce = create_schema_org_model()