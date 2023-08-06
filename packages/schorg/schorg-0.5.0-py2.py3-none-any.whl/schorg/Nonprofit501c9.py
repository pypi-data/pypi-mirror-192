"""
Nonprofit501c9: Non-profit type referring to Voluntary Employee Beneficiary Associations.

https://schema.org/Nonprofit501c9
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c9InheritedProperties(TypedDict):
    """Nonprofit501c9: Non-profit type referring to Voluntary Employee Beneficiary Associations.

    References:
        https://schema.org/Nonprofit501c9
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c9Properties(TypedDict):
    """Nonprofit501c9: Non-profit type referring to Voluntary Employee Beneficiary Associations.

    References:
        https://schema.org/Nonprofit501c9
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c9InheritedPropertiesTd = Nonprofit501c9InheritedProperties()
#Nonprofit501c9PropertiesTd = Nonprofit501c9Properties()


class AllProperties(Nonprofit501c9InheritedProperties , Nonprofit501c9Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c9Properties, Nonprofit501c9InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c9"
    return model
    

Nonprofit501c9 = create_schema_org_model()