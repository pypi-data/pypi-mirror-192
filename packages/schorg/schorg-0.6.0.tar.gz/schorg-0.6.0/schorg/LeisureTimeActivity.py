"""
Any physical activity engaged in for recreational purposes. Examples may include ballroom dancing, roller skating, canoeing, fishing, etc.

https://schema.org/LeisureTimeActivity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LeisureTimeActivityInheritedProperties(TypedDict):
    """Any physical activity engaged in for recreational purposes. Examples may include ballroom dancing, roller skating, canoeing, fishing, etc.

    References:
        https://schema.org/LeisureTimeActivity
    Note:
        Model Depth 5
    Attributes:
    """

    


class LeisureTimeActivityProperties(TypedDict):
    """Any physical activity engaged in for recreational purposes. Examples may include ballroom dancing, roller skating, canoeing, fishing, etc.

    References:
        https://schema.org/LeisureTimeActivity
    Note:
        Model Depth 5
    Attributes:
    """

    

#LeisureTimeActivityInheritedPropertiesTd = LeisureTimeActivityInheritedProperties()
#LeisureTimeActivityPropertiesTd = LeisureTimeActivityProperties()


class AllProperties(LeisureTimeActivityInheritedProperties , LeisureTimeActivityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LeisureTimeActivityProperties, LeisureTimeActivityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LeisureTimeActivity"
    return model
    

LeisureTimeActivity = create_schema_org_model()