"""
Nonprofit501e: Non-profit type referring to Cooperative Hospital Service Organizations.

https://schema.org/Nonprofit501e
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501eInheritedProperties(TypedDict):
    """Nonprofit501e: Non-profit type referring to Cooperative Hospital Service Organizations.

    References:
        https://schema.org/Nonprofit501e
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501eProperties(TypedDict):
    """Nonprofit501e: Non-profit type referring to Cooperative Hospital Service Organizations.

    References:
        https://schema.org/Nonprofit501e
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501eInheritedPropertiesTd = Nonprofit501eInheritedProperties()
#Nonprofit501ePropertiesTd = Nonprofit501eProperties()


class AllProperties(Nonprofit501eInheritedProperties , Nonprofit501eProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501eProperties, Nonprofit501eInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501e"
    return model
    

Nonprofit501e = create_schema_org_model()