"""
Nonprofit501n: Non-profit type referring to Charitable Risk Pools.

https://schema.org/Nonprofit501n
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501nInheritedProperties(TypedDict):
    """Nonprofit501n: Non-profit type referring to Charitable Risk Pools.

    References:
        https://schema.org/Nonprofit501n
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501nProperties(TypedDict):
    """Nonprofit501n: Non-profit type referring to Charitable Risk Pools.

    References:
        https://schema.org/Nonprofit501n
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501nInheritedPropertiesTd = Nonprofit501nInheritedProperties()
#Nonprofit501nPropertiesTd = Nonprofit501nProperties()


class AllProperties(Nonprofit501nInheritedProperties , Nonprofit501nProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501nProperties, Nonprofit501nInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501n"
    return model
    

Nonprofit501n = create_schema_org_model()