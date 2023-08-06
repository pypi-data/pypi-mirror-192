"""
Nonprofit501c22: Non-profit type referring to Withdrawal Liability Payment Funds.

https://schema.org/Nonprofit501c22
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c22InheritedProperties(TypedDict):
    """Nonprofit501c22: Non-profit type referring to Withdrawal Liability Payment Funds.

    References:
        https://schema.org/Nonprofit501c22
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c22Properties(TypedDict):
    """Nonprofit501c22: Non-profit type referring to Withdrawal Liability Payment Funds.

    References:
        https://schema.org/Nonprofit501c22
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c22InheritedPropertiesTd = Nonprofit501c22InheritedProperties()
#Nonprofit501c22PropertiesTd = Nonprofit501c22Properties()


class AllProperties(Nonprofit501c22InheritedProperties , Nonprofit501c22Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c22Properties, Nonprofit501c22InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c22"
    return model
    

Nonprofit501c22 = create_schema_org_model()