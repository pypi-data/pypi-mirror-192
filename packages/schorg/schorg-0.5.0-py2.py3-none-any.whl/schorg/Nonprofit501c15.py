"""
Nonprofit501c15: Non-profit type referring to Mutual Insurance Companies or Associations.

https://schema.org/Nonprofit501c15
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c15InheritedProperties(TypedDict):
    """Nonprofit501c15: Non-profit type referring to Mutual Insurance Companies or Associations.

    References:
        https://schema.org/Nonprofit501c15
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c15Properties(TypedDict):
    """Nonprofit501c15: Non-profit type referring to Mutual Insurance Companies or Associations.

    References:
        https://schema.org/Nonprofit501c15
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c15InheritedPropertiesTd = Nonprofit501c15InheritedProperties()
#Nonprofit501c15PropertiesTd = Nonprofit501c15Properties()


class AllProperties(Nonprofit501c15InheritedProperties , Nonprofit501c15Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c15Properties, Nonprofit501c15InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c15"
    return model
    

Nonprofit501c15 = create_schema_org_model()