"""
The day of the week between Monday and Wednesday.

https://schema.org/Tuesday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TuesdayInheritedProperties(TypedDict):
    """The day of the week between Monday and Wednesday.

    References:
        https://schema.org/Tuesday
    Note:
        Model Depth 5
    Attributes:
    """

    


class TuesdayProperties(TypedDict):
    """The day of the week between Monday and Wednesday.

    References:
        https://schema.org/Tuesday
    Note:
        Model Depth 5
    Attributes:
    """

    

#TuesdayInheritedPropertiesTd = TuesdayInheritedProperties()
#TuesdayPropertiesTd = TuesdayProperties()


class AllProperties(TuesdayInheritedProperties , TuesdayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TuesdayProperties, TuesdayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Tuesday"
    return model
    

Tuesday = create_schema_org_model()