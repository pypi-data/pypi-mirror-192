"""
Nonprofit501c11: Non-profit type referring to Teachers' Retirement Fund Associations.

https://schema.org/Nonprofit501c11
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c11InheritedProperties(TypedDict):
    """Nonprofit501c11: Non-profit type referring to Teachers' Retirement Fund Associations.

    References:
        https://schema.org/Nonprofit501c11
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c11Properties(TypedDict):
    """Nonprofit501c11: Non-profit type referring to Teachers' Retirement Fund Associations.

    References:
        https://schema.org/Nonprofit501c11
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c11InheritedPropertiesTd = Nonprofit501c11InheritedProperties()
#Nonprofit501c11PropertiesTd = Nonprofit501c11Properties()


class AllProperties(Nonprofit501c11InheritedProperties , Nonprofit501c11Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c11Properties, Nonprofit501c11InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c11"
    return model
    

Nonprofit501c11 = create_schema_org_model()