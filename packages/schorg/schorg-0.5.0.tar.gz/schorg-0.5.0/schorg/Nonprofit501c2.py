"""
Nonprofit501c2: Non-profit type referring to Title-holding Corporations for Exempt Organizations.

https://schema.org/Nonprofit501c2
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c2InheritedProperties(TypedDict):
    """Nonprofit501c2: Non-profit type referring to Title-holding Corporations for Exempt Organizations.

    References:
        https://schema.org/Nonprofit501c2
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c2Properties(TypedDict):
    """Nonprofit501c2: Non-profit type referring to Title-holding Corporations for Exempt Organizations.

    References:
        https://schema.org/Nonprofit501c2
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c2InheritedPropertiesTd = Nonprofit501c2InheritedProperties()
#Nonprofit501c2PropertiesTd = Nonprofit501c2Properties()


class AllProperties(Nonprofit501c2InheritedProperties , Nonprofit501c2Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c2Properties, Nonprofit501c2InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c2"
    return model
    

Nonprofit501c2 = create_schema_org_model()