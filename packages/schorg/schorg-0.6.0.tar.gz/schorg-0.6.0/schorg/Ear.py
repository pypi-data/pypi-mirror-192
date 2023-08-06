"""
Ear function assessment with clinical examination.

https://schema.org/Ear
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EarInheritedProperties(TypedDict):
    """Ear function assessment with clinical examination.

    References:
        https://schema.org/Ear
    Note:
        Model Depth 5
    Attributes:
    """

    


class EarProperties(TypedDict):
    """Ear function assessment with clinical examination.

    References:
        https://schema.org/Ear
    Note:
        Model Depth 5
    Attributes:
    """

    

#EarInheritedPropertiesTd = EarInheritedProperties()
#EarPropertiesTd = EarProperties()


class AllProperties(EarInheritedProperties , EarProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EarProperties, EarInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Ear"
    return model
    

Ear = create_schema_org_model()