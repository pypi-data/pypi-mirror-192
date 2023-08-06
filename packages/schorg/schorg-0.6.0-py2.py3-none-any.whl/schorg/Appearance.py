"""
Appearance assessment with clinical examination.

https://schema.org/Appearance
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AppearanceInheritedProperties(TypedDict):
    """Appearance assessment with clinical examination.

    References:
        https://schema.org/Appearance
    Note:
        Model Depth 5
    Attributes:
    """

    


class AppearanceProperties(TypedDict):
    """Appearance assessment with clinical examination.

    References:
        https://schema.org/Appearance
    Note:
        Model Depth 5
    Attributes:
    """

    

#AppearanceInheritedPropertiesTd = AppearanceInheritedProperties()
#AppearancePropertiesTd = AppearanceProperties()


class AllProperties(AppearanceInheritedProperties , AppearanceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AppearanceProperties, AppearanceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Appearance"
    return model
    

Appearance = create_schema_org_model()