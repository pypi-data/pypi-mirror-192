"""
Nonprofit501c27: Non-profit type referring to State-Sponsored Workers' Compensation Reinsurance Organizations.

https://schema.org/Nonprofit501c27
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c27InheritedProperties(TypedDict):
    """Nonprofit501c27: Non-profit type referring to State-Sponsored Workers' Compensation Reinsurance Organizations.

    References:
        https://schema.org/Nonprofit501c27
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c27Properties(TypedDict):
    """Nonprofit501c27: Non-profit type referring to State-Sponsored Workers' Compensation Reinsurance Organizations.

    References:
        https://schema.org/Nonprofit501c27
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c27InheritedPropertiesTd = Nonprofit501c27InheritedProperties()
#Nonprofit501c27PropertiesTd = Nonprofit501c27Properties()


class AllProperties(Nonprofit501c27InheritedProperties , Nonprofit501c27Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c27Properties, Nonprofit501c27InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c27"
    return model
    

Nonprofit501c27 = create_schema_org_model()