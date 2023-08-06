"""
Nonprofit501c7: Non-profit type referring to Social and Recreational Clubs.

https://schema.org/Nonprofit501c7
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c7InheritedProperties(TypedDict):
    """Nonprofit501c7: Non-profit type referring to Social and Recreational Clubs.

    References:
        https://schema.org/Nonprofit501c7
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c7Properties(TypedDict):
    """Nonprofit501c7: Non-profit type referring to Social and Recreational Clubs.

    References:
        https://schema.org/Nonprofit501c7
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c7InheritedPropertiesTd = Nonprofit501c7InheritedProperties()
#Nonprofit501c7PropertiesTd = Nonprofit501c7Properties()


class AllProperties(Nonprofit501c7InheritedProperties , Nonprofit501c7Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c7Properties, Nonprofit501c7InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c7"
    return model
    

Nonprofit501c7 = create_schema_org_model()