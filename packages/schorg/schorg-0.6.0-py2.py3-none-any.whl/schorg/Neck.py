"""
Neck assessment with clinical examination.

https://schema.org/Neck
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NeckInheritedProperties(TypedDict):
    """Neck assessment with clinical examination.

    References:
        https://schema.org/Neck
    Note:
        Model Depth 5
    Attributes:
    """

    


class NeckProperties(TypedDict):
    """Neck assessment with clinical examination.

    References:
        https://schema.org/Neck
    Note:
        Model Depth 5
    Attributes:
    """

    

#NeckInheritedPropertiesTd = NeckInheritedProperties()
#NeckPropertiesTd = NeckProperties()


class AllProperties(NeckInheritedProperties , NeckProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NeckProperties, NeckInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Neck"
    return model
    

Neck = create_schema_org_model()