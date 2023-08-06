"""
Nonprofit501c13: Non-profit type referring to Cemetery Companies.

https://schema.org/Nonprofit501c13
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c13InheritedProperties(TypedDict):
    """Nonprofit501c13: Non-profit type referring to Cemetery Companies.

    References:
        https://schema.org/Nonprofit501c13
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c13Properties(TypedDict):
    """Nonprofit501c13: Non-profit type referring to Cemetery Companies.

    References:
        https://schema.org/Nonprofit501c13
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c13InheritedPropertiesTd = Nonprofit501c13InheritedProperties()
#Nonprofit501c13PropertiesTd = Nonprofit501c13Properties()


class AllProperties(Nonprofit501c13InheritedProperties , Nonprofit501c13Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c13Properties, Nonprofit501c13InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c13"
    return model
    

Nonprofit501c13 = create_schema_org_model()