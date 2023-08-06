"""
Throat assessment with  clinical examination.

https://schema.org/Throat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ThroatInheritedProperties(TypedDict):
    """Throat assessment with  clinical examination.

    References:
        https://schema.org/Throat
    Note:
        Model Depth 5
    Attributes:
    """

    


class ThroatProperties(TypedDict):
    """Throat assessment with  clinical examination.

    References:
        https://schema.org/Throat
    Note:
        Model Depth 5
    Attributes:
    """

    

#ThroatInheritedPropertiesTd = ThroatInheritedProperties()
#ThroatPropertiesTd = ThroatProperties()


class AllProperties(ThroatInheritedProperties , ThroatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ThroatProperties, ThroatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Throat"
    return model
    

Throat = create_schema_org_model()