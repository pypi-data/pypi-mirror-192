"""
The day of the week between Sunday and Tuesday.

https://schema.org/Monday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MondayInheritedProperties(TypedDict):
    """The day of the week between Sunday and Tuesday.

    References:
        https://schema.org/Monday
    Note:
        Model Depth 5
    Attributes:
    """

    


class MondayProperties(TypedDict):
    """The day of the week between Sunday and Tuesday.

    References:
        https://schema.org/Monday
    Note:
        Model Depth 5
    Attributes:
    """

    

#MondayInheritedPropertiesTd = MondayInheritedProperties()
#MondayPropertiesTd = MondayProperties()


class AllProperties(MondayInheritedProperties , MondayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MondayProperties, MondayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Monday"
    return model
    

Monday = create_schema_org_model()