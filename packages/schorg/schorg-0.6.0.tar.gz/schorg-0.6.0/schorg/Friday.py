"""
The day of the week between Thursday and Saturday.

https://schema.org/Friday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FridayInheritedProperties(TypedDict):
    """The day of the week between Thursday and Saturday.

    References:
        https://schema.org/Friday
    Note:
        Model Depth 5
    Attributes:
    """

    


class FridayProperties(TypedDict):
    """The day of the week between Thursday and Saturday.

    References:
        https://schema.org/Friday
    Note:
        Model Depth 5
    Attributes:
    """

    

#FridayInheritedPropertiesTd = FridayInheritedProperties()
#FridayPropertiesTd = FridayProperties()


class AllProperties(FridayInheritedProperties , FridayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FridayProperties, FridayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Friday"
    return model
    

Friday = create_schema_org_model()