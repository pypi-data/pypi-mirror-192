"""
A bowling alley.

https://schema.org/BowlingAlley
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BowlingAlleyInheritedProperties(TypedDict):
    """A bowling alley.

    References:
        https://schema.org/BowlingAlley
    Note:
        Model Depth 5
    Attributes:
    """

    


class BowlingAlleyProperties(TypedDict):
    """A bowling alley.

    References:
        https://schema.org/BowlingAlley
    Note:
        Model Depth 5
    Attributes:
    """

    

#BowlingAlleyInheritedPropertiesTd = BowlingAlleyInheritedProperties()
#BowlingAlleyPropertiesTd = BowlingAlleyProperties()


class AllProperties(BowlingAlleyInheritedProperties , BowlingAlleyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BowlingAlleyProperties, BowlingAlleyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BowlingAlley"
    return model
    

BowlingAlley = create_schema_org_model()