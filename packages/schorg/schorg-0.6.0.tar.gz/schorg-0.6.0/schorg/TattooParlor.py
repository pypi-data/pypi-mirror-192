"""
A tattoo parlor.

https://schema.org/TattooParlor
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TattooParlorInheritedProperties(TypedDict):
    """A tattoo parlor.

    References:
        https://schema.org/TattooParlor
    Note:
        Model Depth 5
    Attributes:
    """

    


class TattooParlorProperties(TypedDict):
    """A tattoo parlor.

    References:
        https://schema.org/TattooParlor
    Note:
        Model Depth 5
    Attributes:
    """

    

#TattooParlorInheritedPropertiesTd = TattooParlorInheritedProperties()
#TattooParlorPropertiesTd = TattooParlorProperties()


class AllProperties(TattooParlorInheritedProperties , TattooParlorProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TattooParlorProperties, TattooParlorInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TattooParlor"
    return model
    

TattooParlor = create_schema_org_model()