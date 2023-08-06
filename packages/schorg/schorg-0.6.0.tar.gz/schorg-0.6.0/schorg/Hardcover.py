"""
Book format: Hardcover.

https://schema.org/Hardcover
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HardcoverInheritedProperties(TypedDict):
    """Book format: Hardcover.

    References:
        https://schema.org/Hardcover
    Note:
        Model Depth 5
    Attributes:
    """

    


class HardcoverProperties(TypedDict):
    """Book format: Hardcover.

    References:
        https://schema.org/Hardcover
    Note:
        Model Depth 5
    Attributes:
    """

    

#HardcoverInheritedPropertiesTd = HardcoverInheritedProperties()
#HardcoverPropertiesTd = HardcoverProperties()


class AllProperties(HardcoverInheritedProperties , HardcoverProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HardcoverProperties, HardcoverInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Hardcover"
    return model
    

Hardcover = create_schema_org_model()