"""
Head assessment with clinical examination.

https://schema.org/Head
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HeadInheritedProperties(TypedDict):
    """Head assessment with clinical examination.

    References:
        https://schema.org/Head
    Note:
        Model Depth 5
    Attributes:
    """

    


class HeadProperties(TypedDict):
    """Head assessment with clinical examination.

    References:
        https://schema.org/Head
    Note:
        Model Depth 5
    Attributes:
    """

    

#HeadInheritedPropertiesTd = HeadInheritedProperties()
#HeadPropertiesTd = HeadProperties()


class AllProperties(HeadInheritedProperties , HeadProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HeadProperties, HeadInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Head"
    return model
    

Head = create_schema_org_model()