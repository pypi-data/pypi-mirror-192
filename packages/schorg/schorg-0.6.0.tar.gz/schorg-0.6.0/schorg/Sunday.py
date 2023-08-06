"""
The day of the week between Saturday and Monday.

https://schema.org/Sunday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SundayInheritedProperties(TypedDict):
    """The day of the week between Saturday and Monday.

    References:
        https://schema.org/Sunday
    Note:
        Model Depth 5
    Attributes:
    """

    


class SundayProperties(TypedDict):
    """The day of the week between Saturday and Monday.

    References:
        https://schema.org/Sunday
    Note:
        Model Depth 5
    Attributes:
    """

    

#SundayInheritedPropertiesTd = SundayInheritedProperties()
#SundayPropertiesTd = SundayProperties()


class AllProperties(SundayInheritedProperties , SundayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SundayProperties, SundayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Sunday"
    return model
    

Sunday = create_schema_org_model()