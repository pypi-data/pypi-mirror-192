"""
A Catholic church.

https://schema.org/CatholicChurch
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CatholicChurchInheritedProperties(TypedDict):
    """A Catholic church.

    References:
        https://schema.org/CatholicChurch
    Note:
        Model Depth 6
    Attributes:
    """

    


class CatholicChurchProperties(TypedDict):
    """A Catholic church.

    References:
        https://schema.org/CatholicChurch
    Note:
        Model Depth 6
    Attributes:
    """

    

#CatholicChurchInheritedPropertiesTd = CatholicChurchInheritedProperties()
#CatholicChurchPropertiesTd = CatholicChurchProperties()


class AllProperties(CatholicChurchInheritedProperties , CatholicChurchProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CatholicChurchProperties, CatholicChurchInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CatholicChurch"
    return model
    

CatholicChurch = create_schema_org_model()