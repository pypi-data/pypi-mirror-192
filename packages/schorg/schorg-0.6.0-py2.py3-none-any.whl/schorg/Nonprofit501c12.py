"""
Nonprofit501c12: Non-profit type referring to Benevolent Life Insurance Associations, Mutual Ditch or Irrigation Companies, Mutual or Cooperative Telephone Companies.

https://schema.org/Nonprofit501c12
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c12InheritedProperties(TypedDict):
    """Nonprofit501c12: Non-profit type referring to Benevolent Life Insurance Associations, Mutual Ditch or Irrigation Companies, Mutual or Cooperative Telephone Companies.

    References:
        https://schema.org/Nonprofit501c12
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c12Properties(TypedDict):
    """Nonprofit501c12: Non-profit type referring to Benevolent Life Insurance Associations, Mutual Ditch or Irrigation Companies, Mutual or Cooperative Telephone Companies.

    References:
        https://schema.org/Nonprofit501c12
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c12InheritedPropertiesTd = Nonprofit501c12InheritedProperties()
#Nonprofit501c12PropertiesTd = Nonprofit501c12Properties()


class AllProperties(Nonprofit501c12InheritedProperties , Nonprofit501c12Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c12Properties, Nonprofit501c12InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c12"
    return model
    

Nonprofit501c12 = create_schema_org_model()