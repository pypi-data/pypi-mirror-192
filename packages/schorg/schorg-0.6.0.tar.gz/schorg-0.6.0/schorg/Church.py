"""
A church.

https://schema.org/Church
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ChurchInheritedProperties(TypedDict):
    """A church.

    References:
        https://schema.org/Church
    Note:
        Model Depth 5
    Attributes:
    """

    


class ChurchProperties(TypedDict):
    """A church.

    References:
        https://schema.org/Church
    Note:
        Model Depth 5
    Attributes:
    """

    

#ChurchInheritedPropertiesTd = ChurchInheritedProperties()
#ChurchPropertiesTd = ChurchProperties()


class AllProperties(ChurchInheritedProperties , ChurchProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ChurchProperties, ChurchInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Church"
    return model
    

Church = create_schema_org_model()