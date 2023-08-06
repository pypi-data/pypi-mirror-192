"""
Pathogenic fungus.

https://schema.org/Fungus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FungusInheritedProperties(TypedDict):
    """Pathogenic fungus.

    References:
        https://schema.org/Fungus
    Note:
        Model Depth 6
    Attributes:
    """

    


class FungusProperties(TypedDict):
    """Pathogenic fungus.

    References:
        https://schema.org/Fungus
    Note:
        Model Depth 6
    Attributes:
    """

    

#FungusInheritedPropertiesTd = FungusInheritedProperties()
#FungusPropertiesTd = FungusProperties()


class AllProperties(FungusInheritedProperties , FungusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FungusProperties, FungusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Fungus"
    return model
    

Fungus = create_schema_org_model()