"""
Nonprofit501c16: Non-profit type referring to Cooperative Organizations to Finance Crop Operations.

https://schema.org/Nonprofit501c16
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c16InheritedProperties(TypedDict):
    """Nonprofit501c16: Non-profit type referring to Cooperative Organizations to Finance Crop Operations.

    References:
        https://schema.org/Nonprofit501c16
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c16Properties(TypedDict):
    """Nonprofit501c16: Non-profit type referring to Cooperative Organizations to Finance Crop Operations.

    References:
        https://schema.org/Nonprofit501c16
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c16InheritedPropertiesTd = Nonprofit501c16InheritedProperties()
#Nonprofit501c16PropertiesTd = Nonprofit501c16Properties()


class AllProperties(Nonprofit501c16InheritedProperties , Nonprofit501c16Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c16Properties, Nonprofit501c16InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c16"
    return model
    

Nonprofit501c16 = create_schema_org_model()