"""
Nonprofit501a: Non-profit type referring to Farmers’ Cooperative Associations.

https://schema.org/Nonprofit501a
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501aInheritedProperties(TypedDict):
    """Nonprofit501a: Non-profit type referring to Farmers’ Cooperative Associations.

    References:
        https://schema.org/Nonprofit501a
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501aProperties(TypedDict):
    """Nonprofit501a: Non-profit type referring to Farmers’ Cooperative Associations.

    References:
        https://schema.org/Nonprofit501a
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501aInheritedPropertiesTd = Nonprofit501aInheritedProperties()
#Nonprofit501aPropertiesTd = Nonprofit501aProperties()


class AllProperties(Nonprofit501aInheritedProperties , Nonprofit501aProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501aProperties, Nonprofit501aInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501a"
    return model
    

Nonprofit501a = create_schema_org_model()