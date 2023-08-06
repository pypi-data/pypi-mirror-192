"""
A casino.

https://schema.org/Casino
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CasinoInheritedProperties(TypedDict):
    """A casino.

    References:
        https://schema.org/Casino
    Note:
        Model Depth 5
    Attributes:
    """

    


class CasinoProperties(TypedDict):
    """A casino.

    References:
        https://schema.org/Casino
    Note:
        Model Depth 5
    Attributes:
    """

    

#CasinoInheritedPropertiesTd = CasinoInheritedProperties()
#CasinoPropertiesTd = CasinoProperties()


class AllProperties(CasinoInheritedProperties , CasinoProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CasinoProperties, CasinoInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Casino"
    return model
    

Casino = create_schema_org_model()