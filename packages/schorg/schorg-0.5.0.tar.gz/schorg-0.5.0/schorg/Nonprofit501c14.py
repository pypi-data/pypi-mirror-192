"""
Nonprofit501c14: Non-profit type referring to State-Chartered Credit Unions, Mutual Reserve Funds.

https://schema.org/Nonprofit501c14
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c14InheritedProperties(TypedDict):
    """Nonprofit501c14: Non-profit type referring to State-Chartered Credit Unions, Mutual Reserve Funds.

    References:
        https://schema.org/Nonprofit501c14
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c14Properties(TypedDict):
    """Nonprofit501c14: Non-profit type referring to State-Chartered Credit Unions, Mutual Reserve Funds.

    References:
        https://schema.org/Nonprofit501c14
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c14InheritedPropertiesTd = Nonprofit501c14InheritedProperties()
#Nonprofit501c14PropertiesTd = Nonprofit501c14Properties()


class AllProperties(Nonprofit501c14InheritedProperties , Nonprofit501c14Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c14Properties, Nonprofit501c14InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c14"
    return model
    

Nonprofit501c14 = create_schema_org_model()