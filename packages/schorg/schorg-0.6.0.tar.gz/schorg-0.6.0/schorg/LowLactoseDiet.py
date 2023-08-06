"""
A diet appropriate for people with lactose intolerance.

https://schema.org/LowLactoseDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LowLactoseDietInheritedProperties(TypedDict):
    """A diet appropriate for people with lactose intolerance.

    References:
        https://schema.org/LowLactoseDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class LowLactoseDietProperties(TypedDict):
    """A diet appropriate for people with lactose intolerance.

    References:
        https://schema.org/LowLactoseDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#LowLactoseDietInheritedPropertiesTd = LowLactoseDietInheritedProperties()
#LowLactoseDietPropertiesTd = LowLactoseDietProperties()


class AllProperties(LowLactoseDietInheritedProperties , LowLactoseDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LowLactoseDietProperties, LowLactoseDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LowLactoseDiet"
    return model
    

LowLactoseDiet = create_schema_org_model()