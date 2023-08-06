"""
The day of the week between Wednesday and Friday.

https://schema.org/Thursday
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ThursdayInheritedProperties(TypedDict):
    """The day of the week between Wednesday and Friday.

    References:
        https://schema.org/Thursday
    Note:
        Model Depth 5
    Attributes:
    """

    


class ThursdayProperties(TypedDict):
    """The day of the week between Wednesday and Friday.

    References:
        https://schema.org/Thursday
    Note:
        Model Depth 5
    Attributes:
    """

    

#ThursdayInheritedPropertiesTd = ThursdayInheritedProperties()
#ThursdayPropertiesTd = ThursdayProperties()


class AllProperties(ThursdayInheritedProperties , ThursdayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ThursdayProperties, ThursdayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Thursday"
    return model
    

Thursday = create_schema_org_model()