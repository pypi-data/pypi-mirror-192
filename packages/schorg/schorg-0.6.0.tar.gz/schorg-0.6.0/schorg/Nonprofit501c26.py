"""
Nonprofit501c26: Non-profit type referring to State-Sponsored Organizations Providing Health Coverage for High-Risk Individuals.

https://schema.org/Nonprofit501c26
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c26InheritedProperties(TypedDict):
    """Nonprofit501c26: Non-profit type referring to State-Sponsored Organizations Providing Health Coverage for High-Risk Individuals.

    References:
        https://schema.org/Nonprofit501c26
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c26Properties(TypedDict):
    """Nonprofit501c26: Non-profit type referring to State-Sponsored Organizations Providing Health Coverage for High-Risk Individuals.

    References:
        https://schema.org/Nonprofit501c26
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c26InheritedPropertiesTd = Nonprofit501c26InheritedProperties()
#Nonprofit501c26PropertiesTd = Nonprofit501c26Properties()


class AllProperties(Nonprofit501c26InheritedProperties , Nonprofit501c26Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c26Properties, Nonprofit501c26InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c26"
    return model
    

Nonprofit501c26 = create_schema_org_model()