"""
Nonprofit501q: Non-profit type referring to Credit Counseling Organizations.

https://schema.org/Nonprofit501q
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501qInheritedProperties(TypedDict):
    """Nonprofit501q: Non-profit type referring to Credit Counseling Organizations.

    References:
        https://schema.org/Nonprofit501q
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501qProperties(TypedDict):
    """Nonprofit501q: Non-profit type referring to Credit Counseling Organizations.

    References:
        https://schema.org/Nonprofit501q
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501qInheritedPropertiesTd = Nonprofit501qInheritedProperties()
#Nonprofit501qPropertiesTd = Nonprofit501qProperties()


class AllProperties(Nonprofit501qInheritedProperties , Nonprofit501qProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501qProperties, Nonprofit501qInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501q"
    return model
    

Nonprofit501q = create_schema_org_model()