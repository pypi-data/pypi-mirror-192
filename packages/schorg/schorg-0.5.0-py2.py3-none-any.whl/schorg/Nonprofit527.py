"""
Nonprofit527: Non-profit type referring to political organizations.

https://schema.org/Nonprofit527
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit527InheritedProperties(TypedDict):
    """Nonprofit527: Non-profit type referring to political organizations.

    References:
        https://schema.org/Nonprofit527
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit527Properties(TypedDict):
    """Nonprofit527: Non-profit type referring to political organizations.

    References:
        https://schema.org/Nonprofit527
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit527InheritedPropertiesTd = Nonprofit527InheritedProperties()
#Nonprofit527PropertiesTd = Nonprofit527Properties()


class AllProperties(Nonprofit527InheritedProperties , Nonprofit527Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit527Properties, Nonprofit527InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit527"
    return model
    

Nonprofit527 = create_schema_org_model()