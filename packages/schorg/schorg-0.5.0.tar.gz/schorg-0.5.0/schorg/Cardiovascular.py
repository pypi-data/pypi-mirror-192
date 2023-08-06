"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of heart and vasculature.

https://schema.org/Cardiovascular
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CardiovascularInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of heart and vasculature.

    References:
        https://schema.org/Cardiovascular
    Note:
        Model Depth 6
    Attributes:
    """

    


class CardiovascularProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of heart and vasculature.

    References:
        https://schema.org/Cardiovascular
    Note:
        Model Depth 6
    Attributes:
    """

    

#CardiovascularInheritedPropertiesTd = CardiovascularInheritedProperties()
#CardiovascularPropertiesTd = CardiovascularProperties()


class AllProperties(CardiovascularInheritedProperties , CardiovascularProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CardiovascularProperties, CardiovascularInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Cardiovascular"
    return model
    

Cardiovascular = create_schema_org_model()