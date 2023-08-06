"""
Skin assessment with clinical examination.

https://schema.org/Skin
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SkinInheritedProperties(TypedDict):
    """Skin assessment with clinical examination.

    References:
        https://schema.org/Skin
    Note:
        Model Depth 5
    Attributes:
    """

    


class SkinProperties(TypedDict):
    """Skin assessment with clinical examination.

    References:
        https://schema.org/Skin
    Note:
        Model Depth 5
    Attributes:
    """

    

#SkinInheritedPropertiesTd = SkinInheritedProperties()
#SkinPropertiesTd = SkinProperties()


class AllProperties(SkinInheritedProperties , SkinProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SkinProperties, SkinInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Skin"
    return model
    

Skin = create_schema_org_model()