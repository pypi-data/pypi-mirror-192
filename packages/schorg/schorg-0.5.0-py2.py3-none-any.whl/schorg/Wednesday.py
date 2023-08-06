"""
The day of the week between Tuesday and Thursday.

https://schema.org/Wednesday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WednesdayInheritedProperties(TypedDict):
    """The day of the week between Tuesday and Thursday.

    References:
        https://schema.org/Wednesday
    Note:
        Model Depth 5
    Attributes:
    """

    


class WednesdayProperties(TypedDict):
    """The day of the week between Tuesday and Thursday.

    References:
        https://schema.org/Wednesday
    Note:
        Model Depth 5
    Attributes:
    """

    

#WednesdayInheritedPropertiesTd = WednesdayInheritedProperties()
#WednesdayPropertiesTd = WednesdayProperties()


class AllProperties(WednesdayInheritedProperties , WednesdayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WednesdayProperties, WednesdayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Wednesday"
    return model
    

Wednesday = create_schema_org_model()