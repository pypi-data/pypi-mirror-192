"""
Nose function assessment with clinical examination.

https://schema.org/Nose
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NoseInheritedProperties(TypedDict):
    """Nose function assessment with clinical examination.

    References:
        https://schema.org/Nose
    Note:
        Model Depth 5
    Attributes:
    """

    


class NoseProperties(TypedDict):
    """Nose function assessment with clinical examination.

    References:
        https://schema.org/Nose
    Note:
        Model Depth 5
    Attributes:
    """

    

#NoseInheritedPropertiesTd = NoseInheritedProperties()
#NosePropertiesTd = NoseProperties()


class AllProperties(NoseInheritedProperties , NoseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NoseProperties, NoseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nose"
    return model
    

Nose = create_schema_org_model()