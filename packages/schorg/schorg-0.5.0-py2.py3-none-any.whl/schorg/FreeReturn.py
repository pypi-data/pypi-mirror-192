"""
Specifies that product returns are free of charge for the customer.

https://schema.org/FreeReturn
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FreeReturnInheritedProperties(TypedDict):
    """Specifies that product returns are free of charge for the customer.

    References:
        https://schema.org/FreeReturn
    Note:
        Model Depth 5
    Attributes:
    """

    


class FreeReturnProperties(TypedDict):
    """Specifies that product returns are free of charge for the customer.

    References:
        https://schema.org/FreeReturn
    Note:
        Model Depth 5
    Attributes:
    """

    

#FreeReturnInheritedPropertiesTd = FreeReturnInheritedProperties()
#FreeReturnPropertiesTd = FreeReturnProperties()


class AllProperties(FreeReturnInheritedProperties , FreeReturnProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FreeReturnProperties, FreeReturnInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FreeReturn"
    return model
    

FreeReturn = create_schema_org_model()