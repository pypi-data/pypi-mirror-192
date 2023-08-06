"""
Nonprofit501c5: Non-profit type referring to Labor, Agricultural and Horticultural Organizations.

https://schema.org/Nonprofit501c5
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c5InheritedProperties(TypedDict):
    """Nonprofit501c5: Non-profit type referring to Labor, Agricultural and Horticultural Organizations.

    References:
        https://schema.org/Nonprofit501c5
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c5Properties(TypedDict):
    """Nonprofit501c5: Non-profit type referring to Labor, Agricultural and Horticultural Organizations.

    References:
        https://schema.org/Nonprofit501c5
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c5InheritedPropertiesTd = Nonprofit501c5InheritedProperties()
#Nonprofit501c5PropertiesTd = Nonprofit501c5Properties()


class AllProperties(Nonprofit501c5InheritedProperties , Nonprofit501c5Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c5Properties, Nonprofit501c5InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c5"
    return model
    

Nonprofit501c5 = create_schema_org_model()