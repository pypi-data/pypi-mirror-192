"""
Abdomen clinical examination.

https://schema.org/Abdomen
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AbdomenInheritedProperties(TypedDict):
    """Abdomen clinical examination.

    References:
        https://schema.org/Abdomen
    Note:
        Model Depth 5
    Attributes:
    """

    


class AbdomenProperties(TypedDict):
    """Abdomen clinical examination.

    References:
        https://schema.org/Abdomen
    Note:
        Model Depth 5
    Attributes:
    """

    

#AbdomenInheritedPropertiesTd = AbdomenInheritedProperties()
#AbdomenPropertiesTd = AbdomenProperties()


class AllProperties(AbdomenInheritedProperties , AbdomenProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AbdomenProperties, AbdomenInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Abdomen"
    return model
    

Abdomen = create_schema_org_model()